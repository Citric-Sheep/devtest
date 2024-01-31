
# Dev Test

## Usage

Make sure you have docker and docker compose installed in your machine:

```bash
docker compose up -d --build
```

or, using uvicorn (install poetry and pyenv):

```bash
poetry shell
```

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```