from copy import deepcopy

class ActionQueue:
    def __init__(self):
        self.queue = []  # List of GameState snapshots
        self.current_index = -1  # Index of the current state in the queue

    def add_action(self, game_state):
        """Adds a new game state to the queue."""
        # Remove any states after the current index (if we've undone something)
        self.queue = self.queue[:self.current_index + 1]

        # Append a deepcopy of the game state
        self.queue.append(deepcopy(game_state))
        self.current_index += 1

    def undo(self, game_state):
        """Restores the previous game state."""
        if self.can_undo():
            self.current_index -= 1
            # Restore the game state from the queue
            self.restore_game_state(game_state, self.queue[self.current_index])

    def redo(self, game_state):
        """Restores the next game state (after an undo)."""
        if self.can_redo():
            self.current_index += 1
            # Restore the game state from the queue
            self.restore_game_state(game_state, self.queue[self.current_index])

    def can_undo(self):
        """Checks if there are any actions to undo."""
        return self.current_index > 0

    def can_redo(self):
        """Checks if there are any actions to redo."""
        return self.current_index < len(self.queue) - 1

    def restore_game_state(self, current_game_state, previous_game_state):
        """Restores the current game state to a previous state."""
        # Efficiently restore the game state by copying the attributes
        current_game_state.deck = deepcopy(previous_game_state.deck)
        current_game_state.hand = deepcopy(previous_game_state.hand)
        current_game_state.discard_pile = deepcopy(previous_game_state.discard_pile)
        current_game_state.health = previous_game_state.health
        current_game_state.power = previous_game_state.power
        current_game_state.enemies = deepcopy(previous_game_state.enemies)
