from copy import deepcopy

SIZE = 9


class SudokuBoard:
    def __init__(self, board=None):
        """
        Initializes the sudoku board with numbers
        """
        if board:
            self.board = deepcopy(board)
        else:
            self.board = []
            for i in range(SIZE):
                self.board.append([])
                for j in range(SIZE):
                    self.board[i].append([0] * (SIZE + 1))
        temp_board = deepcopy(self.board)
        self.solve()
        self.solved = deepcopy(self.board)
        self.board = temp_board
        self.is_uniquely_solvable()

    def is_uniquely_solvable(self):
        temp_board = deepcopy(self.board)
        self.solve((9, 0, -1))
        self.uniquely_solvable = self.solved == self.board
        self.board = temp_board

    def solve(self, numbers=(1, SIZE + 1)):
        """
        Solves the SudokuBoard recursively via backtracking
        :return: False if not solvable, True if solved
        """
        square = self.get_empty_square()

        if not square:
            return True

        for i in range(*numbers):
            if self.is_valid(i, square):
                self.board[square[0]][square[1]][0] = i

                if self.solve(numbers):
                    return True

                self.board[square[0]][square[1]][0] = 0

        return False

    def is_valid(self, number, position):
        """
        Checks if a given number can be placed on a given position in the current sudoku
        :param number: number to be tested
        :param position: position of number
        :return: False if number is not valid, True if it is
        """
        # Check number
        if not (1 <= number <= SIZE):
            return False

        # Check row
        for j in range(SIZE):
            if self.board[position[0]][j][0] == number and j != position[1]:
                return False

        # Check column
        for i in range(SIZE):
            if self.board[i][position[1]][0] == number and i != position[0]:
                return False

        # Check Box
        box_x = (position[1] // 3) * 3
        box_y = (position[0] // 3) * 3

        for i in range(box_y, box_y + 3):
            for j in range(box_x, box_x + 3):
                if self.board[i][j][0] == number and (i, j) != position:
                    return False

        return True

    def print(self, board=None):
        """
        Function to display the sudoku
        """
        if not board:
            board = self.board

        for i in range(SIZE):
            if i % 3 == 0 and i != 0:
                print("---------------------")
            for j in range(SIZE):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                if board[i][j][0] == 0:
                    to_print = " "
                else:
                    to_print = board[i][j][0]
                if j == 8:
                    print(to_print)
                else:
                    print(to_print, end=" ")

    def get_empty_square(self):
        """
        Looks for the first empty square in the sudoku and returns it
        :return: Coordinates of empty square
        """
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j][0] == 0:
                    return i, j
        return None

    def update_numbers(self, number, cells):
        cell_values = []
        number = int(number)
        for cell in cells:
            x, y = [int(i) for i in cell]
            if self.board[x][y][0] == number:
                self.board[x][y][0] = 0
            else:
                self.board[x][y][0] = number
            cell_values.append(self.board[x][y])
        return cell_values

    def update_candidates(self, candidate, cells):
        cell_values = []
        for cell in cells:
            x, y = [int(i) for i in cell]
            self.board[x][y][int(candidate)] ^= 1
            cell_values.append(self.board[x][y])
        return cell_values

    def erase_cells(self, cells):
        cell_values = []
        for cell in cells:
            x, y = [int(i) for i in cell]
            self.board[x][y] = [0] * (SIZE + 1)
            cell_values.append(self.board[x][y])
        return cell_values
