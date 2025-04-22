import flet as ft
from game_state import GameState
from card_data import CardData  # Import CardData
from card_logic import apply_card_effect
from action_queue import ActionQueue
from utils import MAX_HAND_SIZE

def main(page: ft.Page):
    page.title = "Scoundrel"

    # Initialize Game State
    game_state = GameState()

    # Load Card Data (for now, let's create some example cards)
    card_data = {
        "Attack": CardData(name="Attack", description="Deal 2 damage.", cost=1, effects=[{"type": "damage", "value": 2, "target": "enemy"}]),
        "Heal": CardData(name="Heal", description="Heal 3 health.", cost=1, effects=[{"type": "heal", "value": 3, "target": "player"}]),
        "Draw": CardData(name="Draw", description="Draw 1 card.", cost=0, effects=[{"type": "draw", "value": 1}])
    }
    # Populate initial deck (example)
    game_state.deck = [card_data["Attack"], card_data["Heal"], card_data["Draw"]] * 5
    game_state.shuffle_deck()
    game_state.draw_hand()

    # Initialize Action Queue
    action_queue = ActionQueue()

    def handle_card_click(card: CardData):
        """Handles the event when a card is clicked."""
        print(f"Card clicked: {card.name}")

        # Add the card play to the action queue
        action_queue.add_action(game_state) # Take a snapshot of game state
        apply_card_effect(card, game_state) # Apply the card effect
        game_state.discard_card(card)

        # Update UI
        update_ui()

    def update_ui():
        """Updates the Flet UI to reflect the current GameState."""
        # Display current cards in hand
        card_controls = []
        for card in game_state.hand:
            card_controls.append(
                ft.ElevatedButton(
                    text=f"{card.name} ({card.cost})",
                    on_click=lambda e, card=card: handle_card_click(card),
                )
            )

        # Display game state information
        game_state_info = ft.Text(f"Health: {game_state.health}, Deck: {len(game_state.deck)}, Discard: {len(game_state.discard_pile)}")

        # Display undo/redo buttons
        undo_button = ft.ElevatedButton("Undo", on_click=undo)
        redo_button = ft.ElevatedButton("Redo", on_click=redo)

        # Update page content
        page.clean()  # Clear existing controls
        page.add(
            ft.Row(controls=card_controls),
            game_state_info,
            ft.Row(controls=[undo_button, redo_button])
        )

    def undo(e):
        """Undoes the last action."""
        if action_queue.can_undo():
            action_queue.undo(game_state)
            update_ui()

    def redo(e):
        """Redoes the last undone action."""
        if action_queue.can_redo():
            action_queue.redo(game_state)
            update_ui()

    # Initial UI update
    update_ui()

# Entry point
if __name__ == "__main__":
    ft.app(target=main)
