from src.solutions.solving_techniques import SolvingTechniques


class NakedPair(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Naked Pair",
                         """If the same two candidate values occupy two squares of a unit,
                          they divide these two squares, and we at least know that they are
                          not in the other squares of this unit can occur further. Therefore,
                          you can remove these two values in the rest of the affected units""",
                         board, candidates)

    def execute_technique(self):
        temp_candidates = []
        for j in range(9):
            for i in range(9):
                if self.board[i][j] != 0 or sum(self.candidates[i][j]) != 2:
                    continue
                temp_candidates = self.candidates[i][j]
                print(i, j)
                print(temp_candidates)
                influential_cells = SolvingTechniques.get_influential_cells((i, j))
                for key in influential_cells.keys():
                    print(key)
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
        influential_cells = SolvingTechniques.get_influential_cells(self.primary_cells[0])
        for x, y in influential_cells[self.unit]:
            if (x, y) in self.primary_cells or self.board[x][y] != 0:
                continue
            for pair_value in pair_values:
                if self.candidates[x][y][pair_value - 1] == 1:
                    self.cross_out.append(
                        {'value': pair_value,
                         'cell': (x, y)})

    def update_secondary_cells(self):
        print(self.unit)
        influential_cells = SolvingTechniques.get_influential_cells(self.primary_cells[0])
        for x, y in influential_cells[self.unit]:
            if (x, y) in self.primary_cells:
                continue
            self.secondary_cells.append((x, y))
