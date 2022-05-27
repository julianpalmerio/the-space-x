from pydantic import BaseModel, validator


class CardModel(BaseModel):
    """Basic model representation of a card."""
    type: str


class IssueCardModel(CardModel):
    """Model of a issue card."""
    title: str = None
    description: str = None

    @validator('title', pre=True, always=True)
    def validate_title(value):
        """Valid if the title field is not None"""
        if value is None:
            raise ValueError("title is required")
        return value

    @validator('description', pre=True, always=True)
    def validate_description(value):
        """Valid if the description field is not None"""
        if value is None:
            raise ValueError("description is required")
        return value
