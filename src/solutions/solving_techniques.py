from abc import ABC, abstractmethod


class SolvingTechniques(ABC):
    solved_board = []

    def __init__(self, name, board, candidates):
        self.name = name
        self.board = board
        self.candidates = candidates
        self.explanation = ''
        self.cross_outs = []
        self.highlights = []
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
        self.update_explanation()
        return {
            "name": self.name,
            "primary_cells": self.primary_cells,
            "secondary_cells": self.secondary_cells,
            "cross_outs": self.cross_outs,
            "highlights": self.highlights,
            "explanation": self.explanation
        }

    @abstractmethod
    def update_secondary_cells(self):
        pass

    @abstractmethod
    def execute_technique(self):
        pass

    @abstractmethod
    def update_explanation(self):
        pass
