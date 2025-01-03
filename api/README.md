# finops-api

## Setup and Run
- uv pip install -r pyproject.toml
- uv run fastapi dev

## Testing
- Run all tests except e2e: `pytest`
- Run e2e tests only: `pytest *e2e.py -v`
- Run all tests including e2e: `pytest --ignore-glob="" -v`