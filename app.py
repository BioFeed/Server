from typing import Any, Iterable, Iterator, NamedTuple, Optional
from flask import Flask, request
import hashlib
import json

app = Flask(__name__)


class Measure(NamedTuple):
    name: str
    date: int
    photo: Optional[str]
    temperature: Optional[float]
    humidity: Optional[float]
    state: Optional[str]

    @classmethod
    def from_dict(cls, data: Iterable[dict[str, Any]]) -> Iterator['Measure']:
        for x in data:
            yield cls(
                name=x['name'],
                date=x['date'],
                photo=x['photo'],
                temperature=x.get('temperature'),
                humidity=x.get('humidity'),
                state=x.get('state')
            )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> 'Measure':
        return cls(
            name=data['name'],
            date=data['date'],
            photo=data['photo'],
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            state=data.get('state')
        )

    # Il n'y a pas la photo
    @property
    def to_list(self) -> list:
        return [self.name, self.date, self.temperature, self.humidity, self.state]

    # Il n'y a pas la photo
    def __str__(self) -> str:
        return (
            f'{self.date} : '
            f'{self.name} | '
            f'temperature : {self.temperature} | '
            f'humidity : {self.humidity} | '
            f'state : {self.state}'
        )


def print_data(data) -> None:
    measures = Measure.from_dict(data)
    for measure in measures:
        print(measure)


def data_to_string(data) -> list:
    measures = Measure.from_dict(data)
    return [str(x) for x in measures]


def get_data() -> dict:
    global data
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data


def get_tokens() -> dict:
    global tokens
    with open('tokens.json', 'r') as file:
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


def save_data() -> None:
    global data
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    global data
    return data_to_string(data)


@app.route('/store_data', methods=['POST'])
def store_data():
    global data
    new_data = request.json
    if verify_token(new_data['token']):
        data.append(new_data)
        return 'Data saved'
    return 'Not authorized'


@app.route('/command', methods=['GET'])
def command():
    cmd = request.args.get('cmd')
    if cmd == 'save':
        save_data()
        return 'Data saved in file'
    elif cmd == 'clear':
        data.clear()
        return 'Data cleared'
    else:
        return 'Command unknown'


# @app.route('/upload_image', methods=['POST'])
# def upload_image():
#     image_file = request.files['imageFile']
#     # Process the image file here
#     image_file.save('uploaded_image.jpg')
#     return 'Image uploaded successfully'


data = get_data()
tokens = get_tokens()
# app.run()
