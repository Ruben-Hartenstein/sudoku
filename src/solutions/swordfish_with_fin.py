from src.solutions.solving_techniques import SolvingTechniques
from itertools import combinations, chain, groupby


class SwordfishWithFin(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Swordfish With Fin", board, candidates)
        self.box_fields = None
        self.list = None
        self.fin = None
        self.cross_out_coordinates = None
        self.candidate = 0
        self.unit = ''

    def execute_technique(self):
        for self.unit in ['row', 'column']:
            for self.candidate in range(1, 10):
                applicable_units = []
                for j in range(9):
                    unit_cells = SolvingTechniques.get_influential_cells_unit((j, j), self.unit)
                    cells_with_candidate = self.get_cells_with_candidate(unit_cells, self.candidate)
                    if 1 <= len(cells_with_candidate) <= 4:
                        applicable_units.append(cells_with_candidate)
                if len(applicable_units) < 3:
                    continue
                for list1, list2, list3 in (k for k, _ in groupby(combinations(applicable_units, 3))):
                    combination = list(chain(list1, list2, list3))
                    flattened_combination = SolvingTechniques.flatten(combination)
                    coordinates = flattened_combination[1::2] if self.unit == 'row' else flattened_combination[0::2]
                    self.cross_out_coordinates = SolvingTechniques.remove_duplicates(coordinates)
                    primary_coordinates = flattened_combination[1::2] if self.unit == 'column' else flattened_combination[0::2]
                    unique_primary_coordinates = SolvingTechniques.remove_duplicates(primary_coordinates)
                    if len(self.cross_out_coordinates) != 4:
                        continue
                    for coordinate1, coordinate2 in zip(coordinates, primary_coordinates):
                        if coordinates.count(coordinate1) != 1:
                            continue
                        self.fin = (coordinate2, coordinate1) if self.unit == "row" else (coordinate1, coordinate2)
                        for self.list in [list1, list2, list3]:
                            if self.fin not in self.list:
                                continue
                            self.box_fields = []
                            for field in self.list:
                                if field == self.fin or SolvingTechniques.get_box(self.fin) != SolvingTechniques.get_box(field):
                                    continue
                                self.box_fields.append(field)
                            if not self.box_fields:
                                continue
                            self.primary_cells = []
                            for primary_coordinate in unique_primary_coordinates:
                                self.primary_cells.extend(SolvingTechniques.get_influential_cells_unit(
                                    (primary_coordinate, primary_coordinate), self.unit))
                            self.configure_highlighting()
                            if len(self.cross_outs) != 0:
                                return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = []
        self.primary_cells = SolvingTechniques.remove_duplicates(self.primary_cells)

        orthogonal_unit = ['row', 'column']
        orthogonal_unit.remove(self.unit)
        orthogonal_unit = orthogonal_unit[0]

        swordfish_fields = []
        for box_field in self.box_fields:
            swordfish_fields.extend(SolvingTechniques.get_influential_cells_unit(box_field, orthogonal_unit))

        swordfish_fields = SolvingTechniques.remove_duplicates(swordfish_fields)

        for x, y in SolvingTechniques.get_influential_cells_unit(self.fin, 'box'):
            if (x, y) in self.list or (x, y) not in swordfish_fields or (x, y) in self.primary_cells:
                continue
            self.secondary_cells.append((x, y))
            if self.board[x][y] != 0:
                continue
            if self.candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
                self.cross_outs.append({
                    'value': self.candidate,
                    'cell': (x, y)
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
        self.primary_cells.remove(self.fin)
        self.secondary_cells.append(self.fin)

    def update_explanation(self):
        orthogonal_unit = ['row', 'column']
        orthogonal_unit.remove(self.unit)
        self.explanation = f"""The candidate {self.candidate} depicts a swordfish, except for the fin, {self.fin}. It is therefore no real swordfish.
Nevertheless, the candidate {self.candidate} from the overlapping fields of influence of the swordfish and the fin, can be deleted."""
