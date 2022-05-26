from src.solutions.solving_techniques import SolvingTechniques


class ForbiddenRectangleType4(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Forbidden Rectangle Type 4", board, candidates)
        self.orthogonal_cell = None
        self.candidate = None
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
                    if self.board[x][y] != 0 or sum(self.candidates[x][y]) != 2:
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
                    for self.orthogonal_cell in orthogonal_cells:
                        k, l = self.orthogonal_cell
                        if self.board[k][l] != 0 or (k, l) == (x, y):
                            continue
                        candidate_multiple_value = SolvingTechniques.format_candidates(self.candidates[k][l])
                        if not all(elem in candidate_multiple_value for elem in self.candidate_pair_values):
                            continue
                        cross_cells = self.get_cross_cells(self.primary_cells[1], (k, l))
                        self.fourth_cell = list(set(cross_cells) - set(self.primary_cells))
                        if not self.fourth_cell:
                            continue
                        self.fourth_cell = self.fourth_cell[0]
                        candidate_fourth_cell_value = SolvingTechniques.format_candidates(
                            self.candidates[self.fourth_cell[0]][self.fourth_cell[1]])
                        if not all(elem in candidate_fourth_cell_value for elem in self.candidate_pair_values):
                            continue
                        for unit in [self.unit, 'box']:
                            for self.candidate in self.candidate_pair_values:
                                influential_cells = SolvingTechniques.get_influential_cells_unit(self.fourth_cell, unit)
                                cells_with_candidates = self.get_cells_with_candidate(influential_cells, self.candidate)
                                if len(cells_with_candidates) == 2:
                                    self.primary_cells.append(self.orthogonal_cell)
                                    self.primary_cells.append(self.fourth_cell)
                                    self.configure_highlighting()
                                    return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = []
        cross_out_value = self.candidate_pair_values[:]
        cross_out_value.remove(self.candidate)
        cross_out_value = cross_out_value[0]

        for cell in [self.orthogonal_cell, self.fourth_cell]:
            self.highlights.append({
                'value': self.candidate,
                'cell': cell
            })
            self.cross_outs.append({
                'value': cross_out_value,
                'cell': cell
            })

    def update_explanation(self):
        cross_out_value = self.candidate_pair_values[:]
        cross_out_value.remove(self.candidate)
        cross_out_value = cross_out_value[0]
        self.explanation = f"""Since the candidate {self.candidate} cannot be in any other field of its unit outside the rectangle, one of the two fields must be {self.candidate}. For the Sudoku to have a unique solution, the value in the other field must not be a value of the rectangle, therefore {cross_out_value} can be deleted."""
