import chess
import random


def select_best_move(board, depth, color):
    try:
        best_moves = []
        best_value = -float('inf')
        threshold = 0.5  # Seuil de proximité pour l'utilité des coups

        for move in board.legal_moves:
            board.push(move)
            board_value = minimax(board, depth - 1, -float('inf'), float('inf'), color == chess.BLACK)
            board.pop()
            if board_value > best_value:
                best_value = board_value
                best_moves = [(move, board_value)]
            elif board_value >= best_value - threshold:
                best_moves.append((move, board_value))

        if len(best_moves) > 1:
            return random.choice(best_moves)[0]
        else:
            return best_moves[0][0]

    except Exception as e:
        print(e)
        return None


def evaluate_board(board):
    eval = 0
    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    king_safety_penalty = 1

    if board.is_checkmate():
        if board.turn:
            return -9999  # Noir gagne
        else:
            return 9999  # Blanc gagne
    if board.is_stalemate() or board.is_insufficient_material():
        return 0  # Match nul
    

    # Évaluation du matériel
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            value = 1 if piece.piece_type == chess.PAWN else 3 if piece.piece_type in [chess.KNIGHT, chess.BISHOP] else 5 if piece.piece_type == chess.ROOK else 9 if piece.piece_type == chess.QUEEN else 0
            eval += value if piece.color == chess.WHITE else -value

            # Bonus pour le contrôle des cases centrales
            if sq in center_squares:
                eval += 0.5 if piece.color == chess.WHITE else -0.5

            # Bonus pour le contrôle des cases centrales
            attacks = board.attacks(sq)
            for center_sq in center_squares:
                if center_sq in attacks:
                    eval += 0.2 if piece.color == chess.WHITE else -0.2


    # Évaluation de la sécurité du roi
    white_king_square = board.king(chess.WHITE)
    black_king_square = board.king(chess.BLACK)

    # Pénalité si le roi n'a pas roqué ou est potentiellement en danger
    if not board.has_castling_rights(chess.WHITE) or board.is_attacked_by(chess.BLACK, white_king_square):
        eval -= king_safety_penalty
    if not board.has_castling_rights(chess.BLACK) or board.is_attacked_by(chess.WHITE, black_king_square):
        eval += king_safety_penalty

    return eval


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
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

# Exemple d'utilisation dans le jeu
# move = select_best_move(board, 2)  # où 2 est la profondeur
