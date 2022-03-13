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

    def update_associated_fields(self):
        for field in self.fields:
            # Add all in row
            for j in range(9):
                if self.board[field[0]][j][0] != 0:
                    self.associated_fields.append((field[0], j))
            # Add all in column
            for i in range(9):
                if self.board[i][field[1]][0] != 0:
                    self.associated_fields.append((i, field[1]))
            # Add all in Box
            box_x = (field[1] // 3) * 3
            box_y = (field[0] // 3) * 3

            for i in range(box_y, box_y + 3):
                for j in range(box_x, box_x + 3):
                    if self.board[i][j][0] != 0:
                        self.associated_fields.append((i, j))
