import threading
import time
from flask import Flask, abort, request

app = Flask(__name__)
users = {}
host = '0.0.0.0'
port = 5000


def run_mock():
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    time.sleep(2)
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/get_user/<user_id>')
def get_user_by_id(user_id: int):
    user = users.get(str(user_id), None)
    return user['name'] if user is not None else abort(404)


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_data().decode()
    value = data.split('&')
    user_id = None
    user_data = None
    for i in value:
        tmp_data = i.split('=')
        if len(tmp_data) != 2:
            abort(400)
        elif tmp_data[0] == 'id':
            user_id = tmp_data[1]
        elif tmp_data[0] == 'name':
            user_data = {'name': tmp_data[1]}
        else:
            abort(400)
        users[user_id] = user_data
    return 'OK'


@app.route('/shutdown')
def shutdown():
    shutdown_mock()
    return 'OK'


if __name__ == '__main__':
    run_mock()
