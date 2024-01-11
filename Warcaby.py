import pygame
import sys

class Warcaby:
    def __init__(self):
        pygame.init()
        self.width, self.height = 400, 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Warcaby")

        self.board = [[None] * 8 for _ in range(8)]
        self.current_player = 'red'
        self.selected_piece = None
        self.red_count = 0
        self.blue_count = 0
        self.create_board()
        self.place_pieces()

        self.clock = pygame.time.Clock()

    def create_board(self):
        self.black_square = (0, 0, 0)
        self.white_square = (255, 255, 255)
        self.square_size = self.width // 8

        for row in range(8):
            for col in range(8):
                color = self.black_square if (row + col) % 2 == 1 else self.white_square
                pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def draw_piece(self, col, row, color):
        pygame.draw.circle(self.screen, color, (col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2), self.square_size // 2 - 10)

    def place_pieces(self):
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 'red'
                    self.red_count += 1
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 'blue'
                    self.blue_count += 1

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // self.square_size
                    row = event.pos[1] // self.square_size
                    self.handle_click(row, col)

            self.draw_board()

            # Sprawdź warunek zwycięstwa i wyświetl odpowiedni komunikat
            if self.red_count == 0:
                self.display_winner("Wygrał gracz niebieski")
            elif self.blue_count == 0:
                self.display_winner("Wygrał gracz czerwony")
            else:
                pygame.display.flip()

            self.clock.tick(60)

    def draw_board(self):
        self.create_board()
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == 'red':
                    self.draw_piece(col, row, (255, 0, 0))
                elif self.board[row][col] == 'blue':
                    self.draw_piece(col, row, (0, 0, 255))

    def handle_click(self, row, col):
        piece = self.board[row][col]

        if self.selected_piece is None:
            if piece is not None and piece == self.current_player:
                self.selected_piece = (row, col)
        else:
            dest_row, dest_col = row, col
            if piece is not None and piece == self.current_player:
                self.selected_piece = (row, col)
            elif self.is_enemy_piece() and self.is_valid_capture(dest_row, dest_col):
                self.capture_piece(dest_row, dest_col)
                if self.can_continue_capture(dest_row, dest_col):
                    # Jeśli możliwe jest kolejne bicie, nie zmieniaj gracza
                    self.selected_piece = (dest_row, dest_col)
                else:
                    self.switch_player()
            elif not self.is_enemy_piece() and self.is_valid_move(dest_row, dest_col):
                self.move_piece(dest_row, dest_col)
                self.switch_player()


    def can_continue_capture(self, row, col):
        # Sprawdź, czy możliwe jest kolejne bicie z aktualnej pozycji
        self.selected_piece = (row, col)
        return self.is_enemy_piece()
                    
    def is_enemy_piece(self):
        row, col = self.selected_piece
        enemy_row = row + 1
        enemy_col = col + 1
        enemy_row2 = row - 1
        enemy_col2 = col - 1

        valid_move1 = (
            0 <= enemy_row < 8
            and 0 <= enemy_col < 8
            and self.board[enemy_row][enemy_col] is not None
            and self.board[enemy_row][enemy_col] != self.current_player
            and (enemy_row + 1 < 8 and enemy_col + 1 < 8)
            and self.board[enemy_row + 1][enemy_col + 1] is None
        )

        valid_move2 = (
            0 <= enemy_row2 < 8
            and 0 <= enemy_col2 < 8
            and self.board[enemy_row2][enemy_col2] is not None
            and self.board[enemy_row2][enemy_col2] != self.current_player
            and (enemy_row2 - 1 >= 0 and enemy_col2 - 1 >= 0)
            and self.board[enemy_row2 - 1][enemy_col2 - 1] is None
        )

        valid_move3 = (
            0 <= enemy_row < 8
            and 0 <= enemy_col2 < 8
            and self.board[enemy_row][enemy_col2] is not None
            and self.board[enemy_row][enemy_col2] != self.current_player
            and (enemy_row + 1 < 8 and enemy_col2 - 1 >= 0)
            and self.board[enemy_row + 1][enemy_col2 - 1] is None
        )

        valid_move4 = (
            0 <= enemy_row2 < 8
            and 0 <= enemy_col < 8
            and self.board[enemy_row2][enemy_col] is not None
            and self.board[enemy_row2][enemy_col] != self.current_player
            and (enemy_row2 - 1 >= 0 and enemy_col + 1 < 8)
            and self.board[enemy_row2 - 1][enemy_col + 1] is None
        )

        return any([valid_move1, valid_move2, valid_move3, valid_move4])
        
    def is_valid_move(self, dest_row, dest_col):
        row, col = self.selected_piece
        if (dest_row + dest_col) % 2 != 1:
            return False

        # Pionki czerwone mogą poruszać się tylko w dół
        if self.current_player == 'red' and dest_row - row == 1 and abs(dest_col - col) == 1:
            return self.board[dest_row][dest_col] is None

        # Pionki niebieskie mogą poruszać się tylko w górę
        elif self.current_player == 'blue' and dest_row - row == -1 and abs(dest_col - col) == 1:
            return self.board[dest_row][dest_col] is None

        return False

    def is_valid_capture(self, dest_row, dest_col):
        row, col = self.selected_piece
        if (dest_row + dest_col) % 2 != 1:
            return False

        enemy_row = (dest_row + row) // 2
        enemy_col = (dest_col + col) // 2
        if (
            self.board[enemy_row][enemy_col] is not None
            and self.board[enemy_row][enemy_col] != self.current_player
            and self.board[dest_row][dest_col] is None):
                return abs(dest_row - row) == 2 and abs(dest_col - col) == 2

        return False
    
    def move_piece(self, dest_row, dest_col):
        row, col = self.selected_piece
        self.board[dest_row][dest_col] = self.board[row][col]
        self.board[row][col] = None
        self.selected_piece = None

    def capture_piece(self, dest_row, dest_col):
        row, col = self.selected_piece
        enemy_row = (dest_row + row) // 2
        enemy_col = (dest_col + col) // 2

        self.board[dest_row][dest_col] = self.board[row][col]
        self.board[row][col] = None
        self.board[enemy_row][enemy_col] = None
        self.selected_piece = None

        if self.current_player == 'red':
            self.blue_count -= 1
        else:
            self.red_count -= 1

    def switch_player(self):
        self.current_player = 'blue' if self.current_player == 'red' else 'red'

    def display_winner(self, winner_text):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render(winner_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(10000)  # Wyświetl napis przez 3 sekundy przed zakończeniem gry
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Warcaby()
    game.run_game()