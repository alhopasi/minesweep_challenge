from flask import Blueprint
from flask_socketio import SocketIO, emit, send

minesweep_bp = Blueprint('minesweep', __name__)

@minesweep_bp.route('/board', methods = ['GET'])
def post_board():
    return send_file('/data/online/board', mimetype='application/octet-stream')

@minesweep_bp.route('/play', methods = ['GET'])
def next_turn():
    game.play_turn()
    return jsonify(success=True)

@minesweep_bp.route('/hardreset', methods = ['GET'])
def restart_hard():
    game.reset_game(3)
    return jsonify(success=True)

@minesweep_bp.route('/reset', methods = ['GET'])
def restart():
    game.reset_game(game.gameboard.dimension)
    return jsonify(success=True)

@minesweep_bp.route('/stats', methods = ['GET'])
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
