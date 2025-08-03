import tkinter as tk
import math
import random
from PIL import Image, ImageTk
import os


# Constants
BOARD_SIZE = 15
CELL_SIZE = 40
BOARD_PADDING = 20
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING
PLAYER_HUMAN = 2  # White
PLAYER_AI_1 = 1  # Black (Minimax)
PLAYER_AI_2 = 3  # Red (Alpha-Beta)
MAX_DEPTH = 2

def init_board():
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

board = init_board()
game_mode = None
current_player = PLAYER_AI_1

root = tk.Tk()
root.title("Gomoku with AI Modes")
canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE, bg="#b69b4c")
canvas.pack()

try:
    image_path = r"C:\Users\Mr_Turbo\Desktop\University\semister 2\Ai\AI Project\bg.jpeg"
    original_image = Image.open(image_path)
    resized_image = original_image.resize((WINDOW_SIZE, WINDOW_SIZE), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(resized_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
except Exception as e:
    print(f"Background image not loaded: {e}")



mode_frame = tk.Frame(canvas, bg="", highlightthickness=0)
mode_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

tk.Label(mode_frame, text="Choose Game Mode:", font="Helvetica 14", bg="#b69b4c").pack(pady=10)
tk.Button(mode_frame, text="Human vs AI", font="Helvetica 12", width=20, command=lambda: [start_human_vs_ai()]).pack(pady=5)
tk.Button(mode_frame, text="AI vs AI", font="Helvetica 12", width=20, command=lambda: [start_ai_vs_ai()]).pack(pady=5)

def draw_board():
    canvas.delete("all")
    for i in range(BOARD_SIZE):
        x0 = BOARD_PADDING + i * CELL_SIZE
        y0 = BOARD_PADDING
        x1 = BOARD_PADDING + i * CELL_SIZE
        y1 = WINDOW_SIZE - BOARD_PADDING
        canvas.create_line(x0, y0, x1, y1)
        canvas.create_line(y0, x0, y1, x1)
    for i in range(BOARD_SIZE):
        x = BOARD_PADDING + i * CELL_SIZE
        y = BOARD_PADDING + i * CELL_SIZE
        canvas.create_text(BOARD_PADDING / 2, y, text=str(i + 1), font="Helvetica 10")
        canvas.create_text(x, BOARD_PADDING / 2, text=str(i + 1), font="Helvetica 10")

def draw_piece(x, y, player):
    px = BOARD_PADDING + x * CELL_SIZE
    py = BOARD_PADDING + y * CELL_SIZE
    radius = CELL_SIZE // 2 - 2
    color = "black" if player == PLAYER_AI_1 else ("white" if player == PLAYER_HUMAN else "red")
    canvas.create_oval(px - radius, py - radius, px + radius, py + radius, fill=color)

def check_win(board, player):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] != player:
                continue
            if x <= BOARD_SIZE - 5 and all(board[y][x + i] == player for i in range(5)):
                return True
            if y <= BOARD_SIZE - 5 and all(board[y + i][x] == player for i in range(5)):
                return True
            if x <= BOARD_SIZE - 5 and y <= BOARD_SIZE - 5 and all(board[y + i][x + i] == player for i in range(5)):
                return True
            if x >= 4 and y <= BOARD_SIZE - 5 and all(board[y + i][x - i] == player for i in range(5)):
                return True
    return False

def count_sequences(board, player):
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            for dx, dy in directions:
                count = 0
                for i in range(5):
                    nx = x + i * dx
                    ny = y + i * dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                        if board[ny][nx] == player:
                            count += 1
                        elif board[ny][nx] != 0:
                            count = 0
                            break
                    else:
                        count = 0
                        break
                if count == 5:
                    score += 100000
                elif count == 4:
                    score += 10000
                elif count == 3:
                    score += 1000
                elif count == 2:
                    score += 100
    return score

def evaluate_human_vs_ai(board, player):
    return count_sequences(board, player) - count_sequences(
        board, PLAYER_HUMAN if player != PLAYER_HUMAN else PLAYER_AI_1)

def evaluate_ai_vs_ai(board, player):
    opponent = PLAYER_AI_1 if player == PLAYER_AI_2 else PLAYER_AI_2
    return count_sequences(board, player) - count_sequences(board, opponent)

def get_valid_moves(board):
    moves = set()
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] != 0:
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == 0:
                            moves.add((nx, ny))
    if not moves:
        moves.add((BOARD_SIZE // 2, BOARD_SIZE // 2))
    return list(moves)

def minimax(board, depth, maximizing, evaluate_func):
    if check_win(board, PLAYER_AI_1): return None, None, 1000000
    if check_win(board, PLAYER_HUMAN): return None, None, -1000000
    if depth == 0:
        return None, None, evaluate_func(board, PLAYER_AI_1)
    best_move = None
    if maximizing:
        max_eval = -math.inf
        for x, y in get_valid_moves(board):
            board[y][x] = PLAYER_AI_1
            _, _, eval = minimax(board, depth - 1, False, evaluate_func)
            board[y][x] = 0
            if eval > max_eval:
                max_eval = eval
                best_move = (x, y)
        return *best_move, max_eval
    else:
        min_eval = math.inf
        for x, y in get_valid_moves(board):
            board[y][x] = PLAYER_HUMAN
            _, _, eval = minimax(board, depth - 1, True, evaluate_func)
            board[y][x] = 0
            if eval < min_eval:
                min_eval = eval
                best_move = (x, y)
        return *best_move, min_eval

def alpha_beta(board, depth, alpha, beta, maximizing, evaluate_func):
    if check_win(board, PLAYER_AI_2): return None, None, 1000000
    if check_win(board, PLAYER_AI_1): return None, None, -1000000
    if depth == 0:
        return None, None, evaluate_func(board, PLAYER_AI_2)
    best_move = None
    if maximizing:
        max_eval = -math.inf
        for x, y in get_valid_moves(board):
            board[y][x] = PLAYER_AI_2
            _, _, eval = alpha_beta(board, depth - 1, alpha, beta, False, evaluate_func)
            board[y][x] = 0
            if eval > max_eval:
                max_eval = eval
                best_move = (x, y)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return *best_move, max_eval
    else:
        min_eval = math.inf
        for x, y in get_valid_moves(board):
            board[y][x] = PLAYER_AI_1
            _, _, eval = alpha_beta(board, depth - 1, alpha, beta, True, evaluate_func)
            board[y][x] = 0
            if eval < min_eval:
                min_eval = eval
                best_move = (x, y)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return *best_move, min_eval

def human_click(event):
    global current_player
    x = (event.x - BOARD_PADDING + CELL_SIZE // 2) // CELL_SIZE
    y = (event.y - BOARD_PADDING + CELL_SIZE // 2) // CELL_SIZE
    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[y][x] == 0:
        board[y][x] = PLAYER_HUMAN
        draw_piece(x, y, PLAYER_HUMAN)
        if check_win(board, PLAYER_HUMAN):
            canvas.create_text(WINDOW_SIZE // 2, WINDOW_SIZE - 10, text="You (White) win!", font="Helvetica 20", fill="red")
            root.after(3000, root.destroy)
            return
        current_player = PLAYER_AI_1
        canvas.unbind("<Button-1>")
        root.after(100, make_ai_move)

def make_ai_move():
    global current_player
    if game_mode == 'human_vs_ai':
        if current_player == PLAYER_AI_1:
            x, y, _ = minimax(board, MAX_DEPTH, True, evaluate_human_vs_ai)
            if x is not None:
                board[y][x] = PLAYER_AI_1
                draw_piece(x, y, PLAYER_AI_1)
                if check_win(board, PLAYER_AI_1):
                    canvas.create_text(WINDOW_SIZE // 2, WINDOW_SIZE - 10, text="AI (Black) wins!", font="Helvetica 20", fill="blue")
                    root.after(3000, root.destroy)
                    return
                canvas.bind("<Button-1>", human_click)
    elif game_mode == 'ai_vs_ai':
        if current_player == PLAYER_AI_1:
            x, y, _ = minimax(board, MAX_DEPTH, True, evaluate_ai_vs_ai)
        else:
            x, y, _ = alpha_beta(board, MAX_DEPTH, -math.inf, math.inf, True, evaluate_ai_vs_ai)
        if x is not None:
            board[y][x] = current_player
            draw_piece(x, y, current_player)
            if check_win(board, current_player):
                winner_text = "Minimax AI (Black) wins!" if current_player == PLAYER_AI_1 else "Alpha-Beta AI (Red) wins!"
                winner_color = "black" if current_player == PLAYER_AI_1 else "red"
                canvas.create_text(WINDOW_SIZE // 2, WINDOW_SIZE - 10, text=winner_text, font="Helvetica 20", fill=winner_color)
                root.after(3000, root.destroy)
                return
            current_player = PLAYER_AI_2 if current_player == PLAYER_AI_1 else PLAYER_AI_1
            root.after(300, make_ai_move)

def start_human_vs_ai():
    global game_mode, current_player
    game_mode = 'human_vs_ai'
    current_player = PLAYER_HUMAN
    board[:] = init_board()
    mode_frame.destroy()
    draw_board()
    canvas.bind("<Button-1>", human_click)

def start_ai_vs_ai():
    global game_mode, current_player
    game_mode = 'ai_vs_ai'
    current_player = PLAYER_AI_2
    board[:] = init_board()
    mode_frame.destroy()
    draw_board()

    valid = get_valid_moves(board)
    first_black = random.choice(valid)
    board[first_black[1]][first_black[0]] = PLAYER_AI_1
    draw_piece(first_black[0], first_black[1], PLAYER_AI_1)

    valid = get_valid_moves(board)
    first_red = random.choice(valid)
    board[first_red[1]][first_red[0]] = PLAYER_AI_2
    draw_piece(first_red[0], first_red[1], PLAYER_AI_2)

    current_player = PLAYER_AI_2
    root.after(500, make_ai_move)

root.mainloop()
