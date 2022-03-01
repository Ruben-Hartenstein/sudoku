from src.solutions.solving_techniques import SolvingTechniques


class NakedSingle(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Naked Single", board, candidates)

    def execute_technique(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j][0] == 0:
                    if sum(self.candidates[i][j]) == 1:
                        self.cross_outs = self.candidates[i][j].index(1) + 1
                        self.fields.append((i, j))
                        return
