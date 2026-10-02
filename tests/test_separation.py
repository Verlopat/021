from src.analysis.indistinguishability import build_pair_witness, check_l0_factorization


def test_finite_information_separation_witness():
    result = build_pair_witness()
    assert result["claims"]["same_L0"] is True
    assert result["claims"]["different_L1"] is True
    assert result["claims"]["different_L2"] is True


def test_canonical_l0_factorization():
    assert check_l0_factorization()["passed"] is True
