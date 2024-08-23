export SHELL := /usr/bin/env TZ=UTC bash -o pipefail

DEBUG ?=
PYPI_ALIAS ?= testpypi

PYSRC_DIR = $(CURDIR)
export IMG_VERSION=$(shell ./plox-common/scripts/get-version)


all: check


include ./plox-common/makefiles/Makefile.python.in

# these targets are declared "phony" so that make won't skip them if a
# file named after the target exists
.PHONY: all $(python-phonies) $(gittooled-phonies) $(py-check-phonies) $(git-check-phonies) container-app-image publish
