"""
Generates synthetic sentences with known PII entities, using Faker,
for evaluating the detector against ground truth labels.
"""

import random
from dataclasses import dataclass
from faker import Faker

fake = Faker()


@dataclass
class LabelledEntity:
    entity_type: str
    text: str
    start: int
    end: int


@dataclass
class LabelledExample:
    text: str
    entities: list[LabelledEntity]


TEMPLATES = [
    "{PERSON} works at {ORGANIZATION} in {LOCATION}.",
    "Contact {PERSON} at {EMAIL} or {PHONE}.",
    "{PERSON}'s SSN is {SSN} and his card number is {CREDIT_CARD}.",
    "The server at {IP_ADDRESS} was accessed by {PERSON} from {LOCATION}.",
    "{PERSON} previously lived in {LOCATION} before joining {ORGANIZATION}.",
]


def generate_value(entity_type: str) -> str:
    if entity_type == "PERSON":
        return fake.name()
    elif entity_type == "ORGANIZATION":
        return fake.company()
    elif entity_type == "LOCATION":
        return fake.city()
    elif entity_type == "EMAIL":
        return fake.email()
    elif entity_type == "PHONE":
        return fake.phone_number()
    elif entity_type == "SSN":
        return fake.ssn()
    elif entity_type == "CREDIT_CARD":
        return fake.credit_card_number()
    elif entity_type == "IP_ADDRESS":
        return fake.ipv4()
    raise ValueError(f"Unknown entity type: {entity_type}")


def generate_example(template: str) -> LabelledExample:
    """
    Fill a template with fake values, tracking the exact position
    of each inserted entity in the final text.
    """
    text = ""
    entities = []
    cursor = 0
    remaining = template

    while "{" in remaining:
        before, rest = remaining.split("{", 1)
        entity_type, rest = rest.split("}", 1)

        text += before
        cursor += len(before)

        value = generate_value(entity_type)
        start = cursor
        end = cursor + len(value)

        entities.append(LabelledEntity(
            entity_type=entity_type,
            text=value,
            start=start,
            end=end,
        ))

        text += value
        cursor = end
        remaining = rest

    text += remaining
    return LabelledExample(text=text, entities=entities)


def generate_dataset(n: int) -> list[LabelledExample]:
    return [generate_example(random.choice(TEMPLATES)) for _ in range(n)]


if __name__ == "__main__":
    dataset = generate_dataset(5)
    for example in dataset:
        print(example.text)
        for ent in example.entities:
            print(f"  {ent.entity_type}: {ent.text} (pos {ent.start}-{ent.end})")
        print()