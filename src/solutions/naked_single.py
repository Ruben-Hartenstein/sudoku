from src.solutions.solving_techniques import SolvingTechniques


class NakedSingle(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Naked Single",
                         """The yellow field is in the sphere of influence of eight of the nine possible numbers.
                          Therefore, in this box fits only one number (here: 7).""",
                         board, candidates)

    def execute_technique(self):
        print(SolvingTechniques.solved_board)
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    if sum(self.candidates[i][j]) == 1:
                        self.cross_outs = [self.candidates[i][j].index(1) + 1]
                        self.cells.append((i, j))
                        return True
        return False

    def update_associated_cells(self):
        cell = self.cells[0]
        influential_cells = SolvingTechniques.get_influential_cells(cell)
        for key in influential_cells.keys():
            self.associated_cells.extend(influential_cells[key])
        self.associated_cells = SolvingTechniques.remove_duplicates(self.associated_cells)
        self.associated_cells.remove(cell)
