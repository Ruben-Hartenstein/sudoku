from src.solutions.solving_techniques import SolvingTechniques
from itertools import combinations, groupby


class AlmostLockedSets(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Almost Locked Sets", board, candidates)
        self.common_candidate = None
        self.second_common_candidate = None
        self.seeing_cells = None
        self.this = None
        self.that = None

    def execute_technique(self):
        almost_locked_sets = []
        for unit in ['row', 'column', 'box']:
            for index in range(9):
                occurring_candidates = []
                unit_cells = SolvingTechniques.get_unit_cells(index, unit)
                for cell in unit_cells:
                    x, y = cell
                    if self.board[x][y] != 0:
                        continue
                    for candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
                        if candidate not in occurring_candidates:
                            occurring_candidates.append(candidate)
                for size in range(4, 6):
                    for combo in set(combinations(occurring_candidates, size)):
                        matches = []
                        candidates_num = 0
                        for cell in unit_cells:
                            x, y = cell
                            if self.board[x][y] != 0:
                                continue
                            candidates_num = SolvingTechniques.format_candidates(self.candidates[x][y])
                            if all(c in combo for c in candidates_num):
                                matches.append(cell)
                        if len(matches) == size - 1:
                            almost_locked_sets.append(matches)
                        elif len(matches) == size:
                            for match in matches:
                                temp = matches[:]
                                temp.remove(match)
                                if all(c in combo for c in candidates_num):
                                    almost_locked_sets.append(temp)
        for self.this, self.that in (k for k, _ in groupby(combinations(almost_locked_sets, 2))):
            if any(elem in self.that for elem in self.this):
                continue
            this_candidates = SolvingTechniques.flatten([SolvingTechniques.format_candidates(self.candidates[x][y]) for x, y in self.this])
            that_candidates = SolvingTechniques.flatten([SolvingTechniques.format_candidates(self.candidates[x][y]) for x, y in self.that])
            common_candidates = list(set(this_candidates) & set(that_candidates))
            if len(common_candidates) < 2:
                continue
            for self.common_candidate in common_candidates:
                second_common_candidates = common_candidates[:]
                this_cells = self.get_cells_with_candidate(self.this, self.common_candidate)
                that_cells = self.get_cells_with_candidate(self.that, self.common_candidate)
                if all([this_cell in SolvingTechniques.get_unique_influential_cells(that_cell) for this_cell in this_cells for that_cell in that_cells]):
                    second_common_candidates.remove(self.common_candidate)
                    for self.second_common_candidate in second_common_candidates:
                        this_second_cells = self.get_cells_with_candidate(self.this, self.second_common_candidate)
                        that_second_cells = self.get_cells_with_candidate(self.that, self.second_common_candidate)
                        self.seeing_cells = this_second_cells[:]
                        self.seeing_cells.extend(that_second_cells)
                        self.configure_highlighting()
                        if len(self.cross_outs) != 0:
                            return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.primary_cells = self.this[:]
        self.secondary_cells = self.that[:]

        for loop_list in [self.this, self.that]:
            for (x, y) in loop_list:
                if self.common_candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
                    self.highlights.append({
                        'value': self.common_candidate,
                        'cell': (x, y)
                    })

        delete_cells = SolvingTechniques.get_unique_influential_cells(self.seeing_cells[0])
        for seeing_cell in self.seeing_cells[1:]:
            delete_cells = list(set(delete_cells) & set(SolvingTechniques.get_unique_influential_cells(seeing_cell)))
        for (x, y) in delete_cells:
            if self.board[x][y] != 0 or (x, y) in self.this or (x, y) in self.that:
                continue
            if self.second_common_candidate not in SolvingTechniques.format_candidates(self.candidates[x][y]):
                continue
            self.cross_outs.append({
                'value': self.second_common_candidate,
                'cell': (x, y)
            })

    def update_explanation(self):
        self.explanation = f"""There are two almost locked sets (naked sets with one degree of freedom) that share a common candidate {self.common_candidate},  and every candidate {self.common_candidate} from one ALS, sees every {self.common_candidate} from the other.
Thus only one ALS can include this candidate. The two ALS also share a second common candidate {self.second_common_candidate} which consequently has to be in one of the cells in one of the ALS.
Therefore all candidates {self.second_common_candidate} outside of the  ALS seen by all cells with the candidate {self.second_common_candidate} within the ALS can be deleted."""
