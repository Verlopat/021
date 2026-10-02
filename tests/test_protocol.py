from src.models.message import Message
from src.protocols.l1_gather_decision import L1GatherDecisionProtocol


def test_l1_protocol_prefers_quorum_value():
    messages = [
        Message(0, 3, 1, "A"),
        Message(1, 3, 1, "A"),
        Message(2, 3, 1, "A"),
        Message(3, 3, 1, "C"),
    ]
    result = L1GatherDecisionProtocol(quorum=3).run(messages)
    assert result["decision"] == "A"


def test_l1_protocol_falls_back_to_deterministic_domain_rule():
    messages = [Message(0, 2, 1, "A"), Message(1, 2, 1, "C")]
    result = L1GatherDecisionProtocol(quorum=3).run(messages)
    assert result["decision"] == "C"
