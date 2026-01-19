from deck import Card

to_rich = {Card.RED: "[red1]█[/red1]",
                        Card.ORANGE: "[dark_orange3]█[/dark_orange3]",
                        Card.YELLOW: "[bright_yellow]█[/bright_yellow]",
                        Card.GREEN: "[green4]█[/green4]",
                        Card.BLUE: "[dodger_blue2]█[/dodger_blue2]",
                        Card.PURPLE: "[purple4]█[/purple4]",
                        Card.BROWN: "[orange4]█[/orange4]",
                        Card.PLUS_TWO: "[dark_slate_gray1]█[/dark_slate_gray1]",
                        Card.WILD: "[magenta2]█[/magenta2]",
                        Card.END: "FIND COLOR",
                        Card.STACK:  "[grey66]▬[/grey66]",
                        Card.STACK_TAKEN: "[silver]▬[/silver]"
                        }

txt_names = {Card.RED: "Red Card",
                        Card.ORANGE: "Orange Card",
                        Card.YELLOW: "Yellow Card",
                        Card.GREEN: "Green Card",
                        Card.BLUE: "Blue Card",
                        Card.PURPLE: "Purple Card",
                        Card.BROWN: "Brown Card",
                        Card.PLUS_TWO: "+2 Card",
                        Card.WILD: "Wild Card",
                        }

class Tile:

    def __init__(self, tile):
        assert len(tile) >= 1

        self.tile = tile

        self.to_rich = {Card.RED: "[red1]█[/red1]",
                        Card.ORANGE: "[dark_orange3]█[/dark_orange3]",
                        Card.YELLOW: "[bright_yellow]█[/bright_yellow]",
                        Card.GREEN: "[green4]█[/green4]",
                        Card.BLUE: "[dodger_blue2]█[/dodger_blue2]",
                        Card.PURPLE: "[purple4]█[/purple4]",
                        Card.BROWN: "[orange4]█[/orange4]",
                        Card.PLUS_TWO: "[dark_slate_gray1]█[/dark_slate_gray1]",
                        Card.WILD: "[magenta2]█[/magenta2]",
                        Card.END: "FIND COLOR",
                        Card.STACK:  "[grey66]▬[/grey66]"
                        }

        # only for debugging purposes
        self.to_rich2 = {Card.RED: "red",
                         Card.ORANGE: "orange",
                         Card.YELLOW: "yellow",
                         Card.GREEN: "green",
                         Card.BLUE: "blue",
                         Card.PURPLE: "purple",
                         Card.BROWN: "brown",
                         Card.PLUS_TWO: "plus_two",
                         Card.WILD: "wild",
                         Card.END: "FIND COLOR",
                         Card.STACK: "grey"
                         }

    def add_left(self, other):

        if other.is_empty():
            return self

        max_rows = max(self.get_rows(), other.get_rows())

        self.padding(max_rows, self.get_cols())
        other.padding(max_rows, other.get_cols())

        new_tile = []
        for i in range(max_rows):
            row = []
            row.extend(self.tile[i])
            row.extend(other.tile[i])
            new_tile.append(row)
        return Tile(new_tile)

    def add_below(self, other):

        if other.is_empty():
            return self

        max_cols = max(self.get_cols(), other.get_cols())

        self.padding(self.get_rows(), max_cols)
        other.padding(other.get_rows(), max_cols)

        new_tile = self.tile[:]
        new_tile.extend(other.tile)
        return Tile(new_tile)

    def padding(self, rows, columns):
        for row in self.tile:
            if len(row) < columns:
                row.extend([None for _ in range(columns - len(row))])
        if len(self.tile) < rows:
            self.tile.extend([[None for _ in range(columns)] for _ in range(rows - len(self.tile))])

    def get_rows(self):
        return len(self.tile)

    def get_cols(self):
        return len(self.tile[0])

    def is_empty(self):
        return False

    def mirror(self, axis):
        flipped = []

        if axis == 'y':
            for row in self.tile:
                flipped.append(row[::-1])
        if axis == 'x':
            flipped = self.tile[::-1]

        return Tile(flipped)

    def padded_stack(self, cols):
        if cols % 2 != 0:
            cols += 1
        v_spacer = SpacerTile(self.get_rows(), cols // 2)

        return v_spacer.add_left(self).add_left(v_spacer)

    def __repr__(self):
        final_str = ""
        for row in self.tile:
            final_str += str(row) + "\n"
        return final_str[:-1]

    def __str__(self):
        final_str = ""
        for row in self.tile:
            for element in row:
                if element is None:
                    final_str += " "
                else:
                    final_str += self.to_rich[element]
                final_str += " "
            final_str += "\n"
        return final_str


class EmptyTile:

    def __init__(self):
        pass

    def add_left(self, other):
        return other

    def add_below(self, other):
        return other

    def is_empty(self):
        return True

class SpacerTile:

    def __init__(self, rows, columns):
        row = [None for _ in range(columns)]
        self.tile_obj = Tile([row[::] for _ in range(rows)])
        self.tile = self.tile_obj.tile

    def add_left(self, other):
        return self.tile_obj.add_left(other)

    def add_below(self, other):
        return self.tile_obj.tile.add_below(other)

    def padding(self, rows, columns):
        return self.tile_obj.padding(rows, columns)

    def is_empty(self):
        return False

    def get_rows(self):
        return self.tile_obj.get_rows()

    def get_cols(self):
        return self.tile_obj.get_cols()

    def mirror(self, axis):
        return self.tile_obj

