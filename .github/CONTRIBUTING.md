# Contributing Guide

This guide is for anyone who wishes to contribute code to Bhagavad Gita API.

Thank you for your interest and welcome here!

To work on this project you will need the following software installed in your machine.

- git (version control)
- python3.8 or above
- poetry (package management)
- make (command line utils)
- docker (optional, if you want to build docker images)
- docker-compose (optional, if you want to develop with docker-compose)

1. First of all fork and clone this repo. Checkout a new branch to start working.
For more information read
[GitHub's Docs](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
for beginners.

2. If you don't already have `poetry`, then [install it](https://python-poetry.org/docs/#installation).
Move into the project directory and run the following commands.

    ```shell
    poetry config virtualenvs.in-project true
    poetry install
    ```

3. The virtual environment will be created in a `.venv` folder inside your
project directory.
In your code editor set the python interpretor path to `./.venv/bin/python`

4. Activate poetry shell.

    ```shell
    poetry shell
    ```

5. Install pre-commit hooks.

    ```shell
    pre-commit install
    ```

6. Setup .env file refer .env.example.

    ```shell
    cp .env.example .env
    ```

7. Seed data to database.

    ```shell
    python bhagavad_gita_api/cli.py seed-data
    ```

8. To start the server with hot reload,

    ```shell
    uvicorn bhagavad_gita_api.main:app --host 0.0.0.0 --port 8081 --reload
    ```

    By default an in memory Sqlite database is used.
    To set the database DSN, tester API Key and other stuff, read about
    [configuration](../README.md/#Configuration) in the README.

9. Try to write test cases when you are adding a feature or fixing a bug.

10. Make sure that all existing tests, and code quality checks pass.

    ```shell
    pytest # run tests
    pre-commit run -a # run pre-commit for all files
    ```

11. Make sure to write meaningful commit messages.

12. Open a PR. Please explain what your changes does in a simple words.
Attach logs, screenshots and other relevant material.

Congrats and thanks for opening your first PR!
Please wait for the maintainers to respond.

---

## Developing with Docker and docker-compose

```shell

# setup .env file, refer .env.example file
cp .env.example .env

# run the project with docker-compose
docker-compose -f docker-compose.dev.yml up --build

```
