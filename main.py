import flet as ft
from game_state import GameState
from card_data import CardData
from card_logic import apply_card_effect
from action_queue import ActionQueue

def main(page: ft.Page):
    page.title = "Scoundrel: Ace's Wild"

    # Initialize Game State
    game_state = GameState()

    # Create a standard 52-card deck
    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def create_deck():
        deck = []
        for suit in suits:
            for rank in ranks:
                # Determine card value and effects based on suit and rank
                if rank.isdigit():
                    value = int(rank)
                elif rank == "Jack":
                    value = 11
                elif rank == "Queen":
                    value = 12
                elif rank == "King":
                    value = 13
                else:  # Ace - Value will be determined at play time.
                    value = 0  # Placeholder

                card_name = f"{rank} of {suit}"
                card_description = f"{rank} of {suit}"  # More descriptive descriptions would be good.
                cost = 1 #Temporary Value

                effects = []
                if suit == "Diamonds":
                    effects.append({"type": "damage", "value": value, "target": "enemy"})
                elif suit == "Hearts":
                    effects.append({"type": "heal", "value": value, "target": "player"})
                elif suit == "Spades" or suit == "Clubs":
                    # These cards represent enemies; however, the enemy creation is outside the scope of card creation
                    # So we will add a type for summon enemy, and let the card logic handle it.
                    effects.append({"type": "summon_enemy", "health": value})

                card_data = CardData(name=card_name, description=card_description, cost=cost, effects=effects, suit=suit, rank=rank)
                deck.append(card_data)
        return deck

    game_state.deck = create_deck()
    game_state.shuffle_deck()
    game_state.draw_hand()

    # Initialize Action Queue
    action_queue = ActionQueue()

    def handle_card_click(card: CardData):
        """Handles the event when a card is clicked."""
        print(f"Card clicked: {card.name}")

        # Handle Ace value selection
        if card.rank == "Ace":
            def close_dlg(e):
                ace_value = ace_value_field.value
                if ace_value is None:
                    page.show_snack_bar(
                        ft.SnackBar(
                            ft.Text("Please enter a value for Ace."),
                            open=True,
                        )
                    )
                    return  # Don't close the dialog.
                try:
                    ace_value = int(ace_value)
                    if ace_value != 1 and ace_value != 14:
                        page.show_snack_bar(
                            ft.SnackBar(
                                ft.Text("Invalid Ace value. Please enter 1 or 14."),
                                open=True,
                            )
                        )
                        return # Don't close the dialog.
                except ValueError:
                    page.show_snack_bar(
                        ft.SnackBar(
                            ft.Text("Invalid Ace value. Please enter a number."),
                            open=True,
                        )
                    )
                    return #Don't close the dialog.
                page.close_dialog()
                # Continue processing the card with the selected ace_value
                process_card(card, ace_value)

            ace_value_field = ft.TextField(label="Choose Ace value (1 or 14):", keyboard_type=ft.KeyboardType.NUMBER)

            page.add(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Choose Ace Value"),
                    content=ace_value_field,
                    actions=[
                        ft.TextButton("Confirm", on_click=close_dlg),
                    ],
                )
            )
            page.update()


        else:
            process_card(card)

    def process_card(card: CardData, ace_value: int = 0):
        """Processes the card play after Ace value selection (if applicable)."""
        # Add the card play to the action queue
        action_queue.add_action(game_state)

        # Apply the card effect
        apply_card_effect(card, game_state)

        # Discard the card
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
                    text=f"{card.rank} of {card.suit} ({card.cost})",
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
