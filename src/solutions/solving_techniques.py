from abc import ABC, abstractmethod


class SolvingTechniques(ABC):
    solved_board = []

    def __init__(self, name, explanation, board, candidates):
        self.name = name
        self.explanation = explanation
        self.board = board
        self.candidates = candidates
        self.cross_out = []
        self.highlight = []
        self.primary_cells = []
        self.secondary_cells = []

    @classmethod
    def set_solved_board(cls, board):
        cls.solved_board = board

    @staticmethod
    def remove_duplicates(cells):
        return list(dict.fromkeys(cells))

    @staticmethod
    def get_influential_cells(cell):
        x, y = cell
        influential_cells = {}

        # All in row
        influential_cells_row = []
        for j in range(9):
            influential_cells_row.append((x, j))
            influential_cells["row"] = influential_cells_row

        # All in column
        influential_cells_column = []
        for i in range(9):
            influential_cells_column.append((i, y))
            influential_cells["column"] = influential_cells_column

        # All in box
        influential_cells_box = []
        box_x = (y // 3) * 3
        box_y = (x // 3) * 3

        for i in range(box_y, box_y + 3):
            for j in range(box_x, box_x + 3):
                influential_cells_box.append((i, j))
        influential_cells["box"] = influential_cells_box

        return influential_cells

    def get_result(self):
        self.update_secondary_cells()
        return {
            "name": self.name,
            "cross_out": self.cross_out,
            "primary_cells": self.primary_cells,
            "secondary_cells": self.secondary_cells
        }

    @abstractmethod
    def update_secondary_cells(self):
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
