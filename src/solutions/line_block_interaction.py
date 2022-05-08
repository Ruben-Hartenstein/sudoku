from src.solutions.solving_techniques import SolvingTechniques


class LineBlockInteraction(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Line-Block Interaction", board, candidates)
        self.unit = ''
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
                                first_box = SolvingTechniques.get_box(cell)
                            elif first_box != SolvingTechniques.get_box(cell):
                                break
                    else:
                        self.primary_cells = self.unit_cells
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
            if self.board[x][y] != 0:
                continue
            if self.candidates[x][y][self.candidate - 1]:
                self.highlights.append({
                    'value': self.candidate,
                    'cell': cell
                })
        box_cells = SolvingTechniques.get_influential_cells_unit(self.highlights[0]['cell'], 'box')
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

    def update_explanation(self):
        self.explanation = f"""All candidates of the number {self.highlights[0]['value']} are within one box in a {self.unit}.
Therefore all candidates of the number {self.highlights[0]['value']} in the box, that are not in the {self.unit} can be deleted."""
