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
    def format_candidates(candidates):
        return [index + 1 for index, element in enumerate(candidates) if element == 1]

    @staticmethod
    def get_influential_cells_unit(cell, unit):
        x, y = cell
        influential_cells = []
        if unit == 'row':
            influential_cells = []
            for j in range(9):
                influential_cells.append((x, j))
            return influential_cells
        elif unit == 'column':
            for i in range(9):
                influential_cells.append((i, y))
            return influential_cells
        elif unit == 'box':
            box_x = (y // 3) * 3
            box_y = (x // 3) * 3

            for i in range(box_y, box_y + 3):
                for j in range(box_x, box_x + 3):
                    influential_cells.append((i, j))
            return influential_cells

    @staticmethod
    def get_influential_cells(cell):
        return {"row": SolvingTechniques.get_influential_cells_unit(cell, 'row'),
                "column": SolvingTechniques.get_influential_cells_unit(cell, 'column'),
                "box": SolvingTechniques.get_influential_cells_unit(cell, 'box')}

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
