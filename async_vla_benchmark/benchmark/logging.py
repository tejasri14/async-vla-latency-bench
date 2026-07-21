"""Validated, atomic episode output writing."""

from dataclasses import asdict, is_dataclass
import json
import os
from pathlib import Path
from typing import Any, Iterable, Mapping


class OutputDependencyError(RuntimeError):
    pass


def _row(value: Any) -> dict[str, Any]:
    if is_dataclass(value):
        return asdict(value)
    return dict(value)


def write_json_atomic(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(dict(value), indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def write_parquet_atomic(path: Path, rows: Iterable[Any]) -> None:
    records = [_row(row) for row in rows]
    if not records:
        raise ValueError(f"refusing to write empty parquet output: {path}")
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise OutputDependencyError(
            "Parquet output requires pyarrow in the pinned execution environment"
        ) from exc
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    pq.write_table(pa.Table.from_pylist(records), temporary)
    os.replace(temporary, path)


def write_episode_outputs(
    output_dir: Path,
    episode_id: str,
    requests: Iterable[Any],
    actions: Iterable[Any],
    summary: Mapping[str, Any],
) -> None:
    """Write the terminal JSON last, making it the completion marker."""
    write_parquet_atomic(output_dir / "requests" / f"{episode_id}.parquet", requests)
    write_parquet_atomic(output_dir / "actions" / f"{episode_id}.parquet", actions)
    write_json_atomic(output_dir / "episodes" / f"{episode_id}.json", summary)
