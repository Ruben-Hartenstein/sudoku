from abc import ABC, abstractmethod


def remove_duplicates(cells):
    return list(dict.fromkeys(cells))


def get_influential_cells(field):
    influential_fields = []
    # All in row
    for j in range(9):
        influential_fields.append((field[0], j))

    # All in column
    for i in range(9):
        influential_fields.append((i, field[1]))

    # All in box
    box_x = (field[1] // 3) * 3
    box_y = (field[0] // 3) * 3

    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            influential_fields.append([i][j])
    return remove_duplicates(influential_fields)


class SolvingTechniques(ABC):

    def __init__(self, name, explanation, board, candidates):
        self.name = name
        self.explanation = explanation
        self.board = board
        self.candidates = candidates
        self.cross_outs = []
        self.cells = []
        self.associated_cells = []

    def get_result(self):
        self.update_associated_cells()
        return {
            "name": self.name,
            "cross_outs": self.cross_outs,
            "fields": self.cells,
            "associated_fields": self.associated_cells
        }

    @abstractmethod
    def update_associated_cells(self):
        pass

    @abstractmethod
    def execute_technique(self):
        pass

'''
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
        self.associated_fields = remove_duplicates()
        print(self.associated_fields)'''