from copy import deepcopy

SIZE = 9


class SudokuBoard:
    def __init__(self, board=[]):
        """
        Initializes the sudoku board with numbers
        """
        self.solved = None
        self.start_coords = None
        self.candidates = []
        self.board = board
        self.init_candidates()
        if not self.board:
            self.init_board()

    def init_board(self):
        for i in range(SIZE):
            self.board.append([])
            for j in range(SIZE):
                self.board[i].append(0)

    def init_candidates(self):
        for i in range(SIZE):
            self.candidates.append([])
            for j in range(SIZE):
                self.candidates[i].append([1] * SIZE)

    def calculate_start_coords(self):
        self.start_coords = []
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] != 0:
                    self.start_coords.append((i, j))

    def is_uniquely_solvable(self):
        temp_board = deepcopy(self.board)
        self.solve(numbers=(9, 0, -1), board=temp_board)
        return self.solved == temp_board

    def solve(self, numbers=(1, SIZE + 1), board=None):
        """
        Solves the SudokuBoard recursively via backtracking
        :return: False if not solvable, True if solved
        """
        if board is None:
            board = self.board

        square = self.get_empty_square(board)

        if not square:
            return True

        for i in range(*numbers):
            if self.is_valid(i, square, board=board):
                board[square[0]][square[1]] = i

                if self.solve(numbers=numbers, board=board):
                    return True

                board[square[0]][square[1]] = 0

        return False

    def is_board_valid(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] != 0:
                    if not self.is_valid(self.board[i][j], (i, j)):
                        return False
        return True

    def is_valid(self, number, position, board=None):
        """
        Checks if a given number can be placed on a given position in the current sudoku
        :param board: board to be tested
        :param number: number to be tested
        :param position: position of number
        :return: False if number is not valid, True if it is
        """
        if board is None:
            board = self.board

        # Check number
        if not (1 <= number <= SIZE):
            return False

        # Check row
        for j in range(SIZE):
            if board[position[0]][j] == number and j != position[1]:
                return False

        # Check column
        for i in range(SIZE):
            if board[i][position[1]] == number and i != position[0]:
                return False

        # Check Box
        box_x = (position[1] // 3) * 3
        box_y = (position[0] // 3) * 3

        for i in range(box_y, box_y + 3):
            for j in range(box_x, box_x + 3):
                if board[i][j] == number and (i, j) != position:
                    return False

        return True

    def print(self, board=None):
        """
        Function to display the sudoku
        """
        if board is None:
            board = self.board

        for i in range(SIZE):
            if i % 3 == 0 and i != 0:
                print("---------------------")
            for j in range(SIZE):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                if board[i][j] == 0:
                    to_print = " "
                else:
                    to_print = board[i][j]
                if j == 8:
                    print(to_print)
                else:
                    print(to_print, end=" ")

    def get_empty_square(self, board=None):
        """
        Looks for the first empty square in the sudoku and returns it
        :return: Coordinates of empty square
        """
        if board is None:
            board = self.board

        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] == 0:
                    return i, j
        return None

    def get_errors(self):
        errors = []
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] != 0:
                    if self.board[i][j] != self.solved[i][j]:
                        errors.append((i, j))
        return errors

    def update_candidates(self):
        for i in range(SIZE):
            for j in range(SIZE):
                # Ignore cells with filled in value
                if self.board[i][j] == 0:
                    for candidate in range(1, SIZE + 1):
                        # Only delete possible candidates
                        if not self.is_valid(candidate, (i, j)):
                            self.candidates[i][j][candidate - 1] = 0

    def update_numbers(self, number, cells):
        cell_values = []
        number = int(number)
        for cell in cells:
            x, y = [int(i) for i in cell]
            if not (self.start_coords and (x, y) in self.start_coords):
                if self.board[x][y] == number:
                    self.board[x][y] = 0
                else:
                    self.board[x][y] = number
            cell_values.append(self.board[x][y])
        return cell_values

    def erase_cells(self, cells):
        cell_values = []
        for cell in cells:
            x, y = [int(i) for i in cell]
            if not (self.start_coords and (x, y) in self.start_coords):
                self.board[x][y] = 0
            cell_values.append(self.board[x][y])
        return cell_values
