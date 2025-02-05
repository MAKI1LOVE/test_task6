from pydantic import BaseModel, Field


class Message(BaseModel):
    text: str
    deferance: int = Field(0, ge=0)
    periodic: bool = False
