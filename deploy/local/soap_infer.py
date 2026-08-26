"""Generates a SOAP note (Subjective/Objective/Assessment/Plan) from a
doctor-patient conversation transcript via the Gemini API. Needs
GEMINI_API_KEY (see deploy/.env.example). The note is written in English
regardless of the transcript's language -- standard practice for clinical
documentation in the Philippines even when the conversation itself was in
Bisaya/Cebuano.
"""

import os
import re

MODEL_ID = os.environ.get("BISAYA_SOAP_MODEL_ID", "gemini-3.6-flash")

SECTIONS = ["Subjective", "Objective", "Assessment", "Plan"]

_PROMPT = """You are a clinical scribe. Below is a transcript of a doctor-patient \
conversation conducted in Bisaya/Cebuano, produced by automatic speech \
recognition (it may contain transcription errors). Write a SOAP note in \
English summarizing it.

Respond with exactly these four headers, each on its own line, followed by \
that section's content -- no other headers, preamble, or commentary:

Subjective:
Objective:
Assessment:
Plan:

If the transcript doesn't give you enough to fill a section, write \
"Not enough information in the conversation." for that section.

Transcript:
{transcript}
"""


class SoapUnavailableError(Exception):
    """Raised when SOAP generation can't run (e.g. no API key) -- kept
    distinct from a generation failure so the UI can tell the two apart."""


def is_available():
    return bool(os.environ.get("GEMINI_API_KEY"))


def _parse(text):
    # Gemini's headers can come back with or without a trailing colon, and
    # re.split with a capturing group interleaves [pre, header, body, ...].
    pattern = r"(?im)^\s*(" + "|".join(SECTIONS) + r")\s*:?\s*$"
    parts = re.split(pattern, text)
    parsed = {name: "" for name in SECTIONS}
    for i in range(1, len(parts) - 1, 2):
        name = parts[i].strip().title()
        if name in parsed:
            parsed[name] = parts[i + 1].strip()
    return parsed


def generate_soap(transcript):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SoapUnavailableError(
            "GEMINI_API_KEY is not set -- add it to your .env file (see deploy/README.md)."
        )

    from google import genai

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=_PROMPT.format(transcript=transcript),
    )
    return _parse(response.text)
