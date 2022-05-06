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


class NakedTriple(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Naked Triple", board, candidates)
        self.unit = ''
        self.unit_cells = []
        self.combo = []

    def execute_technique(self):
        for self.unit in ['row', 'column', 'box']:
            for j in range(9):
                i = j
                occurring_candidates = []
                if self.unit == 'box':
                    j, i = index2box(j)
                self.unit_cells = SolvingTechniques.get_influential_cells_unit((j, i), self.unit)
                for cell in self.unit_cells:
                    x, y = cell
                    if self.board[x][y] != 0:
                        continue
                    for num, candidate in enumerate(self.candidates[x][y]):
                        if candidate == 0:
                            continue
                        if num + 1 not in occurring_candidates:
                            occurring_candidates.append(num + 1)
                combos = set(combinations(occurring_candidates, 3))
                for self.combo in combos:
                    matches = []
                    for cell in self.unit_cells:
                        x, y = cell
                        if self.board[x][y] != 0:
                            continue
                        candidates_num = SolvingTechniques.format_candidates(self.candidates[x][y])
                        if all(c in self.combo for c in candidates_num):
                            matches.append(cell)
                    if len(matches) >= 3:
                        self.primary_cells = matches
                        self.configure_highlighting()
                        if len(self.cross_outs) != 0:
                            return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = []

        for cell in self.unit_cells:
            x, y = cell
            if self.board[x][y] != 0:
                continue
            if cell in self.primary_cells:
                candidates = self.candidates[x][y]
                candidates_num = candidates_to_values(candidates)
                for candidate in candidates_num:
                    self.highlights.append({
                        'value': candidate,
                        'cell': cell
                    })
            else:
                candidates = self.candidates[x][y]
                candidates_num = candidates_to_values(candidates)
                for value in self.combo:
                    if value in candidates_num:
                        self.cross_outs.append({
                            'value': value,
                            'cell': cell
                        })
        influential_cells = SolvingTechniques.get_influential_cells_unit(self.primary_cells[0], self.unit)
        for x, y in influential_cells:
            if (x, y) in self.primary_cells:
                continue
            self.secondary_cells.append((x, y))

    def update_explanation(self):
        self.explanation = f"""Because only three candidates ({self.combo[0]}, {self.combo[1]} and {self.combo[2]}) exist
in three fields ({self.primary_cells[0]}, {self.primary_cells[1]} and {self.primary_cells[2]}) of a {self.unit},
these candidates can be eliminated in the remaining fields of the {self.unit}"""
