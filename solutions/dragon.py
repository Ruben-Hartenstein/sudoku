from solutions.solving_techniques import SolvingTechniques


class Dragon(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Dragon", board, candidates)
        self.candidate = 0

    def execute_technique(self):
        for self.candidate in range(1, 10, 1):
            for i in range(9):
                unit_cells_row = SolvingTechniques.get_influential_cells_unit((i, i), 'row')
                appearance = 0
                for cell_row in unit_cells_row:
                    x, y = cell_row
                    if self.board[x][y] != 0:
                        continue
                    if self.candidates[x][y][self.candidate - 1]:
                        appearance += 1
                if appearance == 2:
                    for j in range(9):
                        unit_cells_column = SolvingTechniques.get_influential_cells_unit((j, j), 'column')
                        appearance = 0
                        for cell_column in unit_cells_column:
                            x, y = cell_column
                            if self.board[x][y] != 0:
                                continue
                            if self.candidates[x][y][self.candidate - 1]:
                                appearance += 1
                        if appearance == 2:
                            relevant_cells_row = self.get_cells_with_candidate(unit_cells_row, self.candidate)
                            relevant_cells_column = self.get_cells_with_candidate(unit_cells_column, self.candidate)
                            self.primary_cells = []
                            self.primary_cells.extend(relevant_cells_row)
                            self.primary_cells.extend(relevant_cells_column)
                            self.primary_cells = SolvingTechniques.remove_duplicates(self.primary_cells)
                            if len(self.primary_cells) == 4:
                                for k in range(2):
                                    for l in range(2):
                                        if SolvingTechniques.get_box(relevant_cells_row[k]) == SolvingTechniques.get_box(relevant_cells_column[l]):
                                            _, y = relevant_cells_row[1-k]
                                            x, _ = relevant_cells_column[1-l]
                                            if self.board[x][y] != 0:
                                                continue
                                            if self.candidates[x][y][self.candidate - 1]:
                                                self.primary_cells.append((x,y))
                                                self.configure_highlighting()
                                                return True

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = []

        for cell in self.primary_cells:
            self.highlights.append({
                'value': self.candidate,
                'cell': cell
            })

        self.cross_outs.append({
            'value': self.candidate,
            'cell': self.primary_cells[4]
        })

        self.highlights.remove({
            'value': self.candidate,
            'cell': self.primary_cells[4]
        })

        cells = SolvingTechniques.get_influential_cells_unit(self.primary_cells[0], 'row')
        cells.remove(self.primary_cells[0])
        cells.remove(self.primary_cells[1])
        self.secondary_cells.extend(cells)
        cells = SolvingTechniques.get_influential_cells_unit(self.primary_cells[2], 'column')
        cells.remove(self.primary_cells[2])
        cells.remove(self.primary_cells[3])
        self.secondary_cells.extend(cells)

    def update_explanation(self):
        self.explanation = f"""The candidate {self.candidate} exists only twice in a row and a column and two of those cells share one box. 
The cell {self.primary_cells[4]} builds the intersection of the other two cells.
No matter where the candidate {self.candidate} is entered, because of the logical connection the {self.candidate} can be deleted in the cell {self.primary_cells[4]}."""

