import unittest
from board_state import BoardState
from game_logic import GameLogic
from card import Card, SpecialQueen


class TestGameLogic(unittest.TestCase):

    def setUp(self):
        self.board_state = BoardState(2)
        self.game_logic = GameLogic(self.board_state, verbose=False)
        self.player1 = self.board_state.players[0]
        self.player2 = self.board_state.players[1]

    def test_awaken_queen(self):
        king_card = Card("King")
        self.player1.hand = {king_card}
        self.game_logic.awaken_queen(self.player1, king_card)
        if any(
            queen.special_queen == SpecialQueen.ROSE for queen in self.player1.queens
        ):
            self.assertEqual(len(self.player1.queens), 2)
            self.assertEqual(len(self.board_state.sleeping_queens), 10)
        else:
            self.assertEqual(len(self.player1.queens), 1)
            self.assertEqual(len(self.board_state.sleeping_queens), 11)

    def test_steal_queen(self):
        queen_card = Card("Queen", 10)
        self.player2.queens = [queen_card]
        knight_card = Card("Knight")
        self.player2.hand = (
            set()
        )  # Ensure the target player does not have a Dragon card
        self.player1.hand = {knight_card}
        result = self.game_logic.steal_queen(
            self.player1, knight_card, self.player2, queen_card
        )
        self.assertEqual(result, "success")
        self.assertEqual(len(self.player1.queens), 1)
        self.assertEqual(len(self.player2.queens), 0)

    def test_put_queen_to_sleep(self):
        queen_card = Card("Queen", 10)
        self.player2.queens = [queen_card]
        sleeping_potion_card = Card("Sleeping Potion")
        self.player1.hand = {sleeping_potion_card}
        self.player2.hand = set()  # Ensure the target player does not have a Wand card
        result = self.game_logic.put_queen_to_sleep(
            self.player1, sleeping_potion_card, self.player2, queen_card
        )
        self.assertEqual(result, "success")
        self.assertEqual(len(self.player2.queens), 0)
        self.assertEqual(len(self.board_state.sleeping_queens), 13)

    def test_play_jester(self):
        jester_card = Card("Jester")
        self.player1.hand = {jester_card}
        result = self.game_logic.play_jester(self.player1, jester_card)
        self.assertIn(result, ["extra_turn", "no_extra_turn"])

    def test_discard_single(self):
        number_card = Card("Number", 5)
        self.player1.hand = {number_card}
        legal_moves = self.game_logic.get_legal_moves(self.player1)
        discard_single_move = next(
            move for move in legal_moves if move["action"] == "discard_single"
        )
        self.assertEqual(discard_single_move["card"], number_card)

    def test_discard_pair(self):
        card1 = Card("Number", 3)
        card2 = Card("Number", 3)
        self.player1.hand = {card1, card2}
        legal_moves = self.game_logic.get_legal_moves(self.player1)
        discard_pair_move = next(
            move for move in legal_moves if move["action"] == "discard_pair"
        )
        self.assertEqual(discard_pair_move["target"], [card1, card2])

    def test_discard_equation(self):
        card1 = Card("Number", 2)
        card2 = Card("Number", 3)
        card3 = Card("Number", 5)
        self.player1.hand = {card1, card2, card3}
        legal_moves = self.game_logic.get_legal_moves(self.player1)
        discard_equation_move = next(
            move for move in legal_moves if move["action"] == "discard_equation"
        )
        self.assertEqual(discard_equation_move["target"], [card1, card2, card3])

    def test_take_turn_discard_single(self):
        card = Card("Number", 5)
        self.player1.hand = {
            card,
            Card("Number", 4),
            Card("Number", 6),
            Card("Number", 7),
            Card("Number", 8),
        }
        self.game_logic.take_turn(self.player1, move_index=0)
        self.assertNotIn(card, self.player1.hand)
        self.assertIn(card, self.board_state.discard_pile)

    def test_take_turn_discard_pair(self):
        card1 = Card("Number", 3)
        card2 = Card("Number", 3)
        self.player1.hand = {
            card1,
            card2,
            Card("Number", 4),
            Card("Number", 5),
            Card("Number", 6),
        }
        self.game_logic.take_turn(self.player1, move_index=0)
        self.assertNotIn(card1, self.player1.hand)
        self.assertNotIn(card2, self.player1.hand)
        self.assertIn(card1, self.board_state.discard_pile)
        self.assertIn(card2, self.board_state.discard_pile)

    def test_take_turn_discard_equation(self):
        card1 = Card("Number", 2)
        card2 = Card("Number", 3)
        card3 = Card("Number", 5)
        self.player1.hand = {card1, card2, card3, Card("Number", 4), Card("Number", 6)}
        self.game_logic.take_turn(self.player1, move_index=0)
        self.assertNotIn(card1, self.player1.hand)
        self.assertNotIn(card2, self.player1.hand)
        self.assertNotIn(card3, self.player1.hand)
        self.assertIn(card1, self.board_state.discard_pile)
        self.assertIn(card2, self.board_state.discard_pile)
        self.assertIn(card3, self.board_state.discard_pile)
        queen_card = Card("Queen", 50)
        self.player1.queens = [queen_card]
        result = self.game_logic.check_win_condition()
        self.assertEqual(result, f"{self.player1.name} wins!")

    def test_check_win_condition(self):
        queen_card = Card("Queen", 50)
        self.player1.queens = [queen_card]
        result = self.game_logic.check_win_condition()
        self.assertEqual(result, f"{self.player1.name} wins!")


unittest.main()
