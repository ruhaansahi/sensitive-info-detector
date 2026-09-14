"""
NER-based detector for unstructured PII: names, locations,
organizations, and other entities without a fixed pattern.
"""

import spacy
from dataclasses import dataclass

# Entity types spacy detects that we care about for PII
RELEVANT_LABELS = {
    "PERSON": "PERSON",
    "GPE": "LOCATION",       # countries, cities, states
    "LOC": "LOCATION",       # non-GPE locations
    "ORG": "ORGANIZATION",
    "FAC": "LOCATION",       # buildings, airports, etc.
}


@dataclass
class Match:
    entity_type: str
    text: str
    start: int
    end: int
    confidence: float


class NERDetector:
    def __init__(self, model_name: str = "en_core_web_trf"):
        self.nlp = spacy.load(model_name)

    def detect(self, text: str) -> list[Match]:
        doc = self.nlp(text)
        matches = []
        for ent in doc.ents:
            if ent.label_ in RELEVANT_LABELS:
                matches.append(Match(
                    entity_type=RELEVANT_LABELS[ent.label_],
                    text=ent.text,
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=1.0,  # spacy doesn't give per-entity confidence by default
                ))
        return matches


if __name__ == "__main__":
    detector = NERDetector()
    sample = (
        "John Smith works at Google in Toronto. "
        "He previously lived in New York before moving to Canada."
    )
    for match in detector.detect(sample):
        print(f"{match.entity_type}: {match.text} (pos {match.start}-{match.end})")