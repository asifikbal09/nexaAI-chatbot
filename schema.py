from pydantic import BaseModel, Field


class AIResponse(BaseModel):
    """Structured response returned by NexaAI."""

    answer: str = Field(
        description="The main answer to the user's question."
    )

    summary: str = Field(
        description="A short summary of the answer."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="The model's confidence in the answer, between 0 and 1."
    )

    category: str = Field(
        description="The category of the user's question, such as Programming, Math, or General."
    )

    keywords: list[str] = Field(
        description="Important keywords related to the user's question."
    )