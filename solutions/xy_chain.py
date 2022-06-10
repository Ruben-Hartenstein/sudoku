from solutions.solving_techniques import SolvingTechniques
from solutions.chains import Chain


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
                domino = Chain(self, (i, j))
                candidates = SolvingTechniques.format_candidates(self.candidates[i][j])
                chains = []
                for candidate in candidates:
                    domino.calculate_all_domino_chains(candidate)
                    chains.append(domino.chains)

                for self.chain0 in chains[0]:
                    for self.chain1 in chains[1]:
                        self.candidate = domino.get_domino_last_insert(self.chain0, candidates[0])
                        if self.candidate != domino.get_domino_last_insert(self.chain1, candidates[1]):
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
        print(SolvingTechniques.format_candidates(self.candidates[self.primary_cells[0][0]][self.primary_cells[0][1]])[0])
        self.explanation = f"""If the candidate {SolvingTechniques.format_candidates(self.candidates[self.primary_cells[0][0]][self.primary_cells[0][1]])[0]} would be inserted into the field {SolvingTechniques.pretty_print_cells(self.primary_cells[0])}, the candidate {self.candidate} has to be inserted into the field {SolvingTechniques.pretty_print_cells(self.chain0[-1])} via the chain {SolvingTechniques.pretty_print_cells(self.chain0)}.
If the candidate {SolvingTechniques.format_candidates(self.candidates[self.primary_cells[0][0]][self.primary_cells[0][1]])[1]} would be inserted into the field {SolvingTechniques.pretty_print_cells(self.primary_cells[0])}, the candidate {self.candidate} has to be inserted into the field {SolvingTechniques.pretty_print_cells(self.chain1[-1])} via the chain {SolvingTechniques.pretty_print_cells(self.chain1)}.
In all possible cases, the candidate {self.candidate} has to be inserted into one of the two ends of the chains, therefore the candidate can be deleted in all fields, seen by both of them."""
