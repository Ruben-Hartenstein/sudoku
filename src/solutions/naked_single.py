from src.solutions.solving_techniques import SolvingTechniques, remove_duplicates


class NakedSingle(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Naked Single",
                         """The yellow field is in the sphere of influence of eight of the nine possible numbers.
                          Therefore, in this box fits only one number (here: 7).""",
                         board, candidates)

    def execute_technique(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    if sum(self.candidates[i][j]) == 1:
                        self.cross_outs = self.candidates[i][j].index(1) + 1
                        self.cells.append((i, j))
                        return True
        return False

    def update_associated_cells(self):
        for cell in self.cells:
            # Add all in row
            for j in range(9):
                if self.board[cell[0]][j] != 0:
                    self.associated_cells.append((cell[0], j))
            # Add all in column
            for i in range(9):
                if self.board[i][cell[1]] != 0:
                    self.associated_cells.append((i, cell[1]))
            # Add all in Box
            box_x = (cell[1] // 3) * 3
            box_y = (cell[0] // 3) * 3

            for i in range(box_y, box_y + 3):
                for j in range(box_x, box_x + 3):
                    if self.board[i][j] != 0:
                        self.associated_cells.append((i, j))
            self.associated_cells = remove_duplicates(self.associated_cells)
