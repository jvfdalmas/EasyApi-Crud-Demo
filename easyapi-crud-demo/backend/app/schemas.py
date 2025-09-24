from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """Payload for creating a new item."""
    name: str = Field(min_length=1, max_length=255)


class ItemRead(BaseModel):
    """Public representation of an item returned by the API."""
    id: int
    name: str

    class Config:
        from_attributes = True


