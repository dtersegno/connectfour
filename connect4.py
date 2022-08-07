import numpy as np
import matplotlib.pyplot as plt

class GameBoard:
    def __init__(self, board_shape = (6,7)):
        self.shape = board_shape
        self.grid = np.full(board_shape, 0, ).astype('float32')
        black = (0.2,0.2,0.2)
        red = (0.9, 0.3,0.3)
        blue = (0.3,0.3,0.9)
        self.colors = {
            0:black,
            1:red,
            -1:blue
        }
        
    #drop the specified element into the specified column, and return True. Returns False if the column is full and makes no changes.
    def drop(self, color, column):
        #check if the column is full first
        if self.grid[0,column] != 0:
            print(f'Cannot drop a {color} in full column {column}!')
            return False
        else:
            dropping = True
            current_row = 0
            
            #drop the color until the spot below is filled
            while dropping:
                #if it hits the bottom, stop falling
                if current_row == self.shape[0]-1:
                    dropping = False
                #if the next row is empty, drop to it
                elif self.grid[current_row + 1, column] == 0:
                    current_row += 1
                else:
                    dropping = False
                    
            #assign the color to the spot in the grid
            self.grid[current_row, column] = color
            return True
    
    #converts the grid to plottable colors
    def grid_to_color(self, color_dict_in = None):
        if color_dict_in == None:
            color_dict = self.colors
        else:
            color_dict = color_dict_in
        color_grid = self.grid
        color_grid = [
            [
                color_dict[value]
                for value in row
            ]
            for row in color_grid
        ]
        color_grid = np.array(color_grid)
        return color_grid
    
    #shows the grid with plt.imshow
    def show(self, figsize = (6,7), colors = None):
#         if colors == None:
#             color_dict
        fig, ax = plt.subplots(figsize = figsize)
        grid_pic = self.grid_to_color()
        plt.imshow(grid_pic)
#         ax.set_xticks(np.arange(-.5, 7, 1))
#         ax.set_yticks(np.arange(-.5, 6, 1))
        plt.grid(True)
        plt.xticks(np.arange(-.5, 7, 1), labels = range(1,9))
        plt.yticks(np.arange(-.5, 6, 1), labels = [])



class ConnectFour(GameBoard):
    def __init__(self, starting_player = 1, second_player = -1, board_shape = (6,7)):
        super().__init__(board_shape)
        self.current_player = 0
        self.players = [starting_player, second_player]
        self.turns = 0
        self.winning_turn = 0
        self.winner = None
        self.done = False
        self.last_play = None
        self.history = []
        self.scores = [0,0] #scores for player 0 and player 1
        
    def reset(self):
        self.grid = np.full(self.shape, 0)
        self.turns = 0
        self.winner = None
        self.done = False
          
    #checks a single row
    def four_in_row(self, row):
        for window in range(self.shape[1]-3):
            if abs(self.grid[row, window:window+4].sum()) == 4:
                return True
        return False
    
    #checks a single column
    def four_in_col(self, col):
        for window in range(self.shape[0]-3):
            if abs(self.grid[window:window+4, col].sum()) == 4:
                return True
        return False
        
    
    #scan major diagonals drawn from upper left across
    def four_in_diag(self, kth_diagonal, minor = False):
        #optionally mirror the array to check /-tilted diagonals
        if minor:
            this_diagonal = np.diag(np.fliplr(self.grid), kth_diagonal)
        else:
            this_diagonal = np.diag(self.grid, kth_diagonal)
        for window in range(len(this_diagonal)-3):
            if abs(this_diagonal[window:window+4].sum()) == 4:
                return True
        return False
    
    #drop the color of the current player and deal with the consequences
    def play(self, column, to_show = False):
        self.turns += 1
        drop_successful = self.drop(self.players[self.current_player], column)
        
        if drop_successful:
            self.last_play = [self.players[self.current_player], 'drop', column]
            ##check if state is win
            self.check_win()
            self.current_player = (self.current_player+1)%2
        else:
            self.last_play = [self.players[self.current_player], 'attempt', column]
        if to_show:
            self.show()
        self.history.append(self.last_play)
        return drop_successful
        
    #checks how many of 'value' are occupied in cells adjacent to grid[row,col]
    def count_adjacent(self, row, col, value):
        #check if center cell is on the edge of the grid
        top = row == 0
        bottom = row == self.grid.shape[0]-1
        left = col == 0
        right = col == self.grid.shape[1]-1
        
        #row indices
        upper_index = row - 1
        lower_index = row + 1
        if bottom:
            lower_index = row
        elif top:
            upper_index = row #or just upper_index == 0
        
        #column indices
        left_index = col - 1
        right_index = col + 1
        if left:
            left_index = col
        elif right:
            right_index = col
            
        #get slice
        gridslice = self.grid[upper_index:lower_index+1, left_index:right_index + 1]
        gridtruths = gridslice == value
        adjacent_count = gridtruths.sum() - (self.grid[row,col] == value) #subtract 1 to not count the center value, if it is the same
        return adjacent_count
        
        
        
    def play_series(self, moves:list = [1,2,3,4,5,6,6,6,5], to_show = False):
        for move in moves:
            self.play(move)
        if to_show:
            self.show()

    
    def check_win(self):
        if self.done:
            print(f'The game already ended with {self.winner} winning in {self.winning_turn} turns.')
        else:
            row_checks = [
                self.four_in_row(row)
                for row in range(self.shape[0])
            ]
            col_checks = [
                self.four_in_col(col)
                for col in range(self.shape[1])
            ]
            diag_count = max(self.shape)-3
            maj_diag_checks = [
                self.four_in_diag(k)
                for k in range(-diag_count, diag_count)
            ]
            min_diag_checks = [
                self.four_in_diag(k, minor = True)
                for k in range(-diag_count, diag_count)
            ]
            self.done = True in row_checks + col_checks + maj_diag_checks + min_diag_checks
            if self.done:
                self.winner = self.players[self.current_player]
                self.winning_turn = self.turns
                print(f'Player {self.winner} wins in {self.winning_turn} turns.')