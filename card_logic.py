def apply_card_effect(card, game_state):
    """Applies the effects of a card to the game state."""

    if card.suit == "Diamonds":
        damage = card.rank
        if game_state.equipped_class == "Diamonds":
            damage += game_state.class_bonus
        if game_state.enemies:
            game_state.enemies[0].health -= damage
            print(f"Dealt {damage} damage to enemy with {card.name}!")
        else:
            print("No enemies to attack!")

    elif card.suit == "Hearts":
        heal_amount = card.rank
        if game_state.equipped_class == "Hearts":
            heal_amount += game_state.class_bonus
        game_state.apply_healing(heal_amount)
        print(f"Healed {heal_amount} health with {card.name}!")

    elif card.suit == "Spades" or card.suit == "Clubs":
        # Spades and Clubs represent enemies.  For simplicity, we won't "play" them,
        # but they could trigger enemy actions in a more complex system.
        print(f"Encountered enemy: {card.name} (Suit: {card.suit}, Rank: {card.rank})")
        #In a more complex system, this is where you'd trigger the enemy's attack

    # Card Abilities
    for effect in card.effects:
        effect_type = effect["type"]

        if effect_type == "draw":
            value = effect["value"]
            for _ in range(value):
                game_state.draw_card()
            print(f"Drew {value} card(s)!")

        elif effect_type == "equip":
            #Equip a red face card as a character class, granting a bonus.
            suit = card.suit
            if suit in ("Hearts", "Diamonds") and card.rank in (11, 12, 13): #J, Q, K
                game_state.equip_class(card)
            else:
                print(f"Cannot equip {card.name} as a class.")

        else:
            print(f"Unknown effect type: {effect_type}")
