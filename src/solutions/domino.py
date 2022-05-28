from src.solutions.solving_techniques import SolvingTechniques


class Domino:
    def __init__(self, solving_technique, start_cell, board, candidates, max_depth):
        self.solving_technique = solving_technique
        self.start_cell = start_cell
        self.cross_outs = []
        self.board = board[:]
        self.candidates = candidates[:]
        self.max_depth = max_depth
        self.chains = []

    def calculate_all_chains(self, depth, insert, passed_chain=[], cell=None):
        if not cell:
            cell = self.start_cell
            self.chains = []
        chain = passed_chain[:]
        chain.append(cell)
        dominos = self.get_all_dominos(cell, insert)
        if depth < self.max_depth:
            for x, y in dominos:
                if (x, y) in chain:
                    continue
                candidate = SolvingTechniques.format_candidates(self.candidates[x][y])
                candidate.remove(insert)
                candidate = candidate[0]
                self.calculate_all_chains(depth + 1, candidate, chain, (x, y))
        self.chains.append(chain)

    def get_all_dominos(self, cell, insert):
        dominos = []
        for unit in ['row', 'column', 'box']:
            for x, y in self.solving_technique.get_influential_cells_unit(cell, unit):
                if (x, y) == cell or sum(self.candidates[x][y]) != 2 or self.candidates[x][y] == self.candidates[cell[0]][cell[1]]:
                    continue
                if insert in SolvingTechniques.format_candidates(self.candidates[x][y]):
                    dominos.append((x, y))
        dominos = SolvingTechniques.remove_duplicates(dominos)
        return dominos
