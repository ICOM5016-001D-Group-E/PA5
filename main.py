from game.game_state import GameState
from game.rules import Rules
from agents.random_agent import RandomAgent
from agents.heuristic_agent import HeuristicAgent
from agents.smart_heuristic_agent import SmartHeuristicAgent
from agents.monte_carlo_agent import MonteCarloAgent



def display_game(game, player):
    print("\n" + "="*50)
    print(f"Board: {game.board}")
    print(f"Scores -> Team 0: {game.scores[0]} | Team 1: {game.scores[1]}")
    print(f"Hand sizes: {[len(h) for h in game.hands]}")
    print(f"\nYour hand (Player {player}, Team {Rules.get_team(player)}):")
    for i, tile in enumerate(game.hands[player]):
        print(f"  {i}: {tile}")


def get_human_move(game, player):
    legal = game.get_legal_moves()

    # If board is empty, first move must be [6|6]
    if game.board.is_empty() and game.forced_first_tile is not None:
        legal = [game.forced_first_tile]
        print(f"\nFirst move must be [6|6].")
        print(f"  0: {game.forced_first_tile}")
        input("Press Enter to play it automatically...")
        return game.forced_first_tile, None

    if not legal:
        print("No legal moves — you must pass.")
        input("Press Enter to pass...")
        return None, None

    print(f"\nLegal moves:")
    for i, tile in enumerate(legal):
        print(f"  {i}: {tile}")

    # Pick a tile
    while True:
        try:
            choice = int(input("Pick tile number: "))
            if 0 <= choice < len(legal):
                chosen = legal[choice]
                break
            print("Invalid choice, try again.")
        except ValueError:
            print("Enter a number.")

    # Pick a side if board is not empty
    side = None
    if not game.board.is_empty():
        left, right = game.board.get_open_ends()
        fits_left = chosen.has_value(left)
        fits_right = chosen.has_value(right)

        if fits_left and fits_right:
            # Tile fits both sides, ask player
            while True:
                s = input(f"Place on left ({left}) or right ({right})? [l/r]: ").strip().lower()
                if s == 'l':
                    side = 'left'
                    break
                elif s == 'r':
                    side = 'right'
                    break
                print("Enter l or r.")
        elif fits_left:
            side = 'left'
        else:
            side = 'right'

    return chosen, side


def play_game():
    game = GameState()
    game.setup()

    print("=== DOMINOES (YOU vs AI) ===")
    print("You are Player 0 (Team 0)")
    print("Teams: Player 0 & 2 vs Player 1 & 3")
    print(f"Player {game.current_player} has [6|6] and goes first.\n")


    agents = [
        None,                    # Player 0 → HUMAN
        SmartHeuristicAgent(),   # Player 1
        MonteCarloAgent(),       # Player 2 (your teammate)
        HeuristicAgent()         # Player 3
    ]

    while not game.game_over:
        current = game.current_player

        print("\n" + "="*50)
        print(f"Turn: Player {current} (Team {Rules.get_team(current)})")
        print(f"Board: {game.board}")
        print(f"Hand sizes: {[len(h) for h in game.hands]}")


        if current == 0:
            tile, side = get_human_move(game, current)


        else:
            agent = agents[current]

            if game.board.is_empty() and game.forced_first_tile is not None:
                tile = game.forced_first_tile
                side = None
            else:
                tile, side = agent.choose_move(game)

            if tile is None:
                print(f"Player {current} passes.")
            else:
                print(f"Player {current} plays {tile} on {side}")

        # Apply move
        if tile is None:
            game.apply_pass()
        else:
            game.apply_move(tile, side)

    # Game over
    print("\n" + "="*50)
    print("GAME OVER")

    if game.winner is not None:
        print(f"Team {game.winner} wins!")
    else:
        print("It's a tie!")

    print(f"Final scores -> Team 0: {game.scores[0]} | Team 1: {game.scores[1]}")

if __name__ == "__main__":
    play_game()