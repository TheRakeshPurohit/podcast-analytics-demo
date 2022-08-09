"""Api specification for the chat analytics app."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Intent(str, Enum):
    """Intent of a chat message."""

    SALUTATION = "Salutation"
    PRAISE = "Praise"
    COMPLAINT = "Complaint"
    QUESTION = "Question"
    REQUEST = "Request"
    EXPLANATION = "Explanation"


class Sentiment(str, Enum):
    """Sentiment of a chat message."""

    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"


class Message(BaseModel):
    """Structured representation of a chat message."""

    message_id: str = Field(example="001")
    timestamp: datetime
    user_id: str = Field(example="u001")
    text: str = Field(example="Hello. This is a message.")
    sentiment: Optional[Sentiment]
    intent: Optional[Intent]
    root_message_id: Optional[str] = Field(example="001")

    def dict(self, format_dates: bool = False, format_enums: bool = False, **kwargs):
        """Transform object into a dictionary."""
        output = super().dict(**kwargs)
        for k, v in output.items():
            if format_dates and isinstance(v, datetime):
                output[k] = v.isoformat()
            if format_enums and isinstance(v, Enum):
                output[k] = v.value
        return output
