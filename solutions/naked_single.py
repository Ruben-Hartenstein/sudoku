from solutions.solving_techniques import SolvingTechniques


class NakedSingle(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Naked Single", board, candidates)

    def execute_technique(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    continue
                if sum(self.candidates[i][j]) != 1:
                    continue
                self.primary_cells = [(i, j)]
                self.configure_highlighting()
                return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = []

        x, y = self.primary_cells[0]
        self.highlights = [{'value': self.solved_board[x][y],
                            'cell': self.primary_cells[0]}]
        influential_cells = SolvingTechniques.get_influential_cells((x, y))
        for key in influential_cells.keys():
            self.secondary_cells.extend(influential_cells[key])
        self.secondary_cells = SolvingTechniques.remove_duplicates(self.secondary_cells)
        self.secondary_cells.remove((x, y))

    def update_explanation(self):
        self.explanation = f"""Because every other candidate in the field {self.highlights[0]['cell']} is blocked,
the only possibility left, {self.highlights[0]['value']}, can be inserted."""
