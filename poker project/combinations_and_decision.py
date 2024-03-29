import random
import operator

def return_highest_card(list_of_cards):
    return max(list_of_cards, key=operator.attrgetter("number_value"))


def return_lowest_card(list_of_cards):
    return min(list_of_cards, key=operator.attrgetter("number_value"))




def combinations_ranking():
    #lst=[card_1,card_2,card_3,card_4,card_5,card_6,card_7]
    D={"High Card":0, "Pair":1 , "two pair":2, "Three of a kind":3, "Straight":4, "Flush":5, "Full house":6,\
    "Four of a kind":7, "Straight flush":8 , "ROYAL FLUSH":9}
    return D
 




def high_card(list_of_cards):
    higher_card_rank = return_highest_card(list_of_cards)
    return ("High Card", higher_card_rank)


def same_rank_combinations(list_of_cards):
    D={}
    for m in list_of_cards:
        D[m.rank]=m
    lst=[]
    for n in list_of_cards:
        lst.append(n.rank)
    combinations_list=[]
    tokens = 0
    double_value = None
    triple_value = None
    A = []  # list of pairs
    B = []  # list of triples
    for card in lst:
        if lst.count(card)==2:
            if card not in A:
                A.append(card)
        if lst.count(card) == 3:
            if card not in B:
                B.append(card)
        if lst.count(card)==4:
            combinations_list.append(("Four of a kind",[card]))
            break
    if len(A)==3:
          A.remove(return_lowest_card([D[A[0]],D[A[1]],D[A[2]]]).rank)
    if len(A)==2:
        combinations_list.append(("two pair",sorted([A[0],A[1]], reverse= True)))
        tokens=2
    elif len(A)==1:
        combinations_list.append(("Pair",[A[0]]))
        tokens=1
    if len(B)==2:
        triple_value=return_highest_card([D[B[0]],D[B[1]]])
        B.remove(triple_value.rank)
        double_value=B[0]
    elif len(B)==1:
        triple_value=B[0]
        if tokens==2:
            double_value= return_highest_card([D[A[0]],D[A[1]]]).rank
        elif tokens==1:
            double_value= A[0]
        elif tokens==0:
            combinations_list.append(("Three of a kind",[B[0]]))
    if double_value is not None:
        combinations_list.append(("Full house",[triple_value,double_value]))
    if len(combinations_list) == 0:
        return
    E={}
    for t in combinations_list:
        E[t[0]]=t[1]
    a= max(E.keys(),key=combinations_ranking().get)
    return a,E[a]
#to show rest of the code for same_rank_combintaion press on arrow

def cards_same_suit(list_of_cards): #function for flush
    flush = False
    C=[]
    for j in list_of_cards:
        a= sum(t.suit == j.suit for t in list_of_cards)
        #print (a)
        if a >= 5:
            C.append(j)
            if len(C) >= 5:
                flush = True
    if flush is False:
        return 
    return C

def flush(list_of_cards):
    C = cards_same_suit(list_of_cards)
    if C is None:
        return 
    while len(C)>5:
        min_object= C[0]
        for i in range(1,len(C)):
            if min_object != return_lowest_card([C[i],min_object]):
                min_object=C[i]
        C.remove(min_object)
    C = sorted(C, key=operator.attrgetter("number_value"), reverse= True)
    flush_cards_values = []
    for n in C:
        flush_cards_values.append(n.rank)
    return ("Flush", flush_cards_values)

def straight(list_of_cards):
    straight = False
    L= list_of_cards
    K= []
    for j in L:
        K.append(j.number_value)
    if 14 in K:
        K.append(1)  # in case Ace is used as 1 
    M = sorted(set(K))
    for i in range(len(K)- 4):
        if M[i+1]-M[i]==1 and M[i+2]-M[i+1]==1 and M[i+3]-M[i+2]==1 and M[i+4]-M[i+3]==1:
            straight = True
            highest_card_index = i+4
    if not straight:
        return 
    straight_cards = M[highest_card_index -4 : highest_card_index +1]
    straight_cards_values = []
    for n in straight_cards:
        straight_cards_values.append(cards_values_reversed()[n])
    return ("Straight",straight_cards_values)

