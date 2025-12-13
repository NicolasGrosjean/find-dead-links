# Find dead links

> Scrap website to find dead links

## Install

This project use [uv](https://docs.astral.sh/uv/),
an extremely fast Python package and project manager, written in Rust.

```shell
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

## Run

Scrap website with the following command

```shell
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
