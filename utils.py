# utils.py
MAX_HAND_SIZE = 5  # Maximum number of cards in a player's hand

def clamp(value, min_value, max_value):
    """Clamps a value between a minimum and maximum value."""
    return max(min_value, min(value, max_value))
