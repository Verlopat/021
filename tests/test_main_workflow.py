import json
import run_experiments

def test_run_writes_all_artifacts(tmp_path):
    cfg=tmp_path/"c.json"
    cfg.write_text(json.dumps({"seed":1,"values":["A","B"],"max_exec":200,"experiments":[
        {"problem":"crusader","protocol":"count-crusader","configs":[[3,1],[4,1]],"boundary_f":[1]}
    ]}))
    out=run_experiments.run(cfg,tmp_path/"res",log=lambda *_:None)
    for name in ("correctness.csv","communication.csv","resilience.csv","manifest.json","research_matrix.md","witnesses.json"):
        assert (out/name).exists(),name
    assert any((out/"counterexamples").iterdir())
