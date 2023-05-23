#
# --Blackjack--
# Play a single game of blackjack between two players
#

import urllib.request
import json

# define numeric card values
card_Values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10,"A": 11}

def main():
    # initialize game deck
    deck = Deck()

    # initialize players
    player_truls = Player("Truls",[])
    player_marit = Player("Marit",[])

    # initial dealing of two cards to each player's hand
    player_truls.hand.extend(deck.draw_card(2))
    player_marit.hand.extend(deck.draw_card(2))

    # if double aces on initial draw, set the numeric value of the first ace to 1
    player_truls = double_aces(player_truls)
    player_marit = double_aces(player_marit)

    # Check for blackjack (with possible draw) after initial card draw
    if player_truls.player_score() == 21:
        if player_truls.player_score() == player_marit.player_score():
            game_completion("tie",player_truls,player_marit)
        else:
            game_completion(player_truls.name,player_truls,player_marit)
    if player_marit.player_score() == 21:
        game_completion(player_marit.name,player_truls,player_marit)

    # Player actions: Truls
    # Truls draws a card while his total score is below 17. 
    while(player_truls.player_score() < 17):
        player_truls.hand.extend(deck.draw_card())
        if player_truls.player_score() == 21:
            game_completion(player_truls.name,player_truls,player_marit)
        if player_truls.player_score() > 21:
            game_completion(player_marit.name,player_truls,player_marit)

    # Player actions: Marit
    # Marit draws a card until her total is score higher than Truls'. 
    while(player_marit.player_score() <= player_truls.player_score()):
        player_marit.hand.extend(deck.draw_card())
        if player_marit.player_score() == 21:
            game_completion(player_marit.name,player_truls,player_marit)
        if player_marit.player_score() > 21:
            game_completion(player_truls.name,player_truls,player_marit)
    
    # determine winner
    if player_truls.player_score() > player_marit.player_score():
        game_completion(player_truls.name,player_truls,player_marit)
    else:
        game_completion(player_marit.name,player_truls,player_marit)

# card class definition
# cards have a suit, value and a numeric value
class Card:
    def __init__(self,suit,value,valueNumeric):
        self.suit = suit
        self.value = value
        self.valueNumeric = valueNumeric

# deck class definition
# a deck consists of multiple Cards
class Deck:
    def __init__(self):
        self.cards = []
        self.cards = self.generate_deck()
    
    # generate/shuffle deck of cards
    def generate_deck(self):
        
        # define variable to hold source url
        urlData = "https://blackjack.ekstern.dev.nav.no/shuffle"

        # open the url and read the data
        webUrl = urllib.request.urlopen(urlData)
        if webUrl.getcode() == 200:
            data = webUrl.read()
            cards = json.loads(data)
            for card in cards:
                self.cards.append(Card(card["suit"],card["value"],card_Values[card["value"]]))
            return self.cards          
        else:
            print("Received an error from the endpoint when fetching shuffled deck",webUrl.getcode())
            quit()

    # draw num_cards number of cards from the deck
    def draw_card(self,num_cards=1):
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards in the deck..")
        drawn_cards = []
        for i in range (num_cards):
            drawn_cards.append(self.cards.pop())
        return drawn_cards

# player class definition
# Players have a name and a hand
class Player:
    def __init__(self,name,hand):
        self.name = name
        self.hand = hand
    
    # return total player score based on current hand
    def player_score(self):
        Score = 0
        for card in self.hand:
            Score += card.valueNumeric
        return Score
    
    # return player cards in abbreviated form
    def player_hand_output(self):
        player_hand = [card.suit[0] + str(card.value) for card in self.hand]
        return ', '.join(player_hand)
    
# In cases where intial card draw is two Aces, set numeric value of first ace to 1
def double_aces(player):
    if len(player.hand) == 2:
        if player.player_score() == 22:
            player.hand[0].valueNumeric = 1
    return player

# function to print final result and exit game
def game_completion(winner,*players):
    print("winner:",winner,"\n")
    for player in players:
        print(player.name," | ",player.player_score()," | ", player.player_hand_output())
    quit()

if __name__=="__main__":
    main()