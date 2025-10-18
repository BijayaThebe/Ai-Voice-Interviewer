# app/conversation/memory.py
from typing import List, Dict, Optional

class InterviewMemory:
    def __init__(self):
        self.candidate_name: str = ""
        self.transcript: List[Dict] = []  # [{"speaker": "user", "text": "..."}, ...]
        self.key_topics: List[str] = []
        self.follow_up_queue: List[str] = []
        self.detected_contradictions: List[str] = []

    def add_user_response(self, text: str):
        self.transcript.append({"speaker": "user", "text": text})
        # TODO: Use lightweight NLP (or LLM) to extract topics/flags

    def get_context_summary(self, max_words=100) -> str:
        # Summarize last 3 exchanges for LLM context window
        recent = self.transcript[-3:]
        return " ".join([msg["text"] for msg in recent])[:max_words]