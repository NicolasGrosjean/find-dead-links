[![Build Status](https://github.com/NicolasGrosjean/find-dead-links/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/NicolasGrosjean/find-dead-links/actions/workflows/lint_and_test.yml)
[![Tests](badges/tests.svg)](https://github.com/NicolasGrosjean/find-dead-links/actions/workflows/lint_and_test.yml)
[![Coverage](badges/coverage.svg)](https://github.com/NicolasGrosjean/find-dead-links/actions/workflows/lint_and_test.yml)
[![Docker](badges/docker.svg)](https://hub.docker.com/r/nicolasgrosjean38/find_dead_links_from_markdown)


# Find dead links

> Scrap website (or analyse the markdown files) to find dead links

## Install

This project use [uv](https://docs.astral.sh/uv/),
an extremely fast Python package and project manager, written in Rust.

```bash
uv sync
uv run pre-commit install

# Install playwright for the scrapping, not necessary for find dead links from markdown files
uv run python -m playwright install
```

## [Activate environment](https://docs.astral.sh/uv/pip/environments/#using-a-virtual-environment)

Useful to run `task` commands, you can skip this part to run with docker

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

Nota: We can add `--try-again` to retry again non reachable links.

**macOS/Linux** :

```bash
PYTHONPATH=$PWD uv run python find_dead_links/analyse_links_from_files.py ../resources-center/content links.csv http://localhost:3000
```

**windows** :

```bash
set PYTHONPATH=%CD%/..;%PYTHONPATH% && uv run python find_dead_links/analyse_links_from_files.py ../resources-center/content links.csv http://localhost:3000
```

**docker** :

```bash
docker run --rm --name find_dead_links_from_markdown -e DIR_TO_ANALYSE=/data -e OUTPUT_FILE=/data/links.csv -v  $(pwd)/../resources-center/content:/data docker.io/nicolasgrosjean38/find_dead_links_from_markdown
```

Nota: the docker image is built and published with the folowwing commands

```bash
export DOCKER_IMAGE_VERSION="1.0.0"
docker build -t docker.io/nicolasgrosjean38/find_dead_links_from_markdown:$DOCKER_IMAGE_VERSION .
docker login docker.io -u nicolasgrosjean38
# Fill with token get from https://app.docker.com/accounts/nicolasgrosjean38/settings/personal-access-tokens
docker push docker.io/nicolasgrosjean38/find_dead_links_from_markdown:$DOCKER_IMAGE_VERSION
```

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
