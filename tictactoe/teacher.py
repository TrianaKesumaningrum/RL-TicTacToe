import random

class Teacher:
    def __init__(self, ability_level=0.5):
        # Ability level now determines how smart the Teacher is
        self.ability_level = ability_level
        self.memory = []  # Adding memory for a learning element

    def make_move(self, board):
        # Decision-making logic based on teacher's ability level
        if random.random() > self.ability_level:
            return self.random_move(board)
        
        if self.win(board, key='X'):
            return self.find_winning_move(board, key='X')
        
        if self.block_win(board):
            return self.block_win(board)
        
        if self.fork(board):
            return self.fork(board)
        
        if self.block_fork(board):
            return self.block_fork(board)
        
        return self.random_move(board)

    def win(self, board, key):
        # Check if the teacher can win in the next move
        return self.find_winning_move(board, key)

    def find_winning_move(self, board, key):
        # Check rows, columns, and diagonals for winning move
        for i in range(4):
            # Check rows
            if board[i].count(key) == 3 and board[i].count(' ') == 1:
                return board.index(i)
            # Check columns
            column = [board[j][i] for j in range(4)]
            if column.count(key) == 3 and column.count(' ') == 1:
                return column.index(' ') * 4 + i
        # Check diagonals
        if all(board[i][i] == key for i in range(4)):
            for i in range(4):
                if board[i][i] == ' ':
                    return i * 4 + i
        if all(board[i][3 - i] == key for i in range(4)):
            for i in range(4):
                if board[i][3 - i] == ' ':
                    return i * 4 + (3 - i)
        return None

    def block_win(self, board):
        # Block opponent's winning move
        return self.find_winning_move(board, key='O')

    def fork(self, board):
        # Logic to create a fork opportunity
        for i in range(4):
            if board[i].count('X') == 2 and board[i].count(' ') == 2:
                return i  # Return the index of the row to create a fork
        return None

    def block_fork(self, board):
        # Logic to block opponent's fork opportunities
        for i in range(4):
            if board[i].count('O') == 2 and board[i].count(' ') == 2:
                return i  # Return the index of the row to block a fork
        return None

    def random_move(self, board):
        # Teacher makes a random move if no better move is available
        available_moves = [i for i, cell in enumerate(board) if cell == ' ']
        return random.choice(available_moves) if available_moves else None

    def learn(self, outcome):
        # Learning from the outcome (win/loss/draw)
        self.memory.append(outcome)
        if len(self.memory) > 100:
            self.memory.pop(0)  # Forget old outcomes if memory exceeds size
        # Adjust the ability or strategy based on previous outcomes

# Example of how to use the Teacher class in a game loop
def print_board(board):
    for row in board:
        print(' | '.join(row))
        print('-' * 15)

def play_game():
    board = [[' ' for _ in range(4)] for _ in range(4)]
    teacher = Teacher(ability_level=0.7)

    for turn in range(16):
        print_board(board)
        if turn % 2 == 0:  # Teacher's turn
            move = teacher.make_move(board)
            if move is not None:
                board[move // 4][move % 4] = 'X'
        else:  # Player's turn (you can add player input logic here)
            move = int(input("Enter your move (0-15): "))
            if board[move // 4][move % 4] == ' ':
                board[move // 4][move % 4] = 'O'
            else:
                print("Masukkan tidak valid. Harap coba lagi.")
                continue

        # Check for win or draw condition
        # (Implement your win/draw checking logic here)

    print_board(board)
    print("Game Over!")

if __name__ == "__main__":
    play_game()
