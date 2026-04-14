[![Build Status](https://github.com/NicolasGrosjean/find-dead-links/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/NicolasGrosjean/find-dead-links/actions/workflows/lint_and_test.yml)
[![Tests](badges/tests.svg)](https://github.com/NicolasGrosjean/find-dead-links/actions/workflows/lint_and_test.yml)
[![Coverage](badges/coverage.svg)](https://github.com/NicolasGrosjean/find-dead-links/actions/workflows/lint_and_test.yml)


# Find dead links

> Scrap website (or analyse the markdown files) to find dead links

## Install

This project use [uv](https://docs.astral.sh/uv/),
an extremely fast Python package and project manager, written in Rust.

```bash
uv sync
uv run pre-commit install
uv run python -m playwright install
```

## [Activate environment](https://docs.astral.sh/uv/pip/environments/#using-a-virtual-environment)

Useful to run `task` commands

**macOS/Linux** :

```bash
source .venv/bin/activate
```

**windows** :

```bash
.venv\Scripts\activate
```

## Run the search against files

Assuming, the content in which we want to find links is in `../resources-center/content`,
and we want the result into `links.csv`.

**macOS/Linux** :

```bash
PYTHONPATH=$PWD uv run python find_dead_links/analyse_links_from_files.py ../resources-center/content links.csv http://localhost:3000
```

**windows** :

```bash
set PYTHONPATH=%CD%/..;%PYTHONPATH% && uv run python find_dead_links/analyse_links_from_files.py ../resources-center/content links.csv http://localhost:3000
```

We can add `--try-again` to retry again non reachable links.

## Run the scraping

Scrap website with the following command

```bash
cd find_dead_links
scrapy crawl complex_website_links -O links.json -L INFO
```

## Tests

**macOS/Linux** :

```bash
task test
```

**windows** :

```bash
task test-windows
```

## Pre-commit

```bash
task pre-commit
```
