import chess
import pygame
import sys
import minimax
from draw import draw_game, draw_image_button, IMAGES, draw_text_button

pygame.init()
pygame.mixer.init()

move_sound1 = pygame.mixer.Sound("sounds/move1.mp3")
move_sound2 = pygame.mixer.Sound("sounds/move2.mp3")
capture_sound1 = pygame.mixer.Sound("sounds/capture1.mp3")
capture_sound2 = pygame.mixer.Sound("sounds/capture2.mp3")




# Propriétés du bouton pour inverser l'échiquier
INVERSE_BOARD_BUTTON_WIDTH = 40
INVERSE_BOARD_BUTTON_HEIGHT = 40

# Taille de la fenêtre
CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT = 512, 512
DIMENSION = 8  
SQ_SIZE = CHESSBOARD_HEIGHT // DIMENSION
MAX_FPS = 60  # Pour les animations

button_rect = pygame.Rect(0, CHESSBOARD_HEIGHT, INVERSE_BOARD_BUTTON_WIDTH, INVERSE_BOARD_BUTTON_HEIGHT)

# Propriétés du bouton de réinitialisation
RESET_BUTTON_WIDTH = 120
RESET_BUTTON_HEIGHT = 40
reset_button_rect = pygame.Rect(INVERSE_BOARD_BUTTON_WIDTH + 10, CHESSBOARD_HEIGHT, RESET_BUTTON_WIDTH, RESET_BUTTON_HEIGHT)
reset_button_color = pygame.Color('gray')
reset_button_text = 'New Game'





# Charger les images
def load_images():
    # Noms des pièces pour les images
    pieces = ['P', 'R', 'N', 'B', 'Q', 'K']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"images/w{piece.lower()}.png"), (SQ_SIZE, SQ_SIZE)) # majuscule pour white
        IMAGES[piece.lower()] = pygame.transform.scale(pygame.image.load(f"images/b{piece.lower()}.png"), (SQ_SIZE, SQ_SIZE)) # minuscule pour black
    



def main():

    human_color = chess.BLACK

    screen = pygame.display.set_mode((CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT + INVERSE_BOARD_BUTTON_HEIGHT))
    clock = pygame.time.Clock()
    board = chess.Board()
    load_images()
    reverse_board_image = pygame.transform.scale(pygame.image.load("images/reverse_board.png"), (INVERSE_BOARD_BUTTON_WIDTH, INVERSE_BOARD_BUTTON_HEIGHT))

   
    flip_board = True  # false = blanc en bas, true = noir en bas

    dragging_piece = None  # La pièce en cours de déplacement
    dragging_start_sq = None  # La case de départ de la pièce en déplacement

    mouse_x, mouse_y = 0, 0

    running = True
    while running:

        human_turn = board.turn == human_color
        

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[2]:
                    dragging_piece = None 
                    dragging_start_sq = None

                location = pygame.mouse.get_pos()  # Position (x, y) de la souris

                # Inverse l'échiquier
                if button_rect.collidepoint(location):
                    flip_board = not flip_board
                    continue

                # Reset de l'échiquier
                if reset_button_rect.collidepoint(location):
                    board.reset() 
                    continue
                
                if flip_board:
                    col = (CHESSBOARD_WIDTH - location[0]) // SQ_SIZE
                    row = location[1] // SQ_SIZE
                else:
                    col = location[0] // SQ_SIZE
                    row = (CHESSBOARD_HEIGHT - location[1]) // SQ_SIZE

                piece = board.piece_at(chess.square(col, row))
                if piece and (board.turn == piece.color):
                    dragging_piece = piece
                    dragging_start_sq = (col, row)

            elif e.type == pygame.MOUSEBUTTONUP and dragging_piece:
                location = pygame.mouse.get_pos()

                if flip_board:
                    col = (CHESSBOARD_WIDTH - location[0]) // SQ_SIZE
                    row = location[1] // SQ_SIZE
                else:
                    col = location[0] // SQ_SIZE
                    row = (CHESSBOARD_HEIGHT - location[1]) // SQ_SIZE

                source = chess.square_name(chess.square(dragging_start_sq[0], dragging_start_sq[1]))
                destination = chess.square_name(chess.square(col, row))

                if source != destination:
                    move = chess.Move.from_uci(source + destination)
                    if move in board.legal_moves:
                        if board.is_capture(move):
                            capture_sound1.play()
                        else:
                            move_sound1.play()
                        board.push(move)


                dragging_piece = None
                dragging_start_sq = None

            elif e.type == pygame.MOUSEMOTION and dragging_piece:
                mouse_x, mouse_y = pygame.mouse.get_pos()


        draw_image_button(screen, button_rect, reverse_board_image, pygame.Color('gray'))
        draw_text_button(screen, reset_button_rect, reset_button_text, reset_button_color)
        draw_game(screen, board, flip_board, dragging_start_sq)
        
        
        if dragging_piece:
            screen.blit(IMAGES[str(dragging_piece)], pygame.Rect(mouse_x - SQ_SIZE // 2, mouse_y - SQ_SIZE // 2, SQ_SIZE, SQ_SIZE))
        

        pygame.display.flip()
        clock.tick(MAX_FPS)


        # bot turn
        if not human_turn:
            ai_move = minimax.select_best_move(board, 3, chess.WHITE if human_color == chess.BLACK else chess.BLACK)
            if ai_move:
                if board.is_capture(ai_move):
                    capture_sound2.play()
                else:
                    move_sound2.play()
                board.push(ai_move)


        

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
