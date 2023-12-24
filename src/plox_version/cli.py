#!/usr/bin/env python3

import logging
import sys
from pathlib import Path
from typing import List, Optional

from plox_version import common

logger = logging.getLogger(__name__)


def _is_git_dirty(project_dir: Path) -> bool:
    return not not common.gex("status", "--short", cwd=project_dir)


def _head_commit(project_dir: Path) -> str:
    o = common.gex("rev-parse", "--short", "HEAD", cwd=project_dir)
    assert len(o) == 1
    return o[0]


def _version(rargs: Optional[List[str]] = None) -> str:
    project_dir = common.project_dir()

    args = common.args(rargs, lambda pargs: pargs.add_argument("--version", type=str, required=True))

    version: str = args.version
    logger.debug(f"CLI arg 'version': {version}")

    if not version or version == "":
        raise RuntimeError("'version' CLI arg must be provided")

    if _is_git_dirty(project_dir):
        ch = _head_commit(project_dir)
        version = f"{version}+{ch}"

    logger.debug(f"Version string: {version}")
    return version


def plox_version() -> None:
    """
    CLI entrypoint
    """

    version_str = _version(sys.argv[1:])
    print(version_str)
    # this program will always throw an exception instead of exit nonzero
    sys.exit(0)


if __name__ == "__main__":
    plox_version()

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4
