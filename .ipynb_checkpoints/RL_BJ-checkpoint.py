import nbimporter
import numpy as np
import gym
from QLearning import BlackjackAgent
from tqdm import tqdm

def simulate_rl(number_of_games, training_episodes=15000):
    # Paramètres de l'agent d'apprentissage par renforcement
    learning_rate = 0.005
    start_epsilon = 1.0
    epsilon_decay = 0.1
    final_epsilon = 0.01

    # Création de l'agent d'apprentissage par renforcement
    agent = BlackjackAgent(
        learning_rate=learning_rate,
        initial_epsilon=start_epsilon,
        epsilon_decay=epsilon_decay,
        final_epsilon=final_epsilon,
    )
    # Création de l'environnement de jeu Blackjack
    env = gym.make('Blackjack-v1')
    for episode in tqdm(range(training_episodes)):
        obs = env.reset()
        done = False
        while not done:
            action = agent.get_action(obs)
            next_obs, reward, done, _ = env.step(action)[:4]
            agent.update(obs, action, reward, done, next_obs)
            obs = next_obs
        agent.decay_epsilon()

    # Phase de simulation
    results = {'wins': 0, 'losses': 0, 'draws': 0}

    # Boucle sur le nombre de parties à simuler
    for game_number in range(number_of_games):
        obs = env.reset()  # Réinitialisation de l'environnement pour une nouvelle partie
        done = False
        print(f"Jeu {game_number + 1} : Début")
        print(f"État initial : Main du joueur : {obs[0]}, Main du croupier : {obs[1]}")

        while not done:
            action = agent.get_action(obs)  # L'agent choisit une action
            next_obs, reward, done, _, _ = env.step(action)  # Mise à jour de l'environnement après l'action

            if done:
                print(f"État final : Main du joueur : {next_obs[0]}, Main du croupier : {next_obs[1]}")
                # Mise à jour des résultats en fonction du gain
                if reward == 1:
                    results['wins'] += 1
                    print("Résultat : Victoire !")
                elif reward == -1:
                    results['losses'] += 1
                    print("Résultat : Défaite !")
                else:
                    results['draws'] += 1
                    print("Résultat : Égalité !")
            obs = next_obs
        print("----------------------------------------------------")
        env.close()  # Fermeture de l'environnement après la partie
    return results
