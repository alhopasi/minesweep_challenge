from .minesweep import MinesweepBoard

class MinesweepGame:
    def __init__(self):
        try:
            board_file = open('current', 'rb')
            data = board_file.read()
            board_file.close()
            board_y = data[0]
            board_x = data[0]
            self.board = MinesweepBoard(board_y, board_x)
            for y in range(board_y):
                for x in range(board_x):
                    value = data[board_y*y + x + 1]
                    self.board.set_value(y, x, value)

        except FileNotFoundError:
            self.board = MinesweepBoard(3,3)
            self.board.create_mines()
            self.board.save_binary('current')

    def game_status(self):
        return None

    def get_html_board(self):
        line = ''
        for y in range(self.board.y):
            for x in range(self.board.x):
                value = self.board.board[y][x]
                if value > 16:
                    value -= 16
                    line += str(value)
                else: line += str(16)
            line += '<br>'
        return line
    
    def get_binary_data(self):
        binary_data = []
        for y in range(self.board.y):
            for x in range(self.board.x):
                value = self.board.board[y][x]
                if value > 16:
                    value -= 16
                    binary_data.append(value)
                else:
                    binary_data.append(11)
        return binary_data
    
    # Create "flip" on gameboard to set u

    # data sent to server in bits
    # bits 0-3 (4 bits)
    # 0 = game running : 0 = no, 1 = yes
    # 1 = 0 = loss, 1 = victory (if game not running)
    # 2-3 nothing
    #
    # bits 4-16 (12 bits)
    # size of current board (number 3 representing 3x3 board)
    #
    # size of board * 4 bits, starting from bit 17:
    # 0-8 = mines close (0-8)
    # 9 = mine
    # 10 = mine that was hit
    # 11 = not explored


 
