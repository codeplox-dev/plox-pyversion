# -*- coding: utf-8 -*-

# pyright: reportPrivateUsage=false

import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from plox_version import common, cli
from plox_version.test.git_test_project import GitTestProject


@pytest.fixture(scope="function")
def tmp_d() -> Generator[Path, None, None]:
    tmp_d = None
    try:
        tmp_d = tempfile.mkdtemp(prefix="plox-version-")
        yield Path(tmp_d)
    finally:
        if tmp_d is not None:
            shutil.rmtree(tmp_d)


@pytest.fixture(scope="function")
def git_test_project(tmp_d: Path) -> Generator[GitTestProject, None, None]:
    yield GitTestProject(tmp_d)


# Note: these tests may not be executed in parallel b/c they rely on os.environ
# values to be set / unset

@pytest.mark.integration
def test_plox_version_clean(git_test_project: GitTestProject) -> None:
    os.environ[common.project_dir_env] = str(git_test_project.proj_dir)
    version = "2.6.0"

    # repo will be clean b/c we committed our add
    git_test_project.add_content_as_file("foo", "foo content", commit=True)

    version_str = cli._version(["--version", version])

    assert version_str == version


@pytest.mark.integration
def test_plox_version_default_dir(git_test_project: GitTestProject) -> None:
    # os.environ[common.project_dir_env] = str(git_test_project.proj_dir)
    version = "0.5.0"

    # add first thing and commit
    git_test_project.add_content_as_file("foo", "foo content", commit=True)

    del os.environ[common.project_dir_env]

    os.chdir(git_test_project.proj_dir)
    version_str = cli._version(["--version", version])

    assert version_str == version


@pytest.mark.integration
def test_plox_version_dirty(git_test_project: GitTestProject) -> None:
    os.environ[common.project_dir_env] = str(git_test_project.proj_dir)
    version = "0.5.0"

    # add first thing and commit
    git_test_project.add_content_as_file("foo", "foo content", commit=True)

    # repo will be dirty b/c we didn't commit this add
    git_test_project.add_content_as_file("goo", "goo content")

    version_str = cli._version(["--version", version])

    gh = git_test_project("rev-parse", "--short", "HEAD")[0]
    assert version_str == f"{version}+{gh}"


@pytest.mark.integration
def test_plox_version_from_file(git_test_project: GitTestProject) -> None:
    os.environ[common.project_dir_env] = str(git_test_project.proj_dir)
    # ensure there are comments in our test version content
    version = """
    # some notes about this version
    # and some more too
    // and another using the alternate leader
    0.101.0
    """

    # add first thing and commit
    git_test_project.add_content_as_file("VERSION", version, commit=True)

    version_str = cli._version(["--version", version])
    assert version_str == f"{version}"


# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4