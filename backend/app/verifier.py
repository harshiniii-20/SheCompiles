import whois
from datetime import datetime, timezone


FREE_EMAIL_DOMAINS = {
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
    "rediffmail.com",
}


def verify_domain_age(domain: str) -> dict:
    """
    Looks up how long a domain has been registered.
    Newly registered domains are a common scam signal.
    """
    try:
        info = whois.whois(domain)
        creation_date = info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if not creation_date:
            return {
                "status": "Needs verification",
                "organization": domain,
                "detail": "Domain registration date could not be found.",
                "severity": "medium",
            }

        if creation_date.tzinfo is None:
            creation_date = creation_date.replace(tzinfo=timezone.utc)

        age_days = (datetime.now(timezone.utc) - creation_date).days

        if age_days < 180:
            return {
                "status": "Suspicious",
                "organization": domain,
                "detail": (
                    f"Domain was registered only {age_days} days ago. "
                    "New domains are commonly used in scams."
                ),
                "severity": "high",
            }
        elif age_days < 365:
            return {
                "status": "Needs verification",
                "organization": domain,
                "detail": (
                    f"Domain was registered {age_days} days ago "
                    "(under 1 year old). Verify independently."
                ),
                "severity": "medium",
            }
        else:
            years = age_days // 365
            return {
                "status": "Likely legitimate",
                "organization": domain,
                "detail": (
                    f"Domain has been registered for about {years} "
                    "year(s), which is a positive sign."
                ),
                "severity": "low",
            }

    except Exception as exc:
        print(f"WHOIS verification error: {exc}")

        return {
            "status": "Unavailable",
            "organization": domain,
            "detail": "Domain age could not be verified.",
            "severity": "low",
        }


def verify_entities(entities: dict, message: str) -> list[dict]:
    evidence = []

    emails = entities.get("emails", [])
    domains = entities.get("domains", [])
    phones = entities.get("phones", [])

    # --------------------------------------------------
    # 1. EMAIL CHECK
    # --------------------------------------------------
    for email in emails:
        email_domain = email.split("@", 1)[1].lower()

        if email_domain in FREE_EMAIL_DOMAINS:
            evidence.append({
                "category": "email",
                "title": "Free email address used",
                "detail": (
                    f"{email} uses a public email provider instead of "
                    "a company-owned domain."
                ),
                "severity": "medium",
            })
        else:
            evidence.append({
                "category": "email",
                "title": "Organization email domain detected",
                "detail": (
                    f"The sender uses the domain '{email_domain}', "
                    "which may belong to an organization."
                ),
                "severity": "low",
            })

    # --------------------------------------------------
    # 2. WEBSITE CHECK
    # --------------------------------------------------
    if domains:
        for domain in domains:
            evidence.append({
                "category": "website",
                "title": "Website/domain found",
                "detail": (
                    f"The message contains the organization domain "
                    f"'{domain}'."
                ),
                "severity": "low",
            })

    # --------------------------------------------------
    # 3. EMAIL <-> WEBSITE MATCH
    # --------------------------------------------------
    if emails and domains:

        email_domains = {
            email.split("@", 1)[1].lower()
            for email in emails
        }

        matching_domain = any(
            email_domain == domain
            or email_domain.endswith(f".{domain}")
            for email_domain in email_domains
            for domain in domains
        )

        if matching_domain:
            evidence.append({
                "category": "identity",
                "title": "Email and website domain match",
                "detail": (
                    "The sender's email domain matches a website "
                    "domain found in the message."
                ),
                "severity": "low",
            })

        else:
            evidence.append({
                "category": "identity",
                "title": "Email and website do not match",
                "detail": (
                    "The sender's email domain does not match any "
                    "website domain found in the message."
                ),
                "severity": "medium",
            })

    # --------------------------------------------------
    # 4. PHONE CHECK
    # --------------------------------------------------
    if phones:
        evidence.append({
            "category": "contact",
            "title": "Phone number detected",
            "detail": (
                "A phone number was found in the message. "
                "The number should be independently verified."
            ),
            "severity": "low",
        })

    # --------------------------------------------------
    # 5. NO ORGANIZATION INFORMATION
    # --------------------------------------------------
    if not emails and not domains:
        evidence.append({
            "category": "organization",
            "title": "Limited organization information",
            "detail": (
                "No organization email address or website domain "
                "was found in the message."
            ),
            "severity": "medium",
        })

    # --------------------------------------------------
    # 6. DOMAIN AGE VERIFICATION
    # --------------------------------------------------
    if domains:
        for domain in domains:
            verification = verify_domain_age(domain)

            evidence.append({
                "category": "organization",
                "title": "Organization verification",
                "detail": (
                    f"{verification['organization']}: "
                    f"{verification['detail']}"
                ),
                "severity": verification["severity"],
                "status": verification["status"],
                "organization": verification["organization"],
                "domain": domain,
            })

    return evidence