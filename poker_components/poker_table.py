from dealer import Dealer
from player import Player

class Table:
    """This is the table class. It is where the game is actually played. It has 7 functions to
        __init__ (No parameters, for now inserts 4 players and calls the play_hand function)
        add_player (Takes a name as a parameter, calls the dealers deal_player function, then adds the player to the player
        list. If there are no other player's the play is made the focus)
        play_hand (Takes a input of the amount of players and initializes them, then gets the flop, turn and river)
        __str__ (A to string function used for testing)
        reset_round (The dealer calls it's shuffle_deck function, clears the player and card lists, then starts another ronud)
        find_selected_player (Loops through the player list and returns the selected one)
        return_cards(Makes a list of the selected players cards and all cards in the table, then returns said list)"""
    table_dealer = Dealer() #initizalizing the dealer
    player_list = [] #this list will contain all players
    cards_in_play = [] #these are the communal cards everyone can use to form hands
    
    def __init__(self):
        self.add_player('A')
        self.add_player('B')
        self.add_player('C')
        self.add_player('D')
        self.play_hand()

    def add_player(self, name): #this method creates a player and deals them a hand then adds them to the player_list
        hand = self.table_dealer.deal_player() #we get 2 new cards from the dealer to give to the player
        newPlayer = Player(name, hand) #creating the newPlayer

        if(len(self.player_list) == 0): #if there are no other players the 1st one is set to be the focus
            newPlayer.set_focus(True)

        self.player_list.append(newPlayer) #adding the new player to the list

    def play_hand(self):
        # try:
        #     print("How many players are there? (1-4)")
        #     num_players = int(input())
        # except ValueError: #in case a string is given as input instead of a int
        #     print("Please input a number 1 - 4")
        #     num_players = int(input())


        # while num_players > 4 or num_players < 1: #checks to make sure the player count is within the bounds given
        #     print("Invalid number of players. Please try again")
        #     num_players = int(input())

        # for x in range(num_players): #this loop gets a player's name, then passes it to add_player to create the player and add them to the list
        #     print("\nPlease give player " + str(x + 1) + "'s name?")
        #     player_name = str(input())
        #     self.add_player(player_name)

        # print("\nFLOP\n") testing
        self.cards_in_play.extend(self.table_dealer.deal_flop()) #adds the flop to the communal cards
        # print("\nTURN\n") testing
        self.cards_in_play.append(self.table_dealer.deal_turn_river()) #adds the turn to the communal cards
        # print("\nRIVER\n") testing
        self.cards_in_play.append(self.table_dealer.deal_turn_river()) #adds the river to the communal cards

    def __str__(self):
        to_return = ""
        for x in range(len(self.player_list)):
            to_return += str(self.player_list[x])
            
        for x in range(len(self.cards_in_play)):
            to_return += str(self.cards_in_play[x])

        return to_return + '\n'

    def reset_round(self):
        self.table_dealer.shuffle_deck()
        self.player_list.clear()
        self.cards_in_play.clear()
        # self.play_hand()
        self.add_player('A')
        self.add_player('B')
        self.add_player('C')
        self.add_player('D')
        self.play_hand()

    def find_selected_player(self):
        for x in self.player_list:
            if(x.get_focus()):
                return x

    def return_cards(self):
        cards = []
        cards.extend(self.find_selected_player.get_hand())
        cards.extend(self.cards_in_play)
        return cards