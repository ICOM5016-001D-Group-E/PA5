import random

class Domino:
    # single domino title
    # domino has two sides, each with value from 0 to 6
    # domino (3, 5) = 3|5 tile

    def __init__(self, high, low):
        # higher value on left so (3,5) = (5,3) tile
        self.high = max(high, low)
        self.low = min(high, low)

    def total_pips(self):
        # returns the sum of both sides for scoring matters
        return self.high + self.low
    
    def is_double(self):
        # double is a tile where both sides are equal
        return self.high == self.low

    def has_value(self, value):
        # comparing value to both sides of the tile
        return self.high == value or self.low == value
    
    def other_side(self, value):
        # tile = (3,5), other_side(3) returns 5
        if self.high == value:
            return self.low
        if self.low == value:
            return self.high
        raise ValueError(f"Value {value} not on this domino {self}")
    
    def __eq__(self, other):
        # two dominoes are equal if their high and low values are the same
        return isinstance(other, Domino) and self.high == other.high and self.low == other.low
    
    def __hash__(self):
        # dominoes stored in sets can be used as dict keys
        return hash((self.high, self.low))
    
    def __repr__(self):
        """How the tile prints. Example: [3|5]"""
        return f"[{self.high}|{self.low}]"


class DominoSet:
    # Represents the full set of 28 dominoes (double-six set).
    # Handles shuffling and dealing to players.

    def __init__(self):
        self.tiles = self._generate_all_tiles()

    def _generate_all_tiles(self):
        # Generates all 28 unique domino tiles.
        # A double-six set has tiles from [0|0] up to [6|6].
        # We use high >= low to avoid duplicates (e.g. only [3|5], not also [5|3]).
        
        tiles = []
        for high in range(7):       # 0 to 6
            for low in range(high + 1):  # 0 to high
                tiles.append(Domino(high, low))
        return tiles

    def shuffle(self):
        # Randomly shuffles the 28 tiles in place
        random.shuffle(self.tiles)

    def deal(self, num_players=4, tiles_per_player=7):
        # shuffles the set and deals tiles to players
        # returns a list of hands, one per player
        # default: 4 players, 7 tiles each (uses all 28 tiles)
        if num_players * tiles_per_player > len(self.tiles):
            raise ValueError("Not enough tiles to deal to all players.")

        self.shuffle()

        hands = []
        for i in range(num_players):
            start = i * tiles_per_player
            end = start + tiles_per_player
            hands.append(self.tiles[start:end])

        return hands

    def __repr__(self):
        return f"DominoSet({len(self.tiles)} tiles)"