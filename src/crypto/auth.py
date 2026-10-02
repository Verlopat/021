from __future__ import annotations
import hashlib,hmac,json
from dataclasses import dataclass
from typing import Any

def canonical_payload(sender:int,round_id:int,value:Any,kind:str)->bytes:
    return json.dumps({"sender":sender,"round":round_id,"value":value,"kind":kind},sort_keys=True,separators=(",",":")).encode()

def digest(sender:int,round_id:int,value:Any,kind:str)->str:
    return hashlib.sha256(canonical_payload(sender,round_id,value,kind)).hexdigest()

@dataclass(frozen=True,slots=True)
class AuthenticationKey:
    key_id:int
    secret:bytes

def sign(key:AuthenticationKey,sender:int,round_id:int,value:Any,kind:str)->str:
    return hmac.new(key.secret,canonical_payload(sender,round_id,value,kind),hashlib.sha256).hexdigest()

def verify(key:AuthenticationKey,signature:str,sender:int,round_id:int,value:Any,kind:str)->bool:
    return hmac.compare_digest(signature,sign(key,sender,round_id,value,kind))
