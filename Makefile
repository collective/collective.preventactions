#!/usr/bin/make
.PHONY: help  # List phony targets
help:
	@cat "Makefile" | grep '^.PHONY:' | sed -e "s/^.PHONY:/- make/"

.PHONY: install  # Install project
install: ./bin/pip
	./bin/pip install -r https://dist.plone.org/release/6.1.0/requirements.txt
	./bin/buildout -c buildout.cfg

.PHONY: test  # Test project
test: install
	./bin/test

.PHONY: start  # Start project
start: install
	./bin/instance fg

.PHONY: cleanall  # Clean environment
cleanall:
	rm -rf bin develop-eggs downloads include lib parts .installed.cfg .mr.developer.cfg bootstrap.py

.PHONY: update-locales  # Update locales
update-locales:
	./update-locales.sh

./bin/pip:
	python3.12 -m venv .
