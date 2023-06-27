from flask import Flask, request
from modules.data import save_data, add_data, clear_data
from modules.tokens import verify_token


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Flask Server is running'


@app.route('/store_data', methods=['POST'])
def store_data():
    new_data = request.json
    if ('token' in new_data.keys()) and (verify_token(new_data['token'])):
        return add_data(new_data)
    else:
        print('x> Connection refused: wrong token or no token')
        return 'Not authorized'


@app.route('/command', methods=['GET'])
def command():
    cmd = request.args.get('cmd')
    if cmd == 'save':
        return save_data()
    elif cmd == 'clear':
        return clear_data()
    else:
        return 'Command unknown'


app.run()
