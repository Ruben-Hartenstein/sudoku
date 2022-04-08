from src.solutions.solving_techniques import SolvingTechniques


class NakedSingle(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Naked Single",
                         """The yellow field is in the sphere of influence of eight of the nine possible numbers.
                          Therefore, in this box fits only one number (here: 7).""",
                         board, candidates)

    def execute_technique(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    continue
                if sum(self.candidates[i][j]) != 1:
                    continue
                self.primary_cells.append((i, j))
                self.cross_out.append(
                    {'value': self.candidates[i][j].index(1) + 1,
                     'cell': self.primary_cells[0]})
                return True
        return False

    def update_secondary_cells(self):
        cell = self.cross_out[0]['cell']
        influential_cells = SolvingTechniques.get_influential_cells(cell)
        for key in influential_cells.keys():
            self.secondary_cells.extend(influential_cells[key])
        self.secondary_cells = SolvingTechniques.remove_duplicates(self.secondary_cells)
        self.secondary_cells.remove(cell)
