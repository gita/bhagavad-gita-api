<p align="center">
  <a href="https://bhagavadgita.io">
    <img src="gita.png" alt="Logo" width="300">
  </a>

  <h3 align="center">Bhagavad Gita API v2</h3>

  <p align="center">
    Code for the BhagavadGita.io v2 API, which is an app built for Gita readers by Gita readers.
    <br />
    <br />
    <a href="https://api.bhagavadgita.io/docs">View Docs</a>
    ·
    <a href="https://github.com/gita/bhagavadgita-api/issues">Report Bug</a>
    ·
    <a href="https://github.com/gita/bhagavadgita-api/issues">Request Feature</a>
  </p>
</p>

<p align="center">
  <a href="https://github.com/gita/bhagavad-gita-api/blob/master/LICENSE">
    <img alt="LICENSE" src="https://img.shields.io/badge/License-MIT-yellow.svg?maxAge=43200">
  </a>
  <a href="https://starcharts.herokuapp.com/gita/bhagavad-gita-api"><img alt="Stars" src="https://img.shields.io/github/stars/gita/bhagavad-gita-api.svg?style=social"></a>
</p>


## Project Structure
```
.
├── LICENSE
├── README.md
├── gita.png
├── mypy.ini
├── poetry.lock
├── pyproject.toml
├── run.py
└── src
    ├── __init__.py
    ├── api
    │   ├── __init__.py
    │   ├── api_v2
    │   │   ├── __init__.py
    │   │   ├── api.py
    │   │   └── endpoints
    │   │       ├── __init__.py
    │   │       └── gita.py
    │   └── deps.py
    ├── config.py
    ├── crud.py
    ├── data.sh
    ├── db
    │   ├── __init__.py
    │   ├── base_class.py
    │   ├── init_db.py
    │   └── session.py
    ├── gita_data
    │   ├── authors.json
    │   ├── chapters.json
    │   ├── commentary.json
    │   ├── languages.json
    │   ├── translation.json
    │   └── verse.json
    ├── graphql2.py
    ├── initial_data.py
    ├── main.py
    ├── models
    │   ├── __init__.py
    │   ├── gita.py
    │   └── user.py
    ├── schemas
    │   ├── __init__.py
    │   └── gita.py
    ├── scripts
    │   ├── __init__.py
    │   ├── insert_authors.py
    │   ├── insert_chapters.py
    │   ├── insert_commentaries.py
    │   ├── insert_languages.py
    │   ├── insert_reference_verse_into_chapters.py
    │   ├── insert_references_commentaries.py
    │   ├── insert_references_translations.py
    │   ├── insert_translations.py
    │   └── insert_verses.py
    └── utils.py
```

## Developing Locally

### Without Docker

1. Install [pyenv](https://github.com/pyenv/pyenv).
2. Setup Python 3.8.10 using `pyenv install 3.8.10`.
3. Activate that version in the current session shell:

```bash
$ pyenv shell 3.8.10
$ python --version
Python 3.8.10
```

4. Setup the Python version for the project.

```bash
pyenv local 3.8.10
```

5. Install [Poetry](https://python-poetry.org/docs/#installation)
6. Init poetry in the root of the project.

```bash
poetry init
```

7. Install the dependencies using:

```bash
poetry install
```

8. Install `pre-commit` hook in local repo:

```bash
poetry run pre-commit install
```

9. Activate Poetry virtual env using:

```bash
poetry shell
```

10. Create a file called `.env` in app directory with the following credentials:
```
SQLALCHEMY_DATABASE_URI=YOUR_SQLALCHEMY_DATABASE_URI
TESTER_API_KEY=RANDOM_STRING
```
Make sure to replace `YOUR_SQLALCHEMY_DATABASE_URI` with your own local Postgres database credentials.

11. Initialize the database using:
```bash
bash data.sh
```
12. cd to the app folder and run `uvicorn main:app --host 0.0.0.0 --port 8081 --reload`.
13. The docs can be accessed at `http://localhost:8081/docs`.
- Use your TESTER_API_KEY from `.env` on the docs page to test the API.

### With Docker

1. Fork this repository and clone the forked repository.
2. Make sure docker and docker-compose are installed.
3. Use `docker-compose -f docker-compose-dev.yml up` to install the requirements and start the development server.
4. API can be accessed at `http://0.0.0.0:8000/docs`.
