from src.solutions.solving_techniques import SolvingTechniques


class HiddenSingle(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Forbidden Rectangle Type 1", board, candidates)
        self.unit = ""

    def execute_technique(self):
        # Look for only one occurrence of candidate in unit
        for j in range(9):
            for i in range(9):
                if self.board[i][j] != 0:
                    continue
                num = SolvingTechniques.solved_board[i][j]
                influential_cells = SolvingTechniques.get_influential_cells((i, j))
                for key in influential_cells.keys():
                    candidate_once = False
                    for x, y in influential_cells[key]:
                        if self.board[x][y] != 0:
                            continue
                        if self.candidates[x][y][num - 1] == 1:
                            if candidate_once:
                                self.primary_cells = []
                                candidate_once = False
                                break
                            self.primary_cells = [(x, y)]
                            candidate_once = True
                    if candidate_once:
                        self.unit = key
                        self.configure_highlighting()
                        return True
        return False

    def get_squares(self, cell):
        

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = []
        x, y = self.primary_cells[0]
        self.highlights = [{'value': self.solved_board[x][y],
                            'cell': self.primary_cells[0]}]
        self.secondary_cells = SolvingTechniques.get_influential_cells_unit((x, y), self.unit)
        self.secondary_cells.remove((x, y))


    def update_explanation(self):
        self.explanation = f"""Every {self.highlights[0]['value']} in the {self.unit}, except one, is blocked.
Therefore, {self.highlights[0]['value']} can be put in the only possible field in the {self.unit}, {self.highlights[0]['cell']}."""
