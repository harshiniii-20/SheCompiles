import re
from urllib.parse import urlparse


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

URL_PATTERN = re.compile(
    r"https?://[^\s<>\"]+|(?:www\.)[^\s<>\"]+"
)

PHONE_PATTERN = re.compile(
    r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)"
)


def clean_url(value: str) -> str:
    value = value.rstrip(".,!?;:)")

    if not value.startswith(("http://", "https://")):
        value = f"https://{value}"

    return value


def extract_entities(text: str) -> dict:
    emails = sorted(set(EMAIL_PATTERN.findall(text)))

    raw_urls = URL_PATTERN.findall(text)
    urls = sorted(set(clean_url(url) for url in raw_urls))

    phones = sorted(set(PHONE_PATTERN.findall(text)))

    domains = sorted(
        set(
            urlparse(url).netloc.lower().removeprefix("www.")
            for url in urls
        )
    )

    return {
        "emails": emails,
        "urls": urls,
        "domains": domains,
        "phones": phones,
    }