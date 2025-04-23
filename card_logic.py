from card_data import Enemy

def apply_card_effect(card, game_state):
    """Applies the effects of a card to the game state."""
    print(f"Applying effect for {card.name}")

    for effect in card.effects:
        effect_type = effect["type"]

        if effect_type == "damage":
            damage = effect["value"]
            if game_state.equipped_class == "Diamonds":
                damage += game_state.class_bonus
            if game_state.enemies:
                game_state.enemies[0].health -= damage
                print(f"Dealt {damage} damage to enemy with {card.name}!")
            else:
                print("No enemies to attack!")

        elif effect_type == "heal":
            heal_amount = effect["value"]
            if game_state.equipped_class == "Hearts":
                heal_amount += game_state.class_bonus
            game_state.apply_healing(heal_amount)
            print(f"Healed {heal_amount} health with {card.name}!")

        elif effect_type == "summon_enemy":
            health = effect["health"]
            enemy = Enemy(health=health, name=card.name)  # Create an Enemy instance
            game_state.enemies.append(enemy)  # Add the enemy to the game state
            print(f"Summoned enemy: {card.name} with {health} health.")

        elif effect_type == "draw":
            value = effect["value"]
            for _ in range(value):
                game_state.draw_card()
            print(f"Drew {value} card(s)!")

        elif effect_type == "equip":
            #Equip a red face card as a character class, granting a bonus.
            suit = card.suit
            if suit in ("Hearts", "Diamonds") and card.rank in ('Jack', 'Queen', 'King'): #J, Q, K
                game_state.equip_class(card)
            else:
                print(f"Cannot equip {card.name} as a class.")

        else:
            print(f"Unknown effect type: {effect_type}")
