# -*- coding: utf-8 -*-
from plox_version import common

# TODO: add more unit tests, and more meaningful unit tests; testing burden is
#   currently carried by integration tests.


def test_error_on_missing_envvar() -> None:
    try:
        common.env("FOO_MISSING")
        raise AssertionError("function under test failed to raise RuntimeError")
    except RuntimeError:
        pass


# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4
