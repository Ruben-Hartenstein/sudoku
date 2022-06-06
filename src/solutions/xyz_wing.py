from src.solutions.solving_techniques import SolvingTechniques


class XYZWing(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("XYZ-Wing", board, candidates)
        self.unit = None
        self.box_cell = None
        self.unit_cell = None
        self.candidate = None
        self.intersection_cells = None

    def execute_technique(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0 or sum(self.candidates[i][j]) != 3:
                    continue
                candidates = SolvingTechniques.format_candidates(self.candidates[i][j])
                box_cells = SolvingTechniques.get_influential_cells_unit((i, j), 'box')
                for self.unit in ['row', 'column']:
                    unit_cells = SolvingTechniques.get_influential_cells_unit((i, j), self.unit)
                    for self.unit_cell in unit_cells:
                        if self.board[self.unit_cell[0]][self.unit_cell[1]] != 0 or sum(self.candidates[self.unit_cell[0]][self.unit_cell[1]]) != 2 or self.unit_cell in box_cells:
                            continue
                        unit_candidates = SolvingTechniques.format_candidates(self.candidates[self.unit_cell[0]][self.unit_cell[1]])
                        if all([candidate in candidates for candidate in unit_candidates]):
                            for self.box_cell in box_cells:
                                if self.board[self.box_cell[0]][self.box_cell[1]] != 0 or sum(self.candidates[self.box_cell[0]][self.box_cell[1]]) != 2 or self.box_cell in unit_cells:
                                    continue
                                box_candidates = SolvingTechniques.format_candidates(
                                    self.candidates[self.box_cell[0]][self.box_cell[1]])
                                if not all([candidate in candidates for candidate in box_candidates]) or box_candidates == unit_candidates:
                                    continue
                                self.candidate = [candidate for candidate in box_candidates if candidate in unit_candidates][0]
                                self.primary_cells = [(i, j), self.box_cell, self.unit_cell]
                                self.intersection_cells = list(set(box_cells) & set(unit_cells))
                                self.intersection_cells.remove((i, j))
                                self.configure_highlighting()
                                if len(self.cross_outs) != 0:
                                    return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = self.intersection_cells

        for x, y in self.intersection_cells:
            if self.board[x][y] != 0 or self.candidate not in SolvingTechniques.format_candidates(
                    self.candidates[x][y]):
                continue
            self.cross_outs.append({
                'value': self.candidate,
                'cell': (x, y)
            })
        for x, y in self.primary_cells:
            for candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
                self.highlights.append({
                    'value': candidate,
                    'cell': (x, y)
                })

    def update_explanation(self):
        self.explanation = f"""Within a Block and a {self.unit}, there are three fields with a total of three different candidates {SolvingTechniques.format_candidates(self.candidates[self.primary_cells[0][0]][self.primary_cells[0][1]])}.
the candidate {self.candidate} is contained in all three fields. In two fields there are the two different pairs of candidates {SolvingTechniques.format_candidates(self.candidates[self.box_cell[0]][self.box_cell[1]])} and {SolvingTechniques.format_candidates(self.candidates[self.unit_cell[0]][self.unit_cell[1]])}.
If either number would be inserted, the candidate {self.candidate} can be deleted from the intersection of the influential cells of the box and the {self.unit} because either the {self.candidate} has to be inserted itself, or by inserting the other option, a naked pair is formed."""
