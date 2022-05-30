from src.solutions.solving_techniques import SolvingTechniques
from src.solutions.chains import Chain


class XYChain(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("XY-Chain", board, candidates)
        self.chain0 = None
        self.chain1 = None
        self.candidate = None
        self.chain = None

    def execute_technique(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0 or sum(self.candidates[i][j]) != 2:
                    continue
                domino = Chain(self.board, self.candidates, (i, j))
                candidates = SolvingTechniques.format_candidates(self.candidates[i][j])
                chains = []
                for candidate in candidates:
                    domino.calculate_all_chains(candidate)
                    chains.append(domino.chains)

                for self.chain0 in chains[0]:
                    for self.chain1 in chains[1]:
                        self.candidate = domino.get_last_insert(self.chain0, candidates[0])
                        if self.candidate != domino.get_last_insert(self.chain1, candidates[1]):
                            continue
                        self.primary_cells = [self.chain0[0]]
                        self.configure_highlighting()
                        if len(self.cross_outs) != 0:
                            return True

        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []

        self.secondary_cells = self.chain0[:]
        self.secondary_cells.extend(self.chain1)
        self.secondary_cells = SolvingTechniques.remove_duplicates(self.secondary_cells)
        self.secondary_cells.remove(self.chain0[0])

        for x, y in SolvingTechniques.get_overlap_cells(self.chain0[-1], self.chain1[-1]):
            if self.board[x][y] != 0 or (x, y) in self.chain0 or (x, y) in self.chain1:
                continue
            if self.candidate not in SolvingTechniques.format_candidates(self.candidates[x][y]):
                continue
            self.cross_outs.append({'value': self.candidate,
                                    'cell': (x, y)})

        for cell in [self.chain0[-1], self.chain1[-1]]:
            self.highlights.append({'value': self.candidate,
                                    'cell': cell})


    def update_explanation(self):
        self.explanation = f"""If either possible candidate in the field {self.primary_cells[0]} would be inserted, the candidate {self.candidate} either has to be inserted into the field {self.chain0[-1]} or {self.chain1[-1]}.
The candidate {self.candidate} can therefore be deleted from all cells, seen by both of them."""
