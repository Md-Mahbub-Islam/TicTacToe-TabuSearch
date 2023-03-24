import pygame
import random

# initialize Pygame
pygame.init()

# set the window size
window_size = (300, 300)

# create the Pygame window
screen = pygame.display.set_mode(window_size)

# set the window title
pygame.display.set_caption("Tic Tac Toe")

# set the font for the game text
font = pygame.font.SysFont('Arial', 30)

class TicTacToe:
    def __init__(self):
        self.board = ["", "", "", "", "", "", "", "", ""]
        self.current_player = "X"
        self.game_over = False

    def draw_board(self):
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(screen, (255, 255, 255), (i * 100, j * 100, 100, 100), 2)
                text = font.render(self.board[j * 3 + i], True, (255, 255, 255))
                screen.blit(text, (i * 100 + 35, j * 100 + 30))

    def draw_text(self, text, fontsize, color, x,y):
        font = pygame.font.SysFont('Arial', fontsize)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    def get_winner(self):
        for i in range(3):
            if self.board[i * 3] == self.board[i * 3 + 1] == self.board[i * 3 + 2] != "":
                return self.board[i * 3]
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != "":
                return self.board[i]
        if self.board[0] == self.board[4] == self.board[8] != "":
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != "":
            return self.board[2]
        if "" not in self.board:
            return "tie"
        return None

    def make_move(self, position):
        if self.board[position] == "":
            self.board[position] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"

    def undo_move(self, position):
        self.board[position] = ""
        self.current_player = "O" if self.current_player == "X" else "X"

    def get_possible_moves(self):
        moves = []
        for i in range(9):
            if self.board[i] == "":
                moves.append(i)
        return moves

    def evaluate_board(self):
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6]:
                if self.board[i] == "O":
                    return 1
                elif self.board[i] == "X":
                    return -1
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2]:
                if self.board[i] == "O":
                    return 1
                elif self.board[i] == "X":
                    return -1
        if self.board[0] == self.board[4] == self.board[8]:
            if self.board[0] == "O":
                return 1
            elif self.board[0] == "X":
                return -1
        if self.board[2] == self.board[4] == self.board[6]:
            if self.board[2] == "O":
                return 1
            elif self.board[2] == "X":
                return -1
        return 0

    def minimax(self, depth, alpha, beta, is_maximizing):
        winner = self.get_winner()
        if winner is not None:
            if winner == "X":
                return -100 + depth, None
            elif winner == "O":
                return 100 - depth, None
            else:
                return 0, None
        if is_maximizing:
            best_score = float('-inf')
            best_move = None
            for move in self.get_possible_moves():
                self.make_move(move)
                score, _ = self.minimax(depth + 1, alpha, beta, False)
                self.undo_move(move)
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for move in self.get_possible_moves():
                self.make_move(move)
                score, _ = self.minimax(depth + 1, alpha, beta, True)
                self.undo_move(move)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move

    def tabu_search(self, tabu_list_size):
        tabu_list = []
        best_move = None
        best_score = float('-inf')
        while True:
            for move in self.get_possible_moves():
                if move not in tabu_list:
                    self.make_move(move)
                    score, _ = self.minimax(0, float('-inf'), float('inf'), False)
                    self.undo_move(move)
                    if score > best_score:
                        best_score = score
                        best_move = move
            if best_move not in tabu_list:
                tabu_list.append(best_move)
            if len(tabu_list) > tabu_list_size:
                tabu_list.pop(0)
            if best_move is not None:
                return best_move

    def play(self):
        #set current player to "X" or "O" at random
        self.current_player = random.choice(["X", "O"])


        while not self.game_over:
            self.draw_board()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_player == "X":
                        x, y = pygame.mouse.get_pos()
                        row = y // 100
                        col = x // 100
                        position = row * 3 + col

                        if self.board[position] == "":
                            self.make_move(position)
                            self.current_player = "O"
                        else:
                            print("Invalid move")
                            continue


                self.draw_board()
                pygame.display.update()
                winner = self.get_winner()
                if winner is not None:
                    if winner == "tie":
                        print("Tie!")
                        #display winner in the middle of the screen
                        self.draw_text("Tie!", 50, (255, 255, 255), 100, 100)
                    else:
                        print(winner + " wins!")
                        #display winner in the middle of the screen
                        self.draw_text(winner + " wins!", 50, (255, 255, 255), 100, 100)
                    self.game_over = True
                    self.draw_board()
                    pygame.display.update()
                else:
                    if self.current_player == "O":
                        # AI player using Tabu Search
                        position = self.tabu_search(tabu_list_size=5)
                        self.make_move(position)
                        self.current_player = "X"

        
        #wait indefinitely until the user closes the window
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

        

if __name__ == "__main__":
    game = TicTacToe()
    game.play()
