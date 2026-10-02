from src.analysis.separation_search import search_observation_separation

def test_l0_has_strict_observation_gain():
    r=search_observation_separation(3,("A","B"))
    assert r["L0_to_L1"]["strict_observation_gain"]
