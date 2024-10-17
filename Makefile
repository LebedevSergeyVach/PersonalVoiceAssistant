PY = python
POETRY = poetry run python

MAIN_FILE = src/main.py

REQUIREMENTS_FILE = requirements.txt

.PHONY: all

all: run

run: py_run_pva

install: pip_install_lib

pull: git-repository-pull

help: help-makefile


py_run_pva:
	@$(PY) $(MAIN_FILE)

poetry_run_pva:
	@$(POETRY) $(MAIN_FILE)

pip_install_lib:
	@pip install -r $(REQUIREMENTS_FILE)
	@python -m spacy download ru_core_news_sm

git-repository-pull:
	@git status
	@git pull

help-makefile:
	@echo "Makefile for PersonalVoiceAssistant"
	@echo "run       ->   start project"
	@echo "pull      ->   pull project git repository"
	@echo "install   ->   pip install lib for project"
	@echo "help      ->   help commands Makefile"
