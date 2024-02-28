import random

# Define the snake's movement directions
DIRECTIONS = {"up": (0, -1), "right": (1, 0), "down": (0, 1), "left": (-1, 0)}

# Define the game board
board = [[' ' for _ in range(21)] for _ in range(21)]

# Initialize the snake's position and direction
snake_position = (10, 10)
snake_direction = "right"

# Initialize the food position
food_position = (0, 0)

# Game loop flag
running = True

# Clock speed
clock_speed = 50

# Game loop
while running:
    # Draw the game board
    for row in range(len(board)):
        for col in range(len(board[0])):
            if (row, col) == snake_position or (row, col) == food_position:
                board[row][col] = 'S' or 'F'
            else:
                board[row][col] = '.'

    # Move the snake
    snake_position = (snake_position[0] + DIRECTIONS[snake_direction][0], snake_position[1] + DIRECTIONS[snake_direction][1])

    # Check if the snake has eaten the food
    if snake_position == food_position:
        # Generate a new food position
        food_position = (random.randint(0, len(board) - 1), random.randint(0, len(board[0]) - 1))

    # Check if the snake has hit a border
    if snake_position[0] < 0 or snake_position[0] >= len(board):
        running = False
    if snake_position[1] < 0 or snake_position[1] >= len(board[0]):
        running = False

    # Update the clock
    clock_speed.sleep()

# Game over message
print("Game over!")