import math
import random
import nbimporter
import copy
from Strategy import apply_strategy
from Generate_deck import generate_deck
from Deal_hand import deal_hand

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

def mcts(node, iterations):
    for _ in range(iterations):
        selected_node = select(node)
        expanded_node = expand(selected_node)
        simulation_result = simulate(expanded_node)
        backpropagate(expanded_node, simulation_result)

    return best_child(node).player_hand

def select(node):
    while node.children:
        if not best_uct(node).deck:
            best_uct(node).deck = copy.copy(node.deck)
        node = best_uct(node)
        
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

def simulate(node):
    player_hand = node.player_hand
    sumplay_hand = 0

    for card in player_hand:
        if card['value'] in ['J', 'Q', 'K']:
            sumplay_hand += 10
        elif card['value'] == 'A':
            if sumplay_hand > 11:
                sumplay_hand += 1
            else:
                sumplay_hand += 10
        else:
            sumplay_hand += int(card['value'])

    if not node.deck:
        raise IndexError("Cannot choose from an empty deck")

    deck_copy = node.deck.copy()

    while sumplay_hand < 17:
        drawn_card = draw_card(deck_copy)
        if drawn_card['value'] in ['J', 'Q', 'K']:
            sumplay_hand += 10
        elif drawn_card['value'] == 'A':
            if sumplay_hand > 11:
                sumplay_hand += 1
            else:
                sumplay_hand += 10
        else:
            sumplay_hand += int(drawn_card['value'])

    return 1 if sumplay_hand <= 21 else 0 

def backpropagate(node, result):
    while node:
        node.visits += 1
        if result is not None:
            node.wins += result
        node = node.parent

def best_uct(node):
    exploration_weight = 1.0 / math.sqrt(2.0)
    def uct_value(child):
            if child.visits == 0:
                return float('inf') 

            try:
                uct_val = child.wins / child.visits + exploration_weight * math.sqrt(max(0, math.log(node.visits) / child.visits))
                return uct_val if not math.isinf(uct_val) else float('inf')
            except ValueError:
                return float('inf') 
    best_child = max(node.children, key=uct_value)
    return best_child


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
    # Calcul du score du joueur ou du croupier
    score = 0
    num_aces = 0

    for card in hand:
        if card['value'] in ['J', 'Q', 'K']:
            score += 10
        elif card['value'] == 'A':
            num_aces += 1
        else:
            score += int(card['value'])

    # Traitement des As
    while num_aces > 0 and score + 10 <= 21:
        score += 10
        num_aces -= 1

    return score
    
def simulate_games(number_of_games, strategy):
    results = {'wins': 0, 'losses': 0, 'draws': 0}
    for i in range(number_of_games):
        deck = generate_deck()
        player_hand = deal_hand(deck)
        dealer_hand = deal_hand(deck)
        
        if strategy == "mcts":
            player_hand = mcts(BlackjackNode(player_hand, dealer_hand, deck), iterations=10000)
        else:
            player_hand = apply_strategy(player_hand, dealer_hand, strategy)
        
        game_result = play_game(player_hand, dealer_hand, deck)
        
        if game_result['result'] == 'win':
            results['wins'] += 1
        elif game_result['result'] == 'loss':
            results['losses'] += 1
        else:
            results['draws'] += 1
    return results


strategy = "mcts"  
number_of_games = 100
simulation_results = simulate_games(number_of_games, strategy)

print(f"Strategy: {strategy}")
print(f"Total Games: {number_of_games}")
print(f"Wins: {simulation_results['wins']}")
print(f"Losses: {simulation_results['losses']}")
print(f"Draws: {simulation_results['draws']}")