"""
FastAPI backend exposing the PII detector as a web API.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from combined_detector import CombinedDetector
from redactor import redact

app = FastAPI(title="Sensitive Info Detector API")
detector = CombinedDetector()


class TextRequest(BaseModel):
    text: str


class BatchTextRequest(BaseModel):
    texts: list[str]


class EntityResponse(BaseModel):
    entity_type: str
    text: str
    start: int
    end: int
    confidence: float
    source: str


class DetectResponse(BaseModel):
    entities: list[EntityResponse]


class BatchDetectResponse(BaseModel):
    results: list[DetectResponse]


class RedactResponse(BaseModel):
    original: str
    redacted: str
    entities: list[EntityResponse]


@app.post("/detect", response_model=DetectResponse)
def detect_endpoint(request: TextRequest):
    matches = detector.detect(request.text)
    return DetectResponse(
        entities=[
            EntityResponse(
                entity_type=m.entity_type,
                text=m.text,
                start=m.start,
                end=m.end,
                confidence=m.confidence,
                source=m.source,
            )
            for m in matches
        ]
    )


@app.post("/detect-batch", response_model=BatchDetectResponse)
def detect_batch_endpoint(request: BatchTextRequest):
    results = []
    for text in request.texts:
        matches = detector.detect(text)
        results.append(
            DetectResponse(
                entities=[
                    EntityResponse(
                        entity_type=m.entity_type,
                        text=m.text,
                        start=m.start,
                        end=m.end,
                        confidence=m.confidence,
                        source=m.source,
                    )
                    for m in matches
                ]
            )
        )
    return BatchDetectResponse(results=results)


@app.post("/redact", response_model=RedactResponse)
def redact_endpoint(request: TextRequest):
    matches = detector.detect(request.text)
    redacted_text = redact(request.text, matches)
    return RedactResponse(
        original=request.text,
        redacted=redacted_text,
        entities=[
            EntityResponse(
                entity_type=m.entity_type,
                text=m.text,
                start=m.start,
                end=m.end,
                confidence=m.confidence,
                source=m.source,
            )
            for m in matches
        ],
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}