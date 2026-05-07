class SmartHeuristicAgent:
    def choose_move(self, game_state):
        legal_moves = game_state.get_legal_moves()

        if not legal_moves:
            return None, None

        my_hand = game_state.hands[game_state.current_player]

        def score_tile(tile):
            score = 0

            # play high-value tiles
            score += tile.total_pips()

            # preserve flexibility: prefer numbers you have more of
            values = [tile.high, tile.low]
            for v in values:
                score += sum(1 for t in my_hand if t.has_value(v))

            # prefer doubles slightly
            if tile.is_double():
                score += 2

            return score

        tile = max(legal_moves, key=score_tile)

        side = None
        if not game_state.board.is_empty():
            left, right = game_state.board.get_open_ends()

            if tile.has_value(left):
                side = "left"
            elif tile.has_value(right):
                side = "right"

        return tile, side