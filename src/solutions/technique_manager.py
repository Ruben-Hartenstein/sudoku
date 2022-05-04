from src.solutions.solving_techniques import SolvingTechniques
from src.solutions.naked_single import NakedSingle
from src.solutions.hidden_single import HiddenSingle
from src.solutions.naked_pair import NakedPair
from src.solutions.hidden_pair import HiddenPair
from src.solutions.naked_triple import NakedTriple
from src.solutions.hidden_triple import HiddenTriple
from src.solutions.naked_foursome import NakedFoursome
from src.solutions.hidden_foursome import HiddenFoursome
from src.solutions.third_eye import ThirdEye

techniques = [NakedSingle, HiddenSingle, NakedPair, HiddenPair, NakedTriple, HiddenTriple, NakedFoursome, HiddenFoursome, ThirdEye]


def set_solved_board(board):
    SolvingTechniques.set_solved_board(board)


def try_techniques(board, candidates):
    for tech in techniques:
        technique = tech(board, candidates)
        successful = technique.execute_technique()
        if successful:
            return technique.get_result()
    return False
