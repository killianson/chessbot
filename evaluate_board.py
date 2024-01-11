import chess


def evaluate_board(board):
    eval = 0
    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    king_safety_penalty = 0.5
    promotion_bonus = 0.5
    control_bonus = 0.02  # Bonus pour chaque case contrôlée

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

            # Compte du matériel
            value = 1 if piece.piece_type == chess.PAWN else 3 if piece.piece_type in [chess.KNIGHT,
                                                                                       chess.BISHOP] else 5 if piece.piece_type == chess.ROOK else 9 if piece.piece_type == chess.QUEEN else 0
            if piece.color == chess.WHITE:
                eval += value

                # Pion proche de la promotion
                if piece.piece_type == chess.PAWN and chess.square_rank(sq) >= 6:
                    eval += promotion_bonus
            else:
                eval -= value

                # Pion proche de la promotion
                if piece.piece_type == chess.PAWN and chess.square_rank(sq) <= 1:
                    eval -= promotion_bonus

            # Contrôle du centre
            attacks = board.attacks(sq)
            for center_sq in center_squares:
                if center_sq in attacks:
                    eval += 0.2 if piece.color == chess.WHITE else -0.2



    eval += controlled_squares_evaluation(board, control_bonus)
    eval += king_safety_evaluation(board, king_safety_penalty)

    return eval


def controlled_squares_evaluation(board, control_bonus=0.02):
    eval = 0
    # Comptez le nombre de cases distinctes contrôlées par chaque couleur
    white_controlled_squares = set()
    black_controlled_squares = set()

    for move in board.legal_moves:
        if move.from_square != move.to_square:  # Exclure les mouvements de roque
            if board.color_at(move.from_square) == chess.WHITE:
                white_controlled_squares.add(move.to_square)
            else:
                black_controlled_squares.add(move.to_square)

    eval += len(white_controlled_squares) * control_bonus
    eval -= len(black_controlled_squares) * control_bonus
    return eval

def king_safety_evaluation(board, king_safety_penalty=0.5):
    eval = 0
    # Évaluation de la sécurité du roi
    white_king_square = board.king(chess.WHITE)
    black_king_square = board.king(chess.BLACK)

    # Pénalité si le roi n'a pas roqué ou est potentiellement en danger
    if not board.has_castling_rights(chess.WHITE) or board.is_attacked_by(chess.BLACK, white_king_square):
        eval -= king_safety_penalty
    if not board.has_castling_rights(chess.BLACK) or board.is_attacked_by(chess.WHITE, black_king_square):
        eval += king_safety_penalty

    return eval