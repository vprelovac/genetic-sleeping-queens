from board_state import BoardState
from card import SpecialQueen
from itertools import combinations
import random
from collections import deque


class GameLogic:
    def __init__(self, board_state, verbose=True):
        self.verbose = verbose
        self.board_state = board_state

    def calculate_points(self, player):
        return sum(queen.value for queen in player.queens)

    def check_win_condition(self):
        num_players = len(self.board_state.players)
        queens_to_win = 5 if num_players <= 3 else 4
        points_to_win = 50 if num_players <= 3 else 40

        max_points = 0
        winner = None

        # Check if any player has met the win conditions
        for player in self.board_state.players:
            player_points = self.calculate_points(player)
            if len(player.queens) >= queens_to_win or player_points >= points_to_win:
                if self.verbose:
                    if len(player.queens) >= queens_to_win:
                        print(
                            f"{player.name} wins by collecting {len(player.queens)} queens!"
                        )
                    else:
                        print(f"{player.name} wins by scoring {player_points} points!")
                return f"{player.name} wins!"
            if player_points > max_points:
                max_points = player_points
                winner = player

        # Check if the draw pile is empty or all queens have been awakened
        if (
            self.board_state.draw_pile_count == 0
            or not self.board_state.sleeping_queens
        ):
            if winner:
                return f"{winner.name} wins with {max_points} points!"

        if self.verbose:
            print("No winner yet.")
        return "No winner yet."
        return sum(queen.value for queen in player.queens)
        num_players = len(self.board_state.players)
        queens_to_win = 5 if num_players <= 3 else 4
        points_to_win = 50 if num_players <= 3 else 40

        # Check if any player has met the win conditions
        for player in self.board_state.players:
            if (
                len(player.queens) >= queens_to_win
                or self.calculate_points(player) >= points_to_win
            ):
                return f"{player.name} wins!"

        # Check if the draw pile is empty
        if self.board_state.draw_pile_count == 0:
            max_points = 0
            winner = None
            for player in self.board_state.players:
                player_points = self.calculate_points(player)
                if player_points > max_points:
                    max_points = player_points
                    winner = player
            if winner:
                return f"{winner.name} wins with {max_points} points!"

        # Check if all queens have been awakened
        if not self.board_state.sleeping_queens:
            max_points = 0
            winner = None
            for player in self.board_state.players:
                player_points = self.calculate_points(player)
                if player_points > max_points:
                    max_points = player_points
                    winner = player
            if winner:
                return f"{winner.name} wins with {max_points} points!"

        return "No winner yet."

    def awaken_queen(self, player, card):
        player.remove_card_from_hand(card)
        self.board_state.discard_pile.append(card)
        random_queen = random.choice(self.board_state.sleeping_queens)
        player.add_queen(random_queen)
        self.board_state.sleeping_queens.remove(random_queen)

        if self.verbose:
            print(f"{player.name} awakened {random_queen}.")
        if random_queen.special_queen == SpecialQueen.ROSE:
            if self.board_state.sleeping_queens:
                extra_queen = self.board_state.sleeping_queens.pop(0)
                player.add_queen(extra_queen)

    def steal_queen(self, player, card, target_player, queen):
        player.remove_card_from_hand(card)
        if "Dragon" in [c.card_type for c in target_player.hand]:
            target_player.remove_card_from_hand(
                next(c for c in target_player.hand if c.card_type == "Dragon")
            )
            player.add_card_to_hand(card)
            self.board_state.discard_pile.append(card)
            return "blocked"
        target_player.remove_queen(queen)
        player.add_queen(queen)
        self.board_state.discard_pile.append(card)
        return "success"

    def put_queen_to_sleep(self, player, card, target_player, queen):
        player.remove_card_from_hand(card)
        if "Wand" in [c.card_type for c in target_player.hand]:
            target_player.remove_card_from_hand(
                next(c for c in target_player.hand if c.card_type == "Wand")
            )
            player.add_card_to_hand(card)
            return "blocked"
        target_player.remove_queen(queen)
        self.board_state.sleeping_queens.append(queen)
        return "success"

    def play_jester(self, player, card):
        player.remove_card_from_hand(card)
        self.board_state.discard_pile.append(card)
        if not self.board_state.draw_pile:
            self.board_state.draw_pile = deque(self.board_state.discard_pile)
            self.board_state.discard_pile.clear()
        top_card = self.board_state.draw_pile.popleft()
        if self.verbose:
            print(f"{player.name} played a Jester and drew {top_card}.")
        if top_card.card_type in [
            "King",
            "Knight",
            "Dragon",
            "Sleeping Potion",
            "Wand",
            "Jester",
        ]:
            player.add_card_to_hand(top_card)
            if self.verbose:
                print(f"{player.name} gets an extra turn!")
            self.board_state.show_board_state(self.verbose)
            if self.verbose:
                print(f"{player.name}'s hand: {player.hand}")
            return "extra_turn"
        else:
            self.board_state.discard_pile.append(top_card)
            count = top_card.value
            players = self.board_state.players
            index = (players.index(player) + count) % len(players)
            winner = players[index]
            if self.board_state.sleeping_queens:
                queen = self.board_state.sleeping_queens.pop(0)
                winner.add_queen(queen)
                if self.verbose:
                    if self.verbose:
                        print(
                            f"{player.name} does not get an extra turn. {winner.name} gets a queen."
                        )
            else:
                if self.verbose:
                    if self.verbose:
                        print(
                            f"{player.name} does not get an extra turn. No queens available to be awakened."
                        )
            return "no_extra_turn"

    def play_king(self, player, card):
        player.remove_card_from_hand(card)
        if self.board_state.sleeping_queens:
            queen = self.board_state.sleeping_queens.pop(0)
            player.add_queen(queen)
            self.board_state.discard_pile.append(card)
            return queen
        return None

    def play_knight(self, player, card, target_player, queen):
        player.remove_card_from_hand(card)
        if "Dragon" in [c.card_type for c in target_player.hand]:
            target_player.remove_card_from_hand(
                next(c for c in target_player.hand if c.card_type == "Dragon")
            )
            player.add_card_to_hand(card)
            return "blocked"
        target_player.remove_queen(queen)
        player.add_queen(queen)
        return "success"

    def play_sleeping_potion(self, player, card, target_player, queen):
        player.remove_card_from_hand(card)
        if "Wand" in [c.card_type for c in target_player.hand]:
            target_player.remove_card_from_hand(
                next(c for c in target_player.hand if c.card_type == "Wand")
            )
            player.add_card_to_hand(card)
            return "blocked"
        target_player.remove_queen(queen)
        self.board_state.sleeping_queens.append(queen)
        return "success"

    def play_wand(self, player, card):
        player.remove_card_from_hand(card)
        return "success"

    def get_legal_moves(self, player):
        legal_moves = []
        seen_actions = set()

        # Prioritize King, Knight, Potion, Jester in this order
        for card in player.hand:
            if card.card_type == "King" and "awaken_queen" not in seen_actions:
                legal_moves.append({"action": "awaken_queen", "card": card})
                seen_actions.add("awaken_queen")

        sorted_opponent_queens = {}
        for opponent in self.board_state.players:
            if opponent != player:
                sorted_opponent_queens[opponent] = sorted(
                    opponent.queens, key=lambda q: q.value, reverse=True
                )

        for card in player.hand:
            if card.card_type == "Knight":
                for opponent, sorted_queens in sorted_opponent_queens.items():
                    for queen in sorted_queens:
                        if ("steal_queen", queen) not in seen_actions:
                            legal_moves.append(
                                {"action": "steal_queen", "card": card, "target": queen}
                            )
                            seen_actions.add(("steal_queen", queen))

        for card in player.hand:
            if card.card_type == "Sleeping Potion":
                for opponent, sorted_queens in sorted_opponent_queens.items():
                    for queen in sorted_queens:
                        if ("put_queen_to_sleep", queen) not in seen_actions:
                            legal_moves.append(
                                {
                                    "action": "put_queen_to_sleep",
                                    "card": card,
                                    "target": queen,
                                }
                            )
                            seen_actions.add(("put_queen_to_sleep", queen))

        for card in player.hand:
            if card.card_type == "Jester" and "play_jester" not in seen_actions:
                legal_moves.append({"action": "play_jester", "card": card})
                seen_actions.add("play_jester")

        number_cards = [card for card in player.hand if card.card_type == "Number"]
        number_counts = {}
        for card in number_cards:
            if card.value in number_counts:
                number_counts[card.value].append(card)
            else:
                number_counts[card.value] = [card]

        # Discard three or more number cards that make an addition equation, prioritize longer equations
        seen_equations = set()
        for r in range(
            len(number_cards), 2, -1
        ):  # Start from the largest possible combination
            for combo in combinations(number_cards, r):
                values = sorted([card.value for card in combo], reverse=True)
                if sum(values[1:]) == values[0]:
                    equation = tuple(sorted(values))
                    if equation not in seen_equations:
                        legal_moves.append(
                            {"action": "discard_equation", "target": list(combo)}
                        )
                        seen_equations.add(equation)

        # Discard a pair of identical number cards
        for value, cards in number_counts.items():
            if len(cards) >= 2 and ("discard_pair", value) not in seen_actions:
                legal_moves.append({"action": "discard_pair", "target": cards[:2]})
                seen_actions.add(("discard_pair", value))

        # Discard single cards
        seen_single_cards = set()
        for card in player.hand:
            if (card.card_type, card.value) not in seen_single_cards:
                legal_moves.append({"action": "discard_single", "card": card})
                seen_single_cards.add((card.card_type, card.value))

        return legal_moves

    def select_move_based_on_strategy(self, player, legal_moves):
        best_move_index = 0
        best_move_value = -1

        for i, move in enumerate(legal_moves):
            action = move["action"]
            move_value = 0

            if action == "awaken_queen":
                move_value = player.strategy["awaken_queen_weight"]
            elif action == "steal_queen":
                move_value = player.strategy["steal_queen_weight"]
            elif action == "put_queen_to_sleep":
                move_value = player.strategy["put_queen_to_sleep_weight"]
            elif action == "play_jester":
                move_value = player.strategy["play_jester_weight"]
            elif action == "discard_equation":
                move_value = player.strategy["discard_equation_weight"]
            elif action == "discard_pair":
                move_value = player.strategy["discard_pair_weight"]
            elif action == "discard_single":
                card = move["card"]
                if card.card_type == "Number":
                    move_value = player.strategy["discard_single_weight"] + card.value / 100
                else:
                    move_value = player.strategy["discard_single_weight"]

            if move_value > best_move_value:
                best_move_value = move_value
                best_move_index = i

        return best_move_index

    def print_legal_moves(self, player):
        legal_moves = self.get_legal_moves(player)
        if self.verbose:
            print("Legal moves:")
        for i, move in enumerate(legal_moves):
            action = move["action"]
            if action in ["steal_queen", "put_queen_to_sleep"] and "target" in move:
                target = move["target"]
                card = move["card"]
                if self.verbose:
                    print(f"{i}: {action} with {card} targeting {target}")
            elif action in ["discard_pair", "discard_equation"]:
                cards = move["target"]
                card_values = " ".join(str(card) for card in cards)
                if self.verbose:
                    print(f"{i}: {action} with {card_values}")
            else:
                card = move["card"]
                if self.verbose:
                    print(f"{i}: {action} with {card}")

    def take_turn(self, player, move_index=None):
        # Ensure only the active player can take a turn
        if not player.active:
            if self.verbose:
                print(f"{player.name} is not the active player.")
            return

        # Ensure the player has at least 5 cards at the beginning of the turn
        self.board_state.draw_cards_for_player(player)

        self.print_legal_moves(player)
        legal_moves = self.get_legal_moves(player)

        assert legal_moves, "No legal moves available."

        if player.is_ai:
            if player.ai_difficulty == "Easy":
                move_index = random.randint(0, len(legal_moves) - 1)
                #              print('easy', move_index)
                if self.verbose:
                    print(f"{player.name} (Easy AI) chose move index {move_index}")
            elif player.ai_difficulty == "Hard":
                move_index = 0
                #               print('hard', move_index)
                if self.verbose:
                    print(f"{player.name} (Hard AI) chose move index {move_index}")
            elif player.ai_difficulty == "Genetic":
                if player.strategy is None:
                    raise ValueError(f"{player.name} does not have a strategy set.")
                move_index = self.select_move_based_on_strategy(player, legal_moves)
                #             print('gen', move_index)
                if self.verbose:
                    print(f"{player.name} (Genetic AI) chose move index {move_index}")
        else:
            if move_index is None:
                move_index = int(
                    input("Enter the number of the move you want to make: ")
                )
        move = legal_moves[move_index]
        action = move["action"]
        card = move.get("card")

        if action == "awaken_queen":
            self.awaken_queen(player, card)
        elif action == "steal_queen":
            target_player = self.get_player_by_queen(move["target"])
            queen = move["target"]
            result = self.steal_queen(player, card, target_player, queen)
            if result == "blocked":
                if self.verbose:
                    print("Your move was blocked by a Dragon!")
                # Deactivate all players and activate the next player
                for p in self.board_state.players:
                    p.deactivate()
                self.board_state.active_player_index = (
                    self.board_state.active_player_index + 1
                ) % len(self.board_state.players)
                self.board_state.players[
                    self.board_state.active_player_index
                ].activate()
                self.board_state.turn_number += 1
                return
        elif action == "put_queen_to_sleep":
            target_player = self.get_player_by_queen(move["target"])
            queen = move["target"]
            result = self.put_queen_to_sleep(player, card, target_player, queen)
            if result == "blocked":
                if self.verbose:
                    print("Your move was blocked by a Wand!")
                return
        elif action == "play_jester":
            result = self.play_jester(player, card)
            if result == "extra_turn":
                if self.verbose:
                    print("You get an extra turn!")
                self.take_turn(player)
        elif action == "discard_single":
            player.remove_card_from_hand(card)
            self.board_state.discard_pile.append(card)
        elif action == "discard_pair":
            for c in move["target"]:
                player.remove_card_from_hand(c)
                self.board_state.discard_pile.append(c)
        elif action == "discard_equation":
            for c in move["target"]:
                player.remove_card_from_hand(c)
                self.board_state.discard_pile.append(c)
        elif action == "discard_pair" or action == "discard_equation":
            for c in move["target"]:
                player.remove_card_from_hand(c)
                self.board_state.discard_pile.append(c)

        self.board_state.draw_cards_for_player(player)
        self.end_turn()

    def get_player_by_queen(self, queen):
        for player in self.board_state.players:
            if queen in player.queens:
                return player
        return None

    def end_turn(self):

        # Deactivate all players and activate the next player
        for p in self.board_state.players:
            p.deactivate()
        self.board_state.active_player_index = (
            self.board_state.active_player_index + 1
        ) % len(self.board_state.players)
        self.board_state.players[self.board_state.active_player_index].activate()
        self.board_state.turn_number += 1


# Example usage:
# board_state = BoardState(3)
# game_logic = GameLogic(board_state)
# print(game_logic.check_win_condition())
