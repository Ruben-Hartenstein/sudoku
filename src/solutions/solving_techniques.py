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

    def get_result(self):
        self.update_explanation()
        return {
            "name": self.name,
            "primary_cells": self.primary_cells,
            "secondary_cells": self.secondary_cells,
            "cross_outs": self.cross_outs,
            "highlights": self.highlights,
            "explanation": self.explanation
        }

    def get_cells_with_candidate(self, cells, candidate):
        candidate_cells = []
        for cell in cells:
            x, y = cell
            if self.board[x][y] != 0:
                continue
            if self.candidates[x][y][candidate - 1]:
                candidate_cells.append(cell)
        return candidate_cells

    @classmethod
    def set_solved_board(cls, board):
        cls.solved_board = board

    @staticmethod
    def get_cross_cells(cell1, cell2):
        return [(cell1[0], cell2[1]), (cell2[0], cell1[1])]

    @staticmethod
    def get_overlap_cells(cell1, cell2):
        influential_cells1 = SolvingTechniques.get_unique_influential_cells(cell1)
        influential_cells2 = SolvingTechniques.get_unique_influential_cells(cell2)
        return list(set(influential_cells1) & set(influential_cells2))

    @staticmethod
    def flatten(lst):
        def flatten(lst):
            for item in lst:
                if isinstance(item, list) or isinstance(item, tuple):
                    for element in flatten(item):
                        yield element
                else:
                    yield item
        return list(flatten(lst))

    @staticmethod
    def remove_duplicates(cells):
        cells = cells[:]
        return list(dict.fromkeys(cells))

    @staticmethod
    def format_candidates(candidates):
        return [index + 1 for index, element in enumerate(candidates) if element == 1]

    @staticmethod
    def get_influential_cells_unit(cell, unit):
        x, y = cell
        influential_cells = []
        if unit == 'row':
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

    @staticmethod
    def get_unique_influential_cells(cell):
        unique_cells = []
        influential_cells = SolvingTechniques.get_influential_cells(cell)
        for key in influential_cells.keys():
            for influential_cell in influential_cells[key]:
                if influential_cell not in unique_cells:
                    unique_cells.append(influential_cell)
        return unique_cells

    @staticmethod
    def index2box(index):
        box_coords = {0: (1, 1),
                      1: (1, 4),
                      2: (1, 7),
                      3: (4, 1),
                      4: (4, 4),
                      5: (4, 7),
                      6: (7, 1),
                      7: (7, 4),
                      8: (7, 7)}
        return box_coords[index]

    @staticmethod
    def get_box(cell):
        box_x = (cell[1] // 3) * 3
        box_y = (cell[0] // 3) * 3
        return box_x, box_y

    @abstractmethod
    def configure_highlighting(self):
        pass

    @abstractmethod
    def execute_technique(self):
        pass

    @abstractmethod
    def update_explanation(self):
        pass
