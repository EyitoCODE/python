"""
Module containing the AI logic for the Ayo game.
"""

import random
from game_logic import AyoGame

class AyoAI:
    def __init__(self, difficulty='easy'):
        """
        Initialize the AI with a given difficulty.
        Available difficulties: 'easy' or 'hard'.
        """
        self.difficulty = difficulty

    def choose_move(self, game: AyoGame):
        """
        Choose a move for the AI based on the current game state.
        Returns a valid pit index.
        """
        valid_moves = [i for i in range(12) if game.is_valid_move(i)]
        if not valid_moves:
            return None
        
        if self.difficulty == 'easy':
            # Easy mode: randomly select a valid move.
            return random.choice(valid_moves)
        elif self.difficulty == 'hard':
            # Hard mode: select the move that maximizes immediate captures.
            best_move = None
            max_capture = -1
            for move in valid_moves:
                capture = self.simulate_move_capture(game, move)
                if capture > max_capture:
                    max_capture = capture
                    best_move = move
            if best_move is None:
                best_move = random.choice(valid_moves)
            return best_move
        else:
            # Default to random if the difficulty is unrecognized.
            return random.choice(valid_moves)

    def simulate_move_capture(self, game: AyoGame, pit_index):
        """
        Simulate a move and return the number of seeds that would be captured.
        This is a simple heuristic used for the 'hard' difficulty.
        """
        # Create a copy of the game state.
        sim_game = AyoGame()
        sim_game.board = game.board.copy()
        sim_game.player_scores = game.player_scores.copy()
        sim_game.current_player = game.current_player
        sim_game.game_over = game.game_over
        
        before_score = sim_game.player_scores[sim_game.current_player]
        sim_game.make_move(pit_index)
        capture = sim_game.player_scores[sim_game.current_player] - before_score
        return capture
