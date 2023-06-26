from typing import Any, Iterable, Iterator, NamedTuple, Optional
from flask import Flask, request
from modules.data import *
import hashlib
import json
import os

if not os.path.exists("data.json"):
    # Create tokens.json file if it doesn't exist
    with open("data.json", "w") as file:
        json.dump([], file)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Flask Server is running'


def print_data(data) -> None:
    measures = Measure.from_dict(data)
    for measure in measures:
        print(measure)


def data_to_string(data) -> list:
    measures = Measure.from_dict(data)
    return [str(x) for x in measures]


def get_tokens() -> dict:
    with open('data/tokens.json', 'r') as file:
        tokens = json.load(file)
    return tokens


def get_data() -> dict:
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data


def verify_token(token) -> bool:
    global tokens
    if token is None:
        return False
    hash = hashlib.sha256(token.encode()).hexdigest()
    b = False
    for x in tokens:
        b = b or (x['hash'] == hash)
    return b


def save_data(data) -> None:
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data_to_string(data)


@app.route('/store_data', methods=['POST'])
def store_data():
    new_data = request.json
    print("New data: " + str(new_data))
    if verify_token(new_data['token']):
        save_data(new_data)
        return 'Data saved'
    return 'Not authorized'


@app.route('/command', methods=['GET'])
def command():
    cmd = request.args.get('cmd')
    if cmd == 'save':
        save_data([])
        return 'Data saved in file'
    elif cmd == 'clear':
        with open('data.json', 'w') as file:
            file.truncate(0)
        return 'Data cleared'
    else:
        return 'Command unknown'

tokens = get_tokens()
data = get_data()
app.run()
