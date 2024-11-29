from .board import MinesweepBoard

class MinesweepGame:
    def __init__(self):
        try:
            board_file = open('current', 'rb')
            board_dimension = int.from_bytes(board_file.read(2))
            data = board_file.read()
            board_file.close()
            self.gameboard = MinesweepBoard(board_dimension, board_dimension)
            for y in range(board_dimension):
                for x in range(board_dimension):
                    value = data[board_dimension*y + x]
                    self.gameboard.set_value(y, x, value)

        except FileNotFoundError:
            self.gameboard = MinesweepBoard(3,3)
            self.gameboard.create_mines()
            #self.gameboard.calculate_proximity()
            self.save_binary('current')
            self.save_board('current_board')

        self.game_running = True
        self.victory = False

    def play_turn(self):
        # see saved list of votes - check mine hits - flip new flips - save board
        self.save_board('current_board')

    def save_binary(self, filename):
        board_file = open(filename, 'wb')
        binary_int = 0
        board_file.write(self.gameboard.x.to_bytes(2))
        for y in range(self.gameboard.y):
            for x in range(self.gameboard.x):
                binary_int = self.gameboard.board[y][x]
                board_file.write(binary_int.to_bytes())
        board_file.close()

    # NOTES FOR INCOMING EDITS: 
    # USE ONLY 1 BOARD SAVE. EDIT SAVE/READ SYSTEM TO USE THIS. 
    # CHANGE THE BOARD BYTES/BITS TO THIS:
    #
    # on 'board':
    # 0-8 = explored, not mine
    # 9 = not explored
    # 10 = mine, not explored
    # 11 = mine, explored
    # This is: 1 byte (16 bits)
    # Min to write to file = 1 byte. Each byte represents a tile.

    # when saving:
    # bits 0-1: game status:
    # 0 = game running
    # 1 = game stopped, loss
    # 2 = game stopped, victory
    # bits 3-15:
    # size of current board (number 3 representing 3x3 board, max 2^14
    # This is 2 bytes. After that, comes the 'board'
    
    # bytes 1-2:
    # size of current board (number 3 representing 3x3 board, max 2^16
    #
    # each byte after 2, one tile:
    # 0-8 = mines close (0-8)
    # 9 = mine
    # 10 = mine that was hit
    # 11 = not explored
    # add 16 to 0-8 value if explored

    def save_board(self, filename):
        board_file = open(filename, 'wb')
        binary_int = 0
        if self.game_running: board_file.write(int(0).to_bytes())
        else:
            if not self.victory: board_file.write(int(1).to_bytes())
            else: board_file.write(int(2).to_bytes())
        board_file.write(self.gameboard.x.to_bytes(2))
        for y in range(self.gameboard.y):
            for x in range(self.gameboard.x):
                binary_int = self.gameboard.board[y][x]
                if binary_int > 16:
                    binary_int -= 16
                else: 
                    binary_int = 11
                board_file.write(binary_int.to_bytes())
        board_file.close()

    # data sent to server in bytes
    # byte 1:
    # 0 = game running
    # 1 = game not running, loss
    # 2 = game not running, victory
    #
    # bytes 2-3:
    # size of current board (number 3 representing 3x3 board, max 2^16
    #
    # each byte after 3, one tile:
    # 0-8 = mines close (0-8)
    # 9 = mine
    # 10 = mine that was hit
    # 11 = not explored



 
