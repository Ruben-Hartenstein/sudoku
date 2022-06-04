from src.solutions.solving_techniques import SolvingTechniques
from src.solutions.chains import Chain


class XChain(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("X-Chain", board, candidates)
        self.candidate = None
        self.chain = None

    def execute_technique(self):
        for unit in ['row', 'column', 'box']:
            for index in range(9):
                for self.candidate in range(1, 10):
                    unit_cells = SolvingTechniques.get_unit_cells(index, unit)
                    cells = self.get_cells_with_candidate(unit_cells, self.candidate)
                    if len(cells) != 2:
                        continue
                    for cell in cells:
                        x_chain = Chain(self, cell)
                        x_chain.calculate_all_x_chains(self.candidate)
                        x_chains = [x_chain for x_chain in x_chain.chains if len(x_chain) > 1]
                        if not x_chains:
                            continue
                        for self.chain in x_chains:
                            self.configure_highlighting()
                            if len(self.cross_outs) != 0:
                                return True
        return False

    def configure_highlighting(self):
        self.highlights = []
        self.cross_outs = []
        self.primary_cells = self.chain[0::2]
        self.secondary_cells = self.chain[1::2]

        for index in range(9):
            unit_cells = SolvingTechniques.get_unit_cells(index, 'row')
            cells = self.get_cells_with_candidate(unit_cells, self.candidate)
            for x, y in cells:
                if (x, y) in self.chain:
                    continue
                influential_cells = SolvingTechniques.get_unique_influential_cells((x, y))
                if any(cell in self.primary_cells for cell in influential_cells) and any(cell in self.secondary_cells for cell in influential_cells):
                    self.cross_outs.append(
                        {'value': self.candidate,
                         'cell': (x, y)})

        for x, y in self.chain:
            if self.candidate in SolvingTechniques.format_candidates(self.candidates[x][y]):
                self.highlights.append(
                    {'value': self.candidate,
                     'cell': (x, y)})

    def update_explanation(self):
        self.explanation = f"""If a candidate (here {self.candidate}) occurs only twice in a unit one of them is always correct while the other is not.
If there are several such pairs of candidates, and their units overlap, a logical chain can be build in which alternately one candidate is correct while the other is not.
While the order of which is wrong and which is correct cannot be said, any candidate seen from both kind of squares can be eliminated since one definitely is correct."""
