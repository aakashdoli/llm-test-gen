from __future__ import annotations
import os
from typing import Optional

class LLMProvider:
    """Pluggable LLM provider. Returns None if not configured.
    Extend with OpenAI/HF/Ollama backends as needed.
    """

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "").lower().strip()

    def generate(self, prompt: str) -> Optional[str]:
        # Minimal stub: return None if no provider configured.
        # You can implement your own provider here.
        if not self.provider:
            return None

        # Example placeholder (not actually calling external APIs here):
        # In real use, call your chosen API and return the string.
        return None
