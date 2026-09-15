# sensitive-info-detector

# Sensitive Info Detector

Detects and redacts personal information (PII) in text, names, emails, phone numbers, SSNs, credit card numbers, and IP addresses, using a mix of regex pattern matching and a transformer-based NER model. NER stands for Named Entity Recognition, a task where a model reads text and labels parts of it as specific categories, like PERSON or ORGANIZATION, using a neural network trained to understand context.

🔗 **[Live Demo](https://sensitive-info-detector-ruhaansahi-cuqp7jb4wadeix9ecf8aun.streamlit.app/)**

## How it works

There are two detection layers that run on the same text:

1. **Regex** catches anything with a fixed format, emails, phone numbers, SSNs, credit cards, IP addresses. These don't need machine learning since the format is predictable.
2. **NER** (using spaCy's `en_core_web_trf` model) catches things without a fixed format, like names, company names, and locations.

Results from both layers get combined and sorted by where they appear in the text. From there, the detected entities can either just be listed, or the text can be redacted, each one gets swapped out for a placeholder like `[PERSON]` or `[EMAIL]`.

## What's included

- Regex + NER detection, combined into one pipeline
- Redaction (replacing detected entities with placeholders)
- An evaluation script that generates fake test data with Faker (a library that generates realistic fake names, emails, addresses, etc. for testing) and measures precision/recall/F1 for each entity type
- A FastAPI backend, a web server that lets other programs send text to the detector and get results back as structured data (JSON), instead of needing to run the Python code directly. It has three endpoints (specific URLs that do specific things):
  - `/detect` — send one piece of text, get back a list of everything sensitive found in it
  - `/detect-batch` — send multiple pieces of text at once, get back results for each one in a single request
  - `/redact` — send text, get back both the list of detected entities and a redacted version of the text with each one replaced by a placeholder like `[EMAIL]`
- A Streamlit app for a live demo with highlighting
- 14 unit tests covering the detection and redaction logic

## Accuracy

Tested against 50+ generated examples per entity type:

| Entity Type | Precision | Recall | F1 |
|---|---|---|---|
| EMAIL | 1.00 | 1.00 | 1.00 |
| PHONE | 1.00 | 1.00 | 1.00 |
| SSN | 1.00 | 1.00 | 1.00 |
| CREDIT_CARD | 1.00 | 1.00 | 1.00 |
| IP_ADDRESS | 1.00 | 1.00 | 1.00 |
| PERSON | 0.98 | 1.00 | 0.99 |
| ORGANIZATION | 0.91 | 0.95 | 0.93 |
| LOCATION | 1.00 | 0.94 | 0.97 |

The phone number regex originally missed numbers with extensions (like `x1234`), and once I fixed that, it started matching parts of credit card numbers by accident since both are just long digit strings. Had to add a check that blocks a match if it's directly followed by another digit. Similar issue with credit cards, they aren't always 16 digits (Amex uses 15), so the pattern needed to accept a range instead of one fixed length.

## Tech stack

- **Python** — main language
- **spaCy** — an NLP (natural language processing) library, used here to run the NER model (Named Entity Recognition. It's a task in NLP where a model reads through text and picks out specific words or phrases, then labels each one with a category, like PERSON, ORGANIZATION, or LOCATION.)
- **HuggingFace Transformers** — a library for using transformer-based models (the same underlying architecture behind models like BERT and GPT, good at understanding context in text rather than just matching keywords)
- **PyTorch** — the deep learning framework the transformer model runs on
- **FastAPI** — used to build the backend API
- **Streamlit** — used to build the interactive web demo
- **scikit-learn** — used to calculate precision, recall, and F1 for evaluation
- **Faker** — generates fake but realistic test data
- **pytest** — testing framework

## Running it locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_trf

# Streamlit demo
streamlit run src/app.py

# API
cd src
uvicorn api:app --reload
```

## API example

```bash
curl -X POST http://127.0.0.1:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Contact John at john@email.com or 416-555-1234"}'
```

```json
{
  "entities": [
    {"entity_type": "PERSON", "text": "John", "start": 8, "end": 12, "confidence": 1.0, "source": "ner"},
    {"entity_type": "EMAIL", "text": "john@email.com", "start": 16, "end": 30, "confidence": 1.0, "source": "regex"},
    {"entity_type": "PHONE", "text": "416-555-1234", "start": 34, "end": 46, "confidence": 1.0, "source": "regex"}
  ]
}
```

## What's not built yet

- Real confidence scores for the NER layer, right now it just returns 1.0 for every match since spaCy doesn't expose this by default. Would need to swap in a HuggingFace model directly to get real probabilities (a number showing how sure the model is about each prediction).
- File upload (PDF/DOCX), the API only takes raw text right now.
- ORGANIZATION and LOCATION detection could be more accurate, this is a spaCy model limitation more than something in my code.

## Notes

Built with AI-assisted development. I tested and debugged everything myself, made the actual decisions on what to build and how, and can explain every part of this project in detail.
