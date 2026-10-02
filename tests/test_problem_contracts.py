from src.problems.crusader_agreement import CrusaderAgreement
from src.problems.connected_consensus import ConnectedConsensus
from src.problems.multivalued_ba import MultivaluedBA
from src.problems.approximate_agreement import MultidimensionalApproximateAgreement

def test_problem_contracts():
    assert CrusaderAgreement().name
    assert ConnectedConsensus().name
    assert MultivaluedBA().name
    assert MultidimensionalApproximateAgreement().name
