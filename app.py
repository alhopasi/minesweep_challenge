from flask import Flask, render_template, request, jsonify, send_file
from minesweep.game import MinesweepGame

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/board', methods = ['GET'])
def post_board():
    return send_file('current_board', mimetype='application/octet-stream')

@app.route('/play', methods = ['GET'])
def next_turn():
    game.play_turn()
    return jsonify(success=True)

@app.route('/reset', methods = ['GET'])
def restart():
    game = MinesweepGame()
    return jsonify(success=True)


@app.route('/vote', methods = ['POST'])
def get_vote():
    request_data = request.get_json()
    if not ('y' in request_data and 'x' in request_data):
        return jsonify(success=False)
    vote_y = request_data['y']
    vote_x = request_data['x']
    vote_ip = request.remote_addr

    if not game.validate_vote(vote_y, vote_x):
        return jsonify(success=False)

    game.vote(vote_y, vote_x, vote_ip)

    return jsonify(success=True)

game = MinesweepGame()