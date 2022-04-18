from src.solutions.solving_techniques import SolvingTechniques


class NakedPair(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Naked Pair", board, candidates)
        self.unit = ""

    def execute_technique(self):
        for j in range(9):
            for i in range(9):
                if self.board[i][j] != 0 or sum(self.candidates[i][j]) != 2:
                    continue
                temp_candidates = self.candidates[i][j]
                influential_cells = SolvingTechniques.get_influential_cells((i, j))
                for key in influential_cells.keys():
                    candidate_pair_twice = False
                    for x, y in influential_cells[key]:
                        if self.board[x][y] != 0 or (x, y) == (i, j) or self.candidates[x][y] != temp_candidates:
                            continue
                        if candidate_pair_twice:
                            self.primary_cells = []
                            candidate_pair_twice = False
                            break
                        self.primary_cells.append((i, j))
                        self.primary_cells.append((x, y))
                        candidate_pair_twice = True

                    if candidate_pair_twice:
                        self.unit = key
                        self.assemble_cross_out(temp_candidates)
                        return True
        return False

    def assemble_cross_out(self, candidates):
        pair_values = []
        for num, candidate in enumerate(candidates):
            if candidate == 0:
                continue
            pair_values.append(num + 1)
        for x, y in self.primary_cells:
            for pair_value in pair_values:
                self.highlights.append(
                    {'value': pair_value,
                     'cell': (x, y)})
        influential_cells = SolvingTechniques.get_influential_cells(self.primary_cells[0])
        for x, y in influential_cells[self.unit]:
            if (x, y) in self.primary_cells or self.board[x][y] != 0:
                continue
            for pair_value in pair_values:
                if self.candidates[x][y][pair_value - 1] == 1:
                    self.cross_outs.append(
                        {'value': pair_value,
                         'cell': (x, y)})

    def update_secondary_cells(self):
        influential_cells = SolvingTechniques.get_influential_cells(self.primary_cells[0])
        for x, y in influential_cells[self.unit]:
            if (x, y) in self.primary_cells:
                continue
            self.secondary_cells.append((x, y))

    def update_explanation(self):
        self.explanation = f"""The same two candidate values, {self.highlights[0]['value']} and {self.highlights[1]['value']}, occupy two squares of a {self.unit},
they divide the two squares {self.highlights[0]['cell']} and {self.highlights[2]['cell']}, and we know that they can't occur in other squares of the {self.unit}.
Therefore, the values {self.highlights[0]['value']} and {self.highlights[1]['value']} can be removed from the rest of the affected fields."""