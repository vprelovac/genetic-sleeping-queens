import random
from board_state import BoardState
from game_logic import GameLogic
from player import Player


class GeneticAlgorithm:
    def __init__(self, num_generations, population_size, mutation_rate):
        self.num_generations = num_generations
        self.population_size = population_size
        self.mutation_rate = mutation_rate

    def create_individual(self):
        # Create an individual with random strategy parameters
        return {
            "awaken_queen_weight": random.uniform(0, 1),
            "steal_queen_weight": random.uniform(0, 1),
            "put_queen_to_sleep_weight": random.uniform(0, 1),
            "play_jester_weight": random.uniform(0, 1),
            "discard_equation_weight": random.uniform(0, 1),
            "discard_pair_weight": random.uniform(0, 1),
            "discard_single_weight": random.uniform(0, 1),
        }

    def create_population(self):
        return [self.create_individual() for _ in range(self.population_size)]

    def evaluate_fitness(self, individual):
        # Evaluate the fitness of an individual by simulating games
        scores = {"Genetic AI": 0, "Hard AI": 0}
        num_simulations = 500

        for _ in range(num_simulations):
            board_state = BoardState(2)
      
            player1 = Player("Hard AI", board_state, is_ai=True)
            player2 = Player("Genetic AI", board_state, is_ai=True)
            board_state.players = [player1, player2]
            game_logic = GameLogic(board_state, verbose=False)

            player2.strategy = individual

            # Initialize players' hands with cards from the draw pile
            for player in board_state.players:
                board_state.draw_cards_for_player(player)

            # Set AI difficulty
            player2.ai_difficulty = "Genetic"
            player1.ai_difficulty = "Hard"

            # Activate the first player
            board_state.players[0].activate()

            while True:
                for player in board_state.players:
                    game_logic.take_turn(player)

                    # Check for a winner
                    result = game_logic.check_win_condition()
                    if result != "No winner yet.":
                        winner_name = result.split()[0]
                        #                       print(winner_name)
                        if winner_name in ["Easy", "Hard", "Genetic"]:
                            winner_name = f"{winner_name} AI"
                        scores[winner_name] += 1
                        break
                else:
                    continue
                break
        #    print(scores)
        return scores["Genetic AI"] / num_simulations

    def select_parents(self, population, fitnesses):
        # Select parents based on their fitness

        if random.random() < 0.6:
            total_fitness = sum(fitnesses)
            if total_fitness == 0:
                probabilities = [1 / len(fitnesses) for _ in fitnesses]
            else:
                probabilities = [fitness / total_fitness for fitness in fitnesses]
            parents = random.choices(population, probabilities, k=2)
        else:
            parents = [
                self.tournament_selection(population, fitnesses),
                self.tournament_selection(population, fitnesses),
            ]
        # print(f"Selected Parents: {fitnesses[population.index(parents[0])]}, {fitnesses[population.index(parents[1])]}")
        return parents

    def tournament_selection(self, population, fitnesses, tournament_size=3):
        # Select a group of individuals randomly
        selected_indices = random.sample(range(len(population)), tournament_size)
        selected_individuals = [population[i] for i in selected_indices]
        selected_fitnesses = [fitnesses[i] for i in selected_indices]

        # Choose the individual with the highest fitness
        best_index = selected_indices[selected_fitnesses.index(max(selected_fitnesses))]
        return population[best_index]

    def crossover(self, parent1, parent2):
        # Perform crossover between two parents to create a child
        child = {}
        if random.random() < 0.6:
            for key in parent1:
                child[key] = parent1[key] if random.random() < 0.5 else parent2[key]
        else:
            for key in parent1:
                child[key] = (parent1[key] + parent2[key]) / 2
        return child

    def mutate(self, individual):
        # Mutate an individual with a given mutation rate
        for key in individual:
            if random.random() < self.mutation_rate:
                individual[key] = random.uniform(0, 1)
        return individual

    def run(self):
        population = self.create_population()

        best_individual = None
        best_fitness = -1

        for generation in range(self.num_generations):
            fitnesses = [self.evaluate_fitness(individual) for individual in population]

            # Update the best individual found so far
            current_best_fitness = max(fitnesses)
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = population[fitnesses.index(current_best_fitness)]
                print(f"{self.print_best_strategy(best_individual)}")
            new_population = []

            # Sort population based on fitness
            sorted_population = [
                x
                for _, x in sorted(
                    zip(fitnesses, population), key=lambda pair: pair[0], reverse=True
                )
            ]

            # Copy the top two individuals
            new_population.append(sorted_population[0])
            new_population.append(sorted_population[1])

            # Create a child between the top two individuals
            child = self.crossover(sorted_population[0], sorted_population[1])
            new_population.append(self.mutate(child))

            child = self.crossover(sorted_population[0], sorted_population[1])
            new_population.append(self.mutate(child))

            # Fill the rest of the new population
            for _ in range((self.population_size - 4) // 2):
                parent1, parent2 = self.select_parents(population, fitnesses)
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(child1))
                new_population.append(self.mutate(child2))

            population = new_population
            average_fitness = sum(fitnesses) / len(fitnesses)
            median_fitness = sorted(fitnesses)[len(fitnesses) // 2]
            print(
                f"Generation {generation + 1}: Top = {best_fitness} Best Fitness = {current_best_fitness}, Average Fitness = {average_fitness:.2f}, Median Fitness = {median_fitness}"
            )

        self.print_best_strategy(best_individual)
        return best_individual

    def print_best_strategy(self, best_individual):
        sorted_weights = sorted(best_individual.items(), key=lambda item: item[1], reverse=True)
        ranked_strategy = {key: len(sorted_weights) - rank for rank, (key, _) in enumerate(sorted_weights)}
        print(ranked_strategy)


if __name__ == "__main__":
    ga = GeneticAlgorithm(num_generations=100, population_size=30, mutation_rate=0.1)
    best_strategy = ga.run()
