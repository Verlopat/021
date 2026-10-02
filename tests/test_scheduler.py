from src.models.message import Message
from src.models.scheduler import RoundScheduler

def test_scheduler_delivers_selected_heard_of_set():
    messages=[Message(0,2,1,"A"),Message(1,2,1,"B"),Message(2,2,1,"C")]
    got=RoundScheduler().deliver(messages,2,1,{0,2})
    assert [m.sender for m in got]==[0,2]
