import nbimporter
from Generate_deck import generate_deck
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
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            print("Exiting the simulator.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()