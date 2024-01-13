import nbimporter
import numpy as np
import gym
from QLearning import BlackjackAgent
from tqdm import tqdm

learning_rate = 0.01
n_episodes = 100000
start_epsilon = 1.0
epsilon_decay = start_epsilon / (n_episodes / 2)
final_epsilon = 0.1

agent = BlackjackAgent(
    learning_rate=learning_rate,
    initial_epsilon=start_epsilon,
    epsilon_decay=epsilon_decay,
    final_epsilon=final_epsilon,
)
env = gym.make('Blackjack-v1')

for episode in tqdm(range(n_episodes)):
    obs = env.reset()
    done = False

    while not done:
        action = agent.get_action(obs)
        step_result = env.step(action)
        next_obs, reward, done, *_ = step_result
        agent.update(obs, action, reward, done, next_obs)
        obs = next_obs

    agent.decay_epsilon()

def simulate_games(number_of_games,env,agent):
    results = {'wins': 0, 'losses': 0, 'draws': 0}
    for i in range(number_of_games):
        obs = env.reset()
        done = False

        while not done:
            action = agent.get_action(obs)

            step_result = env.step(action)
            obs, reward, done, *_ = step_result

            if reward == 1:
                results['wins'] += 1
            elif reward == -1:
                results['losses'] += 1
            else:
                results['draws'] += 1
    return results

test = simulate_games(300,env,agent)

env.close()

print(test)