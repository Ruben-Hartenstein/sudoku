from solutions.solving_techniques import SolvingTechniques


class Chain:
    def __init__(self, solving_technique, start_cell, max_depth=81):
        self.board = solving_technique.board[:]
        self.candidates = solving_technique.candidates[:]
        self.solving_technique = solving_technique
        self.start_cell = start_cell
        self.max_depth = max_depth
        self.start_insert = ()
        self.chains = []

    def calculate_all_domino_chains(self, insert, depth=1, chain=[], cell=None):
        if not cell:
            cell = self.start_cell
            self.start_insert = insert
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
                if self.check_domino_part_valid((x, y), chain, candidate):
                    self.calculate_all_domino_chains(candidate, depth + 1, chain, (x, y))
        self.chains.append(chain)

    def get_all_dominos(self, cell, insert):
        dominos = []
        for unit in ['row', 'column', 'box']:
            for x, y in SolvingTechniques.get_influential_cells_unit(cell, unit):
                if self.board[x][y] != 0 or (x, y) == cell or sum(self.candidates[x][y]) != 2 or self.candidates[x][
                    y] == self.candidates[cell[0]][cell[1]]:
                    continue
                if insert in SolvingTechniques.format_candidates(self.candidates[x][y]):
                    dominos.append((x, y))
        dominos = SolvingTechniques.remove_duplicates(dominos)
        return dominos

    def check_domino_part_valid(self, part, chain, candidate):
        temp_chain = []
        for chain_part in chain:
            temp_chain.append(chain_part)
            if part in SolvingTechniques.get_unique_influential_cells(chain_part):
                if self.get_domino_last_insert(temp_chain) == candidate:
                    return False
        return True

    def get_domino_last_insert(self, chain, start_insert=None):
        if not start_insert:
            start_insert = self.start_insert
        if len(chain) == 1:
            return start_insert
        last_part = chain[-1]
        prev_last_part = chain[-2]
        last_candidates = SolvingTechniques.format_candidates(self.candidates[last_part[0]][last_part[1]])
        prev_last_candidates = SolvingTechniques.format_candidates(
            self.candidates[prev_last_part[0]][prev_last_part[1]])
        return [insert for insert in last_candidates if insert not in prev_last_candidates][0]

    def calculate_all_x_chains(self, candidate, depth=1, chain=[], cell=None):
        if not cell:
            cell = self.start_cell
            self.start_insert = candidate
            self.chains = []
        chain = chain[:]
        chain.append(cell)
        x_parts = self.get_all_x_parts(cell, candidate)
        if depth < self.max_depth:
            for x, y in x_parts:
                if (x, y) in chain:
                    continue
                if (x, y) not in chain:
                    self.calculate_all_x_chains(candidate, depth + 1, chain, (x, y))
        self.chains.append(chain)

    def get_all_x_parts(self, cell, candidate):
        x_parts = []
        for unit in ['row', 'column', 'box']:
            unit_cells = SolvingTechniques.get_influential_cells_unit(cell, unit)
            cells = self.solving_technique.get_cells_with_candidate(unit_cells, candidate)
            if len(cells) == 2:
                cells.remove(cell)
                x_parts.extend(cells)
        return x_parts
