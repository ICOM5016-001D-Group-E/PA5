class Rules:
    # Handles legal moves, turn order, and end-of-game detection.

    NUM_PLAYERS = 4
    TILES_PER_PLAYER = 7

    # Teams: player 0 and 2 are one team, player 1 and 3 are the other
    TEAMS = {
        0: 0,  # player 0 → team 0
        1: 1,  # player 1 → team 1
        2: 0,  # player 2 → team 0
        3: 1,  # player 3 → team 1
    }

    @staticmethod
    def get_legal_moves(hand, board):
        # Returns all tiles in hand that can be placed on the board
        if board.is_empty():
            return list(hand)  # any tile is legal on an empty board
        return [tile for tile in hand if board.can_place(tile)]

    @staticmethod
    def next_player(current_player):
        # Turns go 0 → 1 → 2 → 3 → 0 → ...
        return (current_player + 1) % Rules.NUM_PLAYERS

    @staticmethod
    def get_team(player):
        # Returns which team a player belongs to (0 or 1)
        return Rules.TEAMS[player]

    @staticmethod
    def get_teammate(player):
        # Players 0 and 2 are teammates, players 1 and 3 are teammates
        return (player + 2) % Rules.NUM_PLAYERS

    @staticmethod
    def is_game_over(hands, board):
        # The game ends in two situations:
        # 1. A player empties their hand (domino!)
        # 2. All 4 players are blocked (no legal moves for anyone)
    
        # Check if any player has no tiles left
        for hand in hands:
            if len(hand) == 0:
                return True

        # Check if all players are blocked
        all_blocked = all(
            len(Rules.get_legal_moves(hand, board)) == 0
            for hand in hands
        )
        return all_blocked

    @staticmethod
    def get_winner(hands, board):
        # returns the winning team (0 or 1).
        # if a player emptied their hand, their team wins.
        # if blocked, the team with the lowest pip count wins.
        
        # Check who emptied their hand
        for player, hand in enumerate(hands):
            if len(hand) == 0:
                return Rules.get_team(player)

        # Blocked game — count pips per team
        team_pips = {0: 0, 1: 0}
        for player, hand in enumerate(hands):
            team = Rules.get_team(player)
            team_pips[team] += sum(tile.total_pips() for tile in hand)

        # Lower pip count wins
        if team_pips[0] < team_pips[1]:
            return 0
        elif team_pips[1] < team_pips[0]:
            return 1
        else:
            return None  # tie

    @staticmethod
    def calculate_score(hands):
        # Score = total pips remaining in the LOSING team's hands.
        # The winning team gets that many points.
        
        team_pips = {0: 0, 1: 0}
        for player, hand in enumerate(hands):
            team = Rules.get_team(player)
            team_pips[team] += sum(tile.total_pips() for tile in hand)
        return team_pips