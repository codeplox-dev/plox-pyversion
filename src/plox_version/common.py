import argparse
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Callable, Dict, Any, Optional

_debug = os.getenv("DEBUG", None)
if _debug:
    level = logging.DEBUG
else:
    level = logging.ERROR
logging.basicConfig(level=level, stream=sys.stderr)

logger = logging.getLogger(__name__)

_utf8 = "UTF-8"
Level = int
project_dir_env = "PROJECT_DIR"


def _decode(by: bytes) -> List[str]:
    return list(filter(lambda li: not not li, by.decode(_utf8).split("\n")))


def _log_process_output(*captured: Tuple[Level, bytes]) -> None:
    for lev, by in captured:
        for line in _decode(by):
            logger.log(lev, line)


def gex(
    *args: str, cwd: Path, env: Optional[Dict[Any, Any]] = None, expected_code: int = 0
) -> List[str]:
    exe = shutil.which("git")
    if not exe:
        raise RuntimeError("Missing required git executable")

    logger.debug(f"{exe=}")
    logger.debug(f"{cwd=}")

    if not env:
        env = {}
    p = subprocess.run(
        [exe] + [a for a in args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, cwd=cwd
    )

    failed = False
    if p.returncode != expected_code:
        failed = True

    if failed or _debug:
        _log_process_output((logging.INFO, p.stdout), (logging.ERROR, p.stderr))

    if failed:
        raise RuntimeError(f"Git cmd {args} failed with code {p.returncode}")

    return _decode(p.stdout)


def env(key: str) -> str:
    if key not in os.environ:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return os.environ[key].strip()


def project_dir() -> Path:
    p = Path(env(project_dir_env))
    if not p.is_dir():
        raise RuntimeError(f"Unusable project directory provided: {p}")

    return p


def args(args: Optional[List[str]] = None, *fns: Callable[[argparse.ArgumentParser], argparse.Action]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    for fn in fns:
        fn(parser)

    return parser.parse_args(args if args is not None else sys.argv[1:])


# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4
