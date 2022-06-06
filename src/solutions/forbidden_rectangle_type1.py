from src.solutions.solving_techniques import SolvingTechniques


class ForbiddenRectangleType1(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Forbidden Rectangle Type 1", board, candidates)
        self.candidate_pair_values = None
        self.fourth_cell = None

    def execute_technique(self):
        for j in range(9):
            for i in range(9):
                if self.board[i][j] != 0:
                    continue
                self.primary_cells = []
                if sum(self.candidates[i][j]) == 2:
                    self.primary_cells.append((i, j))
                    candidate_pair = self.candidates[i][j]
                    for unit in ['row', 'column']:
                        unit_cells = SolvingTechniques.get_influential_cells_unit((i, j), unit)
                        for cell in unit_cells:
                            x, y = cell
                            if self.board[x][y] != 0 or (x, y) == (i, j):
                                continue
                            if self.candidates[x][y] == candidate_pair:
                                self.primary_cells.append(cell)
                                break
                    if len(self.primary_cells) == 3:
                        cross_cells = self.get_cross_cells(self.primary_cells[1], self.primary_cells[2])
                        cross_cells = [cross_cell for cross_cell in cross_cells if self.board[cross_cell[0]][cross_cell[1]] == 0]
                        self.fourth_cell = list(set(cross_cells) - set(self.primary_cells))
                        if not self.fourth_cell:
                            continue
                        self.fourth_cell = self.fourth_cell[0]
                        x, y = self.fourth_cell
                        self.candidate_pair_values = SolvingTechniques.format_candidates(candidate_pair)
                        fourth_cell_values = SolvingTechniques.format_candidates(self.candidates[x][y])
                        if not all(elem in fourth_cell_values for elem in self.candidate_pair_values):
                            break
                        self.configure_highlighting()
                        if len(self.cross_outs) != 0:
                            return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = []

        for cell in self.primary_cells:
            x, y = cell
            for candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
                self.highlights.append({
                    'value': candidate,
                    'cell': cell
                })
        self.primary_cells.append(self.fourth_cell)
        x, y = self.fourth_cell
        for candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
            if candidate in self.candidate_pair_values:
                self.cross_outs.append({
                    'value': candidate,
                    'cell': self.fourth_cell
                })

    def update_explanation(self):
        self.explanation = f"""Because the candidates {self.candidate_pair_values[0]} and {self.candidate_pair_values[1]} are the only candidates in 3 out of 4 fields of the rectangle,
the fourth field, {self.fourth_cell}, cannot possibly be one of those 2 candidates, otherwise the sudoku wouldn't have a unique solution, and they can be removed"""
