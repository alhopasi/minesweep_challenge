from flask import Flask, render_template, request
from minesweep.game import MinesweepGame

app = Flask(__name__)


@app.route('/')
def index():
    #game_string = game.get_html_board()
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def get_vote():
    request_data = request.get_json()
    vote_y = request_data['y']
    vote_x = request_data['x']
    vote_ip = request.remote_addr
    return {}

game = MinesweepGame()