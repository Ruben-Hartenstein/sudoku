from src.solutions.solving_techniques import SolvingTechniques


class Chain:
    def __init__(self, board, candidates, start_cell, max_depth=81):
        self.board = board[:]
        self.candidates = candidates[:]
        self.start_cell = start_cell
        self.max_depth = max_depth
        self.chains = []

    def calculate_all_chains(self, insert, depth=1, chain=[], cell=None):
        if not cell:
            cell = self.start_cell
            self.chains = []
        chain = chain[:]
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
            for x, y in SolvingTechniques.get_influential_cells_unit(cell, unit):
                if (x, y) == cell or sum(self.candidates[x][y]) != 2 or self.candidates[x][y] == \
                        self.candidates[cell[0]][cell[1]]:
                    continue
                if insert in SolvingTechniques.format_candidates(self.candidates[x][y]):
                    dominos.append((x, y))
        dominos = SolvingTechniques.remove_duplicates(dominos)
        return dominos

    def get_last_insert(self, chain, candidate):
        if len(chain) == 1:
            return candidate
        last_part = chain[-1]
        prev_last_part = chain[-2]
        last_candidates = SolvingTechniques.format_candidates(self.candidates[last_part[0]][last_part[1]])
        prev_last_candidates = SolvingTechniques.format_candidates(self.candidates[prev_last_part[0]][prev_last_part[1]])
        return [insert for insert in last_candidates if insert not in prev_last_candidates][0]
