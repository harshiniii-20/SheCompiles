# ScamCheck Backend

FastAPI backend that analyzes job/internship postings and returns a scam risk score.

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Server runs at `http://127.0.0.1:8000`

## API

### `POST /check-posting`

**Request body:**
```json
{
  "jobText": "Urgent! Apply now, pay a registration fee..."
}
```

**Response:**
```json
{
  "score": 65,
  "riskLevel": "High Risk",
  "flaggedReasons": ["Requests payment or deposit", "Uses urgency language"]
}
```

## Tests

```bash
pytest
```