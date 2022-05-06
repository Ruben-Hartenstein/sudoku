from src.solutions.solving_techniques import SolvingTechniques


class ThirdEye(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Third Eye", board, candidates)
        self.occurring_candidates = []

    def execute_technique(self):
        three_candidates_once = False
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0 or sum(self.candidates[i][j]) == 2:
                    continue
                elif sum(self.candidates[i][j]) == 3 and not three_candidates_once:
                    three_candidates_once = True
                    self.primary_cells = [(i, j)]
                    self.occurring_candidates = SolvingTechniques.format_candidates(self.candidates[i][j])
                else:
                    return False

        self.configure_highlighting()
        if len(self.cross_outs) != 0:
            return True
        return False


    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cell = []

        for unit in ['row', 'column', 'box']:
            unit_cells = SolvingTechniques.get_influential_cells_unit(self.primary_cells[0], unit)
            for candidate in self.occurring_candidates:
                appearance = 0
                for cell in unit_cells:
                    x, y = cell
                    if self.board[x][y] != 0:
                        continue
                    if self.candidates[x][y][candidate - 1]:
                        appearance += 1
                if appearance == 3:
                    self.highlights = [{'value': candidate, 'cell': self.primary_cells[0]}]
                    for temp in self.occurring_candidates:
                        self.cross_outs = []
                        if temp != candidate:
                            self.cross_outs.append({
                                'value': temp,
                                'cell': self.primary_cells[0]
                            })
                    break
        influential_cells = SolvingTechniques.get_influential_cells(self.primary_cells[0])
        for key in influential_cells.keys():
            self.secondary_cells.extend(influential_cells[key])
        self.secondary_cells = SolvingTechniques.remove_duplicates(self.secondary_cells)
        self.secondary_cells.remove(self.primary_cells[0])

    def update_explanation(self):
        self.explanation = f"""On the whole board every field has two candidates, except the field {self.highlights[0]['cell']} which has three.
The candidate that is contained in three fields in one unit (in this case {self.highlights[0]['value']}) can be inserted otherwise the sudoku is not uniquely solvable."""
