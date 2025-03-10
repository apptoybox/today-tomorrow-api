# Today Tomorrow API

A simple FastAPI application that provides endpoints for getting today's and tomorrow's dates in PDT timezone.

## Installation

```bash
pip install --requirement requirements.txt
```

## Running the API

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Endpoints

- `/today` - Returns today's date in PDT timezone
- `/tomorrow` - Returns tomorrow's date in PDT timezone
- `/docs` - Interactive API documentation (Swagger UI)
- `/redoc` - Alternative API documentation (ReDoc)
