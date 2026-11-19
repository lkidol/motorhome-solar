import json,base64,numpy as np
d=json.load(open('/home/claude/motorhome/malha.json'))
def dec(p):
    pos=np.frombuffer(base64.b64decode(p['pos']),dtype=np.float32).reshape(-1,3)
    idx=np.frombuffer(base64.b64decode(p['idx']),dtype=np.uint16 if p.get('idxType')=='uint16' else np.uint32).reshape(-1,3)
    return pos,idx
