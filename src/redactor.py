"""
Takes detected PII matches and produces a redacted version of
the input text, replacing each entity with a type placeholder.
"""

from combined_detector import Match


def redact(text: str, matches: list[Match]) -> str:
    """
    Replace each detected entity in the text with [ENTITY_TYPE],
    working from the end of the text backwards so earlier positions
    don't shift as replacements happen.
    """
    sorted_matches = sorted(matches, key=lambda m: m.start, reverse=True)

    redacted = text
    for m in sorted_matches:
        placeholder = f"[{m.entity_type}]"
        redacted = redacted[:m.start] + placeholder + redacted[m.end:]

    return redacted


if __name__ == "__main__":
    from combined_detector import CombinedDetector

    detector = CombinedDetector()
    sample = (
        "John Smith works at Google in Toronto. "
        "Contact him at john.smith@email.com or 416-555-1234. "
        "His SSN is 123-45-6789."
    )
    matches = detector.detect(sample)
    print("Original:")
    print(sample)
    print("\nRedacted:")
    print(redact(sample, matches))