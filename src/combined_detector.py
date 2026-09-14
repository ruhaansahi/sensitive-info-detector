"""
Combines regex-based and NER-based detection into one unified
PII detector, merging results sorted by position in the text.
"""

from dataclasses import dataclass
from regex_detector import detect as regex_detect
from ner_detector import NERDetector


@dataclass
class Match:
    entity_type: str
    text: str
    start: int
    end: int
    confidence: float
    source: str  # "regex" or "ner"


class CombinedDetector:
    def __init__(self, model_name: str = "en_core_web_trf"):
        self.ner = NERDetector(model_name=model_name)

    def detect(self, text: str) -> list[Match]:
        matches = []

        for m in regex_detect(text):
            matches.append(Match(
                entity_type=m.entity_type,
                text=m.text,
                start=m.start,
                end=m.end,
                confidence=1.0,  # regex is deterministic, always exact
                source="regex",
            ))

        for m in self.ner.detect(text):
            matches.append(Match(
                entity_type=m.entity_type,
                text=m.text,
                start=m.start,
                end=m.end,
                confidence=m.confidence,
                source="ner",
            ))

        matches.sort(key=lambda m: m.start)
        return matches


if __name__ == "__main__":
    detector = CombinedDetector()
    sample = (
        "John Smith works at Google in Toronto. "
        "Contact him at john.smith@email.com or 416-555-1234. "
        "His SSN is 123-45-6789."
    )
    for match in detector.detect(sample):
        print(f"[{match.source}] {match.entity_type}: {match.text} (pos {match.start}-{match.end}, conf {match.confidence})")