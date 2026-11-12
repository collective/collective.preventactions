#!/usr/bin/make
TOX=uvx --with tox-uv tox

ifeq (, $(shell which uv ))
  $(error "[ERROR] The 'uv' command is missing from your PATH. Install it from: https://docs.astral.sh/uv/getting-started/installation/")
endif

.PHONY: help
help: ## Display this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Run tests on Python 3.12 with Plone 6.2.3
	$(TOX) -e py312-plone62

.PHONY: test-all
test-all: ## Run lint, all supported Python / Plone versions and dependency checks
	$(TOX)

.PHONY: lint
lint: ## Run pre-commit hooks
	$(TOX) -e lint

.PHONY: format
format: ## Reformat code (pyupgrade, isort, black, zpretty)
	$(TOX) -e format

.PHONY: update-locales
update-locales: ## Update locales
	./update-locales.sh

.PHONY: clean
clean: ## Remove tox environments and build artifacts
	rm -rf .tox .venv build dist htmlcov .coverage coverage.xml src/*.egg-info
