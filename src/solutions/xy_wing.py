from src.solutions.solving_techniques import SolvingTechniques
from src.solutions.chains import Chain


class XYWing(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("XY Wing", board, candidates)
        self.candidate = None
        self.chain = None

    def execute_technique(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0 or sum(self.candidates[i][j]) != 2:
                    continue
                domino = Chain(self.board, self.candidates, (i, j), 3)
                candidates = SolvingTechniques.format_candidates(self.candidates[i][j])
                for candidate in candidates:
                    domino.calculate_all_chains(1, candidate)
                    chains = [chain for chain in domino.chains if len(chain) == 3]
                    for self.chain in chains:
                        x, y = self.chain[-1]
                        self.candidate = candidates[:]
                        self.candidate.remove(candidate)
                        self.candidate = self.candidate[0]
                        if self.candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
                            self.primary_cells = self.chain
                            self.configure_highlighting()
                            if len(self.cross_outs) != 0:
                                return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = []

        for x, y in SolvingTechniques.get_overlap_cells(self.chain[0], self.chain[-1]):
            if self.board[x][y] != 0 or (x, y) in self.chain:
                continue
            if self.candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
                self.cross_outs.append({'value': self.candidate,
                                        'cell': (x, y)})
        for i, cell in enumerate(self.chain):
            if i % 2 == 0:
                candidates = SolvingTechniques.format_candidates(self.candidates[cell[0]][cell[1]])
                candidates.remove(self.candidate)
                candidate = candidates[0]
                self.highlights.append({'value': candidate,
                                        'cell': cell})
            else:
                for candidate in SolvingTechniques.format_candidates(self.candidates[cell[0]][cell[1]]):
                    self.highlights.append({'value': candidate,
                                            'cell': cell})

    def update_explanation(self):
        first_cell = self.chain[0]
        first_other_candidate = SolvingTechniques.format_candidates(self.candidates[first_cell[0]][first_cell[1]])
        first_other_candidate.remove(self.candidate)
        first_other_candidate = first_other_candidate[0]
        self.explanation = f"""If the candidate, {self.candidate} would be inserted into the cell {self.chain[0]}, all candidates {self.candidate} have to be deleted from the influenced cells.
If the other possibility {first_other_candidate} would be inserted, the candidate {self.candidate} has to be placed into the cell {self.chain[-1]}.
Therefore all candidates {self.candidate} that are seen by both cells can be deleted."""
