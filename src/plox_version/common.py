"""Common utilities for plox version tooling."""

import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_debug = os.getenv("DEBUG", None)
level = logging.DEBUG if _debug else logging.ERROR
logging.basicConfig(level=level, stream=sys.stderr)

logger = logging.getLogger(__name__)

_utf8 = "UTF-8"
Level = int
project_dir_env = "PROJECT_DIR"


def _decode(by: bytes) -> List[str]:
    return list(filter(lambda li: bool(li), by.decode(_utf8).split("\n")))


def _log_process_output(*captured: Tuple[Level, bytes]) -> None:
    for lev, by in captured:
        for line in _decode(by):
            logger.log(lev, line)


def gex(
    *args: str, cwd: Path, env: Optional[Dict[Any, Any]] = None, expected_code: int = 0
) -> List[str]:
    """Wrap local git command executable and execute.

    Args:
        args (str): List of args to pass to the ``git`` executable.
        cwd (Path): Working dir.
        env (Optional[Dict[Any, Any]]): Key:Value pairs to set the environement with.
        expected_code (int): Expected integer return code; Defaults to 0.

    Returns:
        List[str]: STDOUT of executable call.
    """
    exe = shutil.which("git")
    if not exe:
        raise RuntimeError("Missing required git executable")

    logger.debug(f"{exe=}")
    logger.debug(f"{cwd=}")

    if not env:
        env = {}

    p = subprocess.run([exe, *list(args)], capture_output=True, env=env, cwd=cwd)  # noqa: S603

    failed = False
    if p.returncode != expected_code:
        failed = True

    if failed or _debug:
        _log_process_output((logging.INFO, p.stdout), (logging.ERROR, p.stderr))

    if failed:
        raise RuntimeError(f"Git cmd {args} failed with code {p.returncode}")

    return _decode(p.stdout)


def env(key: str, default: Optional[str] = None) -> str:
    """Fetch an environment variable.

    environ.get() exists?

    Args:
        key (str): Name of env variable to fetch.
        default (Optional[str]): Default value to get.

    Returns:
        str:
    """
    if key not in os.environ:
        if default is not None:
            logger.debug(f"Using default value {default} for envvar {key}")
            return default
        else:
            raise RuntimeError(f"Missing required environment variable: {key}")

    return os.environ[key].strip()


def project_dir() -> Path:
    """Return path to project dir."""
    p = Path(env(project_dir_env, "."))
    if not p.is_dir() or not Path(p, ".git"):
        raise RuntimeError(f"Unusable project directory provided: {p}")

    return p
