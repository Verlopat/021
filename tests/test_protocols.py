import pytest
from src.analysis.experiments import build
from src.analysis.model_checker import check_protocol

CASES=[("crusader","count-crusader",1),("connected","count-connected",2),("mvba","phase-king",1),("approx","trimmed-midpoint",1)]

@pytest.mark.parametrize("problem,protocol,R",CASES)
def test_counterexample_at_n_equal_3f(problem,protocol,R):
    prob,factory,dom=build(problem,protocol,("A","B"),R); row=check_protocol(prob,factory(3,1),3,1,dom,max_exec=3000)
    assert row["status"]=="COUNTEREXAMPLE_FOUND"

@pytest.mark.parametrize("problem,protocol,R",CASES)
def test_no_counterexample_at_n_equal_3f_plus_1(problem,protocol,R):
    prob,factory,dom=build(problem,protocol,("A","B"),R); row=check_protocol(prob,factory(4,1),4,1,dom,max_exec=3000)
    assert row["status"] in ("VERIFIED_EXHAUSTIVE","NO_COUNTEREXAMPLE_SAMPLED")

def test_crusader_n4_f1_is_exhaustive():
    prob,factory,dom=build("crusader","count-crusader",("A","B")); assert check_protocol(prob,factory(4,1),4,1,dom,max_exec=5000)["status"]=="VERIFIED_EXHAUSTIVE"

def test_blind_protocol_fails_even_without_faults():
    prob,factory,dom=build("crusader","own-input",("A","B")); assert check_protocol(prob,factory(2,0),2,0,dom)["status"]=="COUNTEREXAMPLE_FOUND"

def test_phase_king_needs_l1_observation():
    from src.abstractions.registry import make_abstraction
    from src.simulation.rounds import run_execution
    prob,factory,dom=build("mvba","phase-king",("A","B"))
    with pytest.raises(AttributeError):
        run_execution(factory(4,1),make_abstraction("L0"),4,[3],{0:"A",1:"B",2:"A"},lambda r,b,q,out:"A")
