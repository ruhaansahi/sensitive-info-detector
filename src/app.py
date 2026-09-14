"""
Streamlit demo for the PII detector. Paste text in, see detected
entities highlighted, and view the redacted version.
"""

import streamlit as st
from combined_detector import CombinedDetector

st.set_page_config(page_title="Sensitive Info Detector", layout="wide")

COLORS = {
    "PERSON": "#ffadad",
    "ORGANIZATION": "#ffd6a5",
    "LOCATION": "#fdffb6",
    "EMAIL": "#caffbf",
    "PHONE": "#9bf6ff",
    "SSN": "#a0c4ff",
    "CREDIT_CARD": "#bdb2ff",
    "IP_ADDRESS": "#ffc6ff",
}


@st.cache_resource
def load_detector():
    return CombinedDetector()


def highlight_text(text: str, matches: list) -> str:
    """Build an HTML string with each match wrapped in a coloured span."""
    sorted_matches = sorted(matches, key=lambda m: m.start, reverse=True)
    html = text
    for m in sorted_matches:
        color = COLORS.get(m.entity_type, "#dddddd")
        span = (
            f'<span style="background-color:{color}; padding:2px 4px; '
            f'border-radius:4px;" title="{m.entity_type} ({m.confidence:.2f})">'
            f'{html[m.start:m.end]}</span>'
        )
        html = html[:m.start] + span + html[m.end:]
    return html.replace("\n", "<br>")


st.title("Sensitive Info Detector")
st.write("Paste text below to detect and redact sensitive information.")

detector = load_detector()

text_input = st.text_area("Input text", height=200, placeholder="Paste text here...")

if text_input:
    matches = detector.detect(text_input)

    st.subheader("Detected entities")
    if matches:
        st.markdown(highlight_text(text_input, matches), unsafe_allow_html=True)
    else:
        st.write("No sensitive information detected.")

    st.subheader("Entity list")
    for m in matches:
        st.write(f"**{m.entity_type}** ({m.source}, confidence {m.confidence:.2f}): `{m.text}`")

    with st.expander("View as API response (JSON)"):
        st.json({
            "entities": [
                {
                    "entity_type": m.entity_type,
                    "text": m.text,
                    "start": m.start,
                    "end": m.end,
                    "confidence": m.confidence,
                    "source": m.source,
                }
                for m in matches
            ]
        })

    st.subheader("Redacted text")
    from redactor import redact
    st.write(redact(text_input, matches))