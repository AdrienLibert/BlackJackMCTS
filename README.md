## Simulation de Blackjack Monte Carlo
# Introduction
Le Blackjack, initialement connu sous le nom de "Vingt et un", trouve ses origines dans les casinos français du XVIIIe siècle.

Gagnant en popularité auprès de figures telles que Madame du Barry et Napoléon, le jeu a traversé l'Atlantique après la Révolution, évoluant vers le Blackjack que nous connaissons aujourd'hui dans les cercles de jeu américains.

Le cœur du jeu reste inchangé : les joueurs cherchent à battre le croupier sans dépasser une valeur totale de carte de 21.

# Règles du Jeu
Valeurs des Cartes : Les cartes numérotées valent leur valeur faciale, les figures valent 10, et les As peuvent valoir 1 ou 11.

La Donne : Chaque joueur et le croupier commencent avec deux cartes. Le croupier a une carte face cachée.

Tour du Joueur : Les joueurs peuvent tirer (demander plus de cartes), rester (conserver leur main actuelle), doubler (doubler la mise pour une carte supplémentaire) ou séparer (si elles ont deux cartes de même valeur).

Gagner et Perdre : Les joueurs font faillite et perdent s'ils dépassent 21. Sinon, des valeurs de main plus élevées que celles du croupier gagnent.

# Simulation Monte Carlo
Nous employons la méthode de Monte Carlo et du Q learning pour simuler des milliers de parties de Blackjack, analysant l'efficacité de différentes méthodes.

# Composants Clés
La simulation commence avec un deck aléatoire (generate_deck pour le MCTS et environnement gym pour le Q learning) et distribue des mains aux joueurs et au croupier.

Le croupier suit un ensemble de règles fixes.

La simulation enregistre les victoires, les défaites ou les égalités.

# Exécution de la simulation de Blackjack Monte Carlo
Installation des Dépendances :

'pip install -r requirements.txt'
Lancer la Simulation :

'python Gameplay_Simulation.py'