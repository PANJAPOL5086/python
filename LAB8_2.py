def create_mine_field(mine_positions, field_size=10): 
    field = [[0] * field_size for _ in range(field_size)]
    
    for mine in mine_positions:
        row, col = mine
        field[row][col] = 'X'

    for mine in mine_positions:
        row, col = mine
        for r in range(field_size):
            for c in range(field_size):
                distance = max(abs(row - r), abs(col - c))
                
                if distance == 0:
                    continue

                if field[r][c] == 0 or (isinstance(field[r][c], int) and field[r][c] > distance):
                    field[r][c] = distance

    return field

def display_field(field):
    for row in field:
        print(" ".join(str(cell) for cell in row))

def main():
    num_mines = int(input("Enter Number of Mines (1-5): "))
    
    mine_positions = []
    for i in range(num_mines):
        position = input(f"Enter location of Mine {i + 1} [Row,Col]: ").strip('[]')
        row, col = map(int, position.split(','))
        
        if row < 1 or row > 10 or col < 1 or col > 10:
            print(f"Error")
            return
        
        mine_positions.append((row - 1, col - 1))

    mine_field = create_mine_field(mine_positions)
    display_field(mine_field)

main()
