from src.solutions.solving_techniques import SolvingTechniques
from itertools import combinations


def index2box(index):
    box_coords = {0: (1, 1),
                  1: (1, 4),
                  2: (1, 7),
                  3: (4, 1),
                  4: (4, 4),
                  5: (4, 7),
                  6: (7, 1),
                  7: (7, 4),
                  8: (7, 7)}
    return box_coords[index]


def candidates_to_values(candidates):
    values = []
    for num, candidate in enumerate(candidates):
        if candidate == 0:
            continue
        values.append(num + 1)
    return values


def get_box(cell):
    box_x = (cell[1] // 3) * 3
    box_y = (cell[0] // 3) * 3
    return box_x, box_y


class LineBlockInteraction(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Line-Block Interaction", board, candidates)
        self.unit = ''
        self.unit_cells = []
        self.candidate = 0

    def execute_technique(self):
        for self.unit in ['row', 'column']:
            for j in range(9):
                occurring_candidates = []
                self.unit_cells = SolvingTechniques.get_influential_cells_unit((j, j), self.unit)
                for cell in self.unit_cells:
                    x, y = cell
                    if self.board[x][y] != 0:
                        continue
                    for num, candidate in enumerate(self.candidates[x][y]):
                        if candidate == 0:
                            continue
                        if num + 1 not in occurring_candidates:
                            occurring_candidates.append(num + 1)
                for self.candidate in occurring_candidates:
                    first_box = ()
                    for cell in self.unit_cells:
                        x, y = cell
                        if self.board[x][y] != 0:
                            continue
                        if self.candidates[x][y][self.candidate - 1]:
                            if not first_box:
                                first_box = get_box(cell)
                            elif first_box != get_box(cell):
                                break
                    else:
                        self.primary_cells = self.unit_cells
                        self.assemble_cross_out()
                        if len(self.cross_outs) != 0:
                            return True
        return False

    def assemble_cross_out(self):
        self.highlights = []
        self.cross_outs = []
        candidate_cell = 0
        for cell in self.unit_cells:
            x, y = cell
            if self.board[x][y] != 0:
                continue
            if self.candidates[x][y][self.candidate - 1]:
                candidate_cell = cell
                self.highlights.append({
                    'value': self.candidate,
                    'cell': cell
                })
        box_cells = SolvingTechniques.get_influential_cells_unit(candidate_cell, 'box')
        self.secondary_cells = [x for x in box_cells if x not in self.primary_cells]
        for cell in self.secondary_cells:
            x, y = cell
            if self.board[x][y] != 0:
                continue
            if self.candidates[x][y][self.candidate - 1]:
                self.cross_outs.append({
                    'value': self.candidate,
                    'cell': cell
                })

    def update_secondary_cells(self):
        pass

    def update_explanation(self):
        self.explanation = f"""Bibedi bubedi"""
