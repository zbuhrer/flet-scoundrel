def apply_card_effect(card, game_state):
    """Applies the effects of a card to the game state."""
    for effect in card.effects:
        effect_type = effect["type"]

        if effect_type == "damage":
            target = effect.get("target")  # Use .get() for optional parameters
            value = effect["value"]
            if target == "enemy":
                #  For now, just damage the first enemy.  We'll add targeting later.
                if game_state.enemies:
                    game_state.enemies[0].health -= value
                    print(f"Dealt {value} damage to enemy!")  # Debugging
                else:
                    print("No enemies to attack!")  # Handle no enemies case

            elif target == "player":
                 game_state.apply_damage(value)
                 print(f"Dealt {value} damage to self!")

        elif effect_type == "heal":
            target = effect.get("target")
            value = effect["value"]
            if target == "player":
                game_state.apply_healing(value)
                print(f"Healed {value} health!")

        elif effect_type == "draw":
            value = effect["value"]
            for _ in range(value):
                game_state.draw_card()
            print(f"Drew {value} card(s)!")

        # Add more effect types here as needed (e.g., "apply_buff", "summon_minion")
        else:
            print(f"Unknown effect type: {effect_type}") #Handle unknown effects
