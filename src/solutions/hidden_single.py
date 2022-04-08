from src.solutions.solving_techniques import SolvingTechniques


class HiddenSingle(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Hidden Single",
                         """Every number already entered covers a row, a column and a block.
                          Therefore, very often there are situations in which there is only
                           one free field for a given number within a unit * (in block 9, 
                           the 7 fits only in the green field).""",
                         board, candidates)
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
                            self.primary_cells.append((x, y))
                            candidate_once = True
                    if candidate_once:
                        self.cross_out.append(
                            {'value': num,
                             'cell': self.primary_cells[0]})
                        self.unit = key
                        return True
        return False

    def update_secondary_cells(self):
        cell = self.cross_out[0]['cell']
        cross_out_value = self.cross_out[0]['value']
        influential_cells = SolvingTechniques.get_influential_cells(cell)
        for i, j in influential_cells[self.unit]:
            if (i, j) == cell:
                continue
            if self.board[i][j] != 0:
                self.secondary_cells.append((i, j))
            else:
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
                        if self.board[x][y] == cross_out_value:
                            num_in_unit = True
                    if num_in_unit:
                        self.secondary_cells.extend(temp_cells)
                        break
        self.secondary_cells = SolvingTechniques.remove_duplicates(self.secondary_cells)
