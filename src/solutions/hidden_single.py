from src.solutions.solving_techniques import SolvingTechniques


class HiddenSingle(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Hidden Single", board, candidates)
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
                        self.highlights = [{'value': num, 'cell': self.primary_cells[0]}]
                        self.unit = key
                        return True
        return False

    def update_secondary_cells(self):
        cell = self.highlights[0]['cell']
        highlight_value = self.highlights[0]['value']
        influential_cells = SolvingTechniques.get_influential_cells_unit(cell, self.unit)
        for i, j in influential_cells:
            if (i, j) == cell:
                continue

            self.secondary_cells.append((i, j))
            cells = SolvingTechniques.get_influential_cells((i, j))
            keys = list(cells.keys())
            keys.reverse()
            for key in keys:
                temp_cells = []
                num_in_unit = False
                if key == self.unit:
                    continue
                for x, y in cells[key]:
                    temp_cells.append((x, y))
                    if self.board[x][y] == highlight_value:
                        num_in_unit = True
                if num_in_unit:
                    self.secondary_cells.extend(temp_cells)
                    break
        self.secondary_cells = SolvingTechniques.remove_duplicates(self.secondary_cells)

    def update_explanation(self):
        self.explanation = f"""Every {self.highlights[0]['value']} in the {self.unit}, except one, is blocked.
Therefore, {self.highlights[0]['value']} can be put in the only possible field in the {self.unit}, {self.highlights[0]['cell']}."""
