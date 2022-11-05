DOCKER_BIN := $(shell command -v docker || command -v podman)
SELENIUM_CONTAINER ?= selenium-server

ifneq (,$(wildcard /run/.containerenv))
	DOCKER_HOST := unix:///run/user/$(UID)/podman/podman.sock
	DOCKER_CMD := flatpak-spawn --host podman
else
	DOCKER_CMD := $(DOCKER_BIN)
endif

PYTHON = poetry run python
MANAGE = $(PYTHON) manage.py

install:
	poetry install
.PHONY: install

manage-%:
	$(MANAGE) $*
.PHONY: manage-%

makemigrations: manage-makemigrations
	$(MANAGE) makemigrations trackers
.PHONY: makemigrations

migrate: makemigrations manage-migrate
createsuperuser: manage-createsuperuser
shell: manage-shell
runserver: manage-runserver
test: manage-test

CONTAINER_FILTER = -f name=$(SELENIUM_CONTAINER)
EXITED_CONTAINER_FILTER = -f status=exited $(CONTAINER_FILTER)

selenium-start:
ifneq (,$(shell $(DOCKER_CMD) ps -q $(EXITED_CONTAINER_FILTER)))
	$(DOCKER_CMD) start $(SELENIUM_CONTAINER)
else ifneq (,$(shell $(DOCKER_CMD) ps -q $(CONTAINER_FILTER)))
else
	$(DOCKER_CMD) run -d --network host --privileged --name $(SELENIUM_CONTAINER) \
		docker.io/selenium/standalone-firefox
endif
	$(DOCKER_CMD) ps $(CONTAINER_FILTER)
	sleep 10
.PHONY: selenium-start

selenium-stop:
ifneq (,$(shell $(DOCKER_CMD) ps -q $(CONTAINER_FILTER)))
	$(DOCKER_CMD) stop $(SELENIUM_CONTAINER)
	$(DOCKER_CMD) ps $(EXITED_CONTAINER_FILTER)
endif
.PHONY: selenium-stop

selenium-clean:
ifneq (,$(shell $(DOCKER_CMD) ps -q $(CONTAINER_FILTER)))
	$(DOCKER_CMD) stop $(SELENIUM_CONTAINER)
	sleep 1
endif
ifneq (,$(shell $(DOCKER_CMD) ps -q $(EXITED_CONTAINER_FILTER)))
	$(DOCKER_CMD) container rm $(SELENIUM_CONTAINER)
	@echo $(SELENIUM_CONTAINER) Removed
endif
.PHONY: selenium-clean

functional-test: selenium-start
	poetry run python functional_tests.py
.PHONY: functional-test

clean-deplock:
ifeq (haslock,$(shell [ -f poetry.lock ] && echo haslock ))
	rm poetry.lock
endif
.PHONY: clean-deplock

clean-venv:
ifeq (hasvenv,$(shell [ -d .venv ] && echo hasvenv ))
	rm -r .venv
endif
.PHONY: clean-venv

clean-db:
ifeq (hasdb,$(shell [ -f db.sqlite3 ] && echo hasdb ))
	rm db.sqlite3
endif
.PHONY: clean-db

full-clean: clean-deplock clean-venv clean-db selenium-clean
.PHONY: full-clean
