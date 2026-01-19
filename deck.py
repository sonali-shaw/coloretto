import random
from enum import Enum


class Card(Enum):
    RED = 1
    ORANGE = 2
    YELLOW = 3
    GREEN = 4
    BLUE = 5
    PURPLE = 6
    BROWN = 7
    PLUS_TWO = 8
    WILD = 9
    END = 10
    STACK = 11
    STACK_TAKEN = 12

class Deck:

    def __init__(self, num_colors):

        self.colors = {Card.RED: 9,
                       Card.ORANGE: 9,
                       Card.YELLOW: 9,
                       Card.GREEN: 9,
                       Card.BLUE: 9,
                        }

        if num_colors > 5:
            self.colors[Card.PURPLE] = 9
        if num_colors > 6:
            self.colors[Card.BROWN] = 9

        # self.cards = {Card.PLUS_TWO: 10,
        #               Card.WILD: 2,
        #               Card.END: 1
        #               }

        self.cards = {Card.PLUS_TWO: 10,
                      Card.WILD: 0,
                      Card.END: 1
                      }

        self.deck = []
        for key, value in list(self.colors.items())[:num_colors+1]:
            self.deck.extend([key] * value)

        self.deck.extend([Card.WILD] * self.cards[Card.WILD])
        self.deck.extend([Card.PLUS_TWO] * self.cards[Card.PLUS_TWO])

        self.shuffle()
        self.deck.insert(len(self.deck)-16, Card.END)

    # implement later
    def shuffle(self):
        for _ in range(7):
            random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop(0)

    def undraw(self, card):
        self.deck.insert(0, card)
