import chess
import random
from evaluate_board import evaluate_board


def select_best_move(board, depth, color):
    try:
        best_moves = []
        threshold = 0.1  # Seuil de proximité pour l'utilité des coups

        best_value = -float('inf') if color == chess.WHITE else float('inf')
        compare = max if color == chess.WHITE else min

        for move in board.legal_moves:
            board.push(move)
            board_value = minimax(board, depth, -float('inf'), float('inf'), color == chess.BLACK)
            board.pop()

            # Mise à jour de la meilleure valeur et réinitialisation des meilleurs coups si nécessaire
            if compare(board_value, best_value) == board_value:
                if abs(board_value - best_value) > threshold:
                    best_moves = [(move, board_value)]
                else:
                    best_moves.append((move, board_value))
                best_value = board_value
            elif abs(board_value - best_value) <= threshold:
                best_moves.append((move, board_value))

        # Limiter à trois meilleurs coups
        best_moves = sorted(best_moves, key=lambda x: x[1], reverse=(color == chess.WHITE))[:3]

        if len(best_moves) > 1:
            return random.choice(best_moves)[0]
        else:
            return best_moves[0][0]

    except Exception as e:
        print(e)
        return None


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    moves = list(board.legal_moves)
    # Trier les mouvements : les captures d'abord, puis les autres mouvements
    moves.sort(key=lambda move: (board.is_capture(move), move), reverse=True)

    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


