from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shlex
import subprocess
import time
from typing import Iterable

import pandas as pd

from services.manifest_store import dashboard_text_is_safe, load_manifest
from services.paths import OUTPUTS_DIR, ROOT, repo_relative

DEMO_MODE_LABEL = "Demo Mode"
RUN_LOG_ROOT = OUTPUTS_DIR / "dashboard_runs"
FORBIDDEN_ARG_MARKERS = {";", "&&", "||", ">", "<", "`", "$", "\n", "\r"}


@dataclass(frozen=True)
class DashboardCommand:
    command_id: str
    title: str
    category: str
    argv: tuple[str, ...]
    description: str
    requires_private_data: bool
    writes_ignored_outputs: bool
    requires_confirmation: bool
    enabled_in_coauthor_mode: bool
    enabled_in_demo_mode: bool
    timeout_seconds: int
    log_tail_lines: int
    expected_outputs: str
    docs: str

    @property
    def display_command(self) -> str:
        return shlex.join(self.argv)

    @property
    def tags(self) -> tuple[str, ...]:
        tags = [self.category]
        if self.requires_private_data:
            tags.append("requires private data")
        if self.writes_ignored_outputs:
            tags.append("writes ignored outputs")
        if self.requires_confirmation:
            tags.append("confirmation required")
        return tuple(tags)


@dataclass(frozen=True)
class CommandRunResult:
    command_id: str
    command: str
    status: str
    exit_code: int | None
    duration_seconds: float
    log_dir: Path | None
    log_path: Path | None
    log_tail: str
    timed_out: bool = False
    error_message: str = ""

    @property
    def rel_log_path(self) -> str:
        if self.log_path is None:
            return ""
        return repo_relative(self.log_path)


class CommandRegistryError(ValueError):
    pass


def _parse_bool(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


def _parse_positive_int(value: object, *, default: int) -> int:
    try:
        parsed = int(str(value or "").strip())
    except ValueError:
        return default
    return parsed if parsed > 0 else default


def _validate_argv(argv: Iterable[str], *, command_id: str) -> tuple[str, ...]:
    tokens = tuple(str(token or "").strip() for token in argv)
    if not tokens or tokens[0] != "make":
        raise CommandRegistryError(f"{command_id}: dashboard commands must start with fixed 'make' argv")
    if any(not token for token in tokens):
        raise CommandRegistryError(f"{command_id}: blank argv token")
    for token in tokens:
        if token.startswith(("/", "~")) or not dashboard_text_is_safe(token):
            raise CommandRegistryError(f"{command_id}: unsafe argv token {token!r}")
        if any(marker in token for marker in FORBIDDEN_ARG_MARKERS):
            raise CommandRegistryError(f"{command_id}: shell marker not allowed in argv token {token!r}")
    return tokens


def _command_from_row(row: pd.Series) -> DashboardCommand:
    command_id = str(row.get("command_id", "") or "").strip()
    argv = _validate_argv(str(row.get("argv", "") or "").split("|"), command_id=command_id)
    return DashboardCommand(
        command_id=command_id,
        title=str(row.get("title", "") or "").strip(),
        category=str(row.get("category", "") or "").strip(),
        argv=argv,
        description=str(row.get("description", "") or "").strip(),
        requires_private_data=_parse_bool(row.get("requires_private_data", "")),
        writes_ignored_outputs=_parse_bool(row.get("writes_ignored_outputs", "")),
        requires_confirmation=_parse_bool(row.get("requires_confirmation", "")),
        enabled_in_coauthor_mode=_parse_bool(row.get("enabled_in_coauthor_mode", "")),
        enabled_in_demo_mode=_parse_bool(row.get("enabled_in_demo_mode", "")),
        timeout_seconds=_parse_positive_int(row.get("timeout_seconds", ""), default=300),
        log_tail_lines=_parse_positive_int(row.get("log_tail_lines", ""), default=80),
        expected_outputs=str(row.get("expected_outputs", "") or "").strip(),
        docs=str(row.get("docs", "") or "").strip(),
    )


def load_command_registry() -> tuple[DashboardCommand, ...]:
    frame = load_manifest("dashboard_command_registry.csv")
    commands = tuple(_command_from_row(row) for _, row in frame.iterrows())
    ids = [command.command_id for command in commands]
    duplicates = sorted({command_id for command_id in ids if ids.count(command_id) > 1})
    if duplicates:
        raise CommandRegistryError(f"Duplicate dashboard command IDs: {', '.join(duplicates)}")
    missing = [command.command_id for command in commands if not command.title or not command.category]
    if missing:
        raise CommandRegistryError(f"Dashboard commands missing title/category: {', '.join(missing)}")
    return commands


def commands_by_id(commands: Iterable[DashboardCommand] | None = None) -> dict[str, DashboardCommand]:
    return {command.command_id: command for command in (tuple(commands) if commands is not None else load_command_registry())}


def private_data_root_present(env: dict[str, str] | None = None) -> bool:
    source = env if env is not None else os.environ
    raw = source.get("AIW_DATA_ROOT", "")
    if not raw:
        return False
    return Path(raw).expanduser().exists()


def command_is_enabled(command: DashboardCommand, *, mode: str, env: dict[str, str] | None = None) -> tuple[bool, str]:
    if mode == DEMO_MODE_LABEL:
        return False, "Command execution is disabled in Demo Mode. Switch to Coauthor Mode on a local workstation."
    if not command.enabled_in_coauthor_mode:
        return False, "This command is not enabled for dashboard execution."
    if command.requires_private_data and not private_data_root_present(env):
        return False, "AIW_DATA_ROOT is not set to an existing private data room; data-dependent commands are blocked."
    return True, ""


def _execution_env() -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "AIW_REPO_ROOT": str(ROOT),
            "AIW_OUTPUT_ROOT": str(OUTPUTS_DIR / "reproduced"),
            "AIW_PAPER_ROOT": str(OUTPUTS_DIR / "paper_exports"),
            "PYTHONPATH": str(ROOT / "src"),
        }
    )
    return env


