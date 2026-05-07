import random

class RandomAgent:
    def choose_move(self, game_state):
        legal_moves = game_state.get_legal_moves()

        if not legal_moves:
            return None, None

        tile = random.choice(legal_moves)
        side = None

        if not game_state.board.is_empty():
            left, right = game_state.board.get_open_ends()

            possible_sides = []
            if tile.has_value(left):
                possible_sides.append("left")
            if tile.has_value(right):
                possible_sides.append("right")

            side = random.choice(possible_sides)

        return tile, side