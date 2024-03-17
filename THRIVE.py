import os
import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Thrive")

# Define UI colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to load images from a directory
def load_images_from_dir(directory):
    images = {} 
    for filename in os.listdir(directory):
        if filename.endswith(".png"):  # Adjust the file extension as needed
            path = os.path.join(directory, filename)
            image_name = os.path.splitext(filename)[0]
            images[image_name] = pygame.image.load(path).convert_alpha()
    return images

# Load tile images
tile_images = load_images_from_dir("Assets/Tiles")
background_tile = pygame.image.load("Assets/Background/Green.png").convert_alpha()  # Load background with alpha conversion

# Define class for handling unit animations
class UnitAnimation:
    def __init__(self, frames):
        self.frames = frames
        self.num_frames = len(frames)
        self.current_frame = 0
        self.frame_count = 0
        self.frame_delay = 200  # Adjust the delay for animation speed

    def update(self):
        self.frame_count += 1
        if self.frame_count % self.frame_delay == 0:
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def get_current_frame(self):
        return self.frames[self.current_frame]

# Load unit images for player and AI
num_frames = 4
player_unit_image = [pygame.image.load(f"assets/PlayerAnimals/Wof/WofyAni/Wof{i}.png").convert_alpha() for i in range(1, num_frames + 1)]
ai_unit_image = [pygame.image.load(f"assets/PlayerAnimals/Snek/SnekyAni/Snek{i}.png").convert_alpha() for i in range(1, num_frames + 1)]

# Create unit animations for player and AI
player_unit_animation = UnitAnimation(player_unit_image)
ai_unit_animation = UnitAnimation(ai_unit_image)

# Set tile size
TILE_SIZE = 15
GRID_COLS = 15
GRID_ROWS = 12
GAP_X = 7.3
GAP_Y = 4.57

# Define terrain types and their probabilities
terrain_types = ["GrassTile1", "GrassTile2", "GrassTile3", "DesertTile1", "DesertTile2", "DesertTile3", "WaterTile"]
terrain_probabilities = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]  # Adjust as needed

# Function to randomly choose a terrain type based on probabilities
def choose_terrain_type():
    return random.choices(terrain_types, weights=terrain_probabilities)[0]

# Function to draw the grid of tiles with random terrain generation
def draw_grid():
    # Calculate the starting position to center the grid
    start_x = (WIDTH - GRID_COLS * (TILE_SIZE * 1.42 + GAP_X)) / 2
    start_y = (HEIGHT - GRID_ROWS * (TILE_SIZE * math.sqrt(3) + GAP_Y)) / 2
    
    terrain_grid = []  # Store terrain types for each grid position
    valid_spawn_points = []  # Store valid spawn points
    
    # Create a list of all possible grid positions
    all_grid_positions = [(round(start_x + col * (TILE_SIZE * 1.19 + GAP_X), 1),
                           round(start_y + row * (TILE_SIZE * math.sqrt(3) + GAP_Y) + col % 2 * (TILE_SIZE * math.sqrt(3) / 2), 1))
                          for row in range(GRID_ROWS) for col in range(GRID_COLS)]
    
    # Shuffle the list of all possible grid positions
    random.shuffle(all_grid_positions)

    for row in range(GRID_ROWS):
        terrain_row = []
        for col in range(GRID_COLS):
            # Pop the last position from the shuffled list
            x, y = all_grid_positions.pop()
            
            # Randomly choose a terrain type based on probabilities
            terrain_type = choose_terrain_type()
            terrain_row.append(terrain_type)
            screen.blit(tile_images[terrain_type], (x, y))

            # Check if the terrain type is not water
            if terrain_type != "WaterTile":
                # Add the position to the list of valid spawn points
                valid_spawn_points.append((x, y))

        terrain_grid.append(terrain_row)

    return terrain_grid, valid_spawn_points