def environment_summary(command: DashboardCommand, *, env: dict[str, str] | None = None) -> dict[str, str]:
    source = env if env is not None else os.environ
    return {
        "cwd": "$AIW_REPO_ROOT",
        "AIW_DATA_ROOT": "set" if source.get("AIW_DATA_ROOT") else "not set",
        "requires_private_data": "yes" if command.requires_private_data else "no",
        "writes_ignored_outputs": "yes" if command.writes_ignored_outputs else "no",
        "timeout_seconds": str(command.timeout_seconds),
    }


def sanitize_log_text(text: str, *, env: dict[str, str] | None = None) -> str:
    safe = str(text or "")
    replacements = {
        str(ROOT): "$AIW_REPO_ROOT",
        str(Path.home()): "$HOME",
    }
    source = env if env is not None else os.environ
    data_root = source.get("AIW_DATA_ROOT", "")
    if data_root:
        replacements[str(Path(data_root).expanduser())] = "$AIW_DATA_ROOT"
    for old, new in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        if old:
            safe = safe.replace(old, new)
    return safe


def _tail(text: str, line_count: int) -> str:
    lines = str(text or "").splitlines()
    if not lines:
        return "No command output was captured."
    return "\n".join(lines[-line_count:])


def _blocked_result(command: DashboardCommand, *, message: str) -> CommandRunResult:
    return CommandRunResult(
        command_id=command.command_id,
        command=command.display_command,
        status="blocked",
        exit_code=None,
        duration_seconds=0.0,
        log_dir=None,
        log_path=None,
        log_tail=message,
        error_message=message,
    )


