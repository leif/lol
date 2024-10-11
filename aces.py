"the paradox of the second ace"

import sys
from random import shuffle

text = {
    (52, 4): f"""
Paraphrasing from http://fgrieu.free.fr/histnse/CESG_Research_Report_No_3007_1.pdf :

Two cards have been dealt from a standard 52-card deck, and the problem is to
determine the probability that both are aces given one of two pieces of
information. The information can be either:
    * At least one of the cards in the hand is an ace
    * The hand includes the Ace of Spades (or any specific ace)

There are 52*51/2 ({52*51//2}) possible two-card hands and 48*47/2 ({48*47//2})
possible hands with no aces, so, the number of possible hands with at least one
ace is the difference between these ({(52*51//2)-(48*47//2)}).

There are six (3+2+1) ways of holding two aces, so, the odds that a two-card
hand containing at least one ace also contains another ace is 6/198, which
reduces to 1/33 ({1/33}).

There are 51 ways of holding two cards where one is the Ace of Spades, and 3
ways of holding two aces where one of them is the Ace of Spades. Therefore the
probability of a 2-card hand containing two aces, given that it contains the
Ace of Spaces, is 3/51 or 1/17 ({1/17}).

It is counter-intuitive that a hand known to contain a specific ace is more
likely to contain two aces than a hand known to contain "at least one ace" is,
so, lets simulate it to confirm it.
"""
}


def draw(n, deck_size):
    deck = list(range(deck_size))
    shuffle(deck)
    return deck[:n]


def aces_paradox(C=100_000, deck_size=52, ace_count=4):
    """
    confirming the "aces" paradox, aka "paradox of the second ace"
    """
    print(text.get((deck_size, ace_count), ""))
    at_least_one, two_aces, spades, spades_and_another = 0, 0, 0, 0
    for i in range(C):
        hand = draw(2, deck_size)
        aces = [card < ace_count for card in hand]
        if any(aces):
            at_least_one += 1
        if all(aces):
            two_aces += 1
        if 0 in hand:
            spades += 1
            if all(aces):
                spades_and_another += 1
        if spades > 0:
            print(
                f"{i/C*100:.0f}% dealt {i+1} hands; odds if any ace: {two_aces/at_least_one:.4f}; odds if specific ace: {spades_and_another/spades:.4f}\r",
                end="",
            )
    print(
        f"""

dealt a 2-card hand from a deck of {deck_size}, containing {ace_count} aces, {C} times

    {at_least_one} had at least one ace, {two_aces} had two aces
    odds of at least one ace: {at_least_one/C}
    odds of two aces: {two_aces/C}
    odds of two aces, given one: {two_aces/at_least_one} <-----

    {spades} had ace of spades, and {spades_and_another} of those had another ace
    odds of ace of spades: {spades/C}
    odds of two aces, given one is ace of spades: {spades_and_another/spades} <-----

    you can run this again and supply different arguments for number of
    iterations, cards, and aces. the paradox becomes easier to understand if
    you think about it with a deck of 3 or 4 cards containing only two aces.

    eg:
        python {sys.argv[0]} 100_000 3 2
        python {sys.argv[0]} 100_000 4 2
"""
    )


text.update({
    (3, 2): """
In the 3-card deck with 2 aces, there is always 'at least one ace' in the hand,
so this information doesn't affect the probability at all. Without any useful
information about what is held, the probability of a hand with two aces is 1/3,
because that is the probability that the non-ace will be the card which was not
selected when a 2-card hand is drawn from a 3-card deck. However, if it is
known that a specific ace is in the hand, then the probability of the other ace
also being held becomes 1/2 because there are two equally likely cards which
could be the other card - the ace and the non-ace.
""",
    (4, 2): """
In the 4-card deck with 2 aces, there are six possible hands, one of which
contains two aces and one of which contains zero aces. So, absent any knowledge
of the contents of the hand, the odds of the hand containing two aces is 1/6.
Knowledge that the hand contains at least one ace elimates the possibility of
the hand with no aces, making the odds of two aces 1/5. Knowledge that the hand
contains a specific ace means that the other card in the hand must be one of
the 3 other cards, of which one is an ace, so the probability of two aces
becomes 1/3. Another way to think about it is that knowledge that the hand
contains a specific ace has eliminated the possibility of the three of the six
possible hands which do not contain that specific ace.
""",
})

if __name__ == "__main__":
    aces_paradox(*map(int, sys.argv[1:]))
