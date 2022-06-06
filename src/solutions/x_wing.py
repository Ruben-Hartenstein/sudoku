from src.solutions.solving_techniques import SolvingTechniques
from itertools import chain, combinations, groupby


class XWing(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("X-Wing", board, candidates)
        self.candidate = 0
        self.unit = ''

    def execute_technique(self):
        for self.unit in ['row', 'column']:
            for self.candidate in range(1, 10):
                twice_appearances = []
                for j in range(9):
                    unit_cells = SolvingTechniques.get_influential_cells_unit((j, j), self.unit)
                    appearance = 0
                    for cell in unit_cells:
                        x, y = cell
                        if self.board[x][y] != 0:
                            continue
                        if self.candidates[x][y][self.candidate - 1]:
                            appearance += 1
                    if appearance == 2:
                        twice_appearances.append(unit_cells)
                if len(twice_appearances) >= 2:
                    relevant_cell_pairs = [self.get_cells_with_candidate(twice_appearance, self.candidate) for twice_appearance in twice_appearances]
                    for this, that in (k for k, _ in groupby(combinations(relevant_cell_pairs, 2))):
                        temp = this[:]
                        temp.extend(that)
                        coordinates = list(chain.from_iterable(temp))
                        for coordinate in coordinates:
                            if coordinates.count(coordinate) % 2:
                                break
                        else:
                            self.primary_cells = temp
                            self.configure_highlighting()
                            if len(self.cross_outs) != 0:
                                return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = []

        orthogonal_unit = ['row', 'column']
        orthogonal_unit.remove(self.unit)

        for cell in self.primary_cells:
            self.highlights.append({
                'value': self.candidate,
                'cell': cell
            })

        for i in range(2):
            cells = SolvingTechniques.get_influential_cells_unit(self.primary_cells[i], orthogonal_unit[0])
            cells.remove(self.primary_cells[i])
            cells.remove(self.primary_cells[i + 2])
            self.secondary_cells.extend(cells)
            for cell in cells:
                x, y = cell
                if self.board[x][y] != 0:
                    continue
                if self.candidates[x][y][self.candidate - 1]:
                    self.cross_outs.append({
                        'value': self.candidate,
                        'cell': cell
                    })
        for i in range(2):
            cells = SolvingTechniques.get_influential_cells_unit(self.primary_cells[i+1], self.unit)
            cells.remove(self.primary_cells[i+1])
            self.primary_cells.extend(cells)
        self.primary_cells = SolvingTechniques.remove_duplicates(self.primary_cells)


    def update_explanation(self):
        orthogonal_unit = ['row', 'column']
        orthogonal_unit.remove(self.unit)
        self.explanation = f"""The candidate {self.candidate} only exists twice in two separate {self.unit}s and all 4 fields appear only in two {orthogonal_unit[0]}s.
Because {self.candidate} has to be placed twice in those 4 fields, their place in the {self.unit}s can be restricted to those two {orthogonal_unit[0]}s and 
any other candidate with the value {self.candidate} can be removed from the two {orthogonal_unit[0]}s."""
