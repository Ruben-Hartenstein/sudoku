from src.solutions.solving_techniques import SolvingTechniques

class Turbot(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Turbot", board, candidates)
        self.candidate = 0
        self.unit = ''
        self.other_cell = []

    def execute_technique(self):
        orthogonal_unit = ['column', 'row']
        for self.unit in ['row', 'column']:
            for self.candidate in range(1, 10, 1):
                for j in range(9):
                    relevant_cells = []
                    unit_cells = SolvingTechniques.get_influential_cells_unit((j, j), self.unit)
                    appearance = 0
                    for cell in unit_cells:
                        x, y = cell
                        if self.board[x][y] != 0:
                            continue
                        if self.candidates[x][y][self.candidate - 1]:
                            appearance += 1
                            relevant_cells.append(cell)
                    if appearance == 2:
                        if SolvingTechniques.get_box(relevant_cells[0]) == SolvingTechniques.get_box(relevant_cells[1]):
                            break
                        index = orthogonal_unit.index(self.unit)
                        self.primary_cells = relevant_cells

                        for i in range(2):
                            influential_cells_orthogonal = self.get_cells_with_candidate(SolvingTechniques.get_influential_cells_unit(relevant_cells[i], orthogonal_unit[1-index]), self.candidate)
                            influential_cells_orthogonal.remove(relevant_cells[i])
                            # Überprüfung nicht notwendig, wegen Hidden Single?
                            if not influential_cells_orthogonal:
                                break
                            for cell in influential_cells_orthogonal:
                                removable_cells = []
                                influential_cells_box = self.get_cells_with_candidate(SolvingTechniques.get_influential_cells_unit(cell, 'box'), self.candidate)
                                influential_cells_box.remove(cell)
                                removable_cells = list(set(influential_cells_orthogonal).intersection(influential_cells_box))
                                for removable_cell in removable_cells:
                                    influential_cells_box.remove(removable_cell)
                                if not influential_cells_box:
                                    break
                                elif not self.check_same_height(influential_cells_box, index):
                                    break

                                coordinate_chain = influential_cells_box[0][1-index]
                                coordinate_box = cell[1-index]
                                if coordinate_box != coordinate_chain:
                                    self.other_cell = self.get_cells_with_candidate(SolvingTechniques.get_influential_cells_unit(relevant_cells[1-i], orthogonal_unit[1-index]), self.candidate)
                                    influential_cells_chain = self.get_cells_with_candidate(SolvingTechniques.get_influential_cells_unit(influential_cells_box[0], self.unit), self.candidate)
                                    self.other_cell = list(set(influential_cells_chain).intersection(self.other_cell))
                                    if not self.other_cell:
                                        break
                                    self.primary_cells.append(cell)
                                    self.primary_cells.append(influential_cells_box[0])
                                    self.primary_cells.append(self.other_cell[0])
                                    self.primary_cells = SolvingTechniques.remove_duplicates(self.primary_cells)
                                    self.configure_highlighting()
                                    if len(self.cross_outs) != 0 and len(self.primary_cells) >= 5:
                                        return True

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = []

        orthogonal_unit = ['row', 'column']
        orthogonal_unit.remove(self.unit)

        self.cross_outs.append({
            'value': self.candidate,
            'cell': self.other_cell[0]
        })

        for cell in self.primary_cells:
            self.highlights.append({
                'value': self.candidate,
                'cell': cell
            })

        self.highlights.remove({
            'value': self.candidate,
            'cell': self.other_cell[0]
        })

        self.secondary_cells.extend(SolvingTechniques.get_influential_cells_unit(self.primary_cells[0], self.unit))
        self.secondary_cells.remove(self.primary_cells[0])
        self.secondary_cells.remove(self.primary_cells[1])




    def update_explanation(self):
        self.explanation = f"""The candidate {self.candidate} appears only twice in a {self.unit}, but in different blocks.
The target object is in a field that is logically reached by both of these initial candidates, in this case {self.cross_outs[0]['cell']}. 
Regardless of which of the two candidates in the starting {self.unit} is correct, we can eliminate the {self.candidate} in the orthogonal target field {self.cross_outs[0]['cell']}, 
because the elimination is either directly or via a small chain {self.primary_cells[2]} and {self.primary_cells[3]}.
"""

    def get_cells_with_candidate(self, cells, candidate):
        candidate_cells = []
        for cell in cells:
            x, y = cell
            if self.board[x][y] != 0:
                continue
            if self.candidates[x][y][candidate - 1]:
                candidate_cells.append(cell)
        return candidate_cells

    def check_same_height(self, cells, index):
        height = [el[1-index] for el in cells]
        if len(set(height)) == 1:
            return True
        else:
            return False