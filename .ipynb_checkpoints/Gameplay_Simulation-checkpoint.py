import nbimporter
from Strategy import apply_strategy
from Generate_deck import generate_deck
from Deal_hand import deal_hand
import gym
from Generate_MCTS import simulate_games
from RL_BJ import simulate_rl

print("Quelle méthode voulez-vous utiliser ?")
print("mcts tape 1")
print("reinforcement learning 2")
print("mcts + renforcement learning 3")
cpt = input()

if cpt == "1":
    simulate_games(1)
elif cpt == "2":
    simulate_rl(1)
elif cpt == "3":
    print("attend")
else:
    print("erreur de méthode")
    