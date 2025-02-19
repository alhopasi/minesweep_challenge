from flask import Flask, render_template, request, jsonify, send_file
from minesweep.game_handler import GameHandler
from flask_socketio import SocketIO, emit, send
import os

app = Flask(__name__)
if os.environ.get('ENV', 'PROD') == 'DEV':
    socketio = SocketIO(app, async_mode='threading')
else:
    import eventlet
    socketio = SocketIO(app, async_mode='eventlet')

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/board', methods = ['GET'])
def post_board():
    return send_file('/data/online/board', mimetype='application/octet-stream')

@app.route('/play', methods = ['GET'])
def next_turn():
    game.play_turn()
    return jsonify(success=True)

@app.route('/hardreset', methods = ['GET'])
def restart_hard():
    game.reset_game(3)
    return jsonify(success=True)

@app.route('/reset', methods = ['GET'])
def restart():
    game.reset_game(game.gameboard.dimension)
    return jsonify(success=True)

@app.route('/stats', methods = ['GET'])
def stats():
    return jsonify(dimension = game.gameboard.dimension, board = game.gameboard.board, running = game.game_running, victory = game.victory, votes = game.votes)


@socketio.on('connect')
def handle_connect():
    pass

@socketio.on('message')
def handle_message(message):
    vote_y, vote_x = message.split(" ")
    if not game.validate_vote(vote_y, vote_x):
        return None
    vote_y, vote_x = int(vote_y), int(vote_x)
    vote_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    game.vote(vote_y, vote_x, vote_ip)

game_handler = GameHandler(socketio)
game = game_handler.game


if os.environ.get('ENV', 'PROD') == 'DEV':
    if __name__ == '__main__':
        socketio.run(app, debug=True)
