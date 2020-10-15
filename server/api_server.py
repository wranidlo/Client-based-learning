from flask import Flask, request
import json
from server.api_server_logic import logic

app = Flask(__name__)

api_logic_use = logic()


@app.route("/", methods=['GET'])
def home_view():
    return "<h1>Welcome to Start Page</h1>"


@app.route('/question', methods=['GET'])
def get_top_question():
    if api_logic_use.check_if_empty():
        return Flask.response_class(status=204)
    else:
        json_question = api_logic_use.get_top_question()
        response = Flask.response_class(json.dumps(json_question), status=200)
        return response


@app.route('/question', methods=['POST'])
def post_question():
    username = request.args.get('user')
    data = request.get_json()
    api_logic_use.add_question(data, username)
    response = Flask.response_class(json.dumps(data), status=201)
    return response


@app.route('/answers', methods=['GET'])
def get_all_answers():
    username = request.args.get('user')
    json_question = api_logic_use.get_all_answers()
    response = Flask.response_class(json.dumps(json_question), status=200)
    return response


@app.route('/answer', methods=['POST'])
def post_answer():
    data = request.get_json()
    api_logic_use.add_answer(json.loads(data))
    response = Flask.response_class(json.dumps(data), status=201)
    return response


if __name__ == '__main__':
    app.run(host="localhost", port=9875)
