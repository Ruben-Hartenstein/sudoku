from src.solutions.solving_techniques import SolvingTechniques
from itertools import chain, combinations, count


class SkyScraper(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Skyscraper", board, candidates)
        self.candidate = 0
        self.unit = ''
        self.uneven_cell_pair = []

    def execute_technique(self):
        orthogonal_unit = ['column', 'row']
        for self.unit in ['row', 'column']:
            for self.candidate in range(1, 10, 1):
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
                    for this, that in combinations(relevant_cell_pairs, 2):
                        temp = this[:]
                        temp.extend(that)
                        # check if two candidates are at the same level in row/colum
                        coordinates = [element[orthogonal_unit.index(self.unit)] for element in temp]
                        for coordinate in coordinates:
                            if coordinates.count(coordinate) == 2:
                                # get uneven cell pair
                                self.uneven_cell_pair = []
                                for cell in temp:
                                    if cell[orthogonal_unit.index(self.unit)] != coordinate:
                                        self.uneven_cell_pair.append(cell)
                                self.primary_cells = temp
                                self.configure_highlighting()
                                if len(self.cross_outs) != 0:
                                    return True
                        else:
                            break
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

        for i in range(0, 3, 2):
            cells = SolvingTechniques.get_influential_cells_unit(self.primary_cells[i], self.unit)
            self.secondary_cells.extend(cells)

        influential_cells1 = []
        influential_cells2 = []
        for unit in ['box', orthogonal_unit[0]]:
            influential_cells1.extend(SolvingTechniques.get_influential_cells_unit(self.uneven_cell_pair[0], unit))
            influential_cells2.extend(SolvingTechniques.get_influential_cells_unit(self.uneven_cell_pair[1], unit))

        influential_cells1 = SolvingTechniques.remove_duplicates(influential_cells1)
        influential_cells2 = SolvingTechniques.remove_duplicates(influential_cells2)
        influential_cells = list(set(influential_cells1).intersection(influential_cells2))
        self.secondary_cells.extend(influential_cells)

        for cell in self.primary_cells:
            self.secondary_cells.remove(cell)

        for cell in influential_cells:
            x, y = cell
            if self.board[x][y] != 0:
                continue
            if self.candidates[x][y][self.candidate - 1] and cell not in self.primary_cells:
                self.cross_outs.append({
                    'value': self.candidate,
                    'cell': cell
                })
        print(self.primary_cells)

    def update_explanation(self):
        orthogonal_unit = ['row', 'column']
        orthogonal_unit.remove(self.unit)

        self.explanation = f"""The candidate {self.candidate} only exists twice in two separate {self.unit}s. 
Two of those fields are in the same row and see each other and the other two aren't. 
Thus, a {self.candidate} has to be in one of the cells {self.uneven_cell_pair[0]} and {self.uneven_cell_pair[1]} and all candidates  {self.candidate} in fields that are seen by both of these cells can be removed for certain."""


    def get_cells_with_candidate(self, cells, candidate):
        candidate_cells = []
        for cell in cells:
            x, y = cell
            if self.board[x][y] != 0:
                continue
            if self.candidates[x][y][candidate - 1]:
                candidate_cells.append(cell)
        return candidate_cells

