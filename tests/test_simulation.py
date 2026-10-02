from src.simulation.engine import run_reference_simulation


def test_reference_simulation():
    result = run_reference_simulation(7, 2)
    assert result["boundary_status"] == "inside_target_n_gt_3f_boundary"
    assert result["view_size"] == 7
    assert result["l1_protocol"]["quorum"] == 5