def straight_flush_and_royal_flush(list_of_cards): #also includes flush and straight.
    A= cards_same_suit(list_of_cards) #first we check if there is a flush, if there
    if A is None: #isn't then there can't be straight F or royal F,and all thats left to check is if there is a straight.
        return straight(list_of_cards)
    B= straight(A)# now we check if there is a straight from the flush cards we got,if there
    if B is None:#isn't then there can't be straight F or royal F,and all thats left to return the flush.
        return flush(list_of_cards)# yes, there is some code duplication here.
    #there is no point to check if there is a regular straight because flush beats straight.
    if 10 in B[1] and "Jack" in B[1] and "Queen" in B[1] and "King" in B[1] and "Ace" in B[1]:
        return "ROYAL FLUSH" # we check the option for royal flush
    else:
        return ("Straight flush", B[1])




#######combinations and dscision which combination is stronger ###################################################

def strongest_combination(list_of_cards):
    option_1= straight_flush_and_royal_flush(list_of_cards)
    option_2= same_rank_combinations(list_of_cards)
    #print(option_1, option_2)
    if option_1 is None and option_2 is None:
        return high_card(list_of_cards)
    if option_1 is None:
        return option_2
    elif option_2 is None:
        return option_1 
    if option_1 == "ROYAL FLUSH" or option_2 == "ROYAL FLUSH":
        return "ROYAL FLUSH"
    if combinations_ranking()[option_1[0]] > combinations_ranking()[option_2[0]]:
        return option_1
    else:
        return option_2

def pair_clash(pair_1,pair_2): #the arguments here will be best_hand_1 and best_hand_2
    #return pair_1,pair_2
    if cards_values()[pair_1[1][0]] > cards_values()[pair_2[1][0]]:
        return pair_1
    elif cards_values()[pair_2[1][0]] > cards_values()[pair_1[1][0]]:
        return pair_2
    else:
        return "draw"

def two_pair_clash(two_pair_1, two_pair_2): #same format as pair_clash
    first_pair_comparison = pair_clash(two_pair_1, two_pair_2)
    if first_pair_comparison != "draw":
        return first_pair_comparison
    else:
        if cards_values()[two_pair_1[1][1]] > cards_values()[two_pair_2[1][1]]:
            return two_pair_1
        elif cards_values()[two_pair_2[1][1]] > cards_values()[two_pair_1[1][1]]:
            return two_pair_2
        else:
            return "draw"

def Three_of_a_kind_clash(Three_of_a_kind_1, Three_of_a_kind_2): #same format as pair_clash
    return pair_clash(Three_of_a_kind_1, Three_of_a_kind_2)
    
def straight_clash(straight_1 , straight_2):
    if cards_values()[straight_1[1][-1]] > cards_values()[straight_2[1][-1]]:
        return straight_1
    elif cards_values()[straight_2[1][-1]] > cards_values()[straight_1[1][-1]]:
        return straight_2
    else:
        return "DRAW!"

def flush_clash(flush_1, flush_2):
    #return flush_1, flush_2
    for i in range(len(flush_1[1])):
        cur_high_card_1 = cards_values()[flush_1[1][i]]
        cur_high_card_2 = cards_values()[flush_2[1][i]]
        if cur_high_card_1 != cur_high_card_2: 
            if cur_high_card_1 > cur_high_card_2:
                return flush_1
            else:
                return flush_2
    return "DRAW!"

def full_house_clash(full_house_1, full_house_2):
    result = two_pair_clash(full_house_1, full_house_2)
    if result != "draw":
        return result
    else:
        return "DRAW!"

def four_of_a_kind_clash(four_of_a_kind_1, four_of_a_kind_2):
    return pair_clash(four_of_a_kind_1, four_of_a_kind_2)

def straight_flush_clash(straight_flush_1, straight_flush_2):
    return straight_clash(straight_flush_1, straight_flush_2)


