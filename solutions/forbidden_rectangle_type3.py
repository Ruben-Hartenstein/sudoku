from solutions.solving_techniques import SolvingTechniques
from solutions.chains import Chain

class ForbiddenRectangleType3(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Forbidden Rectangle Type 3", board, candidates)
        self.chain = None
        self.delete_cells = None
        self.candidate = None
        self.unit = None
        self.candidate_pair_values = None

    def execute_technique(self):
        units = ['row', 'column']
        for i, self.unit in enumerate(units):
            for j in range(9):
                unit_cells = SolvingTechniques.get_influential_cells_unit((j, j), self.unit)
                for x, y in unit_cells:
                    self.primary_cells = []
                    if self.board[x][y] != 0 or sum(self.candidates[x][y]) != 2:
                        continue
                    self.primary_cells.append((x, y))
                    candidate_pair = self.candidates[x][y]
                    temp_cells = SolvingTechniques.get_influential_cells_unit((x, y), self.unit)
                    for temp_cell in temp_cells:
                        k, l = temp_cell
                        if self.board[k][l] != 0 or (k, l) == (x, y):
                            continue
                        if self.candidates[k][l] == candidate_pair:
                            self.primary_cells.append((k, l))
                    if len(self.primary_cells) != 2:
                        continue
                    self.candidate_pair_values = SolvingTechniques.format_candidates(candidate_pair)
                    orthogonal_cells = SolvingTechniques.get_influential_cells_unit(self.primary_cells[0], units[1 - i])
                    for third_cell in orthogonal_cells:
                        k, l = third_cell
                        if self.board[k][l] != 0 or (k, l) == (x, y) or 3 > sum(self.candidates[k][l]) < 4:
                            continue
                        candidate_third_cell_value = SolvingTechniques.format_candidates(self.candidates[k][l])
                        if not all(elem in candidate_third_cell_value for elem in self.candidate_pair_values):
                            continue
                        cross_cells = self.get_cross_cells(self.primary_cells[1], (k, l))
                        cross_cells = [cross_cell for cross_cell in cross_cells if self.board[cross_cell[0]][cross_cell[1]] == 0]
                        fourth_cell = list(set(cross_cells) - set(self.primary_cells))
                        if not fourth_cell:
                            continue
                        fourth_cell = fourth_cell[0]
                        candidate_fourth_cell_value = SolvingTechniques.format_candidates(self.candidates[fourth_cell[0]][fourth_cell[1]])
                        if not all(elem in candidate_fourth_cell_value for elem in self.candidate_pair_values):
                            continue
                        candidates = candidate_third_cell_value[:]
                        candidates.extend(candidate_fourth_cell_value)
                        candidates = SolvingTechniques.remove_duplicates(candidates)
                        if len(candidates) != 4:
                            continue
                        self.other_candidates = list(set(candidates) - set(self.candidate_pair_values))
                        chain_start_cells = []
                        for candidate in self.other_candidates:
                            candidate_in_third = candidate in candidate_third_cell_value
                            candidate_in_fourth = candidate in candidate_fourth_cell_value
                            if candidate_in_third and candidate_in_fourth:
                                chain_start_cells.append(SolvingTechniques.get_overlap_cells(third_cell, fourth_cell))
                            elif candidate_in_third:
                                chain_start_cells.append(SolvingTechniques.get_unique_influential_cells(third_cell))
                            elif candidate_in_fourth:
                                chain_start_cells.append(SolvingTechniques.get_unique_influential_cells(fourth_cell))

                        for index, start_cells in enumerate(chain_start_cells):
                            for start_cell in start_cells:
                                if start_cell in [third_cell, fourth_cell]:
                                    continue
                                if self.board[start_cell[0]][start_cell[1]] != 0 or sum(self.candidates[start_cell[0]][start_cell[1]]) != 2:
                                    continue
                                chain_start_candidate = SolvingTechniques.format_candidates(self.candidates[start_cell[0]][start_cell[1]])
                                if self.other_candidates[index] not in chain_start_candidate:
                                    continue
                                self.candidate = self.other_candidates[1 - index]
                                domino = Chain(self, start_cell)
                                chain_start_candidate.remove(self.other_candidates[index])
                                domino.calculate_all_domino_chains(chain_start_candidate[0])
                                chains = domino.chains
                                for self.chain in chains:
                                    if domino.get_domino_last_insert(self.chain) != self.candidate:
                                        continue
                                    primary_cells_copy = self.primary_cells[:]
                                    self.primary_cells.append(third_cell)
                                    self.primary_cells.append(fourth_cell)
                                    self.delete_cells = list(set(SolvingTechniques.get_unique_influential_cells(self.chain[-1])) & set(chain_start_cells[1 - index]) - set(self.primary_cells) - set(self.chain))
                                    self.configure_highlighting()
                                    if len(self.cross_outs) != 0:
                                        return True
                                    self.primary_cells = primary_cells_copy[:]
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = self.chain

        for x, y in self.primary_cells:
            for candidate in self.other_candidates:
                if candidate not in SolvingTechniques.format_candidates(self.candidates[x][y]):
                    continue
                self.highlights.append({
                    'value': candidate,
                    'cell': (x, y)
                })

        for x, y in self.delete_cells:
            if self.board[x][y] != 0:
                continue
            if self.candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
                self.cross_outs.append({'value': self.candidate,
                                        'cell': (x, y)})

    def update_explanation(self):
        self.explanation = f"""The orange squares form a forbidden rectangle. Since there must be a unique solution, 
at least a {self.other_candidates[0]} or a {self.other_candidates[1]} must be entered in one of the two fields. 
Regardless of which number is entered in which field, the candidate {self.candidate} can be deleted either directly or via the blue chain."""