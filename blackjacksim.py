import math
import random
import sys
import matplotlib.pyplot as plt
import numpy

def blackjacksim(n):
    #Play n hands of blackjack.
    #Return array of results.
    
    round_results = []
    for n in range(n):
        round_results.append(blackjack_hand())

    return round_results

#Plays a hand of blackjack
#Returns balance
def blackjack_hand():

    bet = 10
    bet1 = bet
    bet2 = bet

    P1 = []
    P1.append(deal())       #Player's hand
    P1.append(deal())

    P2 = []                 #Player's second hand incase of split

    D = []                  #Dealer's hand
    D.append(deal())         
    D.append(deal())

    #Check if you can split hand
    if (P1[0] == P1[1]):
        #Get split strategy
        split = pair(P1[0],D[0])
    else:
        #Else set split to false
        split = 0
    #Check if you should split hand, if true: give each hand a new card
    if split:
        P1 = [P1[0], deal()]
        P2 = [P1[0], deal()]

    #Play player's hand
    P1, bet1 = playHand(P1, D, bet1)
    #If split, play second hand
    if split:
        P2, bet2 = playHand(P2, D, bet2)

    #Play dealer's hand
    while value(D) <= 16:
        D.append(deal())

    #Payoff
    gameBalance = payOff(P1, D, split, bet1)
    if split:
        gameBalance += payOff(P2, D, split, bet2)

    return gameBalance

#Deal returns a random card value, face = 10
def deal():
    #Simulate continous shuffling machine with infinite deck.
    card = random.randint(1,13)
    if card > 10:
        card = 10
    return card

def value(h):
    #Evaluate hand
    #If a card is the value of 1(ace) and the sum of hand to be equal or less to 11
    #then return the sum of the hand + 10
    v = sum(h)
    if 1 in h and v <= 11:
        v += 10
 
    return v

def playHand(P, D, bet):
    #Play Player's hand

    while value(P) < 21:
        # 0 = stand
        # 1 = hit
        # 2 = double down

        if 1 in P and sum(P) <= 10:
            strategy = soft(value(P)-11, D[0])
        else:
            strategy = hard(value(P), D[0])
        if len(P) > 2 and strategy == 2:
            strategy = 1

        #Stand
        if strategy == 0:
            return (P, bet)
        #Hit
        elif strategy == 1:
            P.append(deal())    #Add card
            return (P, bet)
        #Double down
        elif strategy == 2:
            P.append(deal())    #Add card
            bet = 2*bet         #Double the bet
            return (P, bet)
    
    return (P, bet)

def payOff(P,D, split, bet):
    valP = value(P)
    valD = value(D)
    if valP == 21 and\
        len(P) == 2 and\
        not (valD == 21 and len(D) == 2) and\
        not split:
        s = 1.5*bet
    #Player bust
    elif valP > 21:
        s = -bet
    #Dealer bust
    elif valD > 21:
        s = bet
    #Dealer higher value
    elif valD > valP:
        s = -bet
    #Player higher value
    elif valD < valP:
        s = bet
    #Draw
    else:
        s = 0

    return s

