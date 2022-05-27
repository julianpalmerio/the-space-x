from typing import Optional

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


class BugCardModel(CardModel):
    """Model of a issue card."""
    title: Optional[None] = None
    description: str = None

    @validator('type', pre=True, always=True)
    def validate_type(value):
        """Valid if the type field is 'bug'"""
        if value != "bug":
            raise ValueError("type must be 'bug'")
        return value

    @validator('title', pre=True, always=True)
    def validate_title(value):
        """Valid if the title field is None"""
        if value is not None:
            raise ValueError("title must be None")
        return value

    @validator('description', pre=True, always=True)
    def validate_description(value):
        """Valid if the description field is not None"""
        if value is None:
            raise ValueError("description is required")
        return value
