from src.abstractions.l0 import L0CountOnly
from src.abstractions.l1 import L1GatherEcho
from src.abstractions.l2 import L2FullContent
from src.models.message import Message


def histories():
    a = [Message(0, 2, 1, "A"), Message(1, 2, 1, "A")]
    c = [Message(0, 2, 1, "C"), Message(1, 2, 1, "C")]
    return a, c


def test_l0_hides_payload():
    a, c = histories()
    assert L0CountOnly().observe(a) == L0CountOnly().observe(c)


def test_l1_exposes_certificate_values():
    a, c = histories()
    assert L1GatherEcho().observe(a) != L1GatherEcho().observe(c)


def test_l2_preserves_full_messages():
    a, c = histories()
    assert L2FullContent().observe(a) != L2FullContent().observe(c)
