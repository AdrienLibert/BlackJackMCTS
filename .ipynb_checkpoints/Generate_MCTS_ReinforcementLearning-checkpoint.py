import math
import random
import copy
import numpy as np
from collections import defaultdict
import nbimporter
from QLearning import BlackjackAgent
from Generate_deck import generate_deck


class BlackjackNode:
    def __init__(self, player_hand, dealer_hand, deck, parent=None, is_terminal=False):
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.deck = deck
        self.parent = parent
        self.is_terminal = is_terminal
        self.visits = 0
        self.wins = 0
        self.children = []


def mcts(node, blackjack_agent, iterations):
    for i in range(iterations):
        selected_node = select(node, blackjack_agent)
        expanded_node = expand(selected_node)
        simulation_result, is_terminal, action_taken = simulate(expanded_node, blackjack_agent)
        backpropagate(expanded_node, simulation_result, action_taken)
    return best_child(node).player_hand


def select(node, blackjack_agent):
    while node.children:
        node = best_uct_q(node, blackjack_agent)
    return node


def expand(node):
    draw_child_deck = copy.copy(node.deck)
    if node.player_hand is None:
        player_hand = []
    else:
        player_hand = node.player_hand.copy()

    draw_card_value = draw_card(draw_child_deck)
    player_hand.append(draw_card_value)

    draw_child = BlackjackNode(player_hand=player_hand, dealer_hand=node.dealer_hand, deck=draw_child_deck, parent=node, is_terminal=False)
    stay_child = BlackjackNode(player_hand=node.player_hand, dealer_hand=node.dealer_hand, deck=node.deck, parent=node, is_terminal=True)

    node.children.extend([draw_child, stay_child])
    return draw_child


def simulate(node, blackjack_agent):
    player_hand = node.player_hand
    dealer_hand = node.dealer_hand
    deck = node.deck.copy()

    action = blackjack_agent.get_action([get_state_index_from_node(node)])

    if action == 1:  # 1 represents Hit
        drawn_card = draw_card(deck)
        player_hand.append(drawn_card)
        node.player_hand = player_hand

    reward, is_terminal = calculate_reward_and_terminal(node)
    next_obs = [get_state_index_from_node(node)]

    blackjack_agent.update(get_state_index_from_node(node), action, reward, is_terminal, next_obs)
    blackjack_agent.decay_epsilon()

    current_state_index = [get_state_index_from_node(node)]
    next_state_index = [get_state_index_from_node(node.parent)] if node.parent else [current_state_index[0]]

    blackjack_agent.update(current_state_index, action, reward, is_terminal, next_state_index)


    return reward, is_terminal, action


def backpropagate(node, result, action_taken):
    while node is not None:
        node.visits += 1
        if result is not None:
            node.wins += result
        if node.parent is not None:
            state_index = get_state_index_from_node(node)
            next_state_index = get_state_index_from_node(node.parent)
            blackjack_agent.update(state_index, action_taken, result, next_state_index)
        node = node.parent


def best_uct_q(node, blackjack_agent):
    exploration_weight = 1.0 / math.sqrt(2.0)

    def uct_q_value(child):
        state_index = get_state_index_from_node(child)
        q_value = np.max(blackjack_agent.q_values[state_index])

        if child.visits == 0:
            return float('inf')

        uct_val = (child.wins / child.visits) + exploration_weight * math.sqrt(math.log(node.visits) / child.visits) + q_value

        return uct_val

    return max(node.children, key=uct_q_value)


def best_child(node):
    best_child = max(node.children, key=lambda child: child.wins)
    return best_child


def draw_card(deck):
    if not deck:
        raise IndexError("Cannot choose from an empty deck")
    card = random.choice(deck)
    deck.remove(card)
    return card


def play_game(player_hand, dealer_hand, deck):
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if player_score > 21:
        result = {"result": "loss"}
    elif dealer_score > 21:
        result = {"result": "win"}
    elif player_score > dealer_score:
        result = {"result": "win"}
    elif player_score < dealer_score:
        result = {"result": "loss"}
    else:
        result = {"result": "draw"}

    return result


def calculate_score(hand):
    score = 0
    num_aces = 0

    for card in hand:
        if card['value'] in ['J', 'Q', 'K']:
            score += 10
        elif card['value'] == 'A':
            num_aces += 1
        else:
            score += int(card['value'])
    while num_aces > 0 and score + 10 <= 21:
        score += 10
        num_aces -= 1

    return score


def get_state_index_from_node(node):
    total_hand = calculate_score(node.player_hand)
    has_usable_ace = "A" in [card['value'] for card in node.player_hand] and total_hand + 10 <= 21

    state_index = total_hand - 4
    if has_usable_ace:
        state_index += 18

    if state_index < 0:
        state_index = 0
    elif state_index >= 36:
        state_index = 35

    return state_index


def calculate_reward_and_terminal(node):
    player_score = calculate_score(node.player_hand)
    dealer_score = calculate_score(node.dealer_hand)

    if player_score > 21:
        return -1, True
    elif dealer_score > 21 or player_score == 21:
        return 1, True
    elif node.is_terminal:
        if player_score > dealer_score:
            return 1, True
        elif player_score < dealer_score:
            return -1, True
        else:
            return 0, True
    return 0, False

def deal_hand(deck, num_cards=2):
    hand = []
    for _ in range(num_cards):
        hand.append(draw_card(deck))
    return hand


def simulate_games(number_of_games, blackjack_agent):
    results = {'wins': 0, 'losses': 0, 'draws': 0}
    for _ in range(number_of_games):
        deck = generate_deck()
        player_hand = deal_hand(deck)
        dealer_hand = deal_hand(deck)

        mcts_decision = mcts(BlackjackNode(player_hand, dealer_hand, deck, None, False), blackjack_agent, 1000)

        game_result = play_game(mcts_decision, dealer_hand, deck)
        if game_result['result'] == 'win':
            results['wins'] += 1
        elif game_result['result'] == 'loss':
            results['losses'] += 1
        else:
            results['draws'] += 1

    return results



learning_rate = 0.1
initial_epsilon = 1.0
epsilon_decay = 0.995
final_epsilon = 0.01

# Create an instance of BlackjackAgent
blackjack_agent = BlackjackAgent(learning_rate, initial_epsilon, epsilon_decay, final_epsilon)

number_of_games = 300
strategy = "mcts"
results = simulate_games(number_of_games, blackjack_agent)

print("Simulation results:")
print(results)
