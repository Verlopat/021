from src.models.message import BOT
from src.problems.approximate_agreement import MultidimensionalApproximateAgreement
from src.problems.connected_consensus import CENTER,ConnectedConsensus,spider_distance
from src.problems.crusader_agreement import CrusaderAgreement
from src.problems.validators import in_convex_hull

def test_crusader_allows_bot_but_not_conflict():
    p=CrusaderAgreement(("A","B")); assert p.check({0:"A",1:BOT},{0:"A",1:"B"},{0,1}).passed
    assert not p.check({0:"A",1:"B"},{0:"A",1:"B"},{0,1}).agreement

def test_only_honest_processes_are_checked():
    p=CrusaderAgreement(("A","B")); assert p.check({0:"A",1:"A",2:"B"},{0:"A",1:"A"},{0,1}).passed

def test_spider_graph_distance_and_validity():
    assert spider_distance(("A",2),("A",1))==1; assert spider_distance(("A",1),("B",1))==2; assert spider_distance(CENTER,("B",1))==1
    p=ConnectedConsensus(("A","B"),R=2); assert p.check({0:("A",2),1:("A",1)},{0:"A",1:"B"},{0,1}).passed
    assert not p.check({0:("A",1),1:("B",1)},{0:"A",1:"B"},{0,1}).agreement
    assert not p.check({0:("A",1),1:("A",1)},{0:"A",1:"A"},{0,1}).validity

def test_true_convex_hull_not_bounding_box():
    tri=[(0.,0.),(1.,0.),(0.,1.)]; assert in_convex_hull((.2,.2),tri); assert not in_convex_hull((.9,.9),tri)
    aa=MultidimensionalApproximateAgreement(1,.25); assert not aa.check({0:(1.5,),1:(1.4,)},{0:(0.,),1:(1.,)},{0,1}).validity
