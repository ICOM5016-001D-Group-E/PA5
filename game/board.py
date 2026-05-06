import random


class Board:
    # Represents the domino chain on the table.

    def __init__(self):
        self.chain = []        # list of dominoes in order they were played
        self.left_end = None   # open number on the left side of the chain
        self.right_end = None  # open number on the right side of the chain

    def is_empty(self):
        # True if no tile has been played yet
        return len(self.chain) == 0

    def place_first_tile(self, domino):
        # first tile of the game goes in the middle, both ends are open
        self.chain.append(domino)
        self.left_end = domino.high
        self.right_end = domino.low

    def can_place(self, domino):
        # a tile can be placed if either of its sides matches an open end
        if self.is_empty():
            return True
        return domino.has_value(self.left_end) or domino.has_value(self.right_end)

    def place_tile(self, domino, side):
        """
        Places a tile on the board.
        side = 'left' or 'right'
        """
        if self.is_empty():
            self.place_first_tile(domino)
            return

        if side == 'left':
            if not domino.has_value(self.left_end):
                raise ValueError(f"{domino} does not connect to left end {self.left_end}")
            # the side that matches gets connected, the other side becomes the new open end
            self.left_end = domino.other_side(self.left_end)
            self.chain.insert(0, domino)

        elif side == 'right':
            if not domino.has_value(self.right_end):
                raise ValueError(f"{domino} does not connect to right end {self.right_end}")
            self.right_end = domino.other_side(self.right_end)
            self.chain.append(domino)

        else:
            raise ValueError("side must be 'left' or 'right'")

    def get_open_ends(self):
        # Returns both open ends as a tuple
        return (self.left_end, self.right_end)

    def total_pips_on_board(self):
        # Sum of all pips currently on the board
        return sum(d.total_pips() for d in self.chain)

    def __repr__(self):
        if self.is_empty():
            return "Board: empty"
        chain_str = " - ".join(str(d) for d in self.chain)
        return f"Board: {self.left_end} | {chain_str} | {self.right_end}"