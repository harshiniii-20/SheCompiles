from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobPostingRequest(BaseModel):
    jobText: str

class ScamCheckResponse(BaseModel):
    score: int
    riskLevel: str
    flaggedReasons: List[str]

@app.get("/")
def home():
    return {"message": "ScamCheck Backend is running!"}

@app.post("/check-posting", response_model=ScamCheckResponse)
def check_posting(request: JobPostingRequest):
    text = request.jobText.lower()
    score = 0
    reasons = []

    if any(word in text for word in ["pay", "deposit", "registration fee", "processing fee", "security fee"]):
        score += 30
        reasons.append("Requests payment or deposit")

    if any(word in text for word in ["apply now", "limited seats", "immediate joining", "urgent", "hurry"]):
        score += 15
        reasons.append("Uses urgency language")

    if not any(word in text for word in ["www.", "http", ".com", "our company"]):
        score += 20
        reasons.append("Missing or vague company information")

    if any(word in text for word in ["gmail.com", "yahoo.com", "whatsapp", "telegram"]):
        score += 20
        reasons.append("Contact via personal email or messaging app instead of official channel")

    if any(word in text for word in ["no interview", "instant hire", "instant offer", "guaranteed job"]):
        score += 15
        reasons.append("Claims no interview or instant hiring")

    if any(word in text for word in ["earn up to", "huge salary", "unlimited earning"]):
        score += 15
        reasons.append("Unrealistic salary claims")

    score = min(score, 100)

    if score < 30:
        risk_level = "Safe"
    elif score < 60:
        risk_level = "Suspicious"
    else:
        risk_level = "High Risk"

    return ScamCheckResponse(score=score, riskLevel=risk_level, flaggedReasons=reasons)