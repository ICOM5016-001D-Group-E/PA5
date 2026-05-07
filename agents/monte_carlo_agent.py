import random
from copy import deepcopy
from game.rules import Rules

class MonteCarloAgent:
    def __init__(self, simulations=20):
        self.simulations = simulations

    def choose_move(self, game_state):
        legal_moves = game_state.get_legal_moves()

        if not legal_moves:
            return None, None

        best_move = None
        best_score = -1

        for move in legal_moves:
            score = self.evaluate_move(game_state, move)

            if score > best_score:
                best_score = score
                best_move = move

        side = self.pick_side(game_state, best_move)
        return best_move, side

    def evaluate_move(self, game_state, move):
        wins = 0
        player = game_state.current_player
        team = Rules.get_team(player)

        for _ in range(self.simulations):
            sim_state = deepcopy(game_state)

            # ✅ Handle first move correctly WITHOUT overwriting move
            if sim_state.board.is_empty() and sim_state.forced_first_tile is not None:
                forced_move = sim_state.forced_first_tile
                sim_state.apply_move(forced_move)
            else:
                if sim_state.board.is_empty():
                    sim_state.apply_move(move)
                else:
                    side = self.pick_side(sim_state, move)
                    sim_state.apply_move(move, side)

            winner = self.simulate_random_game(sim_state)

            if winner == team:
                wins += 1

        return wins / self.simulations

    def simulate_random_game(self, sim_state):
        while not sim_state.game_over:
            moves = sim_state.get_legal_moves()

            if not moves:
                sim_state.apply_pass()
            else:
                # ✅ Handle first move rule here too
                if sim_state.board.is_empty() and sim_state.forced_first_tile is not None:
                    tile = sim_state.forced_first_tile
                    sim_state.apply_move(tile)
                else:
                    tile = random.choice(moves)

                    if sim_state.board.is_empty():
                        sim_state.apply_move(tile)
                    else:
                        side = self.pick_side(sim_state, tile)
                        sim_state.apply_move(tile, side)

        return sim_state.winner

    def pick_side(self, game_state, tile):
        if game_state.board.is_empty():
            return None

        left, right = game_state.board.get_open_ends()

        fits_left = tile.has_value(left)
        fits_right = tile.has_value(right)

        if fits_left and not fits_right:
            return "left"
        if fits_right and not fits_left:
            return "right"

        # If both sides possible, choose randomly
        return random.choice(["left", "right"])