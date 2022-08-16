# Connect 4 player

to do:

- get PlayerAC call() responding, a matter of setting up convolutional layers correctly
    - ~~adding channels at deepest dimension has worked
    - ~~now learn how to stack results of convolution layers with concatenate.~~
- set up playing a game and proper distribution of rewards
    - can the results be added together for a single player when considering rewards?
       or do they have to alternate between two models? likely the first
- set up gradient descent adjustment to model variables
- set up repeated games to repeat process of improving plays

## class Gameboard

    GameBoard(board_shape = (6,7))
    - methods
    ```
        drop(color, column)
        grid_to_color(color_dict_in = None)
        show(figsize = (6,7), colors = None) 
    ```
    
## class ConnectFour(GameBoard)

    ConnectFour(starting_player = 1, second_player = -1, board_shape = (6,7))
    - methods
    ```
        reset()
        four_in_row(row)
        four_in_col(col)
        four_in_diag(kth_diagonal, minor = False)
        play(column, to_show = False)
        count_adjacent(row, col, value)
        play_series(moves_list, to_show = False)
        check_win()
        
    ```
    
## class Player
    
    `Player(name = 'Anders', num_actions = 7, random_seed = 2022)`
    - methods
    ```
        decide_random()
    ```
    
## class PlayerAC(Player)

    `PlayerAC(name = 'Anders', num_actions = 7, hidden_size = 1080, random_seed = 2022)`
    - methods
    ```
        simple_call(this_input)
        call(this_input)
    ```