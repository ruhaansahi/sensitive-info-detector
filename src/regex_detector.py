"""
Regex-based detector for structured PII: emails, phone numbers,
credit cards, SSNs, and IP addresses.
"""

import re
from dataclasses import dataclass


@dataclass
class Match:
    entity_type: str
    text: str
    start: int
    end: int


PATTERNS = {
    "EMAIL": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
    "PHONE": re.compile(r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'),
    "SSN": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
    "CREDIT_CARD": re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b'),
    "IP_ADDRESS": re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
}


def detect(text: str) -> list[Match]:
    """
    Scan text against all regex patterns and return matches
    with their type, text, and position.
    """
    matches = []
    for entity_type, pattern in PATTERNS.items():
        for m in pattern.finditer(text):
            matches.append(Match(
                entity_type=entity_type,
                text=m.group(),
                start=m.start(),
                end=m.end(),
            ))
    return matches


if __name__ == "__main__":
    sample = (
        "Contact John at john.doe@email.com or call 416-555-1234. "
        "His SSN is 123-45-6789 and his card number is 4532 1488 0343 6467. "
        "Server IP: 192.168.1.1"
    )
    for match in detect(sample):
        print(f"{match.entity_type}: {match.text} (pos {match.start}-{match.end})")