from .game import MinesweepGame
import threading
import time

class GameHandler:
    def __init__(self, socketio):
        self.socketio = socketio
        self.game_loop_thread = None
        self.game = MinesweepGame()
        self.game_loop_start()

    def game_loop_start(self):
        if self.game_loop_thread is None or not self.game_loop_thread.is_alive():
            self.game_loop_thread = threading.Thread(target=self.game_loop)
            self.game_loop_thread.daemon = True
            self.game_loop_thread.start()

    def game_loop(self):
        while True:
            self.game.play_turn()
            self.game.save_board('/data/board')
            self.game.save_online_board('/data/online/board')
            if self.game.send_data:
                self.socketio.send(bytes(self.game.online_data()))
                self.game.send_data = False
            time.sleep(30)