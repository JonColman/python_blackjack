import random
from art import logo

'''
In this project, I will be ignoring the unlimited deck size rule, and use a finite deck, for extra challenge
As such, cards will also be drawn from the deck, affecting probabilities
'''
cards = [x for x in [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] for _ in range(8)]
random.shuffle(cards)

#Player and Dealer have a hand_obj, this will have a dict detailing cards and quantities, and their total sum
hands = [[{},0] for _ in range(2)]

def deal_initial_cards(hands: list[list[int]]) -> None:
    for _ in range(2):
        for hand in range(2):
            draw_card(hands[hand])

def draw_card(hand_obj, output_text = None) -> bool:
    card = cards.pop()
    if output_text:
        print(f"{output_text} drew a {card} card!\n\n" if card < 11 else f"{output_text} drew an ace!\n\n")
    if not hand_obj[0].get(card):
        hand_obj[0][card] = 1
    else:
        hand_obj[0][card] += 1
    hand_obj[1] += card

    #Recalculate ace to equal 1, not 11, until <= 21 constraint is satisfied
    if hand_obj[1] > 21 and hand_obj[0].get(11):
        hand_obj[1] -= 10   #Set ace value from 11 to 1
        if not hand_obj[0].get(1):
            hand_obj[0][1] = 1
        else:
            hand_obj[0][1] += 1
        hand_obj[0][11] -= 1
    return hand_obj[1] <= 21

def hand_to_list(hand_obj) -> str:
    res = []
    for value, quantity in hand_obj[0].items():
        for _ in range(quantity):
            res.append(str(value) if value != 1 and value != 11 else 'A')
    return f"[{", ".join(res)}]" #"Connect" each element in list by ", "

def show_one_card(hand_obj):
    return list(hand_obj[0].items())[0][0]

def player_turn(hand_obj, comp_hand_obj) -> bool:
    playable = True
    while playable:
        print(f"Your current hand {hand_to_list(hand_obj)} totals to: {hand_obj[1]}")
        print(f"The dealer has a {show_one_card(comp_hand_obj)}")
        if hand_obj[1] < 21:
            choice = True if input("Would you like to Stand or Hit: ").lower() == "hit" else False
            if choice:
                draw_card(hand_obj, output_text = "You")
            else:
                playable = False
        else:
            playable = False
    blackjack_check(hand_obj, "You")
    return hand_obj[1] <= 21

def return_cards_to_deck(hands) -> None:
    for hand_obj in hands:
        hand_obj[1] = 0
        for value, quantity in hand_obj[0].items():
            if value == 1:  #Ensure aces are restored to 11 value when returned to deck
                cards.extend([11]*quantity)
            else:
                cards.extend([value]*quantity)
        hand_obj[0] = {}

def blackjack_check(hand_obj, text) -> None:
    if hand_obj[1] == 21 and sum(hand_obj[0].values()) == 2:
        print(f"{text} got a blackjack!")


def ai_turn(hand_obj) -> bool:
    print(f"Dealer currently has: {hand_to_list(hand_obj)}")
    while hand_obj[1] < 17:
        draw_card(hand_obj, output_text = "Dealer")
        print(f"Dealer currently has: {hand_to_list(hand_obj)}")
    blackjack_check(hand_obj, "Dealer")
    return hand_obj[1] <= 21

def play() -> None:
    deal_initial_cards(hands)
    if player_turn(hands[1], hands[0]):
        if ai_turn(hands[0]):
            print(f"You have: {hands[1][1]} and the dealer has {hands[0][1]}...")
            if hands[1][1] != hands[0][1]:
                print(f"{"You" if hands[1][1] > hands[0][1] else "Dealer"} wins!")
            else:
                print(f"Both you and dealer have the same score! It's a push!")
        else:
            print(f"Dealer busts! You win!")
    else:
        print(f"Unfortunately, you're busted. Dealer wins!")
    return_cards_to_deck(hands)

cycle = True
while cycle:
    print(f"{"\n"*20}{logo}{"\n"*2}")
    play()
    cycle = input("Good game! Would you like to play again? Y or N: ").upper() == "Y"