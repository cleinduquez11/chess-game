from tkinter import Tk, filedialog
import pygame
import chess
import sys
import Analysis
from moviepy.editor import VideoFileClip



print('Welcome to MMSU chess game')
def play_video(video_path):
    clip = VideoFileClip(video_path,audio=True,)
    # pygame.mixer.music.load(music_path)
    # pygame.mixer.music.play(-1)
    # clip = clip.resize(1707,1067)
    clip.fadein(7).fadeout(7)
    clip.preview(fullscreen=True, fps=24)
    # clip.preview(fps=24)
    return clip.w,clip.h
    # clip.preview()


w,h = play_video('chess.mp4')




def fade_in(screen, color=(0, 0, 0), duration=7):
    # Fade-in effect for Pygame screen
    clock = pygame.time.Clock()
    for alpha in range(0, 256):
        screen.fill(color)
        pygame.display.update()
        screen.set_alpha(alpha)
        clock.tick(256 / duration)


# Initialize Pygame
pygame.init()
# pygame.mixer.init()
info = pygame.display.Info()
# screen_width, screen_height = info.current_w, info.current_h
# print(screen_width,screen_height)
# screen_width, screen_height = 1280, 720
# square_size = screen_width // 14
# margin = 30
# panel_width = 220
# captured_width = 250
# captured_piece_size = square_size // 2




screen_width, screen_height = info.current_w, info.current_h
print(screen_width,screen_height)
screen_width, screen_height = 1280, 720
square_size = screen_width // 16
margin = 20
panel_width = 180
captured_width = 200
captured_piece_size = square_size // 2




screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Pygame Game')
screen.fill((0, 0, 0))

# Apply fade-in effect to Pygame screen
fade_in(screen)



BUTTON_WIDTH = 200
BUTTON_HEIGHT = 80

