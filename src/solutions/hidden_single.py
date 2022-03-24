from src.solutions.solving_techniques import SolvingTechniques, remove_duplicates, get_influential_cells


class HiddenSingle(SolvingTechniques):

    def __init__(self, board, candidates):
        super().__init__("Hidden Single",
                         """Every number already entered covers a row, a column and a block.
                          Therefore, very often there are situations in which there is only
                           one free field for a given number within a unit * (in block 9, 
                           the 7 fits only in the green field).""",
                         board, candidates)
        self.unit = ""

    def execute_technique(self):
        # Loop through possible numbers
        for num in range(9):
            # Look for only one occurrence of candidate in rows
            occurrences = 0
            last_occurrence = 0
            for j in range(9):
                for i in range(9):
                    if self.board[i][j][0] == 0:
                        if self.candidates[i][j][num] == 1:
                            occurrences += 1
                            last_occurrence = i
                if occurrences == 1:
                    self.cross_outs = num + 1
                    self.cells.append((last_occurrence, j))
                    self.unit = "row"
                    return True
                occurrences = 0

            # Look for columns
            occurrences = 0
            last_occurrence = 0
            for i in range(9):
                for j in range(9):
                    if self.board[i][j][0] == 0:
                        if self.candidates[i][j][num] == 1:
                            occurrences += 1
                            last_occurrence = j
                if occurrences == 1:
                    self.cross_outs = num + 1
                    self.cells.append((i, last_occurrence))
                    self.unit = "column"
                    return True
                occurrences = 0

            #Look for boxes
            for box_x in range(0, 9, 3):
                for box_y in range(0, 9, 3):
                    for i in range(box_x, box_x + 3):
                        for j in range(box_y, box_y + 3):
                            if self.board[i][j][0] == 0:
                                if self.candidates[i][j][num] == 1:
                                    occurrences += 1
                                    last_occurrence = (i, j)
                    if occurrences == 1:
                        self.cross_outs = num + 1
                        self.cells.append(last_occurrence)
                        self.unit = "box"
                        return True
                    occurrences = 0
        return False

    def update_associated_cells(self):
        print(self.unit)
        cell = self.cells[0]
        if self.unit == "row":
            for i in range(9):
                if self.board[cell[0]][i][0] != 0:
                    self.associated_cells.append((cell[0], i))
                for j in range(9):
                    if self.board[i][j][0] == self.cross_outs:
                        for index in range(9):
                            self.associated_cells.append((index, j))
                        break

        elif self.unit == "column":
            for i in range(9):
                if self.board[i][cell[1]][0] != 0:
                    self.associated_cells.append((i, cell[1]))
                for j in range(9):
                    if self.board[i][j][0] == self.cross_outs:
                        for index in range(9):
                            self.associated_cells.append((i, index))
                        break

        else:
            box_x = (cell[0] // 3) * 3
            box_y = (cell[1] // 3) * 3

            # All in same columns as the box
            for i in range(box_x, box_x + 3):
                for j in range(9):
                    if self.board[i][j][0] == self.cross_outs:
                        for index in range(9):
                            self.associated_cells.append((i, index))
                        break
            # All in same rows as the box
            for j in range(box_y, box_y + 3):
                for i in range(9):
                    if self.board[i][j][0] == self.cross_outs:
                        for index in range(9):
                            self.associated_cells.append((index, j))
                        break

            # All in same box
            for i in range(box_x, box_x + 3):
                for j in range(box_y, box_y + 3):
                    if self.board[i][j][0] != 0:
                        self.associated_cells.append(i, j)
            self.associated_cells = remove_duplicates(self.associated_cells)
