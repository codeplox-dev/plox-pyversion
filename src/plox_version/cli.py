# -*- coding: utf-8 -*-

import argparse
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


def _from_file(version_file: str) -> str:
    p = Path(version_file)
    if not p.is_file():
        raise RuntimeError(f"Missing verison file {version_file}")

    with p.open("r", encoding="utf-8") as inf:
        lines = list(
            filter(lambda li: not li.startswith("#") or li.startswith("//"), inf.readlines())
        )

    if len(lines) != 1:
        raise RuntimeError(
            f"Ill-formed verison file {version_file}; expecting a single line after dropping comments"
        )

    return lines[0].strip()


def _version(rargs: Optional[List[str]] = None) -> str:
    project_dir = common.project_dir()

    parser = argparse.ArgumentParser()
    version_opt_group = parser.add_mutually_exclusive_group(required=True)

    version_opt_group.add_argument("--version", type=str)
    version_opt_group.add_argument("--version-file", type=str)

    args = parser.parse_args(rargs)

    version_str = args.version
    if version_str is None:
        version = _from_file(args.version_file)
    else:
        version = version_str

    # TODO: add version string verification and validity given previous version
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


# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4
