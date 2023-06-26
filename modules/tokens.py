import hashlib
import json


def get_tokens() -> dict:
    with open('data/tokens.json', 'r') as file:
        tokens = json.load(file)
    return tokens


def verify_token(token) -> bool:
    global tokens
    if token is None:
        return False
    hash = hashlib.sha256(token.encode()).hexdigest()
    b = False
    for x in tokens:
        b = b or (x['hash'] == hash)
    return b


tokens = get_tokens()
