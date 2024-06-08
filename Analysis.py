import pygame
import chess
import chess.engine




# screen_width, screen_height = info.current_w, info.current_h
# print(screen_width,screen_height)
# screen_width, screen_height = 1280, 720
# square_size = screen_width // 16
# margin = 20
# panel_width = 180
# captured_width = 200
# captured_piece_size = square_size // 2



class Analysis:
    def __init__(self, moves):
        self.board = chess.Board()
        self.moves = moves
        self.move_index = 0
        self.displayed_moves = []
        # self.suggested_moves = []
        self.score = ''
        self.scores = []
        self.info = pygame.display.Info()
        self.screen_width, self.screen_height = 1280, 720
        self.square_size = self.screen_width // 16
        self.margin = 20
        self.panel_width = 180
        self.captured_width = 200
        self.captured_piece_size = self.square_size // 2
        self.move_history_panel_height = 400
        self.analysis_panel_height = 300

    def move_forward(self):
        if self.move_index < len(self.moves):
            self.board.push_uci(self.moves[self.move_index])
            self.displayed_moves.append(self.moves[self.move_index])
            # self.suggested_moves = self.analyze_position()
            self.move_index += 1
            self.scores.append(self.score)
            return self.move_index 

    def move_backward(self):
        if self.move_index > 0:
            self.board.pop()
            self.displayed_moves.pop()
            # self.suggested_moves = self.analyze_position()
            self.move_index -= 1


    # This is the function for drawing the chess board in the UI
    def draw_playing_board(self, screen):
        colors = [(238, 238, 210), (118, 150, 86)]
        for rank in range(8):
            for file in range(8):
                color = colors[(rank + file) % 2]
                rect = pygame.Rect(file * self.square_size + self.margin + self.captured_width, rank * self.square_size + self.margin, self.square_size, self.square_size)
                pygame.draw.rect(screen, color, rect)

    # This is the function for drawing the chess pieces in the UI
    def draw_playing_pieces(self,screen,piece_images):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                piece_image = piece_images[piece.symbol()]
                rank = 7 - (square // 8)
                file = square % 8
                screen.blit(piece_image, (file * self.square_size + self.margin + self.captured_width , rank * self.square_size + self.margin))


    def draw_coordinates(self, screen):
        font = pygame.font.Font(None, 24)
        for i in range(8):
            file_label = font.render(chr(ord('a') + i), True, (255, 255, 255))
            rank_label = font.render(str(8 - i), True, (255, 255, 255))
            screen.blit(file_label, (i * self.square_size + self.margin + self.square_size // 2 - file_label.get_width() // 2 + self.captured_width, self.screen_height - self.margin - 30))
            screen.blit(rank_label, (10 + self.captured_width, i * self.square_size + self.margin + self.square_size // 2 - rank_label.get_height() // 2))


    def draw_move_history(self, moves, screen):
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(self.screen_width - self.margin * 2 - self.captured_width - 100, 30, self.panel_width, self.screen_height - 900))
        font = pygame.font.Font(None, 24)
        move_text = font.render("Moves:", True, (255, 255, 255))
        screen.blit(move_text, (self.screen_width - self.margin * 2 - self.captured_width - 100, 30, self.panel_width, self.screen_height - 100))

        index = len(moves) 
        latest_values = moves[max(0, index-4):index] 
        y_offset = 60
        for i, move in enumerate(latest_values):


            move_number = (len(moves) - len(latest_values) + i) // 2 + 1
            try:
                color = (255, 255, 255) if i % 2 == 0 else (255, 255, 255)
                move_text = font.render(f'  {move_number}. {str(move)[-2:]}' if (len(moves) - len(latest_values) + i) % 2 == 0 else f'      {str(move)[-2:]}', True, color)
                screen.blit(move_text, (self.screen_width - self.margin * 2 - self.captured_width - 100, y_offset))
                if i % 2 == 0:
                    y_offset += 10
                else:
                    y_offset += 10
            except ValueError:
                move_text = font.render(f'      {str(move)}', True, (255, 0, 0))
                screen.blit(move_text, (self.screen_width - self.margin * 2 - self.captured_width - 100, 30 + i * 20))
            y_offset += 30


    def draw_analysis_panel(self, screen, suggested_moves):
        font = pygame.font.Font(None, 24)
        panel_y = self.margin + self.move_history_panel_height + 30  
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(self.screen_width - self.margin * 2 - self.captured_width - 100, self.screen_height//2 +80, self.panel_width, self.screen_height - 700))
        analysis_text = font.render("Best Moves:", True, (0,0,0))
        screen.blit(analysis_text, (self.screen_width - self.margin * 2 - self.captured_width - 100, self.screen_height//2 + 80))

        for i, move in enumerate(suggested_moves):
            move_text = font.render(f'{i + 1}. {move}', True, (255,255,255))
            screen.blit(move_text, (self.screen_width - self.margin * 2 - self.captured_width - 100, panel_y + 30 + i * 20))


    def analyze_next_moves(self, board, num_moves=6):
        with chess.engine.SimpleEngine.popen_uci("stockfish\stockfish-windows-x86-64.exe") as engine:
            info = engine.analyse(board, chess.engine.Limit(depth=5))
            sc = 0

            # Get the principal variation (best move sequence)
            try:
                pv = info['pv']
                score = info['score'].relative.score()
                if score is None: 
                    if board.is_checkmate():
                        score = -9999 if board.turn == chess.WHITE else 9999
                    else:
                        score = 0

                return pv[:num_moves], score
            
            except:
                score = info['score'].relative.score()
                if score is None:
                    if board.is_checkmate():
                        score = -9999 if board.turn == chess.WHITE else 9999
                    else:
                        score = 0

                return [], score
            


    def draw_progress_bar(self,screen, value):
        bar_width = 15
        bar_height = self.square_size *8
        x, y = 860, 20
        midpoint = y + bar_height // 2
        pygame.draw.rect(screen, (169, 169, 169), (x, y, bar_width, bar_height))
        progress_height = (bar_height * value) / 100
        pygame.draw.rect(screen, (0,0,0), (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, (169, 169, 169), (x, y + bar_height - progress_height, bar_width, progress_height))



    def draw_game_over(self,screen,board,time1,time2, forfeit):
        if time1 <= 0:
            font = pygame.font.SysFont(None, 100)
            text_surface = font.render(f'Time\'s Over: Black wins!', True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2 - 60, self.screen_height // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.wait(5000)

        elif time2 <= 0:
            font = pygame.font.SysFont(None, 100)
            text_surface = font.render(f'Time\'s Over: White wins!', True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2 - 60, self.screen_height // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.wait(5000)

        elif forfeit[0]:
            font = pygame.font.SysFont(None, 100)
            text_surface = font.render(f'Game is Over : {forfeit[1]} wins!', True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2 - 60, self.screen_height // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.wait(5000)
    
        else:
            winner = "White" if board.outcome().winner else "Black"
            font = pygame.font.SysFont(None, 100)
            text_surface = font.render(f'Game Over: {winner} wins!', True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.wait(5000)
