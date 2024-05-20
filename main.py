import sys
from board_state import BoardState
from game_logic import GameLogic
from player import Player
from genetic_algorithm import GeneticAlgorithm


def main():
    num_players = 2
    player1_name = "Player 1"
    player2_name = "Player 2"
    player1_is_ai = False
    player2_is_ai = False

    num_games = None
    run_genetic_algorithm = "-ga" in sys.argv
    if "-num" in sys.argv:
        num_games = int(sys.argv[sys.argv.index("-num") + 1])

    if "-p1" in sys.argv:
        player1_name = sys.argv[sys.argv.index("-p1") + 1]
        if player1_name in ["Easy AI", "Hard AI", "Genetic AI"]:
            player1_is_ai = True

    if "-p2" in sys.argv:
        player2_name = sys.argv[sys.argv.index("-p2") + 1]
        if player2_name in ["Easy AI", "Hard AI", "Genetic AI"]:
            player2_is_ai = True

    best_strategy = {
        'put_queen_to_sleep_weight': 7, 'steal_queen_weight': 6, 'awaken_queen_weight': 5, 'discard_equation_weight': 4, 'play_jester_weight': 3, 'discard_pair_weight': 2, 'discard_single_weight': 1
        #'put_queen_to_sleep_weight': 7, 'steal_queen_weight': 6, 'discard_equation_weight': 5, 'awaken_queen_weight': 4, 'play_jester_weight': 3, 'discard_pair_weight': 2, 'discard_single_weight': 1
    }

    if num_games and (not player1_is_ai or not player2_is_ai):
        print("Error: Both players must be AI to use the -num parameter.")
        return

    if run_genetic_algorithm:
        ga = GeneticAlgorithm(
            num_generations=50, population_size=20, mutation_rate=0.05
        )
        best_strategy = ga.run()
        print("Best Strategy:", best_strategy)
        return

    if not player1_is_ai and not player2_is_ai:
        player1_name = "Player 1"
        player2_name = "Player 2"

    board_state = BoardState(num_players)
    board_state.players[0] = Player(player1_name, board_state, player1_is_ai)
    board_state.players[1] = Player(player2_name, board_state, player2_is_ai)
    game_logic = GameLogic(board_state)
    if player1_is_ai and player1_name == "Genetic AI":
        board_state.players[0].strategy = best_strategy
    if player2_is_ai and player2_name == "Genetic AI":
        board_state.players[1].strategy = best_strategy

    # Initialize players' hands with cards from the draw pile
    for player in board_state.players:
        board_state.draw_cards_for_player(player)

    # Set AI difficulty
    if player1_is_ai:
        board_state.players[0].ai_difficulty = player1_name.split()[0]
    if player2_is_ai:
        board_state.players[1].ai_difficulty = player2_name.split()[0]

    # Activate the first player
    board_state.players[0].activate()

    if num_games:
        scores = {player1_name: 0, player2_name: 0}
        for game_count in range(1, num_games + 1):
            board_state = BoardState(num_players)
            board_state.players[0] = Player(player1_name, board_state, player1_is_ai)
            board_state.players[1] = Player(player2_name, board_state, player2_is_ai)
            game_logic = GameLogic(board_state, verbose=False)

            # Initialize players' hands with cards from the draw pile
            for player in board_state.players:
                board_state.draw_cards_for_player(player)

            # Set AI difficulty
            if player1_is_ai:
                board_state.players[0].ai_difficulty = player1_name.split()[0]
            if player2_is_ai:
                board_state.players[1].ai_difficulty = player2_name.split()[0]
            if player1_is_ai and player1_name == "Genetic AI":
                board_state.players[0].strategy = best_strategy
            if player2_is_ai and player2_name == "Genetic AI":
                board_state.players[1].strategy = best_strategy

            # Activate the first player
            board_state.players[0].activate()

            while True:
                for player in board_state.players:
                    game_logic.take_turn(player)

                    # Check for a winner
                    result = game_logic.check_win_condition()
                    if result != "No winner yet.":
                        winner_name = result.split()[0]
                        if winner_name.startswith("Player"):
                            winner_name = f"{winner_name} {result.split()[1]}"
                        elif winner_name in ["Easy", "Hard", "Genetic"]:
                            winner_name = f"{winner_name} AI"
                        scores[winner_name] += 1
                        break
                else:
                    continue
                break

            if game_count % 100 == 0:
                print(f"After {game_count} games: {scores}")

        print(f"Final scores after {num_games} games: {scores}")
    else:
        while True:
            for player in board_state.players:
                print("\nCurrent Board State:")
                board_state.show_board_state()

                print(f"\n{player.name}'s turn.")
                game_logic.take_turn(player)

                # Check for a winner
                result = game_logic.check_win_condition()
                if result != "No winner yet.":
                    print(result)
                    return


if __name__ == "__main__":
    main()
