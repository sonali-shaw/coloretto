import tile
from player import Player
from deck import *
import random
from stack import Stack
from rich import print as rprint
from tile import *
# from rich.console import Console
from stack import *
import sys
import pyfiglet

# pp4 = 45
# p1 = 35
# p2 = 19
# p3 = 35

class Game:

    def __init__(self, num_players=None):

        if not num_players or num_players not in [2, 3, 4]:
            num_players = self.starting_screen()

        players_to_colors = {2: 5,
                             3: 6,
                             4: 7,
                             5: 7}

        self.players = []
        self.num_players = num_players
        self.last_round = False
        self.deck = Deck(players_to_colors[num_players])
        self.stacks = []
        self.player_nums = {}

        # deal initial hands
        p_num = 1
        colors = self.unique_colors()

        for i in range(num_players):
            player = Player(colors[i])
            self.players.append(player)
            self.player_nums[player] = p_num
            p_num += 1

        # generate stacks
        if num_players == 2:
            self.stacks = [Stack(1), Stack(2), Stack(3)]
        else:
            for _ in range(num_players):
                self.stacks.append(Stack(3))

    def unique_colors(self):
        colors = []
        ref_colors = list(self.deck.colors.keys())
        for i in range(self.num_players):
            colors.append(ref_colors.pop(random.randint(0, len(ref_colors)-1)))
        return colors

    def cycle_players(self, first_player=None):

        cycled = []

        if not first_player:
            first_player = self.players[1]

        first_ind = self.players.index(first_player)

        cycled.extend(self.players[first_ind:])
        cycled.extend(self.players[:first_ind])

        self.players = cycled

    def help_menu(self):
        print("------------------------------------------")
        print("Commands: \n" )
        print("d: Draw a card. You will then be prompted to pick a stack to place this card on to. If all of the stacks"
              " are full (there is nowhere to place a drawn card), this action will be unavailable. \n")
        print("t: Take a stack. You will then be prompted to pick a stack to add to your hand. You may not take an empty"
              " stack. \n")

        print("Card colors: ")
        for key in self.deck.colors | self.deck.cards:
            if key != Card.END:
                rprint(f"{tile.to_rich[key]} {tile.txt_names[key]}")

        print("\n")

        print("q: Quit the game. \n ")

        input("Type any character to continue. ")

    def starting_screen(self):
        print(pyfiglet.figlet_format("Coloretto"))

        valid_num_players = [2, 3, 4]
        num_players = None

        print("At any point, type (q) to quit, or (h) for help.")

        while num_players not in valid_num_players:
            num_players = input("Enter a number of players (2-4) to start: ")

            try:
                num_players = int(num_players)
            except ValueError:
                pass

        print(f"{num_players} player game started!")
        print("------------------------------------------")

        return num_players

    def quit_game(self):
        valid = ['y', 'n']
        action = input("Are you sure you want to quit this game? Type (y) or (n): ")

        if action not in valid:
            self.quit_game()
        if action == 'y' or action == " ":
            sys.exit()
        elif action == 'n':
           return

    # MAKE END CARD BIGGER
    def draw(self):

        new_card = self.deck.draw()
        if new_card == Card.END:
            print(f"You drew the END card. This is the final round.")
            self.last_round = True  # adjust for all players to have a turn
            new_card = self.deck.draw()
        if new_card == Card.PLUS_TWO:
            rprint(f"You drew a {to_rich[new_card]} (plus two)")
        elif new_card == Card.WILD:
            rprint(f"You drew a {to_rich[new_card]} (wild card)")
        else:
            rprint(f"You drew a {to_rich[new_card]}")

        stack = input(f"Now, choose a stack 1-{len(self.stacks)} to add the card to: ")

        if not self.is_valid_draw_take(stack):
            print("That's not a valid option. Try again.")
            self.deck.undraw(new_card)
            self.draw()
            return

        added = self.stacks[int(stack) - 1].add(new_card)
        if not added:
            self.deck.undraw(new_card)
            print('Try again.')
            self.draw()

    # broken when you cannot take a stack, then enter return
    def take(self):

        stack = input(f"Now, choose a stack 1-{len(self.stacks)} to take: ")
        try:
            stack = int(stack)
        except ValueError:
            pass

        if not self.is_valid_draw_take(stack):
            print("Sorry, that's not a valid option. Try again.")
            return self.take()
        # a = self.stacks[stack - 1]
        if not self.stacks[stack - 1].takeable():
            print(f"Choose a different stack, this one cannot be taken.")
            return self.take()
        return self.stacks[stack-1]

    def drawable(self):
        for stack in self.stacks:
            if not stack.is_full():
                return True
        return False

    def takeable(self):
        for stack in self.stacks:
            if not stack.is_empty():
                return True
        return False

    def is_valid(self, action):
        valid = ['h', 't', 'd', 'q']
        return action in valid

    def is_valid_draw_take(self, action):
        valid = [(i + 1) for i in range(len(self.stacks))]
        try:
            action = int(action)
        except ValueError:
            pass
        return action in valid

    def next_player(self, out):
        for player in self.players:
            if player not in out:
                return player

    def round_over(self, out):
        return not len(out) < self.num_players

    def play(self):

        while not self.last_round:
            out_players = []

            while not self.round_over(out_players):

                curr_player = self.next_player(out_players)
                self.cycle_players(first_player=curr_player)

                print(f"It is Player {self.player_nums[curr_player]}'s turn!")

                self.print_game_state()

                action = input("Type d to draw, or t to take:  ")
                # print(f"action: ~{action}~")
                action_completed = False

                if not self.is_valid(action):
                    print(f"Sorry, that's not a valid choice. Please try again. ")
                if action == 'h':
                    self.help_menu()
                if action == 'q':
                    self.quit_game()
                if action == 'd':
                    if self.drawable():
                        self.draw()
                        action_completed = True
                    else:
                        print("Sorry, you can't do this action right now. Pick another one please.")
                if action == 't':
                    if self.takeable():
                        curr_player.add(self.take())
                        action_completed = True
                        out_players.append(curr_player)
                    else:
                        print("Sorry, you can't do this action right now. Pick another one please.")

                if action_completed:
                    if self.round_over(out_players):
                        self.cycle_players(first_player=curr_player)
                    else:
                        self.cycle_players()

                print("------------------------------------------")


            # reset for each round
            self.print_game_state()

            print("------------------------------------------")
            print("ROUND OVER")
            print("------------------------------------------")
            input("Press any key to continue.")
            print("------------------------------------------")

            for stack in self.stacks:
                stack.reset()



        # end of game --- DOES NOT YET ACCOUNT FOR WILD CARDS
        print("------------------------------------------")
        print("Final Scores:")
        winning = 0
        winning_player = None
        self.cycle_players(first_player=self.players[0])

        for player in self.players:
            score = player.score()
            if score > winning:
                winning = score
                winning_player = player

            print(f"Player {self.player_nums[player]}: {score}")
        print("------------------------------------------")
        print(f"Player {self.player_nums[winning_player]} wins!")
        print("------------------------------------------")

    def print_game(self):
        player = Player(Card.RED)
        spacer = SpacerTile(9, 9)
        tile1 = player.to_tile('h')
        tile2 = player.to_tile('v')
        tile3 = player.to_tile('v')
        tile3.mirror('y')
        tile4 = player.to_tile('h')

        stack1 = Stack(3)
        stack2 = Stack(3)
        stack3 = Stack(3)
        stack4 = Stack(3)

        stack1.cards.extend([Card.RED, Card.BLUE, Card.BROWN])
        stack2.cards.extend([Card.ORANGE, Card.BROWN, Card.BROWN])
        stack3.cards.extend([Card.YELLOW, Card.WILD, Card.PURPLE])
        stack4.cards.extend([Card.RED, Card.GREEN, Card.PURPLE])

        stack1_tile = stack1.to_tile()
        stack2_tile = stack2.to_tile()
        stack3_tile = stack3.to_tile()
        stack4_tile = stack4.to_tile()

        stack_tile = stack1_tile.add_left(stack2_tile).add_left(stack3_tile).add_left(stack4_tile)

        tile4.mirror('x')

        final1 = SpacerTile(4, 4).add_left(tile1).add_left(SpacerTile(4, 4))
        final2 = tile2.add_left(SpacerTile(4, 1)).add_left(stack_tile).add_left(SpacerTile(4, 1)).add_left(tile3)
        final3 = SpacerTile(4, 4).add_left(tile4).add_left(SpacerTile(4, 4))

        rprint(str(final1.add_below(SpacerTile(1, 13)).add_below(final2).add_below(SpacerTile(1, 13)).add_below(final3)))

    def make_player_tiles(self):

        # ordering of players (hands) in list
        #      0
        #  1       3
        #      2

        # create and force p_tiles to have four hands
        p_tiles = []

        if len(self.players) == 2:
            for player in self.players:
                p_tiles.append(player.to_tile('h'))

            p23_tile = SpacerTile(5, 1)
            p_tiles.insert(1, p23_tile)
            p_tiles.insert(1, p23_tile)
            return p_tiles
        elif len(self.players) > 2:
            for i, player in enumerate(self.players):
                if i % 2 == 0:
                    p_tiles.append(player.to_tile('h'))
                else:
                    p_tiles.append(player.to_tile('v'))
            if len(self.players) == 3:
                p_tiles.insert(2, SpacerTile(p_tiles[1].get_rows(), p_tiles[1].get_cols()))

        # resize opposite hands
        p_tiles[0].padding(max(p_tiles[0].get_rows(), p_tiles[2].get_rows()), max(p_tiles[0].get_cols(), p_tiles[2].get_cols()))
        p_tiles[2].padding(p_tiles[0].get_rows(), p_tiles[0].get_cols())

        p_tiles[1].padding(max(p_tiles[1].get_rows(), p_tiles[3].get_rows()), max(p_tiles[1].get_cols(), p_tiles[3].get_cols()))
        p_tiles[3].padding(p_tiles[1].get_rows(), p_tiles[1].get_cols())

        # print(f"final ptiles: {p_tiles}")
        return p_tiles

    def make_stack_tile(self):

        stack_tile = EmptyTile()
        for stack in self.stacks:
            stack_tile = stack_tile.add_left(stack.to_tile())
        return stack_tile

    def print_game_state(self):

        # create tiles
        p_tiles = self.make_player_tiles()
        stack_tile = self.make_stack_tile()

        # print(f"PTILES: {p_tiles}")

        # generate and add spacers
        h_val = stack_tile.get_rows()
        v_val = stack_tile.get_cols()

        for i, tile in enumerate(p_tiles):
            if i % 2 == 0:
                if tile.get_rows() > h_val:
                    h_val = tile.get_rows()
                if tile.get_cols() > v_val:
                    v_val = tile.get_cols()
            else:
                if tile.get_cols() > h_val:
                    h_val = tile.get_cols()
                if tile.get_rows() > v_val:
                    v_val = tile.get_rows()

        # print(f"PTILES: {p_tiles}")

        corner_spacer = SpacerTile(h_val, v_val)
        h_spacer = SpacerTile(1, corner_spacer.get_cols() * 3)

        v_spacer_cols = abs(corner_spacer.get_cols() - p_tiles[1].get_cols())
        if v_spacer_cols == 0:
            v_spacer_cols += 1
        short_v_spacer = SpacerTile(1, v_spacer_cols)

        p_tiles[1] = p_tiles[1].add_left(short_v_spacer)
        p_tiles[3] = p_tiles[3].add_left(short_v_spacer)

        # pad out the stack tile
        pad_val = max(p_tiles[0].get_cols(), p_tiles[2].get_cols()) - stack_tile.get_cols()
        stack_tile = stack_tile.padded_stack(pad_val)

        # assemble final tile
        final_row1 = corner_spacer.add_left(p_tiles[0]).add_left(corner_spacer)
        final_row2 = p_tiles[1].add_left(stack_tile).add_left(p_tiles[3].mirror('y'))
        final_row3 = corner_spacer.add_left(p_tiles[2]).add_left(corner_spacer).mirror('x')

        final = final_row1.add_below(h_spacer).add_below(final_row2).add_below(h_spacer).add_below(final_row3)
        rprint(str(final))


# game play

# num_players = 4
#
# try:
#     num_players = int(sys.argv[1])
# except:
#     print("(4 player game)")
#
# num_players = max(2,min(num_players,4))

num_players = None

game = Game(num_players)
game.play()
