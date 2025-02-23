"""
Module containing the GUI logic for the Ayo game using tkinter.
"""

import tkinter as tk
from tkinter import messagebox
from game_logic import AyoGame
from ai import AyoAI

class AyoGUI:
    def __init__(self, root):
        """
        Initialize the GUI, the game logic, and the AI.
        """
        self.root = root
        self.root.title("Ayo Game")
        # Initialize game logic.
        self.game = AyoGame()
        # Default mode is Player vs Player.
        self.mode = tk.StringVar(value="PvP")
        # Default AI difficulty is 'easy'.
        self.ai_difficulty = tk.StringVar(value="easy")
        self.ai_player = AyoAI(difficulty=self.ai_difficulty.get())
        # Create the GUI components.
        self.create_widgets()
        self.update_board()

    def create_widgets(self):
        """Create and layout the GUI components."""
        # Mode selection frame.
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=10)
        tk.Label(mode_frame, text="Select Mode:").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Player vs Player", variable=self.mode, value="PvP", command=self.on_mode_change).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Player vs AI", variable=self.mode, value="PvAI", command=self.on_mode_change).pack(side=tk.LEFT)
        
        # AI difficulty selection frame.
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack(pady=10)
        tk.Label(difficulty_frame, text="AI Difficulty:").pack(side=tk.LEFT)
        tk.Radiobutton(difficulty_frame, text="Easy", variable=self.ai_difficulty, value="easy", command=self.on_difficulty_change).pack(side=tk.LEFT)
        tk.Radiobutton(difficulty_frame, text="Hard", variable=self.ai_difficulty, value="hard", command=self.on_difficulty_change).pack(side=tk.LEFT)
        
        # Board frame for displaying pits.
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=20)
        
        # Create pit buttons.
        self.pit_buttons = []
        # Top row for Player 2's pits (displayed in reverse order: indices 11 to 6).
        top_row = tk.Frame(self.board_frame)
        top_row.pack()
        for i in range(11, 5, -1):
            btn = tk.Button(top_row, text="", width=8, height=4, command=lambda idx=i: self.on_pit_click(idx))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.pit_buttons.append(btn)
        
        # Bottom row for Player 1's pits (indices 0 to 5).
        bottom_row = tk.Frame(self.board_frame)
        bottom_row.pack()
        for i in range(0, 6):
            btn = tk.Button(bottom_row, text="", width=8, height=4, command=lambda idx=i: self.on_pit_click(idx))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.pit_buttons.append(btn)
        
        # Label to display game info.
        self.info_label = tk.Label(self.root, text="Player 1's turn")
        self.info_label.pack(pady=10)
        
        # Button frame for extra controls.
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        # Restart button.
        restart_btn = tk.Button(control_frame, text="Restart Game", command=self.on_restart)
        restart_btn.pack(side=tk.LEFT, padx=5)
        # Tutorial button.
        tutorial_btn = tk.Button(control_frame, text="Tutorial", command=self.show_tutorial)
        tutorial_btn.pack(side=tk.LEFT, padx=5)

    def on_mode_change(self):
        """Handle changes in game mode (PvP vs PvAI)."""
        self.update_board()
        self.check_ai_turn()

    def on_difficulty_change(self):
        """Handle changes in AI difficulty."""
        self.ai_player = AyoAI(difficulty=self.ai_difficulty.get())
        self.update_board()

    def on_pit_click(self, pit_index):
        """
        Handle the event when a pit button is clicked.
        Processes the move if it is valid.
        """
        if self.game.game_over:
            messagebox.showinfo("Game Over", "The game is over. Please restart to play again.")
            return
        
        # In PvAI mode, assume Player 2 is controlled by the AI.
        if self.mode.get() == "PvAI" and self.game.current_player == 2:
            messagebox.showinfo("Wait", "It's the AI's turn!")
            return

        if self.game.make_move(pit_index):
            self.update_board()
            self.check_game_over()
            # In PvAI mode, if it becomes the AI's turn, trigger the AI move.
            self.check_ai_turn()
        else:
            messagebox.showwarning("Invalid Move", "Please choose a valid pit.")

    def check_ai_turn(self):
        """If it is the AI's turn in PvAI mode, trigger the AI move."""
        if self.mode.get() == "PvAI" and self.game.current_player == 2 and not self.game.game_over:
            # Delay AI move slightly for a natural feel.
            self.root.after(500, self.make_ai_move)

    def make_ai_move(self):
        """Perform the AI move."""
        move = self.ai_player.choose_move(self.game)
        if move is not None:
            self.game.make_move(move)
            self.update_board()
            self.check_game_over()
        else:
            messagebox.showinfo("No Moves", "AI has no valid moves!")
        # Check again if it is still AI’s turn (e.g., if the move grants an extra turn).
        self.check_ai_turn()

    def check_game_over(self):
        """Check if the game is over and display the result."""
        if self.game.game_over:
            winner = self.game.get_winner()
            if winner == 0:
                result = "It's a tie!"
            else:
                if self.mode.get() == "PvAI":
                    # In PvAI mode, Player 1 is the human, Player 2 is the AI.
                    result = "You win!" if winner == 1 else "AI wins!"
                else:
                    result = f"Player {winner} wins!"
            self.info_label.config(text=f"Game Over! {result}")
            messagebox.showinfo("Game Over", result)
        else:
            self.info_label.config(text=f"Player {self.game.current_player}'s turn")

    def update_board(self):
        """Update the display of the board to reflect the current game state."""
        for i in range(12):
            # Map the board index to the correct pit button.
            if i >= 6:
                # For Player 2, the top row order is reversed.
                btn_index = 11 - i
            else:
                btn_index = 6 + i
            self.pit_buttons[btn_index].config(text=str(self.game.board[i]))

    def on_restart(self):
        """Restart the game and update the GUI."""
        self.game.reset_game()
        self.info_label.config(text="Player 1's turn")
        self.update_board()

    def show_tutorial(self):
        """
        Display a tutorial message explaining how to play the game.
        """
        tutorial_text = (
            "Welcome to the Ayo Game!\n\n"
            "How to Play:\n"
            "1. The board consists of 12 pits. Pits 0-5 belong to Player 1, and pits 6-11 belong to Player 2.\n"
            "2. Each pit starts with 4 seeds.\n"
            "3. On your turn, click on one of your pits to sow its seeds counterclockwise.\n"
            "4. If the last seed lands in an opponent's pit with exactly 2 or 3 seeds, those seeds are captured.\n"
            "5. The game ends when one player's side is empty. The player with the most captured seeds wins.\n\n"
            "Controls:\n"
            "- Use the mode selection buttons to switch between Player vs Player and Player vs AI.\n"
            "- Adjust the AI difficulty as needed.\n"
            "- Click 'Restart Game' to start a new match.\n\n"
            "Enjoy the game and reminisce about the childhood fun of playing Ayo!"
        )
        messagebox.showinfo("Tutorial", tutorial_text)
