from src.solutions.solving_techniques import SolvingTechniques
from itertools import combinations


class Swordfish(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Swordfish", board, candidates)
        self.cross_out_coordinates = None
        self.candidate = 0
        self.unit = ''

    def execute_technique(self):
        for self.unit in ['row', 'column']:
            for self.candidate in range(1, 10, 1):
                applicable_units = []
                for j in range(9):
                    unit_cells = SolvingTechniques.get_influential_cells_unit((j, j), self.unit)
                    cells_with_candidate = self.get_cells_with_candidate(unit_cells, self.candidate)
                    if 1 <= len(cells_with_candidate) <= 3:
                        applicable_units.append(cells_with_candidate)
                if len(applicable_units) < 3:
                    continue
                for combination in combinations(applicable_units, 3):
                    flattened_combination = SolvingTechniques.flatten(combination)
                    self.cross_out_coordinates = flattened_combination[1::2] if self.unit == 'row' else flattened_combination[0::2]
                    self.cross_out_coordinates = SolvingTechniques.remove_duplicates(self.cross_out_coordinates)
                    primary_coordinates = flattened_combination[1::2] if self.unit == 'column' else flattened_combination[0::2]
                    primary_coordinates = SolvingTechniques.remove_duplicates(primary_coordinates)
                    if len(self.cross_out_coordinates) == 3:
                        self.primary_cells = []
                        for primary_coordinate in primary_coordinates:
                            self.primary_cells.extend(SolvingTechniques.get_influential_cells_unit((primary_coordinate, primary_coordinate), self.unit))
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

        for coordinate in self.cross_out_coordinates:
            cells = SolvingTechniques.get_influential_cells_unit((coordinate, coordinate), orthogonal_unit[0])
            cells = list(set(cells) - set(self.primary_cells))
            for cell in cells:
                x, y = cell
                self.secondary_cells.append(cell)
                if self.board[x][y] != 0:
                    continue
                if self.candidates[x][y][self.candidate - 1]:
                    self.cross_outs.append({
                        'value': self.candidate,
                        'cell': cell
                    })
        for cell in self.primary_cells:
            x, y = cell
            if self.board[x][y] != 0:
                continue
            if self.candidates[x][y][self.candidate - 1]:
                self.highlights.append({
                    'value': self.candidate,
                    'cell': cell
                })

    def update_explanation(self):
        orthogonal_unit = ['row', 'column']
        orthogonal_unit.remove(self.unit)
        self.explanation = f"""The candidate {self.candidate} exists in three separate {self.unit}s and all fields containing this candidates in those {self.unit}s share only three separate {orthogonal_unit[0]}s.
Since the number {self.candidate} must occur once in each {self.unit}, there is definitely a {self.candidate} in one of the intersections in each {orthogonal_unit[0]}, and the remaining candidates can be eliminated from the {orthogonal_unit[0]}."""
