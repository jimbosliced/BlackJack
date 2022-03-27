# Milestone Project 2 - Blackjack .. Step 3 : Create a Deck Class Feb 13 2022

import random

suits = ('Hearts,', 'Diamonds,', 'Spades,', 'Clubs,')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True  ############


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_cards = ' '
        for card in self.deck:
            deck_cards += card.__str__() + '\n'
        return deck_cards

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        one_card = self.deck.pop()
        return one_card


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))

        except:
            print("Sorry, you must bet an integer value!")

        else:
            if chips.bet > chips.total:
                print("Sorry, you don't have enough to bet that much!")
            else:
                break


# Step 7 Function Definitions BLACKJACK
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while hand.value < 21:
        h_or_s = input("Would you like to hit or stand? type 'h' for hit and type 's' for stand: ")

        if h_or_s == 'h':
            hit(deck, hand)
        elif h_or_s == 's':
            print("Okay, now the dealer will play")
            playing = False
        else:
            print("Please enter 'h' or 's': ")
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:", dealer.cards[0])  ############
    print("\nPlayer's Hand:", *player.cards)  ############


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards)  # * ... what the asterisk does, is call each card from the dealer's or player's deck
    print("\nPlayer's Hand:", *player.cards)  ############


def player_busts(chips):
    print("You bust!")
    chips.lose_bet()


def player_wins(chips):
    print("You win!")
    chips.win_bet()


def dealer_busts(chips):
    print("Dealer busts!")
    chips.win_bet()


def dealer_wins(chips):
    print("Dealer wins!")
    chips.lose_bet()


def push():
    print("Dealer and player ties. Nobody wins!")


# Main Body
player_chips = Chips()
while True:

    # Print an opening statement
    print("Welcome to the game of Blackjack!")

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    player_hand.adjust_for_ace()
    dealer_hand.adjust_for_ace()

    # Set up the Player's chips

    print(f"You have a total of {player_chips.total} chips")  ############

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_chips)
            break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:  ############
        while dealer_hand.value < 17:
            print("Dealer hits!\n")  ############
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:  ############
            print(f"Dealer busts with a score of {dealer_hand.value}")
            dealer_busts(player_chips)
        elif player_hand.value > dealer_hand.value:
            print(f"Player wins with a score of {player_hand.value} vs dealer score of {dealer_hand.value}")
            player_wins(player_chips)
        elif dealer_hand.value > player_hand.value:
            print(f"Dealer wins with a score of {dealer_hand.value} vs player score of {player_hand.value}")
            dealer_wins(player_chips)
        elif player_hand.value == dealer_hand.value:
            push()

    # Inform Player of their chips total
    print(f"Here are your chips' total: {player_chips.total}")  ############

    # Ask to play again
    play_again = input("Would you like to play again? 'y' or 'n': ").lower()

    if play_again == 'y':
        playing = True
        print("\n" * 5)  ############
        continue
    elif play_again == 'n':
        print("\n" * 5)  ############
        print("Thank you for playing!")
        break