# Function to draw the pattern grid background
def draw_background():
    num_tiles_x = math.ceil(WIDTH / TILE_SIZE)
    num_tiles_y = math.ceil(HEIGHT / TILE_SIZE)

    for row in range(num_tiles_y):
        for col in range(num_tiles_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            screen.blit(background_tile, (x, y))

def draw_ui():
    # Player UI
    player_ui_font = pygame.font.Font(None, 24)
    player_ui_text = player_ui_font.render("Player Stats", True, WHITE)
    screen.blit(player_ui_text, (10, 10))
    player_ui_text = player_ui_font.render("Survival Points: 10", True, WHITE)
    screen.blit(player_ui_text, (10, 40))
    player_ui_text = player_ui_font.render("Units: 1", True, WHITE)
    screen.blit(player_ui_text, (10, 70))
    
    # AI UI
    ai_ui_font = pygame.font.Font(None, 24)
    ai_ui_text = ai_ui_font.render("AI Stats", True, WHITE)
    screen.blit(ai_ui_text, (WIDTH - 150, 10))
    ai_ui_text = ai_ui_font.render("Survival Points: 10", True, WHITE)
    screen.blit(ai_ui_text, (WIDTH - 150, 40))
    ai_ui_text = ai_ui_font.render("Units: 1", True, WHITE)
    screen.blit(ai_ui_text, (WIDTH - 150, 70))

# Draw initial background
draw_background()

# Run the setup function to draw the terrain tiles
terrain_grid, valid_spawn_points = draw_grid()

# Define start_x and start_y
start_x = (WIDTH - GRID_COLS * (TILE_SIZE * 1.42 + GAP_X)) / 2
start_y = (HEIGHT - GRID_ROWS * (TILE_SIZE * math.sqrt(3) + GAP_Y)) / 2

# Randomly select spawn points for player and AI ensuring they are not on top of each other
player_spawn_point = random.choice(valid_spawn_points)
ai_spawn_point = random.choice([point for point in valid_spawn_points if point != player_spawn_point])

# Output the selected spawn points
print("Player Spawn Point:", player_spawn_point)
print("AI Spawn Point:", ai_spawn_point)

# Function to update unit animations
def update_unit_animations():
    player_unit_animation.update()
    ai_unit_animation.update()

# Function to draw units on their spawn points with animation
def draw_units():
    # Draw player unit animation
    player_unit_position = (player_spawn_point[0] - 16, player_spawn_point[1] - 6)
    current_player_frame = player_unit_animation.get_current_frame()
    screen.blit(current_player_frame, player_unit_position)

    # Draw AI unit animation
    ai_unit_position = (ai_spawn_point[0] - 16, ai_spawn_point[1] - 6)
    current_ai_frame = ai_unit_animation.get_current_frame()
    screen.blit(current_ai_frame, ai_unit_position)

# Define game states
PLACING_UNIT, REGULAR_GAME = range(2)
game_state = REGULAR_GAME

# Define functions to handle unit placement
def get_clicked_tile(x, y):
    col = round((x - start_x) / (TILE_SIZE * 1.19 + GAP_X))
    row = round((y - start_y - (col % 2) * (TILE_SIZE * math.sqrt(3) / 2 + GAP_Y)) / (TILE_SIZE * math.sqrt(3) + GAP_Y))
    return col, row

def is_adjacent_to_spawn_point(spawn_point, tile):
    return abs(spawn_point[0] - tile[0]) <= 1 and abs(spawn_point[1] - tile[1]) <= 1

def is_empty_tile(tile):
    # For now, let's assume all tiles are empty
    return True

def place_unit(tile):
    global game_state
    player_spawn_point = (start_x + tile[0] * (TILE_SIZE * 1.19 + GAP_X), start_y + tile[1] * (TILE_SIZE * math.sqrt(3) + GAP_Y) + (tile[0] % 2) * (TILE_SIZE * math.sqrt(3) / 2 + GAP_Y))
    game_state = REGULAR_GAME

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == REGULAR_GAME:
                # Existing code for handling regular game events
                pass
            elif game_state == PLACING_UNIT:
                if event.button == 1:  # Left mouse button
                    # Get the mouse click position
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check if the click is on an empty adjacent tile
                    clicked_tile = get_clicked_tile(mouse_x, mouse_y)
                    if is_adjacent_to_spawn_point(player_spawn_point, clicked_tile) and is_empty_tile(clicked_tile):
                        # Place the unit on the clicked tile
                        place_unit(clicked_tile)
                        game_state = REGULAR_GAME  # Switch back to the regular game state
                        break

    # Update unit animations
    update_unit_animations()

    # Update display    
    draw_ui() # Draw UI for player and AI stats
    draw_units() # Draw units with animation
    pygame.display.update()

# Quit Pygame
pygame.quit()
