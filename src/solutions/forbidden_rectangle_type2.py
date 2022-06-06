from src.solutions.solving_techniques import SolvingTechniques


class ForbiddenRectangleType2(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Forbidden Rectangle Type 2", board, candidates)
        self.remaining_value = None
        self.unit = None
        self.candidate_pair_values = None
        self.fourth_cell = None

    def execute_technique(self):
        units = ['row', 'column']
        for i, self.unit in enumerate(units):
            for j in range(9):
                unit_cells = SolvingTechniques.get_influential_cells_unit((j, j), self.unit)
                for cell in unit_cells:
                    self.primary_cells = []
                    x, y = cell
                    if self.board[x][y] != 0:
                        continue
                    if sum(self.candidates[x][y]) != 2:
                        continue
                    self.primary_cells.append((x, y))
                    candidate_pair = self.candidates[x][y]
                    temp_cells = SolvingTechniques.get_influential_cells_unit((x, y), self.unit)
                    for temp_cell in temp_cells:
                        k, l = temp_cell
                        if self.board[k][l] != 0 or (k, l) == (x, y):
                            continue
                        if self.candidates[k][l] == candidate_pair:
                            self.primary_cells.append((k, l))
                    if len(self.primary_cells) != 2:
                        continue
                    if SolvingTechniques.get_box(self.primary_cells[0]) != SolvingTechniques.get_box(
                            self.primary_cells[1]):
                        continue
                    self.candidate_pair_values = SolvingTechniques.format_candidates(candidate_pair)
                    orthogonal_cells = SolvingTechniques.get_influential_cells_unit(self.primary_cells[0], units[1 - i])
                    for orthogonal_cell in orthogonal_cells:
                        k, l = orthogonal_cell
                        if self.board[k][l] != 0 or (k, l) == (x, y):
                            continue
                        if sum(self.candidates[k][l]) != 3:
                            continue
                        candidate_triple_value = SolvingTechniques.format_candidates(self.candidates[k][l])
                        if not all(elem in candidate_triple_value for elem in self.candidate_pair_values):
                            continue
                        self.remaining_value = list(set(candidate_triple_value) - set(self.candidate_pair_values))[0]
                        cross_cells = self.get_cross_cells(self.primary_cells[1], (k, l))
                        cross_cells = [cross_cell for cross_cell in cross_cells if self.board[cross_cell[0]][cross_cell[1]] == 0]
                        self.fourth_cell = list(set(cross_cells) - set(self.primary_cells))
                        if not self.fourth_cell:
                            continue
                        self.fourth_cell = self.fourth_cell[0]
                        if self.candidates[self.fourth_cell[0]][self.fourth_cell[1]] == self.candidates[k][l]:
                            primary_cells_copy = self.primary_cells[:]
                            self.primary_cells.append(orthogonal_cell)
                            self.primary_cells.append(self.fourth_cell)
                            self.configure_highlighting()
                            if len(self.cross_outs) != 0:
                                return True
                            self.primary_cells = primary_cells_copy[:]
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = []

        for cell in self.primary_cells:
            x, y = cell
            if self.candidates[x][y][self.remaining_value-1]:
                self.highlights.append({
                    'value': self.remaining_value,
                    'cell': cell
                })

        for unit in [self.unit, "box"]:
            cells = SolvingTechniques.get_influential_cells_unit(self.fourth_cell, unit)
            for cell in cells:
                x, y = cell
                if self.board[x][y] != 0 or cell in self.primary_cells or not self.candidates[x][y][self.remaining_value-1]:
                    continue
                self.cross_outs.append({
                    'value': self.remaining_value,
                    'cell': cell
                })

    def update_explanation(self):
        self.explanation = f"""Because the candidate {self.remaining_value} is the only different value besides {self.candidate_pair_values[0]} and {self.candidate_pair_values[1]} in the 4 highlighted cells of the rectangle,
one of the 2 cells has to be the value {self.remaining_value}. Because those 2 cells are in the same box and in the same {self.unit}, every other candidate in this box and {self.unit} can be deleted."""