def hard(P, D):
    #Strategy for hands without aces-
    #Strategy = hard(player's_total, dealer's_upcard)

    # 0 = stand
    # 1 = hit
    # 2 = double down

                       #1,2,3,4,5,6,7,8,9,10
    HARD_MATRIX = []
    HARD_MATRIX.append([1,1,1,1,1,1,1,1,1,1])   #1
    HARD_MATRIX.append([1,1,1,1,1,1,1,1,1,1])   #2
    HARD_MATRIX.append([1,1,1,1,1,1,1,1,1,1])   #3
    HARD_MATRIX.append([1,1,1,1,1,1,1,1,1,1])   #4
    HARD_MATRIX.append([1,1,1,1,1,1,1,1,1,1])   #5
    HARD_MATRIX.append([1,1,1,1,1,1,1,1,1,1])   #6
    HARD_MATRIX.append([1,1,1,1,1,1,1,1,1,1])   #7
    HARD_MATRIX.append([2,2,2,2,2,1,1,1,1,1])   #8
    HARD_MATRIX.append([2,2,2,2,2,2,2,2,1,1])   #9
    HARD_MATRIX.append([2,2,2,2,2,2,2,2,2,2])   #10
    HARD_MATRIX.append([1,1,0,0,0,1,1,1,1,1])   #11
    HARD_MATRIX.append([0,0,0,0,0,1,1,1,1,1])   #12
    HARD_MATRIX.append([0,0,0,0,0,1,1,1,1,1])   #13
    HARD_MATRIX.append([0,0,0,0,0,1,1,1,1,1])   #14
    HARD_MATRIX.append([0,0,0,0,0,1,1,1,1,1])   #15 
    HARD_MATRIX.append([0,0,0,0,0,0,0,0,0,0])   #16
    HARD_MATRIX.append([0,0,0,0,0,0,0,0,0,0])   #17
    HARD_MATRIX.append([0,0,0,0,0,0,0,0,0,0])   #18
    HARD_MATRIX.append([0,0,0,0,0,0,0,0,0,0])   #19 
    HARD_MATRIX.append([0,0,0,0,0,0,0,0,0,0])   #20
    HARD_MATRIX.append([0,0,0,0,0,0,0,0,0,0])   #21

    #Adjusting from matlab matrix to python matrix
    P -= 2
    D -= 2
    #print("Hard: P:" , P , " D: ", D)
    return HARD_MATRIX[P][D]

def soft(P, D):
    #Strategy array for hands with aces.
    #Strategy = soft(player's_total, dealer's_upcard)

    # 0 = stand
    # 1 = hit
    # 2 = double down
                       #1,2,3,4,5,6,7,8,9,10
    SOFT_MATRIX = []
    SOFT_MATRIX.append([1,1,2,2,2,1,1,1,1,1])   #1
    SOFT_MATRIX.append([1,1,2,2,2,1,1,1,1,1])   #2
    SOFT_MATRIX.append([1,1,2,2,2,1,1,1,1,1])   #3
    SOFT_MATRIX.append([1,1,2,2,2,1,1,1,1,1])   #4
    SOFT_MATRIX.append([2,2,2,2,2,1,1,1,1,1])   #5
    SOFT_MATRIX.append([0,2,2,2,2,0,0,1,1,0])   #6
    SOFT_MATRIX.append([0,0,0,0,0,0,0,0,0,0])   #7
    SOFT_MATRIX.append([0,0,0,0,0,0,0,0,0,0])   #8
    SOFT_MATRIX.append([0,0,0,0,0,0,0,0,0,0])   #9

    P -= 2
    D -= 2
    #print("Soft: P:" , P , " D: ", D)
    return SOFT_MATRIX[P][D]

def pair(P, D):
    # Strategy for splitting pairs
    # strategy = pair(paired_card, dealer's_upcard)

    # 0 = keep pair
    # 1 = split pair

    PAIR_MATRIX = []
    PAIR_MATRIX.append([1,1,1,1,1,1,0,0,0,0])
    PAIR_MATRIX.append([1,1,1,1,1,1,0,0,0,0])
    PAIR_MATRIX.append([0,0,0,1,0,0,0,0,0,0])
    PAIR_MATRIX.append([0,0,0,0,0,0,0,0,0,0])
    PAIR_MATRIX.append([1,1,1,1,1,1,0,0,0,0])
    PAIR_MATRIX.append([1,1,1,1,1,1,1,0,0,0])
    PAIR_MATRIX.append([1,1,1,1,1,1,1,1,1,1])
    PAIR_MATRIX.append([1,1,1,1,1,1,1,1,0,0])
    PAIR_MATRIX.append([0,0,0,0,0,0,0,0,0,0])
    PAIR_MATRIX.append([1,1,1,1,1,1,1,1,1,1])

    P -= 2
    D -= 2
    #print("Pair: P:" , P , " D: ", D)
    return PAIR_MATRIX[P][D]

if not len(sys.argv) == 2:
    print("Missing game amount input.")
    print("Try: python blackjacksim.py 1000")
else:
    round_results = blackjacksim(int(sys.argv[1]))
    totalGames = int(sys.argv[1])
    round_results_accumulated = numpy.cumsum(round_results)
    print("---------------------------------")
    print("Total balance: " , sum(round_results))
    print("Total games: ", totalGames)

    plt.figure()
    plt.grid()
    plt.plot(round_results_accumulated)
    plt.show()