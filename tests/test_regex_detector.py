"""
Unit tests for the regex-based PII detector.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from regex_detector import detect


def test_email_detection():
    result = detect("Contact me at john@email.com")
    emails = [m for m in result if m.entity_type == "EMAIL"]
    assert len(emails) == 1
    assert emails[0].text == "john@email.com"


def test_phone_detection():
    result = detect("Call me at 416-555-1234")
    phones = [m for m in result if m.entity_type == "PHONE"]
    assert len(phones) == 1
    assert phones[0].text == "416-555-1234"


def test_phone_with_extension():
    result = detect("Call 513-913-1481x05125 for support")
    phones = [m for m in result if m.entity_type == "PHONE"]
    assert len(phones) == 1
    assert phones[0].text == "513-913-1481x05125"


def test_ssn_detection():
    result = detect("His SSN is 123-45-6789")
    ssns = [m for m in result if m.entity_type == "SSN"]
    assert len(ssns) == 1
    assert ssns[0].text == "123-45-6789"


def test_credit_card_detection():
    result = detect("Card number: 4532 1488 0343 6467")
    cards = [m for m in result if m.entity_type == "CREDIT_CARD"]
    assert len(cards) == 1


def test_credit_card_does_not_match_phone():
    """Ensures the phone regex doesn't false-positive inside a card number."""
    result = detect("Card number is 376173825636")
    phones = [m for m in result if m.entity_type == "PHONE"]
    assert len(phones) == 0


def test_ip_address_detection():
    result = detect("Server IP: 192.168.1.1")
    ips = [m for m in result if m.entity_type == "IP_ADDRESS"]
    assert len(ips) == 1
    assert ips[0].text == "192.168.1.1"


def test_no_false_positives_on_plain_text():
    result = detect("This is just a normal sentence with no PII at all.")
    assert len(result) == 0