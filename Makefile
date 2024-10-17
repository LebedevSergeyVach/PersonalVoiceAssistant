PY = python
POETRY = poetry run python

MAIN_FILE = src/main.py

REQUIREMENTS_FILE = requirements.txt

NAME_REPOSITORY = PersonalVoiceAssistant

SSH = git@github.com:LebedevSergeyVach/PersonalVoiceAssistant.git
HTTPS = https://github.com/LebedevSergeyVach/PersonalVoiceAssistant.git

.PHONY: all

all: run

run: py_run_pva

install: pip_install_lib

pull: git-repository-pull

restart: full-restart-project

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

full-restart-project: pip_install_lib
	@echo "Starting to reinstall the project"
	@echo "Complete deletion of the project"
	@cd ..
	@rm -rf $(NAME_REPOSITORY)
	@echo "Installing a remote repository on your computer"
	@git clone $(HTTPS)
	@cd $(NAME_REPOSITORY)
	@echo "Installing all necessary libraries and packages"
	@pip_install_lib
	@echo "The project is completely reinstalled and ready to work"


help-makefile:
	@echo "Makefile for PersonalVoiceAssistant"
	@echo "run       ->   start project"
	@echo "pull      ->   pull project git repository"
	@echo "install   ->   pip install lib for project"
	@echo "help      ->   help commands Makefile"
