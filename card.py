from enum import Enum


class SpecialQueen(Enum):
    NONE = "None"
    ROSE = "Rose"
    DOG = "Dog"
    CAT = "Cat"


class Card:
    def __init__(self, card_type, value=None, special_queen=SpecialQueen.NONE):
        self.card_type = card_type
        self.value = value
        self.special_queen = special_queen

    def __str__(self):
        if self.card_type == "Number":
            return str(self.value)
        if self.value:
            if self.special_queen != SpecialQueen.NONE:
                return f"{self.card_type} (Value: {self.value}, Special: {self.special_queen.value})"
            return f"{self.card_type} (Value: {self.value})"
        if self.special_queen != SpecialQueen.NONE:
            return f"{self.card_type} (Special: {self.special_queen.value})"
        return f"{self.card_type}"

    def __repr__(self):
        return self.__str__()


# Example card types: "Queen", "King", "Knight", "Dragon", "Jester", "Sleeping Potion", "Wand", "Number"
# Example usage:
# queen_card = Card("Queen", 5, SpecialQueen.ROSE)
# king_card = Card("King")
# number_card = Card("Number", 7)