def high_card_clash(high_card_1, high_card_2):
    sorted_1 = sorted(high_card_1, key=cards_values().get, reverse= True)
    sorted_2 = sorted(high_card_2, key=cards_values().get, reverse= True)
    for i in range(5):
        cur_high_card_1 = cards_values()[sorted_1[i]]
        cur_high_card_2 = cards_values()[sorted_2[i]]
        if cur_high_card_1 != cur_high_card_2: 
            if cur_high_card_1 > cur_high_card_2:
                return ("High Card" , sorted_1[i])
            else:
                return ("High Card" , sorted_2[i])
    return "DRAW!"



def strongest_hand(hand_1,hand_2):
    draw = False
    best_hand_1 = strongest_combination(hand_1)
    best_hand_2 = strongest_combination(hand_2)
    #return best_hand_1,best_hand_2
    if best_hand_1 == "ROYAL FLUSH" and best_hand_2 == "ROYAL FLUSH":
        return "DRAW"
    if best_hand_1 == "ROYAL FLUSH" or best_hand_2 == "ROYAL FLUSH":
        return "ROYAL FLUSH"

    if combinations_ranking()[best_hand_1[0]] > combinations_ranking()[best_hand_2[0]]: # to fix this so it will use the card_values dict for the comparison
        #print("lalala")
        return best_hand_1
    elif combinations_ranking()[best_hand_2[0]] > combinations_ranking()[best_hand_1[0]]:
        return best_hand_2
    else:
        if best_hand_1[0] == "High Card":
            print("lalalalal")
            lst_1 = []
            lst_2 = []
            for i in hand_1:
                lst_1.append(i.rank)
            for j in hand_2:
                lst_2.append(j.rank)
            return high_card_clash(lst_1, lst_2)

        #print("yoyo")
        if best_hand_1[0] == "Pair": # later on make one function for all 3 cases
            result = pair_clash(best_hand_1,best_hand_2)
            if result != "draw":
                return result
            else:
                draw = True
        elif best_hand_1[0] == "two pair":
            result = two_pair_clash(best_hand_1,best_hand_2)
            if result != "draw":
                return result
            else:
                draw = True

        elif best_hand_1[0] == "Three of a kind":
            result = Three_of_a_kind_clash(best_hand_1,best_hand_2)
            if result != "draw":
                return result
            else:
                draw = True

        elif best_hand_1[0] == "Four of a kind":
            result = four_of_a_kind_clash(best_hand_1,best_hand_2)
            if result != "draw":
                return result
            else:
                draw = True
        
        if best_hand_1[0] == "Pair" or best_hand_1[0] == "two pair" or best_hand_1[0] == "Three of a kind"\
            or best_hand_1[0] == "Four of a kind": 
            if draw is True:
                Kicker_1 = Kicker(hand_1,best_hand_1[1])
                Kicker_2 = Kicker(hand_2,best_hand_2[1])
                if Kicker_1.number_value != Kicker_2.number_value:
                    higher_kicker = return_highest_card([Kicker_1,Kicker_2])
                    return [best_hand_1, "kicker: " + str(higher_kicker.rank)] # couldeve written best_hand_2 as well
                else:
                    return "DRAW!"


        if best_hand_1[0] == "Straight":
            return straight_clash(best_hand_1, best_hand_2)
        
        if best_hand_1[0] == "Flush": 
            return flush_clash(best_hand_1, best_hand_2)
        
        if best_hand_1[0] == "Full house":
            return full_house_clash(best_hand_1, best_hand_2)

        #if best_hand_1[0] == "Four of a kind":
            #return four_of_a_kind_clash(best_hand_1, best_hand_2)
         
        if best_hand_1[0] == "Straight flush":
            return straight_flush_clash(best_hand_1, best_hand_2)

    

def Kicker(hand, combination):
    not_in_combination = [card for card in hand if card.rank not in combination]
    Kicker = return_highest_card(not_in_combination)
    return Kicker

#######combinations and descision which combination is stronger ##################################################3

