from flask import Flask, render_template, request, jsonify, send_file
from minesweep.game import MinesweepGame
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socketio = SocketIO(app)

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

@app.route('/hardreset', methods = ['GET'])
def restart_hard():
    game.reset_game(3)
    return jsonify(success=True)

@app.route('/reset', methods = ['GET'])
def restart():
    game.reset_game(game.gameboard.dimension)
    return jsonify(success=True)

@app.route('/vote', methods = ['POST'])
def get_vote():
    request_data = request.get_json()
    if not ('y' in request_data and 'x' in request_data):
        return jsonify(success=False)
    vote_y, vote_x, vote_ip = request_data['y'], request_data['x'], request.remote_addr

    if not game.validate_vote(vote_y, vote_x):
        return jsonify(success=False)

    game.vote(vote_y, vote_x, vote_ip)

    return jsonify(success=True)

@app.route('/stats', methods = ['GET'])
def stats():
    return jsonify(dimension = game.gameboard.dimension, board = game.gameboard.board, running = game.game_running, victory = game.victory, votes = game.votes)


@socketio.on('connect')
def handle_connect():
    print('A client connected')

@socketio.on('message')
def handle_message(message):
    print(f"Received message: {message}")
    # Broadcast the message to all clients except the sender
    emit('message', message, broadcast=True)


game = MinesweepGame()

if __name__ == '__main__':
    socketio.run(app, debug=True)


