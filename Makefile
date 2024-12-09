PROJECT_NAME := $(shell basename $(PWD))
VENV_PATH = ~/.venv/$(PROJECT_NAME)

DATA_DIR := data
TCX_FILES := $(shell find $(DATA_DIR) -type f -name '*.TCX')

all: clean

venv:
	@python3 -m venv $(VENV_PATH)

install: venv
	@source $(VENV_PATH)/bin/activate && \
	pip install --disable-pip-version-check -q -r requirements.txt

jupyter: install
	@source $(VENV_PATH)/bin/activate && \
	python3 -m ipykernel install \
	--user \
	--name "$(PROJECT_NAME)" \
	--display-name "$(PROJECT_NAME)" \
	> /dev/null 2>&1

clean: $(TCX_FILES)
	@for file in $^ ; do \
		source $(VENV_PATH)/bin/activate && \
		python3 scripts/clean.py $${file}; \
	done

.PHONY: venv install jupyter
