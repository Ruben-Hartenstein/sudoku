from src.solutions.solving_techniques import SolvingTechniques
from src.solutions.naked_single import NakedSingle
from src.solutions.hidden_single import HiddenSingle
from src.solutions.naked_pair import NakedPair
from src.solutions.hidden_pair import HiddenPair
from src.solutions.naked_triple import NakedTriple
from src.solutions.hidden_triple import HiddenTriple
from src.solutions.naked_foursome import NakedFoursome
from src.solutions.hidden_foursome import HiddenFoursome
from src.solutions.line_block_interaction import LineBlockInteraction
from src.solutions.block_line_interaction import BlockLineInteraction
from src.solutions.x_wing import XWing
from src.solutions.turbot import Turbot
from src.solutions.third_eye import ThirdEye
from src.solutions.skyscraper import SkyScraper
from src.solutions.swordfish import Swordfish
from src.solutions.dragon import Dragon
from src.solutions.forbidden_rectangle_type1 import ForbiddenRectangleType1
from src.solutions.forbidden_rectangle_type2 import ForbiddenRectangleType2
from src.solutions.forbidden_rectangle_type4 import ForbiddenRectangleType4
from src.solutions.xy_wing import XYWing
from src.solutions.swordfish_with_fin import SwordfishWithFin

#techniques = [NakedSingle, HiddenSingle, NakedPair, HiddenPair, NakedTriple, HiddenTriple, NakedFoursome, HiddenFoursome, LineBlockInteraction, BlockLineInteraction, XWing, Turbot, ThirdEye, SkyScraper, Swordfish, Dragon, ForbiddenRectangleType1, ForbiddenRectangleType2, ForbiddenRectangleType4, XYWing]

techniques = [SwordfishWithFin]


def set_solved_board(board):
    SolvingTechniques.set_solved_board(board)


def try_techniques(board, candidates):
    for tech in techniques:
        technique = tech(board, candidates)
        successful = technique.execute_technique()
        if successful:
            return technique.get_result()
    return False
