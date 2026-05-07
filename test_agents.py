##this file is just for verifying agent functionality

from game.game_state import GameState
from agents.random_agent import RandomAgent
from agents.heuristic_agent import HeuristicAgent
from agents.smart_heuristic_agent import SmartHeuristicAgent
from agents.monte_carlo_agent import MonteCarloAgent

# def test_agent(agent, name):
#     game = GameState()
#     game.setup()

#     print(f"\nTesting {name}")
#     print(game)

#     if game.board.is_empty() and game.forced_first_tile is not None:
#         tile = game.forced_first_tile
#         side = None
#     else:
#         tile, side = agent.choose_move(game)

#     print("Chosen tile:", tile)
#     print("Chosen side:", side)

#     if tile is None:
#         game.apply_pass()
#     else:
#         game.apply_move(tile, side)

#     print("Move applied successfully.")
#     print(game)

# test_agent(RandomAgent(), "Random Agent")
# test_agent(HeuristicAgent(), "Heuristic Agent")
# test_agent(SmartHeuristicAgent(), "Smart Heuristic Agent")
# test_agent(MonteCarloAgent(), "Monte Carlo Agent")


def test_full_game(agent, name):
    game = GameState()
    game.setup()

    print(f"\nFull game test: {name}")

    while not game.game_over:
        tile, side = agent.choose_move(game)

        if game.board.is_empty() and game.forced_first_tile is not None:
            tile = game.forced_first_tile
            side = None

        if tile is None:
            game.apply_pass()
        else:
            game.apply_move(tile, side)

    print("Winner:", game.winner)
    print("Final score:", game.scores)


test_full_game(RandomAgent(), "Random Agent")
test_full_game(HeuristicAgent(), "Heuristic Agent")
test_full_game(SmartHeuristicAgent(), "Smart Heuristic Agent")
test_full_game(MonteCarloAgent(), "Monte Carlo Agent")