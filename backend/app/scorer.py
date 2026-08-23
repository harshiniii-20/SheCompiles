RISK_RULES = [
    (
        [
            "registration fee",
            "processing fee",
            "security fee",
            "training fee",
            "refundable deposit",
            "advance payment",
            "pay a fee",
            "pay to apply",
            "processing charge",
            "activation fee",
        ],
        30,
        "Requests payment or deposit",
    ),
    (
        [
            "apply now",
            "limited seats",
            "immediate joining",
            "urgent",
            "hurry",
        ],
        15,
        "Uses urgency language",
    ),
    (
        [
            "gmail.com",
            "yahoo.com",
            "hotmail.com",
            "outlook.com",
            "whatsapp",
            "telegram",
        ],
        20,
        "Uses personal email or messaging app instead of an official channel",
    ),
    (
        [
            "no interview",
            "instant hire",
            "instant offer",
            "guaranteed job",
        ],
        15,
        "Claims no interview or instant hiring",
    ),
    (
        [
            "earn up to",
            "huge salary",
            "unlimited earning",
        ],
        15,
        "Makes unrealistic salary claims",
    ),
]


COMPANY_INFO_MARKERS = [
    "www.",
    "http",
    ".com",
    ".in",
    ".org",
    "our company",
]


def analyze_posting(job_text: str) -> tuple[int, list[str]]:
    """
    Scores a job posting for scam-risk keywords.
    Returns (score, reasons) - risk level is decided by the caller,
    which also folds in verification evidence.
    """
    text = job_text.lower().strip()

    score = 0
    reasons = []

    for keywords, weight, reason in RISK_RULES:
        if any(keyword in text for keyword in keywords):
            score += weight
            reasons.append(reason)

    if not any(marker in text for marker in COMPANY_INFO_MARKERS):
        score += 20
        reasons.append("Missing or vague company information")

    score = min(score, 100)

    return score, reasons