from src.solutions.solving_techniques import SolvingTechniques


class ThirdEye(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Third Eye", board, candidates)
        self.unit = ''

    def execute_technique(self):
        three_candidates_once = False
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    continue
                if sum(self.candidates[i][j]) == 2:
                    continue
                elif sum(self.candidates[i][j]) == 3 and not three_candidates_once:
                    three_candidates_once = True
                    self.primary_cells.append((i, j))
                    occurring_candidates = SolvingTechniques.format_candidates(self.candidates[i][j])
                    continue
                else:
                    return False

        for self.unit in ['row', 'column', 'box']:
            unit_cells = SolvingTechniques.get_influential_cells_unit(self.primary_cells[0], self.unit)
            for candidate in occurring_candidates:
                appereances = 0
                for cell in unit_cells:
                    x, y = cell
                    if self.board[x][y] != 0:
                        continue
                    if candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
                        appereances += 1
                if appereances == 3:
                    self.highlights.append({
                        'value': candidate,
                         'cell': self.primary_cells[0]
                         })
                    for temp in occurring_candidates:
                        if temp != candidate:
                            self.cross_outs.append({
                                'value': temp,
                                'cell': self.primary_cells[0]
                            })
                    return True


    def update_secondary_cells(self):
        cell = self.primary_cells[0]
        influential_cells = SolvingTechniques.get_influential_cells(cell)
        for key in influential_cells.keys():
            self.secondary_cells.extend(influential_cells[key])
        self.secondary_cells = SolvingTechniques.remove_duplicates(self.secondary_cells)
        self.secondary_cells.remove(cell)

    def update_explanation(self):
        self.explanation = f"""On the whole board every field has two candidates, except the field {self.highlights[0]['cell']} which has three.
The candidate that is contained in three fields in one unit (in this case {self.highlights[0]['value']}) can be inserted otherwise the sudoku is not uniquely solvable."""