<div align="center">
    <img height=100 src="https://fastapi.tiangolo.com/img/favicon.png" alt="Barone API icon">
    <h1>Markitdown API</h1>
    <p>Markitdown CLI tool wrapped in FastAPI.</p>
    <p>
        <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI"></img></a>
        <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.12%2B-blue" alt="Python3.12"></img></a>
    </p>
    <p>
        <a href="https://github.com/seyLu/markitdown-api/issues/new">Report Bug</a>
        ·
        <a href="https://github.com/seyLu/markitdown-api/issues/new">Request Feature</a>
        ·
        <a href="https://github.com/seyLu/markitdown-api/discussions">Ask Question</a>
    </p>
</div>

<br>

### Architecture

This project is a Modular Monolith built with Vertical Slice Architecture (VSA). Each domain is a self-contained package encapsulating its own API, logic, and data models.

```
src
|- [domain]
   |- router.py    # API Endpoints
   |- models.py    # Database Tables
   |- service.py   # Business Logic
   |- ...
```

It is inspired by [Netflix/dispatch](https://github.com/Netflix/dispatch) and the [Official FastAPI template](https://github.com/fastapi/full-stack-fastapi-template).

<br>

### Developing locally

> NOTE: This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/). Make sure it is installed before proceeding.

#### 1. Create virtual environment

```bash
uv venv
```

#### 2. Activate virtual environment

```bash
source .venv/bin/activate
```

#### 3. Install dependencies

```bash
uv sync
```

#### 4. Create .env file

```bash
cp .env.example .env
```

Supply `.env` with your values.

#### 5. Run the app locally

```bash
fastapi dev
```

Documentation is located on `/docs`.

<br>

### Configure pre-commit for linting and automatic client generation

```bash
pre-commit install
```
