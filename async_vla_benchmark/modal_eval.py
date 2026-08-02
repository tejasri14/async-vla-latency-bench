"""Pinned Modal launcher for π0.5-LIBERO setup inspection and one smoke episode.

Run locally with:

    .venv/bin/modal run async_vla_benchmark/modal_eval.py --mode inspect
    .venv/bin/modal run async_vla_benchmark/modal_eval.py --mode eval

The evaluation deliberately runs one seed on LIBERO-Spatial task 0. It is an
official LeRobot smoke evaluation, not a Days 1–3 benchmark result.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any

import modal


APP_NAME = "async-vla-pi05-libero"
GPU_TYPE = "L40S"
LEROBOT_COMMIT = "8fff0fde7c79f23a93d845d1a50e985de01f8b8a"  # v0.4.4
TRANSFORMERS_COMMIT = "dcddb970176382c0fcf4521b0c0e6fc15894dfe0"
MODEL_ID = "lerobot/pi05_libero_finetuned_v044"
MODEL_REVISION = "dbf8a3f794a9c4297b44f40b752712f50073d945"
DATASET_ID = "HuggingFaceVLA/libero"
DATASET_REVISION = "86958911c0f959db2bbbdb107eb3e17c5f9c798e"

CACHE_ROOT = Path("/cache")
OUTPUT_ROOT = Path("/outputs")
MODEL_PATH = CACHE_ROOT / "models" / "pi05_libero_finetuned_v044"


image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04",
        add_python="3.10",
    )
    .entrypoint([])
    .apt_install(
        "build-essential",
        "clang",
        "cmake",
        "ffmpeg",
        "git",
        "libegl1",
        "libgl1",
        "libglib2.0-0",
        "libglvnd0",
        "libosmesa6",
        "libsm6",
        "libxext6",
        "libxrender1",
        "ninja-build",
        "pkg-config",
    )
    .run_commands(
        "python -m pip install --upgrade pip",
        "git clone https://github.com/huggingface/lerobot.git /opt/lerobot",
        f"git -C /opt/lerobot checkout --detach {LEROBOT_COMMIT}",
        # v0.4.4 declares pi's OpenPI Transformers fork as conflicting with the
        # libero extra's generic transformers-dep. Install the base plus both
        # non-conflicting payloads explicitly, pinning the fork commit.
        "python -m pip install -e /opt/lerobot",
        (
            "CMAKE_POLICY_VERSION_MINIMUM=3.5 "
            "python -m pip install --no-build-isolation "
            f"'transformers @ git+https://github.com/huggingface/transformers.git@{TRANSFORMERS_COMMIT}' "
            "'scipy>=1.10.1,<1.15' 'hf-libero==0.1.4'"
        ),
        "python -m pip install pyarrow pandas matplotlib pyyaml",
    )
    .env(
        {
            "MUJOCO_GL": "egl",
            "PYOPENGL_PLATFORM": "egl",
            "HF_HOME": str(CACHE_ROOT / "huggingface"),
            "HF_HUB_DISABLE_TELEMETRY": "1",
            "TOKENIZERS_PARALLELISM": "false",
        }
    )
)

app = modal.App(APP_NAME, image=image)
cache_volume = modal.Volume.from_name("async-vla-hf-cache", create_if_missing=True)
output_volume = modal.Volume.from_name("async-vla-eval-outputs", create_if_missing=True)


def _run(command: list[str]) -> str:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def _metadata() -> dict[str, Any]:
    import importlib.metadata
    import platform
    import sys

    import mujoco
    import torch

    if not torch.cuda.is_available():
        raise RuntimeError("Modal function received no CUDA-capable GPU")

    # This is a real EGL context creation check, not merely an environment-variable check.
    context = mujoco.GLContext(8, 8)
    context.make_current()
    context.free()

    package_names = ("lerobot", "libero", "mujoco", "robosuite", "torch")
    packages: dict[str, str | None] = {}
    for name in package_names:
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None

    return {
        "status": "ready_for_official_smoke_eval",
        "platform": platform.platform(),
        "python_version": sys.version,
        "lerobot_git_commit": _run(["git", "-C", "/opt/lerobot", "rev-parse", "HEAD"]),
        "transformers_git_commit": TRANSFORMERS_COMMIT,
        "checkpoint_id": MODEL_ID,
        "checkpoint_revision_sha": MODEL_REVISION,
        "dataset_id": DATASET_ID,
        "dataset_revision_sha": DATASET_REVISION,
        "gpu_requested": GPU_TYPE,
        "gpu_name": torch.cuda.get_device_name(0),
        "cuda_available": torch.cuda.is_available(),
        "torch_cuda_version": torch.version.cuda,
        "nvidia_smi": _run(
            [
                "nvidia-smi",
                "--query-gpu=name,uuid,driver_version,memory.total",
                "--format=csv,noheader",
            ]
        ),
        "mujoco_backend": "egl",
        "egl_context_created": True,
        "packages": packages,
    }


@app.function(
    gpu=GPU_TYPE,
    timeout=30 * 60,
    volumes={str(CACHE_ROOT): cache_volume, str(OUTPUT_ROOT): output_volume},
)
def inspect_setup() -> dict[str, Any]:
    metadata = _metadata()
    path = OUTPUT_ROOT / "modal" / "environment.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    output_volume.commit()
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return metadata


@app.function(
    gpu=GPU_TYPE,
    timeout=2 * 60 * 60,
    volumes={str(CACHE_ROOT): cache_volume, str(OUTPUT_ROOT): output_volume},
)
def evaluate_smoke() -> dict[str, Any]:
    from datetime import datetime, timezone

    from huggingface_hub import snapshot_download

    metadata = _metadata()
    snapshot_download(
        repo_id=MODEL_ID,
        revision=MODEL_REVISION,
        local_dir=MODEL_PATH,
    )
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = OUTPUT_ROOT / "modal" / "official_eval" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "environment.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n"
    )

    command = [
        "lerobot-eval",
        f"--output_dir={run_dir / 'lerobot'}",
        "--env.type=libero",
        "--env.task=libero_spatial",
        "--env.task_ids=[0]",
        "--env.max_parallel_tasks=1",
        "--eval.batch_size=1",
        "--eval.n_episodes=1",
        f"--policy.path={MODEL_PATH}",
        "--policy.device=cuda",
        "--policy.n_action_steps=10",
        "--policy.compile_model=false",
        "--seed=0",
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    (run_dir / "command.json").write_text(json.dumps(command, indent=2) + "\n")
    (run_dir / "stdout.log").write_text(result.stdout)
    (run_dir / "stderr.log").write_text(result.stderr)
    outcome = {
        "status": "passed" if result.returncode == 0 else "failed",
        "returncode": result.returncode,
        "run_id": run_id,
        "output_path": str(run_dir),
        "command": command,
        "note": "Official LeRobot smoke evaluation; not a benchmark episode.",
    }
    (run_dir / "outcome.json").write_text(
        json.dumps(outcome, indent=2, sort_keys=True) + "\n"
    )
    output_volume.commit()
    print(result.stdout)
    if result.returncode:
        print(result.stderr)
        raise RuntimeError(f"lerobot-eval failed with exit code {result.returncode}")
    return outcome


@app.local_entrypoint()
def main(mode: str = "inspect") -> None:
    if mode == "inspect":
        result = inspect_setup.remote()
    elif mode == "eval":
        result = evaluate_smoke.remote()
    else:
        raise ValueError("mode must be 'inspect' or 'eval'")
    print(json.dumps(result, indent=2, sort_keys=True))
