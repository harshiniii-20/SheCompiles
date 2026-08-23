from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.extractor import extract_entities
from app.models import JobPostingRequest, ScamCheckResponse
from app.scorer import analyze_posting
from app.verifier import verify_entities


app = FastAPI(title="ScamCheck API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "ScamCheck Backend is running!"}


@app.post("/check-posting", response_model=ScamCheckResponse)
def check_posting(request: JobPostingRequest):
    score, reasons = analyze_posting(request.jobText)

    entities = extract_entities(request.jobText)
    evidence = verify_entities(entities, request.jobText)

    reasons = list(reasons)

    for item in evidence:
        if item["detail"] not in reasons:
            reasons.append(item["detail"])

        if item["severity"] == "high":
            score += 15
        elif item["severity"] == "medium":
            score += 8
        else:
            score += 3

    score = min(score, 100)

    if score >= 70:
        risk_level = "High Risk"
    elif score >= 40:
        risk_level = "Suspicious"
    else:
        risk_level = "Low Risk"

    return {
        "score": score,
        "riskLevel": risk_level,
        "flaggedReasons": reasons,
        "extractedEntities": entities,
        "evidence": evidence,
    }