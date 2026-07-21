from async_vla_benchmark.benchmark.execution import CompletedPolicyRequest
from async_vla_benchmark.benchmark.latency import LatencyProfile, request_delay_steps
from async_vla_benchmark.benchmark.runner import run_episode


class FakeEnvironment:
    def __init__(self, terminal_step=8):
        self.steps = 0
        self.terminal_step = terminal_step

    def reset(self, *, seed):
        self.steps = 0
        return {"seed": seed, "step": 0}, {"initialization_index": seed}

    def step(self, action):
        self.steps += 1
        done = self.steps >= self.terminal_step
        return {"step": self.steps}, 0.0, done, False, {"success": done}


class FakePolicy:
    def __init__(self, latency_ms=250.0):
        self.latency_ms = latency_ms

    def request(
        self, observation, *, strategy, profile, control_period_seconds,
        previous_chunk_remainder, execution_horizon,
    ):
        delay = request_delay_steps(profile, self.latency_ms, control_period_seconds)
        return CompletedPolicyRequest(
            actions=[[float(i), 0, 0, 0, 0, 0, 1] for i in range(10)],
            measured_request_latency_ms=self.latency_ms,
            timing={"observation_capture_time": 1, "request_complete_time": 2},
            rtc_delay_steps=delay if strategy == "rtc" else None,
            rtc_overlap_actions=len(previous_chunk_remainder) if strategy == "rtc" else 0,
        )


def run(strategy, horizon=2, latency=250.0):
    profile = LatencyProfile("ideal", False) if strategy == "ideal_sync" else LatencyProfile("native", True)
    return run_episode(
        episode_id="episode", environment=FakeEnvironment(), policy=FakePolicy(latency),
        strategy=strategy, profile=profile, fixed_horizon=horizon,
        control_frequency_hz=10, seed=3, max_steps=20,
    )


def test_ideal_episode_has_provenance_and_terminal_summary():
    result = run("ideal_sync")
    assert result.summary["success"] is True
    assert result.summary["environment_steps"] == 8
    assert all(row["chunk_id"] and row["source_observation_id"] for row in result.actions)
    assert all(row["is_hold_action"] is False for row in result.actions)


def test_blocking_uses_holds_for_each_request_delay():
    result = run("blocking_sync")
    assert [row["is_hold_action"] for row in result.actions[:3]] == [True, True, True]
    assert result.summary["queue_underrun_steps"] >= 3


def test_async_executes_old_actions_until_replacement_and_records_age():
    result = run("naive_async")
    assert result.requests[0]["startup_ideal"] is True
    assert max(row["action_age_steps"] for row in result.actions) > 0
    assert result.summary["number_of_policy_requests"] > 1


def test_rtc_executor_must_report_request_specific_delay():
    result = run("rtc")
    assert all(
        row["startup_ideal"] or row["rtc_delay_steps"] == row["delay_steps"]
        for row in result.requests
    )
