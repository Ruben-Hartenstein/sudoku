from solutions.solving_techniques import SolvingTechniques
from solutions.chains import Chain


class DoubleChain(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Double Chain", board, candidates)
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
                    chains.append([chain for chain in domino.chains if len(chain) >= 3])
                if not all(chain for chain in chains):
                    continue
                for self.chain in chains[0]:
                    for chain1 in chains[1]:
                        if len(self.chain) != len(chain1):
                            continue
                        first_part = chain1.pop(0)
                        chain1.reverse()
                        chain1.insert(0, first_part)
                        if chain1 != self.chain:
                            continue
                        if self.chain[0] not in SolvingTechniques.get_unique_influential_cells(self.chain[-1]):
                            continue
                        if domino.get_domino_last_insert(self.chain) not in SolvingTechniques.format_candidates(
                                self.candidates[self.chain[0][0]][self.chain[0][1]]):
                            continue
                        self.primary_cells = self.chain
                        self.configure_highlighting()

                        if len(self.cross_outs) != 0:
                            return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.secondary_cells = []

        for x, y in self.chain:
            for candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
                for unit in ['column', 'row', 'box']:
                    unit_cells = SolvingTechniques.get_influential_cells_unit((x, y), unit)
                    if not any([candidate in SolvingTechniques.format_candidates(self.candidates[cell[0]][cell[1]]) and cell != (x, y) and cell in self.chain for cell in unit_cells]):
                        continue
                    for cell in unit_cells:
                        if self.board[cell[0]][cell[1]] or cell in self.chain:
                            continue
                        if candidate in SolvingTechniques.format_candidates(self.candidates[cell[0]][cell[1]]):
                            self.secondary_cells.append(cell)
                            self.cross_outs.append({
                                'value': candidate,
                                'cell': cell
                            })

    def update_explanation(self):
        self.explanation = f"""Two closed chains are on the same fields, {self.chain}.
    If two parts of the chain with the same candidate are in the same unit, all other candidates of that value in the unit can be deleted."""
