"""Production discrete-event episode orchestration over isolated adapters."""

from dataclasses import asdict, dataclass
from time import perf_counter
from typing import Any, Sequence

from .execution import (
    ChunkRef,
    EpisodeEnvironment,
    ObservationRef,
    PolicyRequestExecutor,
    action_age_ms,
    action_age_steps,
    make_hold_action,
)
from .latency import LatencyProfile, request_delay_steps
from .metrics import mean_continuity, percentile
from .queues import ActionQueue, QueuedAction


@dataclass(frozen=True)
class EpisodeResult:
    requests: list[dict[str, Any]]
    actions: list[dict[str, Any]]
    summary: dict[str, Any]


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else float("nan")


def run_episode(
    *,
    episode_id: str,
    environment: EpisodeEnvironment,
    policy: PolicyRequestExecutor,
    strategy: str,
    profile: LatencyProfile,
    fixed_horizon: int,
    control_frequency_hz: float,
    seed: int,
    max_steps: int,
) -> EpisodeResult:
    """Run one episode without real-time sleeps or implicit latency averages."""
    if strategy not in {"ideal_sync", "blocking_sync", "naive_async", "rtc"}:
        raise ValueError(f"unsupported strategy: {strategy}")
    if fixed_horizon <= 0 or max_steps <= 0 or control_frequency_hz <= 0:
        raise ValueError("horizon, max steps, and control frequency must be positive")
    period = 1.0 / control_frequency_hz
    observation, reset_info = environment.reset(seed=seed)
    queue = ActionQueue(fixed_horizon)
    request_rows: list[dict[str, Any]] = []
    action_rows: list[dict[str, Any]] = []
    observations: dict[str, ObservationRef] = {}
    chunks: dict[str, ChunkRef] = {}
    pending: dict[str, Any] | None = None
    last_gripper = 0.0
    start = perf_counter()

    def submit(step: int, startup: bool = False) -> None:
        nonlocal pending
        if pending is not None:
            raise RuntimeError("only one policy request may be outstanding")
        observation_id = f"{episode_id}:obs:{step}:{len(observations)}"
        obs_ref = ObservationRef(observation_id, step, step * period)
        observations[observation_id] = obs_ref
        request_id = f"{episode_id}:request:{len(request_rows)}"
        remainder = queue.remainder()
        result = policy.request(
            observation,
            strategy=strategy,
            profile=profile,
            control_period_seconds=period,
            previous_chunk_remainder=remainder,
            execution_horizon=fixed_horizon,
        )
        delay = 0 if startup else request_delay_steps(profile, result.measured_request_latency_ms, period)
        if strategy == "rtc" and not startup and result.rtc_delay_steps != delay:
            raise RuntimeError("RTC executor did not use this request's measured delay_steps")
        available_step = step + delay
        chunk_id = f"{episode_id}:chunk:{len(chunks)}"
        chunk = ChunkRef(
            chunk_id, observation_id, step, step * period, available_step,
            result.measured_request_latency_ms, profile.added_latency_ms, delay,
        )
        chunks[chunk_id] = chunk
        queued = [QueuedAction(list(a), chunk_id, i, observation_id, step) for i, a in enumerate(result.actions)]
        if len(queued) < fixed_horizon:
            raise RuntimeError("policy chunk is shorter than the configured horizon")
        request_rows.append({
            "episode_id": episode_id, "request_id": request_id, **asdict(chunk),
            **dict(result.timing), "rtc_delay_steps": result.rtc_delay_steps,
            "rtc_overlap_actions": result.rtc_overlap_actions,
            "rtc_guided_actions": result.rtc_guided_actions,
            "startup_ideal": startup,
        })
        if startup:
            queue.startup(queued)
            pending = None
        else:
            queue.begin_request(request_id)
            if available_step == step:
                queue.replace(request_id, queued)
                pending = None
            else:
                pending = {"request_id": request_id, "available_step": available_step, "actions": queued}

    # Async strategies get an explicitly labelled ideal startup fill.
    if strategy in {"naive_async", "rtc"}:
        submit(0, startup=True)

    success = False
    for step in range(max_steps):
        if pending is not None and step >= pending["available_step"]:
            queue.replace(pending["request_id"], pending["actions"])
            pending = None
        if strategy in {"ideal_sync", "blocking_sync"} and not queue.remainder() and pending is None:
            submit(step)
        elif strategy in {"naive_async", "rtc"} and queue.should_request():
            submit(step)

        depth_before = len(queue)
        queued_action = queue.pop()
        underrun = queued_action is None
        if underrun:
            vector = make_hold_action(last_gripper)
            chunk_id = None
            chunk_index = None
            source_id = None
            source_step = step
        else:
            vector = list(map(float, queued_action.value))
            last_gripper = vector[-1]
            chunk_id = queued_action.chunk_id
            chunk_index = queued_action.chunk_action_index
            source_id = queued_action.source_observation_id
            source_step = queued_action.source_observation_step
        age_steps = action_age_steps(step, source_step)
        observation, _reward, terminated, truncated, info = environment.step(vector)
        action_rows.append({
            "episode_id": episode_id, "control_step": step, "logical_time_seconds": step * period,
            "strategy": strategy, "latency_profile": profile.name, "fixed_horizon": fixed_horizon,
            "chunk_id": chunk_id, "chunk_action_index": chunk_index,
            "source_observation_id": source_id, "source_observation_step": source_step,
            "action_age_steps": age_steps, "action_age_ms": action_age_ms(age_steps, period),
            "queue_depth_before": depth_before, "queue_depth_after": len(queue),
            "is_hold_action": underrun, "is_queue_underrun": underrun,
            "action_vector": vector,
        })
        if terminated or truncated:
            success = bool(info.get("success", terminated))
            break

    ages = [row["action_age_ms"] for row in action_rows]
    latencies = [row["measured_request_latency_ms"] for row in request_rows]
    vectors = [row["action_vector"] for row in action_rows]
    summary = {
        "episode_id": episode_id, "terminal_result": True, "success": success,
        "environment_steps": len(action_rows), "logical_completion_time_seconds": len(action_rows) * period,
        "wall_clock_runtime_seconds": perf_counter() - start, "number_of_policy_requests": len(request_rows),
        "total_model_inference_ms": sum(latencies), "mean_request_latency_ms": _mean(latencies),
        "p95_request_latency_ms": percentile(latencies, .95), "mean_action_age_ms": _mean(ages),
        "p95_action_age_ms": percentile(ages, .95), "maximum_action_age_ms": max(ages),
        "mean_queue_depth": _mean([r["queue_depth_before"] for r in action_rows]),
        "minimum_queue_depth": min(r["queue_depth_before"] for r in action_rows),
        "queue_underrun_steps": sum(r["is_queue_underrun"] for r in action_rows),
        "hold_action_steps": sum(r["is_hold_action"] for r in action_rows),
        "discarded_old_actions": queue.discarded_old_actions,
        "mean_action_delta_l2": mean_continuity(vectors, 1),
        "mean_action_acceleration_l2": mean_continuity(vectors, 2),
        "mean_action_jerk_l2": mean_continuity(vectors, 3),
        "seed": seed, "strategy": strategy, "latency_profile": profile.name,
        "fixed_horizon": fixed_horizon, "reset_info": dict(reset_info),
    }
    return EpisodeResult(request_rows, action_rows, summary)
