class NakedSingle:
    def __init__(self, board, candidates):
        self.name = "Naked Single"
        self.board = board
        self.candidates = candidates
        self.cross_outs = []
        self.fields = []
        self.associated_fields = []

    def execute_technique(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j][0] == 0:
                    if sum(self.candidates[i][j]) == 1:
                        self.cross_outs = self.candidates[i][j].index(1) + 1
                        self.fields.append((i, j))
                        return

    def get_result(self):
        self.update_associated_fields()
        return {
            "name": self.name,
            "cross_outs": self.cross_outs,
            "fields": self.fields,
            "associated_fields": self.associated_fields
        }

    def update_associated_fields(self):
        def remove_duplicates():
            return list(dict.fromkeys(self.associated_fields))

        for field in self.fields:
            # Add all in row
            for j in range(9):
                self.associated_fields.append((field[0], j))
            # Add all in column
            for i in range(9):
                self.associated_fields.append((i, field[1]))
            # Add all in Box
            box_x = (field[1] // 3) * 3
            box_y = (field[0] // 3) * 3

            for i in range(box_y, box_y + 3):
                for j in range(box_x, box_x + 3):
                    self.associated_fields.append((i, j))
        print(self.associated_fields)
        self.associated_fields = remove_duplicates()
        print(self.associated_fields)
