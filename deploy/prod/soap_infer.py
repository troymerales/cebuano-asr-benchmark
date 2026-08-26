"""Placeholder SOAP-note generator for the public demo. Deliberately does
NOT call the Gemini API -- this app gets anonymous public traffic, and a
real call per transcription would burn the deployer's API quota. Real
generation only runs in the local demo, gated behind a personal
GEMINI_API_KEY (see deploy/local/soap_infer.py). Same generate_soap()
interface as that module, so both apps' UI code renders identically.
"""

SECTIONS = ["Subjective", "Objective", "Assessment", "Plan"]

_PLACEHOLDER = (
    "SOAP generation is disabled in this public demo to avoid using up "
    "API quota on anonymous traffic. Run the local demo with your own "
    "GEMINI_API_KEY to see a real SOAP note here -- see deploy/README.md."
)


class SoapUnavailableError(Exception):
    pass


def is_available():
    return True


def generate_soap(transcript):
    return {name: _PLACEHOLDER for name in SECTIONS}
