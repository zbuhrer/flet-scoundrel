from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class CardData:
    name: str
    description: str
    cost: int
    suit: Optional[str] = None  # "Diamonds", "Hearts", "Spades", "Clubs"
    rank: Optional[str] = None  # "2", "3", ..., "K", "A"
    effects: List[Dict[str, Any]] = field(default_factory=list)
    health: Optional[int] = None

    def __post_init__(self):
        # Validate effects (optional, but good practice)
        for effect in self.effects:
            if "type" not in effect:
                raise ValueError("Effect must have a 'type' field")

@dataclass
class Enemy:
    health: int
    attack: int = 1  # Default attack value
    name: str = "Generic Enemy"
