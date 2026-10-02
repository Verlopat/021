from src.abstractions.registry import make_abstraction
from src.analysis.indistinguishability import build_pair_witness,check_l0_factorization
from src.models.message import Message

def test_strict_information_chain(): assert build_pair_witness()["strict_chain"] is True

def test_l0_is_anonymous_but_counts_values():
    a=[Message(0,3,1,"A"),Message(1,3,1,"B")]; b=[Message(1,3,1,"A"),Message(0,3,1,"B")]; c=[Message(0,3,1,"A"),Message(1,3,1,"A")]
    l0=make_abstraction("L0"); assert l0.observe(a)==l0.observe(b); assert l0.observe(a)!=l0.observe(c)

def test_l1_model_a_rejects_bad_signatures():
    from src.simulation.rounds import _signed
    good=_signed(0,3,1,"A"); bad=_signed(1,3,1,"B",bad_signature=True)
    cert=make_abstraction("L1",auth="A").certificate([good,bad])
    assert [(e.sender,e.value) for e in cert]==[(0,"A")]
    assert len(make_abstraction("L1",auth="B").certificate([good,bad]))==2

def test_l0_factorization_regression(): assert check_l0_factorization()["passed"] is True
