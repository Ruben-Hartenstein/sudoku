from solutions.solving_techniques import SolvingTechniques
from itertools import combinations


class HiddenPair(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Hidden Pair", board, candidates)
        self.unit = ''
        self.unit_cells = []
        self.combo = []

    def execute_technique(self):
        for self.unit in ['row', 'column', 'box']:
            for i in range(9):
                occurring_candidates = []
                self.unit_cells = SolvingTechniques.get_unit_cells(i, self.unit)
                for cell in self.unit_cells:
                    x, y = cell
                    if self.board[x][y] != 0:
                        continue
                    for candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
                        if candidate not in occurring_candidates:
                            occurring_candidates.append(candidate)
                combos = set(combinations(occurring_candidates, 2))
                for self.combo in combos:
                    matches = []
                    for cell in self.unit_cells:
                        x, y = cell
                        if self.board[x][y] != 0:
                            continue
                        candidates_num = SolvingTechniques.format_candidates(self.candidates[x][y])
                        if any(c in self.combo for c in candidates_num):
                            matches.append(cell)
                    if len(matches) == 2:
                        self.primary_cells = matches
                        self.configure_highlighting()
                        if len(self.cross_outs) != 0:
                            return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cell = []

        for cell in self.unit_cells:
            x, y = cell
            if cell in self.primary_cells:
                candidates = self.candidates[x][y]
                candidates_num = SolvingTechniques.format_candidates(candidates)
                for value in candidates_num:
                    if value in self.combo:
                        self.highlights.append({
                            'value': value,
                            'cell': cell
                        })
                    else:
                        self.cross_outs.append({
                            'value': value,
                            'cell': cell
                        })
        self.secondary_cells = [cell for cell in self.unit_cells if cell not in self.primary_cells]

    def update_explanation(self):
        self.explanation = f"""The total of two candidates, ({self.combo[0]} and {self.combo[1]}),
occur in exactly two fields {SolvingTechniques.pretty_print_cells(self.primary_cells[0])} and {SolvingTechniques.pretty_print_cells(self.primary_cells[1])} of a {self.unit}.
Therefore all other candidates in these fields can be removed."""
