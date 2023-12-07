## Blackjack Monte Carlo Simulation

# Introduction
Blackjack, originally known as "Vingt et un" (Twenty-One), has its roots in 18th-century French casinos. 
Gaining popularity among figures like Madame du Barry and Napoleon, the game crossed the Atlantic post-Revolution, evolving into the Blackjack we know today in American gambling circles. 
The game's core remains unchanged: players aim to beat the dealer without exceeding a total card value of 21.

# Rules Overview
Card Values: Number cards are worth their face value, face cards are worth 10, and Aces can be 1 or 11.
The Deal: Each player and the dealer start with two cards. The dealer has one card face down.
Player's Turn: Players can hit (ask for more cards), stand (keep their current hand), double down (double the bet for one more card), or split (if they have two cards of the same value).
Special Cases: Players can take insurance against the dealer's potential blackjack.
Winning and Losing: Players bust and lose if they exceed 21. Otherwise, higher hand values than the dealer's win.
Strategies
Basic Strategy: A set of rules for the best mathematical action based on the player's hand and the dealer's visible card.
Simple Strategy: A less detailed, more general approach than Basic Strategy.
Card Counting: Advanced strategy involving tracking high and low cards to inform betting and playing decisions.
Monte Carlo Simulation
We employ the Monte Carlo method to simulate thousands of Blackjack games, analyzing the effectiveness of different strategies.

# Key Components

Random Deck Generator (generate_deck): Generates a shuffled 52-card deck.
Card Distribution (deal_hand): Deals two cards to players and the dealer.
Strategy Implementation (apply_strategy): Simulates player decisions based on their hand, the dealer's visible card, and a chosen strategy.
Gameplay Simulation (play_game): Plays out a hand of Blackjack following the game rules and strategies.
Simulation and Result Recording (simulate_games): Repeats gameplay to record results and assess strategy effectiveness.
Process

The simulation starts with a random deck and deals hands to players and the dealer.
Players play according to their chosen strategy (Basic, Simple, or Card Counting).
The dealer follows a set of fixed rules (e.g., hitting until reaching 17 or higher).
The simulation records wins, losses, or ties.
Repeating this process thousands of times, the algorithm averages out results to determine the most effective strategy.

# Run the Blackjack Monte Carlo simulation

Install Dependencies:
'pip install -r requirements.txt'

Run the Simulation:
'python Gameplay_Simulation.py'
