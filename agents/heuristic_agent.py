class HeuristicAgent:
    def choose_move(self, game_state):
        legal_moves = game_state.get_legal_moves()

        if not legal_moves:
            return None, None

        tile = max(legal_moves, key=lambda t: t.total_pips())
        side = None

        if not game_state.board.is_empty():
            left, right = game_state.board.get_open_ends()

            if tile.has_value(left):
                side = "left"
            elif tile.has_value(right):
                side = "right"

        return tile, side