from typing import Optional
import random

from pydantic import BaseModel, validator
from random_word import RandomWords


class CardModel(BaseModel):
    """Basic model representation of a card."""
    type: str
    title: Optional[str] = None
    description: Optional[str] = None
    label_name: Optional[str]
    random_member: Optional[bool]
    category: Optional[str]


class IssueCardModel(CardModel):
    """Model of a issue card."""

    @validator('type', pre=True, always=True)
    def validate_type(value):
        """Valid if the type field is 'issue'"""
        if value != "issue":
            raise ValueError("type must be 'issue'")
        return value

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

    @validator('category', pre=True, always=True)
    def validate_category(value):
        """Valid if the category field is None"""
        if value is not None:
            raise ValueError("category must be None")
        return value


class BugCardModel(CardModel):
    """Model of a issue card."""

    @validator('type', pre=True, always=True)
    def validate_type(value):
        """Valid if the type field is 'bug'"""
        if value != "bug":
            raise ValueError("type must be 'bug'")
        return value

    @validator('title', pre=True, always=True)
    def validate_title(value):
        """Valid if the title field is None and return a random title"""
        if value is not None:
            raise ValueError("title must be None")
        random_words = RandomWords()
        random_word = random_words.get_random_word().replace('-', '')
        random_int = random.randint(1, 100)
        return f"bug-{random_word}-{random_int}"

    @validator('description', pre=True, always=True)
    def validate_description(value):
        """Valid if the description field is not None"""
        if value is None:
            raise ValueError("description is required")
        return value

    @validator('label_name', pre=True, always=True)
    def validate_label_name(value):
        """Valid if the label_name field is 'Bug'"""
        if value is None:
            return "Bug"
        if value != "Bug":
            raise ValueError("label_name must be 'Bug'")
        return value

    @validator('random_member', pre=True, always=True)
    def validate_random_member(value):
        """Valid if the random_member field is True"""
        if value is None:
            return True
        if not value:
            raise ValueError("random_member must be True")
        return value

    @validator('category', pre=True, always=True)
    def validate_category(value):
        """Valid if the category field is None"""
        if value is not None:
            raise ValueError("category must be None")
        return value


class TaskCardModel(CardModel):
    """Model of a task card."""

    @validator('type', pre=True, always=True)
    def validate_type(value):
        """Valid if the type field is 'task'"""
        if value != "task":
            raise ValueError("type must be 'task'")
        return value

    @validator('title', pre=True, always=True)
    def validate_title(value):
        """Valid if the title field is not None"""
        if value is None:
            raise ValueError("title is required")
        return value

    @validator('category', pre=True, always=True)
    def validate_category(value):
        """Valid if the category field is valid"""
        valid_categories = ["Maintenance", "Research", "Test"]
        if value not in valid_categories:
            raise ValueError(f"category is not valid, valid categories are {valid_categories}")
        return value

    @validator('description', pre=True, always=True)
    def validate_description(value):
        """Valid if the description field is None"""
        if value is not None:
            raise ValueError("description must be None")
        return value
