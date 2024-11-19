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
                if self.board[mine_y][mine_x] == 0:
                    self.board[mine_y][mine_x] = 1
                break
    
#    def set_mine(self, y, x):
#        self.board[y][x] = 1
    
    def set_value(self, y, x, value):
        self.board[y][x] = value

    def is_flipped(self, y, x):
        return self.board[y][x] >= 16
    
    def flip(self, y, x):
        self.board[y][x] = self.board[y][x] + 16

#    def save(self, filename):
#        board_file = open(filename, 'w')
#        for y in range(self.y):
#           line = ''
#            for x in range(self.x):
#                line += str(self.board[y][x])
#            board_file.write(line)
#            board_file.write('\n')
#        board_file.close()
    
    def get_tile(self, y, x):
        return self.board[y][x]
    
    def save_binary(self, filename):
        board_file = open(filename, 'wb')
        binary_int = 0
        board_file.write(self.x.to_bytes(1, 'little'))
        for y in range(self.y):
            for x in range(self.x):
                binary_int = self.board[y][x]
                board_file.write(binary_int.to_bytes(1, 'little'))
        board_file.close()

    def getStatus(self):
        return str(self.mines)


