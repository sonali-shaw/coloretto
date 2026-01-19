from tile import *
from player import *
from deck import *
from rich import print as rprint
import pyfiglet

class Stack:

    def __init__(self, slots):
        self.slots = slots + 1
        self.cards = [Card.STACK]
        self.taken = False

    def add(self, card):
        if len(self.cards) >= self.slots:
            print("Stack is full, try again.")
            return False
        elif self.taken:
            print("Sorry, this stack is out of play because it has been taken already.")
            return False
        else:
            self.cards.append(card)
            return True

    def take(self):
        if self.taken:
            print("Sorry, this stack has been taken already.")
            return []
        elif len(self.cards) == 1:
            print("Sorry, you can't take this stack, it's empty.")
            return []
        else:
            cards = self.cards[:]
            self.taken = True
            self.cards = [Card.STACK, Card.STACK]
            return cards[1:]

    def takeable(self):
        return not(self.taken or len(self.cards) == 1)

    def reset(self):
        self.taken = False
        self.cards = [Card.STACK]

    def to_tile(self):
        tile_list = []
        for card in self.cards:
            tile_list.append([card])
        return Tile(tile_list)

    def is_full(self):
        return len(self.cards) == self.slots

    def is_empty(self):
        return len(self.cards) == 1

    def clear(self):
        self.cards = [Card.STACK]

    def __str__(self):
        return [Card.STACK] + self.cards