export SHELL := /usr/bin/env TZ=UTC bash -o pipefail

DEBUG ?=
PYPI_ALIAS ?= testpypi

all: check

ifndef VERBOSE:
.SILENT:
endif

artifact: check
	@echo "+ $@"
	poetry build

check: test lint
	@echo "+ $@"

clean:
	@echo "+ $@"
	for d in src; do \
		find $$d -name "__pycache__" -exec rm -Rf {} + ; \
	done

distclean: clean
	@echo "+ $@"
	rm -Rf dist*

format:
	poetry run black .

install-deps:
	@echo "+ $@"
	poetry install

lint:
	@echo "+ $@"
	poetry run mypy .
	poetry run pyright .

realclean: distclean
	rm -Rf .venv

release: check
	@echo "+ $@"
	poetry publish -r $(PYPI_ALIAS) --build

test: test-unit test-integration

test-integration:
	@echo "+ $@"
	poetry run pytest -m "integration"

test-unit:
	@echo "+ $@"
	poetry run pytest -m "not integration"

.PHONY: artifact check clean distclean format install-deps lint realclean release test test-integration test-unit
