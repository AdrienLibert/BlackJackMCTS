import math
import random
import nbimporter
import copy
from Generate_deck import generate_deck

class BlackjackNode:
    def __init__(self, player_hand, dealer_hand, deck,countCard = 0 , money = 20, parent=None, is_terminal=False):
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.deck = deck
        self.countCard = countCard
        self.money = money
        self.parent = parent
        self.is_terminal = is_terminal
        self.visits = 0
        self.wins = 0
        self.children = []

def deal_hand(deck):
    return [deck.pop(), deck.pop()] 

def mcts(node, iterations):
    for _ in range(iterations):
        selected_node = select(node)
        expanded_node = expand(selected_node)
        simulation_result = simulate(expanded_node)
        play_game(expanded_node.player_hand,expanded_node.dealer_hand)
        backpropagate(expanded_node, simulation_result)
    return best_child(node)

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
    
    draw_child = BlackjackNode(player_hand=player_hand, dealer_hand=node.dealer_hand ,deck=draw_child_deck, countCard = node.countCard, money = node.money,parent=node, is_terminal=False)
    stay_child = BlackjackNode(player_hand=node.player_hand, dealer_hand=node.dealer_hand, deck=node.deck,countCard = node.countCard, money = node.money ,parent=node, is_terminal=True)
    
    node.children.extend([draw_child, stay_child])
    return draw_child

def simulate(node):
    player_hand = node.player_hand
    player_score = calculate_score(player_hand)

    while player_score < 17:
        drawn_card = draw_card(node.deck)

        if drawn_card['value'] in ['10','J', 'Q', 'K']:
            player_score += 10
            node.countCard -= 1 
        elif drawn_card['value'] in ['A']:
            node.countCard -= 1 
            if player_score > 11:
                player_score += 1
            else:
                player_score += 10
        elif drawn_card['value'] in ['7','8','9']:
             player_score += int(drawn_card['value'])
        else:
            player_score += int(drawn_card['value'])
            node.countCard += 1 
        play_dealer(node)
    return 1 if player_score <= 21 else 0


def backpropagate(node, result):
    while node:
        node.visits += 1
        if result is not None:
            node.wins += result
        node = node.parent

def play_dealer(node):
    dealer_hand = node.dealer_hand
    dealer_score = calculate_score(dealer_hand)

    while dealer_score < 17:
        drawn_card = draw_card(node.deck)

        if drawn_card['value'] in ['10','J', 'Q', 'K']:
            dealer_score += 10
            node.countCard -= 1 
        elif drawn_card['value'] in ['A']:
            node.countCard -= 1 
            if dealer_score > 11:
                dealer_score += 1
            else:
                dealer_score += 10
        elif drawn_card['value'] in ['7','8','9']:
             dealer_score += int(drawn_card['value'])
        else:
            dealer_score += int(drawn_card['value'])
            node.countCard += 1 


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

def betting (node):
    if node.countCard <-1:
        bet = node.money//20
    elif node.countCard>1:
        bet = node.money//2
    else :
        bet = node.money//10
    return bet

def best_child(node):
    best_child = max(node.children, key=lambda child: child.wins)
    return best_child

def draw_card(deck):
    if not deck:
        raise IndexError("Cannot choose from an empty deck")
    card = random.choice(deck)
    deck.remove(card)
    return card
    
def play_game(player_hand, dealer_hand):
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
        result = compare_hands(player_hand, dealer_hand)

    return result

def compare_hands(player_hand, dealer_hand):
    player_best_score = best_score(player_hand)
    dealer_best_score = best_score(dealer_hand)

    if player_best_score > dealer_best_score:
        return {"result": "win"}
    elif player_best_score < dealer_best_score:
        return {"result": "loss"}
    else:
        return {"result": "draw"}

def best_score(hand):
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

def calculate_score(hand):
    # Calcul du score du joueur ou du croupier
    score = 0
    num_aces = 0

    for card in hand:
        if card['value'] in ['10','J', 'Q', 'K']:
            score += 10
        elif card['value'] in ['A']:
            num_aces += 1
        else:
            score += int(card['value'])

    # Traitement des As
    while num_aces > 0 and score + 10 <= 21:
        score += 10
        num_aces -= 1

    return score
def draw_card_dealer(deck, dealer_hand):
    if not deck:
        raise IndexError("Cannot choose from an empty deck")

    card = random.choice(deck)
    deck.remove(card)
    dealer_hand.append(card)

    # Gestion des As dans la main du croupier
    if card['value'] == 'A':
        # Si la valeur de la main du croupier dépasse 21 avec l'As comme 11, réduisez la valeur de l'As à 1.
        if calculate_score(dealer_hand) > 21:
            for card in dealer_hand:
                if card['value'] == 'A':
                    card['value'] = '1'
                    break
    # Gestion des J, Q, K dans la main du croupier
    elif card['value'] in ['J', 'Q', 'K']:
        # Ajouter la valeur de 10 à la main du croupier
        for _ in range(10):
            dealer_hand.append({'value': '10', 'suit': card['suit']})

def simulate_games(number_of_games):
    results = {'wins': 0, 'losses': 0, 'draws': 0}
    for i in range(number_of_games):
        deck = generate_deck()
        player_hand = deal_hand(deck)
        print(player_hand)
        dealer_hand = deal_hand(deck)
        print(dealer_hand)
        node = mcts(BlackjackNode(player_hand, dealer_hand, deck), iterations=2000)
        # Pioche du croupier
        while calculate_score(dealer_hand) < 17:
            draw_card_dealer(deck, dealer_hand)

        game_result = play_game(node.player_hand, node.dealer_hand)
        if game_result['result'] == 'win':
            results['wins'] += 1
            print(f"Game {i + 1}: Win!")
        elif game_result['result'] == 'loss':
            results['losses'] += 1
            print(f"Game {i + 1}: Loss! ")
        else:
            results['draws'] += 1
            print(f"Game {i + 1}: Draw!")

    return results