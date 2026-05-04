from game.domino import DominoSet
from game.board import Board
from game.rules import Rules


class GameState:
    # Central object that holds everything about the current game.
    # Ties together the board, all hands, turn order, and scoring.
    

    def __init__(self):
        self.board = Board()
        self.hands = []          # hands[i] = list of tiles for player i
        self.current_player = 0  # whose turn it is
        self.scores = {0: 0, 1: 0}  # team scores across rounds
        self.pass_count = 0      # tracks consecutive passes (for blocked game)
        self.game_over = False
        self.winner = None
        self.forced_first_tile = None 

    def setup(self):
        # Deal tiles to all 4 players and reset the board
        domino_set = DominoSet()
        self.hands = domino_set.deal()
        self.board = Board()
        self.current_player = self._find_starting_player()
        self.pass_count = 0
        self.game_over = False
        self.winner = None

    def _find_starting_player(self):
    # The player with [6|6] goes first and must play it immediately
        for player, hand in enumerate(self.hands):
            for tile in hand:
                if tile.high == 6 and tile.low == 6:
                    self.forced_first_tile = tile  # remember it
                    return player
        self.forced_first_tile = None
        return 0

    def get_legal_moves(self):
        # Returns legal moves for the current player
        return Rules.get_legal_moves(self.hands[self.current_player], self.board)

    def apply_move(self, domino, side=None):
        # Places a tile for the current player.
        # domino = the Domino object to play
        # side   = 'left' or 'right' (ignored on first move)
  
        hand = self.hands[self.current_player]
        if self.board.is_empty() and self.forced_first_tile is not None:
            if domino != self.forced_first_tile:
                raise ValueError(f"First move must be [6|6], got {domino}")
        if domino not in hand:
            raise ValueError(f"Player {self.current_player} does not have {domino}")

        # First tile of the game — no side needed
        if self.board.is_empty():
            self.board.place_first_tile(domino)
        else:
            if side is None:
                # Auto-pick side if only one side is valid
                side = self._auto_pick_side(domino)
            self.board.place_tile(domino, side)

        # Remove tile from player's hand
        hand.remove(domino)

        # Reset pass counter since someone played
        self.pass_count = 0

        # Check if game is over
        self._check_game_over()

        # Advance to next player
        if not self.game_over:
            self.current_player = Rules.next_player(self.current_player)

    def apply_pass(self):
        # Current player has no legal moves, must pass
        self.pass_count += 1
        self.current_player = Rules.next_player(self.current_player)

        # If all 4 players passed in a row, game is blocked
        if self.pass_count >= Rules.NUM_PLAYERS:
            self._check_game_over()

    def _auto_pick_side(self, domino):
        # If a tile fits on both ends, defaults to 'right'.
        # If it only fits on one end, picks that one automatically.

        left_end, right_end = self.board.get_open_ends()
        fits_left = domino.has_value(left_end)
        fits_right = domino.has_value(right_end)

        if fits_left and not fits_right:
            return 'left'
        return 'right'  # default to right if both or only right fits

    def _check_game_over(self):
        # Checks win condition and updates score if game ended
        if Rules.is_game_over(self.hands, self.board):
            self.game_over = True
            self.winner = Rules.get_winner(self.hands, self.board)
            team_pips = Rules.calculate_score(self.hands)

            # Winning team gets the loser's pip count as points
            if self.winner is not None:
                losing_team = 1 - self.winner
                self.scores[self.winner] += team_pips[losing_team]

    def get_observable_state(self, player):
        # Returns only what a given player is allowed to see.
        # - Their own hand
        # - The board
        # - How many tiles each opponent has (not which ones)
        # This is what the AI agents will call — no cheating.
     
        return {
            "my_hand":       self.hands[player],
            "board":         self.board,
            "current_player": self.current_player,
            "hand_sizes":    [len(h) for h in self.hands],
            "scores":        self.scores,
            "game_over":     self.game_over,
            "winner":        self.winner,
        }

    def __repr__(self):
        return (
            f"Turn: Player {self.current_player} | "
            f"{self.board} | "
            f"Hand sizes: {[len(h) for h in self.hands]}"
        )