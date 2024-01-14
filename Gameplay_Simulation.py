import nbimporter
from Generate_deck import generate_deck
from QLearning import BlackjackAgent
from Deal_hand import deal_hand
import gym
from Generate_MCTS import simulate_games
from RL_BJ import simulate_rl
from Generate_MCTS_ReinforcementLearning import simulate_g

def main():
    print("Welcome to Blackjack Simulator")
    while True:
        print("\nSelect the method you want to use:")
        print("1: Monte Carlo Tree Search (MCTS)")
        print("2: Reinforcement Learning")
        print("3: MCTS with Reinforcement Learning")
        print("4: Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            number_of_games = int(input("Enter the number of games to simulate: "))
            results = simulate_games(number_of_games)
            print("Simulation results:", results)
        elif choice == "2":
            number_of_games = int(input("Enter the number of games to simulate: "))
            results = simulate_rl(number_of_games)
            print("Simulation results:", results)

        elif choice == "3":
            learning_rate = 0.1
            initial_epsilon = 1.0
            epsilon_decay = 0.995
            final_epsilon = 0.01
            blackjack_agent = BlackjackAgent(learning_rate, initial_epsilon, epsilon_decay, final_epsilon)
            number_of_games = int(input("Enter the number of games to simulate: "))
            results = simulate_g(number_of_games, blackjack_agent)
            print("Simulation results:", results)
        elif choice == "4":
            print("Exiting the simulator.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()