def _write_run_artifacts(
    command: DashboardCommand,
    *,
    log_root: Path,
    started_at: datetime,
    duration_seconds: float,
    exit_code: int | None,
    timed_out: bool,
    stdout: str,
    stderr: str,
) -> tuple[Path, Path]:
    stamp = started_at.strftime("%Y%m%dT%H%M%SZ")
    run_dir = log_root / f"{stamp}_{command.command_id}"
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "run.log"
    metadata_path = run_dir / "metadata.json"
    log_text = "\n".join(
        [
            f"command_id: {command.command_id}",
            f"command: {command.display_command}",
            "cwd: $AIW_REPO_ROOT",
            f"started_at_utc: {started_at.isoformat()}",
            f"duration_seconds: {duration_seconds:.3f}",
            f"exit_code: {exit_code}",
            f"timed_out: {timed_out}",
            "--- stdout ---",
            stdout or "",
            "--- stderr ---",
            stderr or "",
        ]
    )
    log_path.write_text(log_text, encoding="utf-8")
    metadata = {
        "command_id": command.command_id,
        "command": command.display_command,
        "category": command.category,
        "cwd": "$AIW_REPO_ROOT",
        "requires_private_data": command.requires_private_data,
        "writes_ignored_outputs": command.writes_ignored_outputs,
        "duration_seconds": round(duration_seconds, 3),
        "exit_code": exit_code,
        "timed_out": timed_out,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return run_dir, log_path


def _failure_hint(command: DashboardCommand, *, exit_code: int | None, timed_out: bool) -> str:
    if timed_out:
        return f"The command exceeded its {command.timeout_seconds}-second timeout. Open the raw log under outputs/dashboard_runs for details."
    if command.requires_private_data:
        return "The command failed. First verify AIW_DATA_ROOT points to the private data room and run make check-private-data."
    return f"The command exited with code {exit_code}. Review the log tail and raw ignored log for details."


def run_dashboard_command(
    command_id: str,
    *,
    mode: str,
    confirmed: bool = False,
    registry: Iterable[DashboardCommand] | None = None,
    log_root: Path = RUN_LOG_ROOT,
    runner=subprocess.run,
) -> CommandRunResult:
    command = commands_by_id(registry).get(command_id)
    if command is None:
        raise CommandRegistryError(f"Unknown dashboard command ID: {command_id}")

    enabled, reason = command_is_enabled(command, mode=mode)
    if not enabled:
        return _blocked_result(command, message=reason)
    if command.requires_confirmation and not confirmed:
        return _blocked_result(command, message="This command requires explicit confirmation before it can run.")

    env = _execution_env()
    started_at = datetime.now(timezone.utc)
    start = time.monotonic()
    stdout = ""
    stderr = ""
    exit_code: int | None
    timed_out = False
    try:
        completed = runner(
            list(command.argv),
            cwd=ROOT,
            env=env,
            shell=False,
            capture_output=True,
            text=True,
            timeout=command.timeout_seconds,
            check=False,
        )
        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
        exit_code = int(completed.returncode)
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = exc.stdout or ""
        stderr = exc.stderr or f"Command timed out after {command.timeout_seconds} seconds."
        exit_code = None

    duration = time.monotonic() - start
    run_dir, log_path = _write_run_artifacts(
        command,
        log_root=log_root,
        started_at=started_at,
        duration_seconds=duration,
        exit_code=exit_code,
        timed_out=timed_out,
        stdout=stdout,
        stderr=stderr,
    )
    combined = "\n".join(part for part in [stdout, stderr] if part)
    status = "timeout" if timed_out else "passed" if exit_code == 0 else "failed"
    message = "" if status == "passed" else _failure_hint(command, exit_code=exit_code, timed_out=timed_out)
    return CommandRunResult(
        command_id=command.command_id,
        command=command.display_command,
        status=status,
        exit_code=exit_code,
        duration_seconds=duration,
        log_dir=run_dir,
        log_path=log_path,
        log_tail=sanitize_log_text(_tail(combined, command.log_tail_lines), env=env),
        timed_out=timed_out,
        error_message=message,
    )