BUTTON_PADDING = 20  # Padding between buttons
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)
ORANGE_BUTTON_COLOR = (255, 165, 0)
ORANGE_BUTTON_HOVER_COLOR = (255, 140, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 40
NUM_BUTTONS = 3
TOTAL_BUTTON_HEIGHT = BUTTON_HEIGHT * NUM_BUTTONS
PADDING = (screen_height - TOTAL_BUTTON_HEIGHT) // (NUM_BUTTONS + 1)

BUTTON_txtfont = pygame.font.Font(None, FONT_SIZE)


# Initial configurations for setting up the display parameters of the game
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.FULLSCREEN

# screen.fill((255, 255, 255))


# pygame.time.wait(3000)



# screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
background_image = pygame.image.load('images/chess_1.jpg') 
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# This is the Name of the game
pygame.display.set_caption('Chess Game')

# This are the chess pieces and their respective ranks
piece_images = {}
pieces = ['r', 'n', 'b', 'q', 'k', 'p', 'R', 'N', 'B', 'Q', 'K', 'P']
pieces_trans = {'r': 'black rook', 'n': 'black knight', 'b': 'black bishop', 'q': 'black queen', 'k': 'black king', 'p': 'black pawn', 'R': 'white rook', 'N': 'white knight', 'B': 'white bishop', 'Q': 'white queen', 'K': 'white king', 'P': 'white pawn'}
for piece in pieces:
    image = pygame.image.load(f'images/{pieces_trans[piece]}.png')
    piece_images[piece] = pygame.transform.scale(image, (square_size, square_size))

# Initialize the chess board
board = chess.Board()

# Temporary storage for the captured pieces
captured_white = []
captured_black = []

# Timer variables (time in seconds)
# player1_time = 300  # 5 minutes
# player2_time = 300  # 5 minutes

player1_time = 60  # 5 minutes
player2_time = 60  # 5 minutes
turn = 1  # 1 for player 1's turn, 2 for player 2's turn

# Font for timer
font = pygame.font.Font(None, 45)
default_color = (255,168,0)
color1 = (255,255,255)
color2 = (255,255,255)



# Forfeit button
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (10, 255, 10)
forfeit_font = pygame.font.Font(None, 36)
FORFEIT_BUTTON_WIDTH, FORFEIT_BUTTON_HEIGHT = 150, 50
forfeit_button = pygame.Rect(screen_width - margin - captured_width - FORFEIT_BUTTON_WIDTH + 120, screen_height - FORFEIT_BUTTON_HEIGHT - 100, FORFEIT_BUTTON_WIDTH, FORFEIT_BUTTON_HEIGHT)




# Forfeit button
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# GREEN = (10, 255, 10)
# play_font = pygame.font.Font(None, 40)
# BUTTON_WIDTH, BUTTON_HEIGHT = 200, 80
# play_button = pygame.Rect(screen_width//2 -100, screen_height//2-250, BUTTON_WIDTH, BUTTON_HEIGHT)




# Clock to control framerate
clock = pygame.time.Clock()

# Function to format time
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

# This is the function for drawing the chess board in the UI
def draw_playing_board():
    colors = [(238, 238, 210), (118, 150, 86)]
    for rank in range(8):
        for file in range(8):
            color = colors[(rank + file) % 2]
            rect = pygame.Rect(file * square_size + margin + captured_width, rank * square_size + margin, square_size, square_size)
            pygame.draw.rect(screen, color, rect)

# This is the function for drawing the chess pieces in the UI
def draw_playing_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_image = piece_images[piece.symbol()]
            rank = 7 - (square // 8)
            file = square % 8
            screen.blit(piece_image, (file * square_size + margin + captured_width , rank * square_size + margin))

# This is the function in drawing chess coordinates in the board 
def draw_coordinates():
    font = pygame.font.Font(None, 24)
    for i in range(8):
        file_label = font.render(chr(ord('a') + i), True, (255, 255, 255))
        rank_label = font.render(str(8 - i), True, (255, 255, 255))
        screen.blit(file_label, (i * square_size + margin + square_size // 2 - file_label.get_width() // 2 + captured_width, screen_height - margin - 30))
        screen.blit(rank_label, (10 + captured_width, i * square_size + margin + square_size // 2 - rank_label.get_height() // 2))

# This is the function in displaying the move history of both player
def draw_move_history():
    pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(screen_width - margin * 2 - captured_width - 100, 30, panel_width, screen_height - 900))
    font = pygame.font.Font(None, 24)
    move_text = font.render("  Moves:", True, (255, 255, 255))
    screen.blit(move_text, (screen_width - margin * 2 - captured_width - 100, 30, panel_width, screen_height - 100))

    moves = list(board.move_stack)[-4:]
    y_offset = 60
    for i, move in enumerate(moves):
        move_number = (len(board.move_stack) - len(moves) + i) // 2 + 1
        try:
            color = (255, 255, 255) if i % 2 == 0 else (255, 255, 255)
            move_text = font.render(f'  {move_number}. {str(move)[-2:]}' if (len(board.move_stack) - len(moves) + i) % 2 == 0 else f'      {str(move)[-2:]}', True, color)
            screen.blit(move_text, (screen_width - margin * 2 - captured_width - 100, y_offset))
            if i % 2 == 0:
                y_offset += 20
            else:
                y_offset += 30
        except ValueError:
            move_text = font.render(f'      {str(move)}', True, (255, 0, 0))
            screen.blit(move_text, (screen_width - margin * 2 - captured_width - 100, 30 + i * 20))
            y_offset += 30

# This function will display the legal moves that the 
def highlight_squares(squares, color):
    for square in squares:
        rank = 7 - (square // 8)
        file = square % 8
        rect = pygame.Rect(file * square_size + margin + captured_width, rank * square_size + margin, square_size, square_size)
        pygame.draw.rect(screen, color, rect, 3)

# This function will get the current cursor position to identify what square is being pressed 
def get_square_under_mouse():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x < margin + captured_width or mouse_x >= 8 * square_size + margin + captured_width or mouse_y < margin or mouse_y >= 8 * square_size + margin:
        return None
    file = (mouse_x - margin - captured_width) // square_size
    rank = 7 - (mouse_y - margin) // square_size
    return chess.square(file, rank)

# This function will handle the logic for capturing chess pieces
def draw_captured_pieces():
    font = pygame.font.Font(None, 24)
    text = font.render("Captured Pieces:", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    
    y_offset_white = 40
    y_offset_black = 40
    for piece in captured_white:
        piece_image = piece_images[piece.symbol()]
        small_piece_image = pygame.transform.scale(piece_image, (captured_piece_size, captured_piece_size))
        screen.blit(small_piece_image, (10, y_offset_white))
        y_offset_white += captured_piece_size + 5

    for piece in captured_black:
        piece_image = piece_images[piece.symbol()]
        small_piece_image = pygame.transform.scale(piece_image, (captured_piece_size, captured_piece_size))
        screen.blit(small_piece_image, (90, y_offset_black))
        y_offset_black += captured_piece_size + 5

# This function will handle promotions
def draw_promotion_selection(color):
    rect = pygame.Rect(screen_width // 2 - square_size * 2, screen_height // 2 - square_size, square_size * 4, square_size)
    pygame.draw.rect(screen, (200, 200, 200), rect)

    pieces = ['q', 'r', 'b', 'n'] if color == chess.WHITE else ['Q', 'R', 'B', 'N']
    for i, piece in enumerate(pieces):
        piece_image = piece_images[piece]
        screen.blit(piece_image, (screen_width // 2 - square_size * 2 + i * square_size, screen_width // 2 - square_size))

# This function will handle the logic when the game is over
def draw_game_over(board,time1,time2, forfeit):
    if time1 <= 0:
        font = pygame.font.SysFont(None, 100)
        text_surface = font.render(f'Time\'s Over: Black wins!', True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_width // 2 - 60, screen_height // 2))
        screen.blit(text_surface, text_rect)
        all_parsed_moves = []
        all_moves = list(board.move_stack)
        with open('results/white_out_of_time_match.txt', 'w') as f:
            for i in all_parsed_moves:
                f.write(f'{str(i)}\n')
        pygame.display.flip()
        pygame.time.wait(5000)

    elif time2 <= 0:
        font = pygame.font.SysFont(None, 100)
        text_surface = font.render(f'Time\'s Over: White wins!', True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_width // 2 - 60, screen_height // 2))
        screen.blit(text_surface, text_rect)
        all_parsed_moves = []
        all_moves = list(board.move_stack)
        for i, move in enumerate(all_moves):
            all_parsed_moves.append(str(move))
        print(all_parsed_moves)
        with open('results/black_out_of_time_match.txt', 'w') as f:
            for i in all_parsed_moves:
                f.write(f'{str(i)}\n')
        pygame.display.flip()
        pygame.time.wait(5000)

    elif forfeit[0]:
        font = pygame.font.SysFont(None, 100)
        text_surface = font.render(f'Game is Over : {forfeit[1]} wins!', True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_width // 2 - 60, screen_height // 2))
        screen.blit(text_surface, text_rect)
        all_parsed_moves = []
        all_moves = list(board.move_stack)
        for i, move in enumerate(all_moves):
            all_parsed_moves.append(str(move))
        print(all_parsed_moves)
        with open('results/Forfeited_match.txt', 'w') as f:
            for i in all_parsed_moves:
                f.write(f'{str(i)}\n')
        pygame.display.flip()
        pygame.time.wait(5000)
   
    else:
        winner = "White" if board.outcome().winner else "Black"
        font = pygame.font.SysFont(None, 100)
        text_surface = font.render(f'Game Over: {winner} wins!', True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surface, text_rect)
        print(list(board.move_stack))
        all_parsed_moves = []
        all_moves = list(board.move_stack)

        for i, move in enumerate(all_moves):
            all_parsed_moves.append(str(move))
        print(all_parsed_moves)
        with open('results/Final_match.txt', 'w') as f:
            for i in all_parsed_moves:
                f.write(f'{str(i)}\n')
        pygame.display.flip()
        pygame.time.wait(5000)



# This function will make a surrender button in the UI
def surrender_button():
    pygame.draw.rect(screen, RED, forfeit_button)
    text = forfeit_font.render('Resign', True, WHITE)
    screen.blit(text, (forfeit_button.x + 30 , forfeit_button.y + 15))


# This function will handle the logic behind forfeiting the game
def forfeit_game(b_turn):
    global game_over, winner
    game_over = True
    print(b_turn)
    winner = "Black" if b_turn == "black" else "White"
    forfeit = [game_over,winner]
    draw_game_over(board,time1=player1_time,time2=player2_time, forfeit=forfeit)


# Function to draw buttons
def draw_button(screen, color, x, y, width, height, text=''):
    pygame.draw.rect(screen, color, (x, y, width, height))
    if text != '':
        text_surface = BUTTON_txtfont.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
        screen.blit(text_surface, text_rect)




def open_file_dialog():
    Tk().withdraw()  
    file_path = filedialog.askopenfilename()
    if file_path:
        return read_file(file_path)
    return None

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content





def draw_pop_up():
    font = pygame.font.SysFont(None, 100)
    text_surface = font.render(f'Feature is under development', True, (0, 0, 255))
    text_rect = text_surface.get_rect(center=(screen_width // 2 - 60, screen_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(1000)


# def show_popup(message):
#     popup_width, popup_height = 300, 150
#     popup_x = (screen_width - popup_width) // 2
#     popup_y = (screen_height - popup_height) // 2
#     popup_surface = pygame.Surface((popup_width, popup_height))
#     popup_surface.fill(WHITE)
#     pygame.draw.rect(popup_surface, RED, popup_surface.get_rect(), 2)
#     text_surface = font.render(message, True, BLACK)
#     text_rect = text_surface.get_rect(center=(popup_width // 2, popup_height // 2))
#     popup_surface.blit(text_surface, text_rect)
#     screen.blit(popup_surface, (popup_x, popup_y))
#     pygame.display.flip()





# def play_video(video_path):
#     # Initialize Pygame
#     pygame.init()

#     # Set up the display in fullscreen mode
#     screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#     pygame.display.set_caption('Fullscreen Video')

#     # Get the screen dimensions
#     screen_width, screen_height = screen.get_size()

#     # Load the video using moviepy
#     clip = VideoFileClip(video_path, audio=True)

#     # Resize the video to fit the screen dimensions
#     clip_resized = clip.resize(newsize=(screen_width, screen_height))

#     # Get the video frame generator
#     video_frames = clip_resized.iter_frames()

#     # Get the audio if available
#     # if clip.audio:
#     #     audio = clip.audio.to_soundarray()
#     #     sound = pygame.mixer.Sound(audio)
#     #     sound.play()

#     # Main loop to display the video
#     running = True
#     clock = pygame.time.Clock()
#     for frame in video_frames:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     running = False

#         # Convert the frame to a Pygame surface
#         frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
#         frame_surface = pygame.transform.scale(frame_surface, (screen_width, screen_height))

#         # Display the frame
#         screen.blit(frame_surface, (0, 0))
#         pygame.display.flip()

#         # Control the frame rate
#         clock.tick(clip.fps)

#         if not running:
#             break

#     # Quit Pygame
#     pygame.quit()
#     # sys.exit()


# def play_video(video_path, fps, music_path):
#     clip = VideoFileClip(video_path)
#     pygame.mixer.music.load(music_path)
#     pygame.mixer.music.play(-1)
#     clip_resized = clip.resize(height=screen_height, width = screen_width)

#     for frame in clip_resized.iter_frames(fps=fps, dtype='uint8'):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
        
#         frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
#         screen.blit(frame_surface, (0, 0))
#         pygame.display.flip()
#         clock.tick(fps)

# play_video('chess.mp4',12, 'bini.mp3')




# This function will execute the main thread and runs a game loop
def main():
    running = True
    selected_square = None
    legal_moves = []
    promoting = False
    promotion_square = None
    state = 'menu'
    b_turn = True
    game_started = False
    file_content = None
    run_once = True
    progress_val = 50
    sg_moves = []
    moves = []
    show_notification = False
    global captured_white, captured_black, player1_time, player2_time, turn
    analysis = Analysis.Analysis(moves)
    while running:
        if state == 'menu':
            screen.blit(background_image, (0, 0))
            
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            button_x = (screen_width - BUTTON_WIDTH) / 2
            button_y = PADDING
            button_y_analysis = button_y + BUTTON_HEIGHT + PADDING
            button_y_spectate = button_y_analysis + BUTTON_HEIGHT + PADDING



            if button_x < mouse[0] < button_x + BUTTON_WIDTH and button_y < mouse[1] < button_y + BUTTON_HEIGHT:
                if click[0] == 1:
                    state = 'mode'
                    pygame.time.wait(500)
                draw_button(screen, BUTTON_HOVER_COLOR, button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, 'Play')

            else:
                draw_button(screen, BUTTON_COLOR, button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, 'Play')



            if button_x < mouse[0] < button_x + BUTTON_WIDTH and button_y_analysis < mouse[1] < button_y_analysis + BUTTON_HEIGHT:
                draw_button(screen, ORANGE_BUTTON_HOVER_COLOR, button_x, button_y_analysis, BUTTON_WIDTH, BUTTON_HEIGHT, 'Analysis')
                if click[0] == 1:
                    file_content = open_file_dialog()
                    state = 'analysis'
            else:
                draw_button(screen, ORANGE_BUTTON_COLOR, button_x, button_y_analysis, BUTTON_WIDTH, BUTTON_HEIGHT, 'Analysis')

            if button_x < mouse[0] < button_x + BUTTON_WIDTH and button_y_spectate < mouse[1] < button_y_spectate + BUTTON_HEIGHT:
                draw_button(screen, ORANGE_BUTTON_HOVER_COLOR, button_x, button_y_spectate, BUTTON_WIDTH, BUTTON_HEIGHT, 'Spectate')
                if click[0] == 1:
                    screen.fill((255, 255, 255))
                    screen.blit(background_image, (0, 0))
                    draw_pop_up()
            else:
                draw_button(screen, ORANGE_BUTTON_COLOR, button_x, button_y_spectate, BUTTON_WIDTH, BUTTON_HEIGHT, 'Spectate')



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False



        elif state == 'analysis':       
            if file_content:
                lines = file_content.split('\n')
                moves = lines[:-1]
            if run_once:
                analysis.moves = moves          
                print(analysis.moves)
                run_once = False

                        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        nb = chess.Board()
                        fw = analysis.move_forward()
                        for move in moves[:fw]:
                            nb.push_uci(move)


                        print(f'{nb}')

                        best_moves, score = analysis.analyze_next_moves(nb,  num_moves=6)
                        sg_moves = best_moves

                        if nb.is_game_over():
                            analysis.draw_game_over(board=nb,screen=screen,time1=player1_time,time2=player2_time,forfeit=[False,''])



                        if score == 9999:
                            normalized_score = 100
                        elif score == -9999:
                            normalized_score = -100
                        else:
                            normalized_score = max(0, min(100, (score / 100) + 50))



                        progress_val = normalized_score

                        print(f'Score: {progress_val}')



                    elif event.key == pygame.K_LEFT:
                        analysis.move_backward()

            screen.blit(background_image, (0, 0))
            analysis.draw_playing_board(screen=screen)
            analysis.draw_playing_pieces(screen=screen,piece_images=piece_images)
            analysis.draw_coordinates(screen=screen)
            analysis.draw_move_history(screen=screen, moves=analysis.displayed_moves)
            analysis.draw_analysis_panel(screen, sg_moves)
            analysis.draw_progress_bar(screen=screen, value=progress_val)


        elif state == 'mode':
            screen.fill((255, 255, 255))
            screen.blit(background_image, (0, 0))

            mouse1 = pygame.mouse.get_pos()
            click1 = pygame.mouse.get_pressed()

            button_x = (screen_width - BUTTON_WIDTH) / 2 
            button_y = PADDING 
            button_y_analysis = button_y + BUTTON_HEIGHT + PADDING
            button_y_spectate = button_y_analysis + BUTTON_HEIGHT + PADDING
            


            if button_x < mouse1[0] < button_x + BUTTON_WIDTH and button_y < mouse1[1] < button_y + BUTTON_HEIGHT:
                if click1[0] == 1:
                    screen.fill((255, 255, 255))
                    screen.blit(background_image, (0, 0))
                    draw_pop_up()
                draw_button(screen, ORANGE_BUTTON_HOVER_COLOR, button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, 'Swiss')

            else:
                draw_button(screen, ORANGE_BUTTON_COLOR, button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, 'Swiss')


            if button_x < mouse1[0] < button_x + BUTTON_WIDTH and button_y_analysis < mouse1[1] < button_y_analysis + BUTTON_HEIGHT:
                draw_button(screen, ORANGE_BUTTON_HOVER_COLOR, button_x, button_y_analysis, BUTTON_WIDTH, BUTTON_HEIGHT, 'Round Robin')
                if click1[0] == 1:
                    screen.fill((255, 255, 255))
                    screen.blit(background_image, (0, 0))
                    draw_pop_up()
            else:
                draw_button(screen, ORANGE_BUTTON_COLOR, button_x, button_y_analysis, BUTTON_WIDTH, BUTTON_HEIGHT, 'Round Robin')

            if button_x < mouse1[0] < button_x + BUTTON_WIDTH and button_y_spectate < mouse1[1] < button_y_spectate + BUTTON_HEIGHT:
                draw_button(screen, ORANGE_BUTTON_HOVER_COLOR, button_x, button_y_spectate, BUTTON_WIDTH, BUTTON_HEIGHT, 'Knockout')
                if click1[0] == 1:
                    state = 'Knockout'
            else:
                draw_button(screen, ORANGE_BUTTON_COLOR, button_x, button_y_spectate, BUTTON_WIDTH, BUTTON_HEIGHT, 'Knockout')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False



        elif state == 'Knockout':
            screen.fill((255, 255, 255))
            screen.blit(background_image, (0, 0))
            surrender_button()
            draw_playing_board()
            draw_coordinates()
            draw_move_history()
            draw_captured_pieces()
            draw_playing_pieces()
            if promoting:
                draw_promotion_selection(board.turn)

            if board.is_game_over():
                draw_game_over(board=board,time1=player1_time,time2=player2_time,forfeit=[False,''])
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    square = get_square_under_mouse()
                    if forfeit_button.collidepoint(event.pos):
                        if b_turn:
                            forfeit_game('black')
                            running = False
                        else:
                            forfeit_game('white')
                            running = False
                            
                    if square is not None:
                        piece = board.piece_at(square)
                        if selected_square is None:
                            if piece is not None and piece.color == board.turn:
                                selected_square = square
                                legal_moves = [move.to_square for move in board.legal_moves if move.from_square == square]
                        else:
                            move = chess.Move(selected_square, square)
                            if move in board.legal_moves:
                                if board.is_capture(move):
                                    captured_piece = board.piece_at(square)
                                    if captured_piece.color == chess.WHITE:
                                        captured_white.append(captured_piece)
                                    else:
                                        captured_black.append(captured_piece)
                                if chess.square_rank(square) == 7 and board.piece_type_at(selected_square) == chess.PAWN and board.turn == chess.WHITE:
                                    promoting = True
                                    promotion_square = square
                                elif chess.square_rank(square) == 0 and board.piece_type_at(selected_square) == chess.PAWN and board.turn == chess.BLACK:
                                    promoting = True
                                    promotion_square = square
                                else:
                                    board.push(move)
                                    game_started = True
                                    b_turn = not b_turn
                                    turn = 3 - turn  
                            selected_square = None
                            legal_moves = []

            highlight_squares(legal_moves, (0, 255, 0))
            if selected_square is not None:
                highlight_squares([selected_square], (255, 0, 0))

            # Update timers
            if game_started:
                if turn == 1:
                    player1_time -= clock.get_time() / 1000
                    color1 = (0, 255, 45)
                    color2 = default_color
                else:
                    color1 = default_color
                    color2 = (0, 255, 45)
                    player2_time -= clock.get_time() / 1000

                if player1_time <= 0 or player2_time <= 0:
                    draw_game_over(board=board,time1=player1_time,time2=player2_time, forfeit=[False,''])
                    running = False 

                player1_timer_text = font.render(f"White: {format_time(int(player1_time))}", True, color1)
                player2_timer_text = font.render(f"Black: {format_time(int(player2_time))}", True, color2)
                screen.blit(player1_timer_text, (margin + captured_width + 8 * square_size + 60, (screen_height//2 - 60)+60))
                screen.blit(player2_timer_text, (margin + captured_width + 8 * square_size + 60, (screen_height//2 - 60)))
            else:
                player1_timer_text = font.render(f"White: {format_time(int(player1_time))}", True, default_color)
                player2_timer_text = font.render(f"Black: {format_time(int(player2_time))}", True, default_color)
                screen.blit(player1_timer_text, (margin + captured_width + 8 * square_size + 60, (screen_height//2 - 60)+60))
                screen.blit(player2_timer_text, (margin + captured_width + 8 * square_size + 60, (screen_height//2 - 60)))



        pygame.display.flip()
        clock.tick(30) 

# Call main loop
main()

# Quit Pygame
pygame.quit()
sys.exit()
