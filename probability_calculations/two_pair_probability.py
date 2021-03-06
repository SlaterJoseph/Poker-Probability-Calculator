from probability_helper import truncate, process_matches, build_ranks

def calculate_two_pair(hand, table, round):
    """This processes the probability of getting two pairs 

    There are parameters for the player's hand, table's cards and current round. Based on the round, a different if statement 
    contains the proper function calls, passing the right amount of card from the table. The hand is always passed"""
    
    if round == 'preflop': #Only the hand is available
        probability = [flop(hand), turn(hand), river(hand), flop(hand) + turn(hand) + river(hand)]

    elif round == 'flop': #The hand and 3 table cards are avialable
        if turn(hand, table[0:3]) == 100: #If the probabilty is 100, we found a two pairs on the flop
            probability = [flop(hand), 100, 100, 100] #no need to check the what the likelyhood is for future rounds
        else: #if there isn't a two pairs, we pass the table's first 3 cards and the hand to the methods
            probability = [flop(hand), turn(hand, table[0:3]), river(hand, table[0:3]),\
                 turn(hand, table[0:3]) + river(hand, table[0:3])]
    
    elif round == 'turn': #The hand and 4 table cards are available
        if turn(hand, table[0:3]) == 100: #checks if the flop contained two pairs
            probability = [flop(hand), 100, 100, 100]
        elif river(hand, table[0:4]) == 100: #checks if the turn contained two pairs
            probability = [flop(hand), turn(hand, table[0:3]), 100, 100]
        else: #There are not 2 pairs yet, so the hand and 4 table cards are passed
            probability = [flop(hand), turn(hand, table[0:3]), river(hand, table[0:4]), river(hand, table[0:4])]

    else: #The hand and all 5 table cards are avialable 
        if turn(hand, table[0:3]) == 100: #checks if the flop contained two pairs
            probability = [flop(hand), 100, 100, 100] 
        elif river(hand, table[0:4]) == 100: #checks if the turn contained two pairs
            probability = [flop(hand), turn(hand, table[0:3]), 100, 100] 
        elif final_check(hand, table) == 100: #to see if by the end of the game there is two pairs
            probability = [flop(hand), turn(hand, table[0:3]), river(hand, table[0:4]), 100]
        else: #There was not two pairs, so the final check is 0
            probability = [flop(hand), turn(hand, table[0:3]), river(hand, table[0:4]), 0]

    return probability
    
def flop(hand): 
    """This function checks the probability of getting two pairs specifically on the flop"""
    ranks = {hand[0].get_value(), hand[1].get_value()}
    if len(ranks) == 1:
        flop_two_pair = ((66 * 4 * 6) / 19600) + ((12 * 4) / 19600) + ((2 * 12 * 6) / 19600)

    else:
        flop_two_pair = ((3 * 3 * 11 * 4) / 19600) + ((2 * 3 * 11 * 6) / 19600) + ((2 * 3 * 3) / 19600)
    return truncate(flop_two_pair)

def turn(hand, table = 'n/a'): 
    """This function checks the probability of getting two pairs specifally on the turn"""
    if table == 'n/a': #No flop is available yet
        ranks = {hand[0].get_value(), hand[1].get_value()}
        if len(ranks) == 1: #we have a pocket pair
           turn_two_pair = ((220 * 4 * 4 * 4)/19600) * (9 / 47) + ((2 * 66 * 4 * 4)/19600) * (6 / 47) \
           + ((12 * 4)/19600) * (3 / 47)

        else: #our hand does not make a pocket pair
            turn_two_pair =  (((2 * 3 * 55 * 4 * 4) / 19600) * (9 / 47)) + (((55 * 6 * 4) / 19600) * (9 / 47)) \
            + (((11 * 4) / 19600) * ((6 / 47))) + ((2 / 19600) * (3 / 47)) + (((2 * 3 * 11 * 4) / 19600) * (6 / 47))
    else: #We have the flop available 
        ranks = build_ranks(hand, table, 3) #these if and elif assume there is a pair or better (3 of a kind, 4 of a kind)
        if process_matches(ranks, 4) == 1: # if we have 4s, only 1 card can make a pair on the flop
            turn_two_pair = 3 / 47 
        elif process_matches(ranks, 3) == 1: #if we have 3s, 2 cards can make a pair on the flop
            turn_two_pair = 6 / 47 
        elif process_matches(ranks, 2) == 1: #if we have 1 pair, 3 cards can make a pair on the flop
            turn_two_pair = 9 / 47 
        else: #either we have no pairs or 2 pairs
            turn_two_pair = 0 if process_matches(ranks, 2) == 0 else 100
    return truncate(turn_two_pair)

