"""
Unit tests for the redaction module.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from redactor import redact
from regex_detector import detect


def test_redact_single_entity():
    text = "Contact me at john@email.com"
    matches = detect(text)
    result = redact(text, matches)
    assert result == "Contact me at [EMAIL]"


def test_redact_multiple_entities():
    text = "Email john@email.com or call 416-555-1234"
    matches = detect(text)
    result = redact(text, matches)
    assert "[EMAIL]" in result
    assert "[PHONE]" in result
    assert "john@email.com" not in result
    assert "416-555-1234" not in result


def test_redact_no_entities():
    text = "This has no PII in it at all."
    matches = detect(text)
    result = redact(text, matches)
    assert result == text