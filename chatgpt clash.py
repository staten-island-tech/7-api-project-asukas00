import tkinter as tk
from tkinter import messagebox
import copy
import random

# --- Constants for Chess Pieces (Unicode) ---
PIECES = {
    'wP': '♙', 'wN': '♘', 'wB': '♗', 'wR': '♖', 'wQ': '♕', 'wK': '♔',
    'bP': '♟', 'bN': '♞', 'bB': '♝', 'bR': '♜', 'bQ': '♛', 'bK': '♚',
}

# --- Piece Values for AI Evaluation ---
PIECE_VALUES = {
    'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 900
}

# --- Initial Board Setup ---
INITIAL_BOARD = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

class ChessGameGUI:
    """
    A Tkinter-based chess game with a simple Minimax AI.
    """
    def __init__(self, master, square_size=80):
        self.master = master
        master.title("Tkinter Chess AI")
        self.square_size = square_size

        # Tkinter Canvas Setup
        self.canvas_width = 8 * square_size
        self.canvas_height = 8 * square_size
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack(padx=20, pady=10)
        self.canvas.bind("<Button-1>", self.handle_click)

        # Status Label
        self.status_text = tk.StringVar()
        self.status_label = tk.Label(master, textvariable=self.status_text, font=("Arial", 14, "bold"), pady=10)
        self.status_label.pack()

        # Control Button
        self.reset_button = tk.Button(master, text="Reset Game", command=self.reset_game, font=("Arial", 12))
        self.reset_button.pack(pady=5)

        # Game State Variables
        self.board = self._get_initial_board()
        self.current_player = 'w'  # 'w' for White (Human), 'b' for Black (AI)
        self.selected_pos = None  # (row, col) of the currently selected piece
        self.possible_moves = []  # List of valid (row, col) destinations for the selected piece
        self.game_over = False
        self.ai_depth = 3  # Depth for Minimax search

        self.draw_board()
        self.update_status()

    # --- Initialization and UI Drawing ---

    def _get_initial_board(self):
        """Returns a deep copy of the initial board setup."""
        return copy.deepcopy(INITIAL_BOARD)

    def draw_board(self):
        """Draws the board squares and pieces on the canvas."""
        self.canvas.delete("all")
        
        for r in range(8):
            for c in range(8):
                x1 = c * self.square_size
                y1 = r * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                
                # Checkered pattern
                color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863" 
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags=f"square_{r}_{c}")

                piece = self.board[r][c]
                if piece:
                    text_color = "black" if piece[0] == 'b' else "white"
                    # Draw piece (center it in the square)
                    self.canvas.create_text(x1 + self.square_size / 2, y1 + self.square_size / 2,
                                            text=PIECES[piece], fill=text_color,
                                            font=("Arial", int(self.square_size * 0.5), "bold"),
                                            tags=("piece", f"piece_{r}_{c}"))

        # Redraw highlights if a piece is selected
        self.draw_highlights()

    def draw_highlights(self):
        """Draws highlights for the selected piece and possible moves."""
        
        # 1. Highlight Selected Square
        if self.selected_pos:
            r, c = self.selected_pos
            x1, y1 = c * self.square_size, r * self.square_size
            x2, y2 = x1 + self.square_size, y1 + self.square_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#64b5f6", tags="highlight_select") # Blue selection

        # 2. Highlight Possible Move Destinations
        for r, c in self.possible_moves:
            x1, y1 = c * self.square_size, r * self.square_size
            x2, y2 = x1 + self.square_size, y1 + self.square_size
            
            # Use a slightly transparent circle or a border for move targets
            self.canvas.create_oval(x1 + self.square_size * 0.3, y1 + self.square_size * 0.3, 
                                    x2 - self.square_size * 0.3, y2 - self.square_size * 0.3, 
                                    fill="#a8cf61", tags="highlight_move") # Green move target

        # Send pieces to front so they are visible over highlights
        self.canvas.tag_raise("piece")

    def update_status(self):
        """Updates the status bar text."""
        if self.game_over:
            self.status_text.set("Game Over! " + ("White Wins!" if self.current_player == 'b' else "Black Wins!"))
        else:
            status_message = f"{'White (Human)' if self.current_player == 'w' else 'Black (AI)'} to move."
            if self.is_in_check(self.board, self.current_player):
                status_message += " - CHECK!"
            self.status_text.set(status_message)
        self.draw_board()

    def reset_game(self):
        """Resets the game state to the initial position."""
        self.board = self._get_initial_board()
        self.current_player = 'w'
        self.selected_pos = None
        self.possible_moves = []
        self.game_over = False
        self.update_status()
        self.draw_board()

    # --- User Interaction ---

    def handle_click(self, event):
        """Handles a mouse click event on the canvas."""
        if self.game_over or self.current_player == 'b':
            return # Block clicks during AI turn or if game is over

        c = event.x // self.square_size
        r = event.y // self.square_size
        
        if not (0 <= r < 8 and 0 <= c < 8):
            return

        piece = self.board[r][c]
        
        # 1. Selection Phase: Click on a piece of the current player's color
        if piece and piece[0] == self.current_player:
            self.selected_pos = (r, c)
            # Use the new legal move generation
            self.possible_moves = self.get_valid_moves(self.board, r, c) 
            self.draw_board() # Redraw to show selection and possible moves
        
        # 2. Movement Phase: Click on a possible destination square
        elif self.selected_pos and (r, c) in self.possible_moves:
            from_r, from_c = self.selected_pos
            self.make_move(from_r, from_c, r, c)
            self.selected_pos = None
            self.possible_moves = []
            self.draw_board()
            self.switch_turn()
            
            # Start AI turn
            if not self.game_over and self.current_player == 'b':
                self.master.after(500, self.ai_move) # Delay AI move for better UX
            
        # 3. Deselection/Invalid Click: Clicked elsewhere
        else:
            self.selected_pos = None
            self.possible_moves = []
            self.draw_board()

    def switch_turn(self):
        """Switches the current player and checks for game end conditions (Checkmate/Stalemate)."""
        self.current_player = 'b' if self.current_player == 'w' else 'w'
        
        legal_moves = self.get_all_valid_moves(self.board, self.current_player)

        if not legal_moves:
            self.game_over = True
            
            if self.is_in_check(self.board, self.current_player):
                # Checkmate: Player cannot move AND is in check
                messagebox.showinfo("Game Over", f"Checkmate! {'Black' if self.current_player == 'w' else 'White'} wins.")
            else:
                # Stalemate: Player cannot move BUT is NOT in check
                messagebox.showinfo("Game Over", "Stalemate! It's a Draw.")
        
        self.update_status()

    # --- Core Game Logic ---

    def make_move(self, from_r, from_c, to_r, to_c, board_state=None):
        """Performs a move on the board (updates the state)."""
        board = board_state if board_state is not None else self.board
        piece = board[from_r][from_c]
        
        if not piece:
            return False

        # Execute move
        board[to_r][to_c] = piece
        board[from_r][from_c] = None

        # Pawn Promotion (Simplified: to Queen only)
        if piece[1] == 'P' and (to_r == 0 or to_r == 7):
            new_piece = piece[0] + 'Q'
            board[to_r][to_c] = new_piece
        
        return True

    def is_on_board(self, r, c):
        """Checks if a position (r, c) is within the 8x8 boundaries."""
        return 0 <= r < 8 and 0 <= c < 8

    def get_piece_color(self, piece):
        """Returns the color ('w' or 'b') of a piece."""
        return piece[0] if piece else None

    # --- Check and Attack Logic ---

    def find_king(self, board, color):
        """Locates and returns the (r, c) position of the King of the given color."""
        king_piece = color + 'K'
        for r in range(8):
            for c in range(8):
                if board[r][c] == king_piece:
                    return (r, c)
        return None 

    def is_square_attacked(self, board, r, c, attacker_color):
        """Checks if the square (r, c) is attacked by a piece of the attacker_color."""
        
        opponent_color = attacker_color
        
        # Check every square for an opponent piece that can move to (r, c)
        for from_r in range(8):
            for from_c in range(8):
                piece = board[from_r][from_c]
                if piece and piece[0] == opponent_color:
                    # Get pseudo-legal moves for this piece (without checking for check)
                    moves = self.get_pseudo_legal_moves(board, from_r, from_c)
                    if (r, c) in moves:
                        return True
        return False

    def is_in_check(self, board, color):
        """Checks if the King of the given color is currently in check."""
        king_pos = self.find_king(board, color)
        if not king_pos:
            return False 
            
        king_r, king_c = king_pos
        attacker_color = 'b' if color == 'w' else 'w'
        
        return self.is_square_attacked(board, king_r, king_c, attacker_color)

    # --- Move Validation with Check Rules ---

    def get_pseudo_legal_moves(self, board, r, c):
        """
        Calculates all possible moves for a piece at (r, c) without 
        checking if the move exposes the King (pseudo-legal).
        (The logic for this function remains the same)
        """
        piece = board[r][c]
        if not piece: return []

        color = piece[0]
        opponent_color = 'b' if color == 'w' else 'w'
        piece_type = piece[1]
        moves = []

        # Helper for sliding pieces (Rook, Bishop, Queen)
        def _check_directions(directions):
            for dr, dc in directions:
                for i in range(1, 8):
                    nr, nc = r + dr * i, c + dc * i
                    if not self.is_on_board(nr, nc): break
                    target = board[nr][nc]
                    
                    if target is None:
                        moves.append((nr, nc))
                    elif self.get_piece_color(target) == opponent_color:
                        moves.append((nr, nc)) # Capture
                        break
                    else:
                        break # Blocked by own piece

        # Rook moves
        if piece_type == 'R' or piece_type == 'Q':
            _check_directions([(0, 1), (0, -1), (1, 0), (-1, 0)])

        # Bishop moves
        if piece_type == 'B' or piece_type == 'Q':
            _check_directions([(1, 1), (1, -1), (-1, 1), (-1, -1)])
            
        # Knight moves
        if piece_type == 'N':
            knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
            for dr, dc in knight_moves:
                nr, nc = r + dr, c + dc
                if self.is_on_board(nr, nc):
                    target = board[nr][nc]
                    if target is None or self.get_piece_color(target) == opponent_color:
                        moves.append((nr, nc))

        # King moves
        if piece_type == 'K':
            king_moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in king_moves:
                nr, nc = r + dr, c + dc
                if self.is_on_board(nr, nc):
                    target = board[nr][nc]
                    if target is None or self.get_piece_color(target) == opponent_color:
                        moves.append((nr, nc))

        # Pawn moves
        if piece_type == 'P':
            direction = -1 if color == 'w' else 1
            start_row = 6 if color == 'w' else 1

            # 1. Single forward move
            nr, nc = r + direction, c
            if self.is_on_board(nr, nc) and board[nr][nc] is None:
                moves.append((nr, nc))
                
                # 2. Double forward move from start row
                if r == start_row:
                    nnr = r + 2 * direction
                    if board[nnr][nc] is None:
                        moves.append((nnr, nc))

            # 3. Captures
            for dc in [-1, 1]:
                nr, nc = r + direction, c + dc
                if self.is_on_board(nr, nc):
                    target = board[nr][nc]
                    if target and self.get_piece_color(target) == opponent_color:
                        moves.append((nr, nc))

        return moves

    def get_valid_moves(self, board, r, c):
        """
        Gets all legal moves for a piece, filtering out moves that leave the
        King in check (truly legal moves).
        """
        piece = board[r][c]
        if not piece: return []
        
        pseudo_moves = self.get_pseudo_legal_moves(board, r, c)
        legal_moves = []
        player_color = piece[0]

        for to_r, to_c in pseudo_moves:
            # 1. Create a temporary board copy
            temp_board = copy.deepcopy(board)
            
            # 2. Make the move on the temporary board
            # Note: We must return the captured piece (if any) to reset the temp board later, 
            # but since we are using deepcopy, we don't need to manually reset.
            self.make_move(r, c, to_r, to_c, temp_board)
            
            # 3. Check if the King of the current player is in check on the new board
            if not self.is_in_check(temp_board, player_color):
                legal_moves.append((to_r, to_c))

        return legal_moves

    def get_all_valid_moves(self, board, player_color):
        """Generates all legal (start_r, start_c, end_r, end_c) moves for a player."""
        all_moves = []
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and piece[0] == player_color:
                    # Use the check-aware move generation
                    valid_destinations = self.get_valid_moves(board, r, c) 
                    for dr, dc in valid_destinations:
                        all_moves.append((r, c, dr, dc))
        return all_moves

    # --- AI Implementation (Minimax) ---
    
    def evaluate_board(self, board):
        """
        Simple material evaluation function.
        Positive score favors White (Human), negative favors Black (AI).
        """
        score = 0
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece:
                    color = piece[0]
                    piece_type = piece[1]
                    value = PIECE_VALUES.get(piece_type, 0)
                    
                    if color == 'w':
                        score += value
                    else:
                        score -= value
        return score

    def minimax(self, board, depth, alpha, beta, is_maximizing_player):
        """
        The Minimax algorithm with Alpha-Beta Pruning.
        Maximizing player is White (Human), Minimizing player is Black (AI).
        """
        # Note: The minimax algorithm now correctly uses the legal move generator.
        if depth == 0 or self.game_over:
            return self.evaluate_board(board)

        current_color = 'w' if is_maximizing_player else 'b'
        all_moves = self.get_all_valid_moves(board, current_color)

        if not all_moves:
            # Check for Checkmate/Stalemate
            if self.is_in_check(board, current_color):
                # Checkmate: Return very high/low score to favor win/loss
                return -float('inf') if is_maximizing_player else float('inf')
            else:
                # Stalemate: Draw (score 0)
                return 0

        if is_maximizing_player:
            max_eval = -float('inf')
            for from_r, from_c, to_r, to_c in all_moves:
                temp_board = copy.deepcopy(board)
                self.make_move(from_r, from_c, to_r, to_c, temp_board)
                
                eval = self.minimax(temp_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval
        else: # Minimizing Player (AI - Black)
            min_eval = float('inf')
            for from_r, from_c, to_r, to_c in all_moves:
                temp_board = copy.deepcopy(board)
                self.make_move(from_r, from_c, to_r, to_c, temp_board)
                
                eval = self.minimax(temp_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval

    def ai_move(self):
        """Determines and executes the best move for the AI."""
        if self.game_over or self.current_player != 'b':
            return

        self.status_text.set("Black (AI) is thinking...")
        self.master.update() # Force status update

        best_score = float('inf')
        best_move = None
        
        # Get all possible legal moves for Black (AI)
        all_ai_moves = self.get_all_valid_moves(self.board, 'b')
        
        if not all_ai_moves:
             self.game_over = True
             self.update_status()
             return

        # Shuffle moves to introduce some non-determinism for equal evaluations
        random.shuffle(all_ai_moves) 

        # Find the move that results in the lowest (best for Black) score
        for from_r, from_c, to_r, to_c in all_ai_moves:
            temp_board = copy.deepcopy(self.board)
            self.make_move(from_r, from_c, to_r, to_c, temp_board)
            
            # Run minimax from the perspective of the maximizing player (White)
            score = self.minimax(temp_board, self.ai_depth - 1, -float('inf'), float('inf'), True)
            
            if score < best_score:
                best_score = score
                best_move = (from_r, from_c, to_r, to_c)

        if best_move:
            from_r, from_c, to_r, to_c = best_move
            self.make_move(from_r, from_c, to_r, to_c)
            self.switch_turn()
        else:
            # Should not happen if checkmate/stalemate was handled correctly in switch_turn, 
            # but acts as a final fail-safe.
            print("AI could not find a legal move.")
            self.game_over = True
            self.update_status()
            
# --- Main Execution Block ---
if __name__ == '__main__':
    root = tk.Tk()
    game = ChessGameGUI(root)
    root.mainloop()