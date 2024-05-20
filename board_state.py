from player import Player
import random
from collections import deque


class BoardState:
    def __init__(self, num_players):
        self.players = [Player(f"Player {i+1}", self) for i in range(num_players)]
        draw_pile, self.sleeping_queens = self.initialize_draw_pile()
        self.draw_pile = deque(draw_pile)
        self.discard_pile = []
        self.active_player_index = 0
        self.turn_number = 1
        self.draw_pile_count = len(self.draw_pile)
        for player in self.players:
            self.draw_cards_for_player(player)
            player.deactivate()
        self.players[0].activate()

    def draw_cards_for_player(self, player):
        while len(player.hand) < 5:
            if not self.draw_pile:
                self.draw_pile = deque(self.discard_pile)
                self.discard_pile = []
                random.shuffle(self.draw_pile)
                self.draw_pile_count = len(self.draw_pile)
            new_card = self.draw_pile.popleft()
            player.add_card_to_hand(new_card)
            self.draw_pile_count -= 1

    def initialize_draw_pile(self):
        from card import Card, SpecialQueen

        # Create the deck with the appropriate number of cards
        queens = [
            Card("Queen", 15, SpecialQueen.CAT),
            Card("Queen", 5, SpecialQueen.NONE),
            Card("Queen", 10, SpecialQueen.NONE),
            Card("Queen", 20, SpecialQueen.NONE),
            Card("Queen", 5, SpecialQueen.ROSE),
            Card("Queen", 15, SpecialQueen.DOG),
            Card("Queen", 10, SpecialQueen.NONE),
            Card("Queen", 15, SpecialQueen.NONE),
            Card("Queen", 5, SpecialQueen.NONE),
            Card("Queen", 10, SpecialQueen.NONE),
            Card("Queen", 10, SpecialQueen.NONE),
            Card("Queen", 15, SpecialQueen.NONE),
        ]
        kings = [Card("King") for _ in range(8)]
        jesters = [Card("Jester") for _ in range(5)]
        knights = [Card("Knight") for _ in range(4)]
        sleeping_potions = [Card("Sleeping Potion") for _ in range(4)]
        wands = [Card("Wand") for _ in range(3)]
        dragons = [Card("Dragon") for _ in range(3)]
        numbers = [Card("Number", value) for value in range(1, 11) for _ in range(4)]

        deck = (
            queens
            + kings
            + jesters
            + knights
            + sleeping_potions
            + wands
            + dragons
            + numbers
        )

        # Shuffle the deck
        random.shuffle(deck)

        queens = [card for card in deck if card.card_type == "Queen"]
        non_queens = [card for card in deck if card.card_type != "Queen"]
        return non_queens, queens

    def show_board_state(self, verbose=True):
        if verbose:
            print("Board State:")
            for player in self.players:
                print(player)
            print(f"Turn Number: {self.turn_number}")
            print(f"Draw Pile Count: {self.draw_pile_count}")
            print(f"Discard Pile: {self.discard_pile}")
            print(f"Sleeping Queens: {self.sleeping_queens}")

        if verbose:
            print("Board State:")
            for player in self.players:
                print(player)
            print(f"Turn Number: {self.turn_number}")
            print(f"Draw Pile Count: {self.draw_pile_count}")
            print(f"Discard Pile: {self.discard_pile}")
            print(f"Sleeping Queens: {self.sleeping_queens}")


# Example usage:
# board_state = BoardState(3)
# print(board_state)