def river(hand, table = 'n/a'):
    """This function checks the probability of getting two pairs specifally on the flop"""
    if table == 'n/a':
        ranks = {hand[0].get_value(), hand[1].get_value()}
        if len(ranks) == 1: #Our hand contains a pokcet pair
            river_two_pair = (((2 * 66 * 4 * 4) / 19600) * ((10 * 4) / 47) * (9 / 46)) \
            + (((220 * 4 * 4 * 4) / 19600) * ((9 * 4) / 47) * (12 / 46)) + (((12 * 4) / 19600) * ((11 * 4) / 47) * (6 / 46)) \
            + (((220 * 4 * 4 * 4) / 19600) * ((2 * 4) / 47) * (9 / 46)) + (((2 * 66 * 4 * 4) / 19600) * (1 / 47) * (9 / 46))
        else:
            river_two_pair =  (((2 * 3 * 55 * 4 * 4) / 19600) * ((9 * 4) / 47) * (12 / 46)) \
            + (((2 * 3 * 11 * 4) / 19600) * ((10 * 4) / 47) * (9 / 46)) + ((2  / 19600) * ((11 * 4) / 47) * (6 / 46)) \
            + (((55 * 6 * 4) / 19600) * ((9 * 4) / 47) * (12 / 46)) + (((11 * 4) / 19600) * ((10 * 4) / 47) * (9 / 46)) \
            + (((165 * 4 * 4 * 4) / 19600) * ((2 * 3) / 47) * (12 / 46)) \
            + (((2 * 3 * 55 * 4 * 4) / 19600) * (2 / 47) * (9 / 46)) + (((2 * 3 * 11 * 4 * 4) / 19600) * (1 / 47) * (6 / 46)) \
            + (((165 * 4 * 4 * 4) / 19600) * ((3 * 3) / 47) * (12 / 46)) \
            + (((55 * 6 * 4) / 19600) * (2 / 47) * (9 / 46)) + (((11 * 4) / 19600) * (1 / 47) * (6 / 46))

    elif len(table) == 3: #We have the flop available 
        ranks = build_ranks(hand, table, 3)
        if process_matches(ranks, 4) == 1: # if we have fours, only 1 card can make a pair on the flop
            river_two_pair = ((11 * 4) / 47) * (6 / 46) 
        elif process_matches(ranks, 3) == 1: #if we have 3s, 2 cards can make a pair on the flop
            river_two_pair = (2 / 47) * (6 / 46) + ((10 * 4) / 47) * (9 / 46) 
        elif process_matches(ranks, 2) == 1: #if we have 1 pair, 3 cards can make a pair on the flop
            river_two_pair = ((9 * 4) / 47) * (12 / 46) + (2 / 47) * (9 / 46)  
        else: #either we have no pairs or 2 pairs
            river_two_pair = ((5 * 3) / 47) * ((4 * 3) / 46) if process_matches(ranks, 2) == 2 else 0

    else: #We have the turn avialable 
        ranks = build_ranks(hand, table, 4)
        if process_matches(ranks, 4) == 1: # if we have fours, only 1 card can make a pair on the flop
            river_two_pair = (6 / 46) 
        elif process_matches(ranks, 3) == 1: #if we have 3s, 2 cards can make a pair on the flop
            river_two_pair = (9 / 46) 
        elif process_matches(ranks, 2) == 1: #if we have 1 pair, 3 cards can make a pair on the flop
            river_two_pair = (12 / 46)  
        else: #either we have no pairs or 2 pairs
            river_two_pair = 0 if process_matches(ranks, 2) == 0 else 100

    return truncate(river_two_pair)

def final_check(hand, table): 
    """This function checks if by the end of the game if there are two pairs"""
    ranks = build_ranks(hand, table, 5)
    return 100 if process_matches(ranks, 2) >= 2 else 0