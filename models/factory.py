from typing import Callable, Any

from models.card import CardModel

card_model_creation_funcs: "dict[str, Callable[..., CardModel]]" = {}


def register(card_model: str, creation_func: Callable[..., CardModel]):
    """Register a new Card Model."""
    card_model_creation_funcs[card_model] = creation_func


def unregister(card_model: str):
    """Unregister a Card Model."""
    card_model_creation_funcs.pop(card_model, None)


def create(arguments: "dict[str, Any]") -> CardModel:
    """Create a Card Model of a specific type, given a dictionary of arguments."""
    card_model_type = arguments["type"]
    try:
        creation_func = card_model_creation_funcs[card_model_type]
        return creation_func(**arguments)
    except KeyError:
        raise ValueError(f"Unknown Card Model type {card_model_type}")
