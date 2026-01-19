import random

from deck import Card
from tile import *

class Player():

    def __init__(self, intial_card, random_hand=False):
        self.hand = {Card.RED: 0,
                     Card.ORANGE: 0,
                     Card.YELLOW: 0,
                     Card.GREEN: 0,
                     Card.BLUE: 0,
                     Card.PURPLE: 0,
                     Card.BROWN: 0,
                     Card.PLUS_TWO: 0,
                     Card.WILD: 0
                     }

        if random_hand:
            for key in self.hand:
                self.hand[key] += random.randint(0, 4)

        self.hand[intial_card] += 1

        self.out = False

    def add(self, stack):
        cards = stack.take()
        for card in cards:
            if card not in self.hand:
                self.hand[card] = 0
            self.hand[card] += 1
        self.out = True

    # DOESNT WORK AT ALL
    def score(self):

        # deal with plus twos
        num_plus_two = self.hand[Card.PLUS_TWO]
        self.hand[Card.PLUS_TWO] = 0

        # deal with wilds right now -- just incase
        self.hand[Card.WILD] = 0

        # score each set
        color_scores = []
        for set in self.hand.values():
            if set > 6:
                set = 6
            color_scores.append(set * (set + 1) / 2)

        color_scores.sort()
        color_scores.reverse()

        # add / subtract the scores
        final_score = sum(color_scores[:3]) - sum(color_scores[3:]) + num_plus_two * 2

        return int(final_score)

    def to_tile(self, orientation):

        final_tile = EmptyTile()

        if orientation == 'h':
            for card_type, amount in self.hand.items():
                if amount > 0:
                    card_tile = Tile([[card_type] for _ in range(amount)])
                else:
                    card_tile = EmptyTile()
                final_tile = final_tile.add_left(card_tile)

        if orientation == 'v':
            for card_type, amount in self.hand.items():
                if amount > 0:
                    card_tile = Tile([[card_type for _ in range(amount)]])
                else:
                    card_tile = EmptyTile()
                final_tile = final_tile.add_below(card_tile)

        return final_tile






