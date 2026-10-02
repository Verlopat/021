from src.crypto.auth import AuthenticationKey,digest,sign,verify

def test_authenticated_digest_and_signature():
    key=AuthenticationKey(1,b"research-key")
    d=digest(1,1,"A","proposal")
    s=sign(key,1,1,"A","proposal")
    assert len(d)==64
    assert verify(key,s,1,1,"A","proposal")
    assert not verify(key,s,1,1,"B","proposal")
