from __future__ import annotations
from src.problems.connected_consensus import ConnectedConsensus
from src.problems.crusader_agreement import CrusaderAgreement
from src.problems.multivalued_ba import MultivaluedBA
from src.problems.approximate_agreement import MultidimensionalApproximateAgreement
from src.problems.exploratory import SetAgreement, VectorAgreement
from .model_checker import run_matrix

def run_full_characterization(max_n:int=5,max_exec:int=256)->dict:
    problems=[CrusaderAgreement(),ConnectedConsensus(),MultidimensionalApproximateAgreement(),MultivaluedBA(),SetAgreement(),VectorAgreement()]
    return run_matrix(problems,max_n=max_n,max_exec=max_exec)
