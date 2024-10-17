PY = python
POETRY = poetry run python

MAIN_FILE = src/main.py

REQUIREMENTS_FILE = requirements.txt

NAME_REPOSITORY = PersonalVoiceAssistant

SSH = git@github.com:LebedevSergeyVach/PersonalVoiceAssistant.git
HTTPS = https://github.com/LebedevSergeyVach/PersonalVoiceAssistant.git

GCC = gcc

C_FILE = assistant.c
EXE_FILE = assistant.exe

.PHONY: all

all: run

run: py_run_pva

install: pip_install_lib

pull: git-repository-pull

restart: full-restart-project

exe: add-path-exe-for-command

help: help-makefile


py_run_pva:
	@$(PY) $(MAIN_FILE)

poetry_run_pva:
	@$(POETRY) $(MAIN_FILE)

pip_install_lib:
	@echo "Installing all necessary libraries and packages"
	@pip install -r $(REQUIREMENTS_FILE)
	@python -m spacy download ru_core_news_sm

git-repository-pull:
	@git status
	@git pull

full-restart-project:
	@echo "Starting to reinstall the project"
	@echo "Complete deletion of the project"
	@if [ -d $(NAME_REPOSITORY) ]; then \
		cd .. && rm -rf $(NAME_REPOSITORY); \
	else \
		echo "Directory $(NAME_REPOSITORY) does not exist"; \
	fi
	@echo "Installing a remote repository on your computer"
	@cd .. && git clone $(HTTPS)
	@cd $(NAME_REPOSITORY)
	@echo "Installing all necessary libraries and packages"
	@pip_install_lib
	@echo "The project is completely reinstalled and ready to work"

add-path-exe-for-command:
	@echo "Be sure to add this directory to the PATH to call the assistant command"
	@$(GCC) $(C_FILE) -o $(EXE_FILE)

help-makefile:
	@echo "Makefile for PersonalVoiceAssistant"
	@echo "run       ->   Launching the Voice Assistant"
	@echo "pull      ->   Pull project git repository"
	@echo "install   ->   installing all libraries and packages PIP"
	@echo "restart   ->   Complete reinstallation of the project"
	@echo "exe       ->   Assemble the exe file to launch the voice assistant"
	@echo "help      ->   Help with Makefile commands"
