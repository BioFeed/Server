import hashlib
import json
import os

ABS_PATH = os.path.abspath('.')
TOKENS_PATH = ABS_PATH + '/data/tokens.json'


def get_tokens() -> list:
    if not os.path.exists(TOKENS_PATH):
        with open(TOKENS_PATH, 'w') as file:
            json.dump([], file)
            return []
    else:
        with open(TOKENS_PATH, 'r') as file:
            t = json.load(file)
            return t


def verify_token(token: str) -> bool:
    global tokens
    if token is None:
        return False
    h = hashlib.sha256(token.encode()).hexdigest()
    b = False
    for x in tokens:
        b = b or (x['hash'] == h)
    return b


tokens = get_tokens()
