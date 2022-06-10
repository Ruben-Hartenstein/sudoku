from solutions.solving_techniques import SolvingTechniques
from solutions.naked_single import NakedSingle
from solutions.hidden_single import HiddenSingle
from solutions.naked_pair import NakedPair
from solutions.hidden_pair import HiddenPair
from solutions.naked_triple import NakedTriple
from solutions.hidden_triple import HiddenTriple
from solutions.naked_foursome import NakedFoursome
from solutions.hidden_foursome import HiddenFoursome
from solutions.line_block_interaction import LineBlockInteraction
from solutions.block_line_interaction import BlockLineInteraction
from solutions.x_wing import XWing
from solutions.turbot import Turbot
from solutions.third_eye import ThirdEye
from solutions.skyscraper import SkyScraper
from solutions.swordfish import Swordfish
from solutions.dragon import Dragon
from solutions.forbidden_rectangle_type1 import ForbiddenRectangleType1
from solutions.forbidden_rectangle_type2 import ForbiddenRectangleType2
from solutions.forbidden_rectangle_type3 import ForbiddenRectangleType3
from solutions.forbidden_rectangle_type4 import ForbiddenRectangleType4
from solutions.xy_wing import XYWing
from solutions.xyz_wing import XYZWing
from solutions.x_chain import XChain
from solutions.xy_chain import XYChain
from solutions.swordfish_with_fin import SwordfishWithFin
from solutions.double_chain import DoubleChain
from solutions.almost_locked_sets import AlmostLockedSets

techniques = [NakedSingle, HiddenSingle, NakedPair, HiddenPair, NakedTriple, HiddenTriple, NakedFoursome,
              HiddenFoursome, LineBlockInteraction, BlockLineInteraction, XWing, Turbot, ThirdEye, SkyScraper,
              Swordfish, Dragon, ForbiddenRectangleType1, ForbiddenRectangleType2, ForbiddenRectangleType3,
              ForbiddenRectangleType4, XYWing, XYZWing, XChain, XYChain, SwordfishWithFin, DoubleChain,
              AlmostLockedSets]


def set_solved_board(board):
    SolvingTechniques.set_solved_board(board)


def try_techniques(board, candidates):
    for tech in techniques:
        technique = tech(board, candidates)
        successful = technique.execute_technique()
        if successful:
            return technique.get_result()
    return False
