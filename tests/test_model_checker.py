from src.analysis.model_checker import check_protocol
from src.problems.connected_consensus import ConnectedConsensus

def test_checker_returns_research_status():
    r=check_protocol(ConnectedConsensus(),"L0",3,1,("A","B"),max_exec=8)
    assert r["status"] in {"COUNTEREXAMPLE_FOUND","NO_COUNTEREXAMPLE_IN_FINITE_SPACE"}
