from card import SpecialQueen


class Player:
    def __init__(self, name, board_state, is_ai=False):
        self.board_state = board_state
        self.name = name
        self.hand = set()
        self.queens = []
        self.active = True
        self.special_queens = set()
        self.is_ai = is_ai
        self.ai_difficulty = "Easy" if is_ai else None
        self.strategy = None

    def add_card_to_hand(self, card):
        self.hand.add(card)

    def remove_card_from_hand(self, card):
        try:
            self.hand.remove(card)
        except KeyError:
            raise ValueError(f"Card {card} not in hand")

    def add_queen(self, queen):
        self.queens.append(queen)

        # Add to special queens set if applicable
        if queen.special_queen != SpecialQueen.NONE:
            self.special_queens.add(queen.special_queen)

        # Handle special queen powers using the set
        if (
            SpecialQueen.DOG in self.special_queens
            and SpecialQueen.CAT in self.special_queens
        ):
            if queen.special_queen == SpecialQueen.DOG:
                self.queens.remove(queen)
                self.board_state.sleeping_queens.append(queen)
                self.board_state.discard_pile.append(queen)
                self.special_queens.remove(SpecialQueen.DOG)
            elif queen.special_queen == SpecialQueen.CAT:
                self.queens.remove(queen)
                self.board_state.sleeping_queens.append(queen)
                self.special_queens.remove(SpecialQueen.CAT)

    def remove_queen(self, queen):
        self.queens.remove(queen)

    def remove_queen(self, queen):
        self.queens.remove(queen)
        if queen.special_queen != SpecialQueen.NONE:
            self.special_queens.remove(queen.special_queen)

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def __str__(self):
        return f"Player({self.name}, Hand: {list(self.hand)}, Queens: {self.queens}, Active: {self.active})"
