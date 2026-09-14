"""
Unit tests for the NER-based PII detector.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ner_detector import NERDetector


def test_person_detection():
    detector = NERDetector()
    result = detector.detect("John Smith works here.")
    persons = [m for m in result if m.entity_type == "PERSON"]
    assert len(persons) == 1
    assert persons[0].text == "John Smith"


def test_location_detection():
    detector = NERDetector()
    result = detector.detect("He lives in Toronto.")
    locations = [m for m in result if m.entity_type == "LOCATION"]
    assert len(locations) == 1
    assert locations[0].text == "Toronto"


def test_organization_detection():
    detector = NERDetector()
    result = detector.detect("She works at Google.")
    orgs = [m for m in result if m.entity_type == "ORGANIZATION"]
    assert len(orgs) == 1
    assert orgs[0].text == "Google"