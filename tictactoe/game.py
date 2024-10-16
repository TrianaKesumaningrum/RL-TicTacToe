import random

class Game:
    """ The game class. New instance created for each new game. """
    def __init__(self, agent, teacher=None):
        self.agent = agent
        self.teacher = teacher
        # Initialize the game board
        self.board = [['-', '-', '-', '-'], 
                      ['-', '-', '-', '-'], 
                      ['-', '-', '-', '-'], 
                      ['-', '-', '-', '-']]

    def playerMove(self):
        """ Query player for a move and update the board accordingly. """
        if self.teacher is not None:
            action = self.teacher.makeMove(self.board)
            self.board[action[0]][action[1]] = 'X'
        else:
            printBoard(self.board)
            while True:
                move = input("Giliranmu! Silakan pilih baris dan kolom dari 0-3 "
                             "dalam format baris, kolom: ")
                print('\n')
                try:
                    row, col = map(int, move.split(','))
                except ValueError:
                    print("MASUKAN TIDAK VALID! Harap gunakan format yang benar.")
                    continue
                if row not in range(4) or col not in range(4) or self.board[row][col] != '-':
                    print("MASUKAN TIDAK VALID! Silahkan pilih kembali.")
                    continue
                self.board[row][col] = 'X'
                break

    def agentMove(self, action):
        """ Update board according to agent's move. """
        self.board[action[0]][action[1]] = 'O'

    def checkForWin(self, key):
        """ Check to see whether the player/agent with token 'key' has won. """
        # Check for player win on diagonals
        a = [self.board[i][i] for i in range(4)]
        b = [self.board[i][3 - i] for i in range(4)]
        if a.count(key) == 4 or b.count(key) == 4:
            return True
        # Check for player win on rows/columns
        for i in range(4):
            col = [self.board[j][i] for j in range(4)]
            row = self.board[i]
            if col.count(key) == 4 or row.count(key) == 4:
                return True
        return False

    def checkForDraw(self):
        """ Check to see whether the game has ended in a draw. """
        return all(elt != '-' for row in self.board for elt in row)

    def checkForEnd(self, key):
        """ Checks if player/agent with token 'key' has ended the game. """
        if self.checkForWin(key):
            if self.teacher is None:
                printBoard(self.board)
                if key == 'X':
                    print("Pemain menang!")
                else:
                    print("Agent RL menang!")
            return 1
        elif self.checkForDraw():
            if self.teacher is None:
                printBoard(self.board)
                print("Seri!")
            return 0
        return -1

    def playGame(self, player_first):
        """ Begin the tic-tac-toe game loop. """
        # Initialize the agent's state and action
        if player_first:
            self.playerMove()
        prev_state = getStateKey(self.board)
        prev_action = self.agent.get_action(prev_state)

        # Iterate until game is over
        while True:
            self.agentMove(prev_action)
            check = self.checkForEnd('O')
            if check != -1:
                reward = check
                break
            self.playerMove()
            check = self.checkForEnd('X')
            if check != -1:
                reward = -1 * check
                break
            reward = 0
            new_state = getStateKey(self.board)

            # Determine new action (epsilon-greedy)
            new_action = self.agent.get_action(new_state)
            # Update Q-values
            self.agent.update(prev_state, new_state, prev_action, new_action, reward)
            # Reset "previous" values
            prev_state = new_state
            prev_action = new_action

        # Game over. Perform final update
        self.agent.update(prev_state, None, prev_action, None, reward)

    def start(self):
        """ Determine who moves first, and subsequently, start the game. """
        if self.teacher is not None:
            if random.random() < 0.5:
                self.playGame(player_first=False)
            else:
                self.playGame(player_first=True)
        else:
            while True:
                response = input("Apakah kamu ingin mulai duluan? [y/n]: ")
                print('')
                if response.lower() in ['n', 'no']:
                    self.playGame(player_first=False)
                    break
                elif response.lower() in ['y', 'yes']:
                    self.playGame(player_first=True)
                    break
                else:
                    print("Masukan tidak valid. Masukkan 'y' atau 'n'.")

def printBoard(board):
    """ Prints the game board as text output to the terminal. """
    print('    0   1   2   3\n')
    for i, row in enumerate(board):
        print('%i   ' % i, end='')
        for elt in row:
            print('%s   ' % elt, end='')
        print('\n')

def getStateKey(board):
    """ Converts 2D list representing the board state into a string key for that state. """
    return ''.join(''.join(row) for row in board)
