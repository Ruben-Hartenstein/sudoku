from src.solutions.solving_techniques import SolvingTechniques
from src.solutions.naked_single import NakedSingle
from src.solutions.hidden_single import HiddenSingle
from src.solutions.naked_pair import NakedPair
from src.solutions.naked_triple import NakedTriple
from src.solutions.hidden_triple import HiddenTriple
from src.solutions.naked_foursome import NakedFoursome

techniques = [HiddenTriple]


def set_solved_board(board):
    SolvingTechniques.set_solved_board(board)


def try_techniques(board, candidates):
    for tech in techniques:
        technique = tech(board, candidates)
        successful = technique.execute_technique()
        if successful:
            return technique.get_result()
    return False
