import random
ROWS = 6
COLS = 6
grid = [['o' for _ in range(COLS)] for _ in range(ROWS)]

def display_grid():
    for row in grid:
        print(" ".join(row))
    print("-----------")  

def is_column_available(col):
    return grid[0][col] == 'o'

def find_available_row_in_column(col):
    for row in range(ROWS - 1, -1, -1):  
        if grid[row][col] == 'o':  
            return row
    return None

def place_piece(row, col, piece):
    grid[row][col] = piece

def check_for_winner(piece):
    for row in range(ROWS):
        for col in range(COLS - 2):
            if grid[row][col] == piece and grid[row][col + 1] == piece and grid[row][col + 2] == piece:
                return True

    for col in range(COLS):
        for row in range(ROWS - 2):
            if grid[row][col] == piece and grid[row + 1][col] == piece and grid[row + 2][col] == piece:
                return True

    for row in range(ROWS - 2):
        for col in range(COLS - 2):
            if grid[row][col] == piece and grid[row + 1][col + 1] == piece and grid[row + 2][col + 2] == piece:
                return True

    for row in range(ROWS - 2):
        for col in range(2, COLS):
            if grid[row][col] == piece and grid[row + 1][col - 1] == piece and grid[row + 2][col - 2] == piece:
                return True

    return False

def get_available_columns():
    return [col for col in range(COLS) if is_column_available(col)]

def bot_select_column():
    available_columns = get_available_columns()
    if available_columns:
        return random.choice(available_columns)
    return None

def start_game():
    game_over = False
    turn = 0  

    while not game_over:
        display_grid()

        if turn == 0:
            col = int(input("Enter slot (1-6): ")) - 1
            if is_column_available(col):
                row = find_available_row_in_column(col)
                place_piece(row, col, 'P')

                if check_for_winner('P'):
                    display_grid()
                    print("PlayerWin!")
                    game_over = True
            else:
                print("This column is full. Try another slot")
        else:
            col = bot_select_column()
            if col is not None:
                row = find_available_row_in_column(col)
                place_piece(row, col, 'B')

                if check_for_winner('B'):
                    display_grid()
                    print("BotWin!")
                    game_over = True

        turn += 1
        turn %= 2

    print("Game End!")

start_game()
