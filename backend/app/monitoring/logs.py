from collections import deque

_LOGS = deque(maxlen=500)

def log(msg: str):
    _LOGS.append(msg)

def get_logs():
    return list(_LOGS)
