import random
import struct

class MinesweepBoard:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.board = [ [0]*x for i in range(y) ]

    def create_mines(self):
        self.mines = round(self.y * self.x * random.uniform(0.15, 0.21))

        for i in range(self.mines):
            while True:
                mine_y = random.randint(0,self.y-1)
                mine_x = random.randint(0,self.x-1)
                if self.board[mine_y][mine_x] != 9:
                    self.board[mine_y][mine_x] = 9
                break

    def set_value(self, y, x, value):
        self.board[y][x] = value

    def is_flipped(self, y, x):
        return self.board[y][x] >= 16
    
    def flip(self, y, x):
        if not self.is_flipped(y, x):
            self.board[y][x] = self.board[y][x] + 16
    
    def get_tile(self, y, x):
        return self.board[y][x]



