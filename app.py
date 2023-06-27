from flask import Flask, request
from modules.data import save_data, add_data, clear_data
from modules.tokens import verify_token


app = Flask(__name__)


def check(r: dict) -> bool:
    if ('token' not in r.keys()) or (not verify_token(r['token'])):
        print('x> Connection refused: wrong token or no token')
        return False
    else:
        print('-> Connection authorized')
        return True


@app.route('/', methods=['GET'])
def index() -> str:
    return 'Flask Server is running'


@app.route('/store_data', methods=['POST'])
def store_data() -> str:
    new_data = request.json
    if check(new_data):
        # Enlever le token de la requête avant de l'ajouter
        del new_data['token']
        return add_data(new_data)
    else:
        return 'Not authorized'


@app.route('/command', methods=['POST'])
def command() -> str:
    r = request.json
    if check(r):
        if 'command' in r.keys():
            if r['command'] == 'save':
                return save_data()
            elif r['command'] == 'clear':
                return clear_data()
            else:
                return 'Command unknown'
        else:
            return 'No command'
    else:
        'Not authorized'


app.run()
