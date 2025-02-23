"""
Module containing the game logic for the Ayo game.
"""

class AyoGame:
    def __init__(self):
        """Initialize the game board and state."""
        # The board is represented by 12 pits.
        # Indices 0-5 belong to Player 1; indices 6-11 belong to Player 2.
        # Each pit starts with 4 seeds.
        self.board = [4] * 12
        # Store captured seeds for each player.
        self.player_scores = {1: 0, 2: 0}
        # Player 1 starts the game.
        self.current_player = 1
        self.game_over = False

    def is_valid_move(self, pit_index):
        """
        Check if the selected pit is a valid move.
        A move is valid if:
          - The pit is on the current player's side.
          - The pit contains at least one seed.
        """
        if self.game_over:
            return False
        if self.current_player == 1 and 0 <= pit_index <= 5 and self.board[pit_index] > 0:
            return True
        elif self.current_player == 2 and 6 <= pit_index <= 11 and self.board[pit_index] > 0:
            return True
        return False

    def make_move(self, pit_index):
        """
        Perform a move from the selected pit.
        - Picks up all seeds from the pit.
        - Sows them counterclockwise one by one.
        - Handles capturing rules after sowing.
        Returns True if the move was successful.
        """
        if not self.is_valid_move(pit_index):
            return False
        
        seeds = self.board[pit_index]
        self.board[pit_index] = 0
        current_index = pit_index

        # Distribute the seeds in a counterclockwise fashion.
        while seeds > 0:
            current_index = (current_index + 1) % 12
            self.board[current_index] += 1
            seeds -= 1

        # Handle capturing seeds from the opponent's pits.
        self.handle_captures(current_index)
        
        # Check if the game has ended.
        self.check_end_game()
        
        # Switch the turn to the other player if the game is not over.
        if not self.game_over:
            self.switch_player()
        return True

    def handle_captures(self, last_index):
        """
        Capture seeds based on where the last seed was sown.
        Starting from the last pit and moving backwards, if a pit (on the opponent's side)
        has 2 or 3 seeds, capture them.
        """
        captured = 0
        # Define the opponent's pit range.
        if self.current_player == 1:
            opponent_range = range(6, 12)
        else:
            opponent_range = range(0, 6)
        
        index = last_index
        while index in opponent_range and self.board[index] in [2, 3]:
            captured += self.board[index]
            self.board[index] = 0
            index = (index - 1) % 12
        self.player_scores[self.current_player] += captured

    def switch_player(self):
        """Switch the turn to the other player."""
        self.current_player = 2 if self.current_player == 1 else 1

    def check_end_game(self):
        """
        Check if the game is over.
        The game ends when one player's side is completely empty.
        """
        p1_empty = all(seeds == 0 for seeds in self.board[0:6])
        p2_empty = all(seeds == 0 for seeds in self.board[6:12])
        if p1_empty or p2_empty:
            self.game_over = True
            # Collect remaining seeds to the opponent's score.
            if p1_empty:
                for i in range(6, 12):
                    self.player_scores[2] += self.board[i]
                    self.board[i] = 0
            if p2_empty:
                for i in range(0, 6):
                    self.player_scores[1] += self.board[i]
                    self.board[i] = 0

    def get_winner(self):
        """Determine the winner of the game. Returns 1 or 2 (or 0 for a tie)."""
        if not self.game_over:
            return None
        if self.player_scores[1] > self.player_scores[2]:
            return 1
        elif self.player_scores[2] > self.player_scores[1]:
            return 2
        else:
            return 0  # Tie

    def reset_game(self):
        """Reset the game to its initial state."""
        self.board = [4] * 12
        self.player_scores = {1: 0, 2: 0}
        self.current_player = 1
        self.game_over = False
