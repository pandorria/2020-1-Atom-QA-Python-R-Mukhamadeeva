import threading
import vk

from flask import Flask, request, json, jsonify

app = Flask(__name__)
host = '0.0.0.0'
port = 5000
session = vk.Session(access_token='ff3ad3a10e0fed3023daf7f6128ed48e7197b48e9439d2138d96f8bb28c2340294da1f3fc86c4caff0c9a')
vk_api = vk.API(session)


def run_mock():
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/vk_id/<username>')
def get_user_by_id(username):
    try:
        response = app.response_class(
            response=json.dumps({'vk_id': vk_api.users.get(user_ids=username, v=5.103)[0]['id']}),
            status=200,
            mimetype='application/json'
        )
    except:
        response = app.response_class(
            response=json.dumps({}),
            status=404,
            mimetype='application/json'
        )
    return response


@app.route('/shutdown')
def shutdown():
    shutdown_mock()


if __name__ == '__main__':
    run_mock()
