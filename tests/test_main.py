import asyncio
import json
import os
import signal
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


async def _run_until_sigterm(tmp_path: Path, environment: str) -> tuple[int, list[str]]:
    # Run in tmp_path, so the app does not read the repo .env or write to the repo logs/
    env = {
        **os.environ,
        "APP_ENVIRONMENT": environment,
        "PYTHONPATH": str(ROOT),
        "PYTHONUNBUFFERED": "1",
    }
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "main",
        cwd=tmp_path,
        env=env,
        stdout=asyncio.subprocess.PIPE,
    )
    assert proc.stdout is not None
    try:
        lines: list[str] = []
        while not lines or "Starting application" not in lines[-1]:
            line = await asyncio.wait_for(proc.stdout.readline(), timeout=10)
            assert line, "app exited before it started"
            lines.append(line.decode())

        proc.send_signal(signal.SIGTERM)
        out, _ = await asyncio.wait_for(proc.communicate(), timeout=10)
        lines += out.decode().splitlines()
    finally:
        if proc.returncode is None:
            proc.kill()
            await proc.wait()

    assert proc.returncode is not None
    return proc.returncode, lines


async def test_main_stops_on_sigterm(tmp_path: Path) -> None:
    returncode, lines = await _run_until_sigterm(tmp_path, "local")

    assert returncode == 0
    assert "Shutdown complete" in lines[-1]


async def test_main_logs_json_to_stdout_in_production(tmp_path: Path) -> None:
    _, lines = await _run_until_sigterm(tmp_path, "production")

    events = [json.loads(line)["event"] for line in lines]
    assert events[-1] == "Shutdown complete"
