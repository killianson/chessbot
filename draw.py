import pygame
import chess

DIMENSION = 8 
CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT = 512, 512
SQ_SIZE = CHESSBOARD_HEIGHT // DIMENSION
IMAGES = {}

# Dessiner l'échiquier et les pièces
def draw_game(screen, board, flip_board, dragging_start_sq=None):
    draw_board(screen)  # Dessiner les cases de l'échiquier
    draw_pieces(screen, board, flip_board, dragging_start_sq)  # Dessiner les pièces sur l'échiquier

def draw_board(screen):
    colors = [pygame.Color(255, 247, 226), pygame.Color(180, 210, 130)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
"""
def draw_pieces(screen, board, flip_board, dragging_start_sq):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if (c, r) != dragging_start_sq:
                piece = board.piece_at(chess.square(c, r))
                if piece:                        
                    piece_str = str(piece).upper() if piece.color == chess.WHITE else str(piece).lower()
                    if flip_board:
                        screen.blit(IMAGES[piece_str], pygame.Rect((7-c)*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    else:
                        screen.blit(IMAGES[piece_str], pygame.Rect(c*SQ_SIZE, (7-r)*SQ_SIZE, SQ_SIZE, SQ_SIZE))
"""

def draw_pieces(screen, board, flip_board, dragging_start_sq):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if (c, r) != dragging_start_sq:
                piece = board.piece_at(chess.square(c, r))
                if piece:
                    piece_str = str(piece).upper() if piece.color == chess.WHITE else str(piece).lower()
                    if flip_board:
                        screen.blit(IMAGES[piece_str], pygame.Rect((7-c)*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    else:
                        screen.blit(IMAGES[piece_str], pygame.Rect(c*SQ_SIZE, (7-r)*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_image_button(screen, rect, image, color):
    pygame.draw.rect(screen, color, rect)
    # Blitter l'image du bouton par-dessus le fond
    screen.blit(image, rect)

def draw_text_button(screen, rect, text, color):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.SysFont(None, 24)
    text_render = font.render(text, True, pygame.Color('black'))
    text_rect = text_render.get_rect(center=rect.center)
    screen.blit(text_render, text_rect)
