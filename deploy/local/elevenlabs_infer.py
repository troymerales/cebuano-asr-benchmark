"""ElevenLabs Scribe transcription for one ad-hoc audio file -- calls the
same API evaluate_elevenlabs.ipynb uses. Needs ELEVENLABS_API_KEY in the
environment (see deploy/README.md).
"""

import os


class QuotaExceededError(RuntimeError):
    """Raised when ElevenLabs reports the API key is out of credits/quota
    (HTTP 401/429) -- kept distinct from other failures so the UI can show
    a specific warning banner instead of a generic error message."""


_client = None


def is_available():
    return bool(os.environ.get("ELEVENLABS_API_KEY"))


def _get_client():
    global _client
    if _client is None:
        if not is_available():
            raise RuntimeError(
                "ELEVENLABS_API_KEY is not set -- add it to your .env file "
                "(see deploy/README.md)."
            )
        from elevenlabs.client import ElevenLabs
        _client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    return _client


def _is_quota_error(e):
    # The SDK can raise different exception shapes depending on transport;
    # check both a status-code attribute (however it's spelled) and the
    # message text, rather than relying on one specific exception class.
    status = (
        getattr(e, "status_code", None)
        or getattr(getattr(e, "response", None), "status_code", None)
    )
    if status in (401, 429):
        return True
    message = str(e).lower()
    return "quota" in message or "credit" in message or " 401" in message or " 429" in message


def transcribe(audio_path):
    client = _get_client()
    try:
        with open(audio_path, "rb") as f:
            result = client.speech_to_text.convert(
                file=f, model_id="scribe_v2", language_code="ceb",
            )
    except Exception as e:
        if _is_quota_error(e):
            raise QuotaExceededError(
                "ElevenLabs transcription failed: Token quota exceeded. "
                "Please check your API credits."
            ) from e
        raise RuntimeError(f"ElevenLabs transcription failed: {e}") from e
    return result.text
