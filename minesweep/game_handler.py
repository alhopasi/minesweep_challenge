from .game import MinesweepGame
import threading
import time

class GameHandler:
    LOOPTIME = 10000

    def __init__(self, socketio):
        self.socketio = socketio
        self.game_loop_thread = None
        self.game = MinesweepGame()

        self.next_game_loop = self.time_now_ms() + self.LOOPTIME
        self.game_loop_start()

    def time_now_ms(self):
        return int(time.time() * 1000)

    def game_loop_start(self):
        if self.game_loop_thread is None or not self.game_loop_thread.is_alive():
            self.game_loop_thread = threading.Thread(target=self.game_loop)
            self.game_loop_thread.daemon = True
            self.game_loop_thread.start()

    def game_loop(self):
        while True:
            if self.time_now_ms() > self.next_game_loop:
                self.next_game_loop = self.time_now_ms() + self.LOOPTIME

                self.game.play_turn()
                self.game.save_board('/data/board')
                self.game.save_online_board('/data/online/board')
                if self.game.send_data:
                    self.socketio.send(bytes(self.game.online_data()))
                    self.game.send_data = False
                self.game.new_board = False
                self.game.gameboard.explored.clear()
            time.sleep(0.2)