#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nbimporter
from Strategy import apply_strategy
from Generate_deck import generate_deck
from Deal_hand import deal_hand


# In[2]:


def play_game(player_hand, dealer_hand, deck):
    #We need to install the logic of game
    result = {"win" : "dealer_hand"}
    return result


# In[3]:


def simulate_games(number_of_games, strategy):
    results = {'wins': 0, 'losses': 0, 'draws': 0}
    for i in range(number_of_games):
        deck = generate_deck()
        player_hand = deal_hand(deck)
        dealer_hand = deal_hand(deck)
        player_hand = apply_strategy(player_hand, dealer_hand, strategy)
        game_result = play_game(player_hand, dealer_hand, deck)
        
        if game_result['result'] == 'win':
            results['wins'] += 1
        elif game_result['result'] == 'loss':
            results['losses'] += 1
        else:
            results['draws'] += 1
    return results


# In[4]:


strategy = "counting"
number_of_games = 1000
simulation_results = simulate_games(number_of_games, strategy)

print(f"Strategy: {strategy}")
print(f"Total Games: {number_of_games}")
print(f"Wins: {simulation_results['wins']}")
print(f"Losses: {simulation_results['losses']}")
print(f"Draws: {simulation_results['draws']}")

