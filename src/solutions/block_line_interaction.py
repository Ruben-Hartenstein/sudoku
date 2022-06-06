from src.solutions.solving_techniques import SolvingTechniques


class BlockLineInteraction(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Block-Line Interaction", board, candidates)
        self.unit = ''
        self.candidate = 0

    def execute_technique(self):
        for i in range(9):
            occurring_candidates = []
            self.unit_cells = SolvingTechniques.get_influential_cells_unit(SolvingTechniques.index2box(i), 'box')
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
                first_row = False
                first_column = False
                for cell in self.unit_cells:
                    x, y = cell
                    if self.board[x][y] != 0:
                        continue
                    if self.candidates[x][y][self.candidate - 1]:
                        if not first_row and type(first_row) != int:
                            first_row = x
                        elif first_row != x:
                            self.unit = 'column'
                            first_row = -1
                        if not first_column and type(first_column) != int:
                            first_column = y
                        elif first_column != y:
                            self.unit = 'row'
                            first_column = -1
                        if first_row == -1 and first_column == -1:
                            break
                else:
                    self.secondary_cells = self.unit_cells
                    self.configure_highlighting()
                    if len(self.cross_outs) != 0:
                        return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.primary_cells = []
        highlight_cells = []
        for cell in self.secondary_cells:
            x, y = cell
            if self.board[x][y] != 0:
                continue
            if self.candidates[x][y][self.candidate - 1]:
                highlight_cells.append(cell)
                self.highlights.append({
                    'value': self.candidate,
                    'cell': cell
                })
        self.primary_cells = SolvingTechniques.get_influential_cells_unit(self.highlights[0]['cell'], self.unit)
        self.secondary_cells = [x for x in self.secondary_cells if x not in self.primary_cells]
        for cell in self.primary_cells:
            x, y = cell
            if self.board[x][y] != 0 or cell in highlight_cells:
                continue
            if self.candidates[x][y][self.candidate - 1]:
                self.cross_outs.append({
                    'value': self.candidate,
                    'cell': cell
                })

    def update_explanation(self):
        self.explanation = f"""All candidates of the number {self.highlights[0]['value']} are within one {self.unit} in a box.
Therefore all candidates of the number {self.highlights[0]['value']} in the {self.unit}, that are not in the box can be deleted."""
