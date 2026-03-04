import pygame 
import sys
import random
import json
import os

pygame.init()

#global constants
window_width = 640
header_height = 60

color_background = (20, 20, 20)
color_header_background = (10, 10, 10)
color_normal_text = (255,255, 255)
color_selected_text = (255,215,0)
color_snake_body = (50, 205, 50)
color_snake_head = (0, 155, 0)

#apple power ups (mechanics)
apples_types_data = {
    "small": {"color": (255, 60, 60), "growth_value": 1, "spawn-chance": 0.70},
    "medium": {"color": (255, 165, 0), "growth_value": 3, "spawn-chance": 0.20},
    "large": {"color": (147, 112, 219), "growth_value": 5, "spawn-chance": 0.10}
}

BASE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIGURATION_FILE_PATH = os.path.join(BASE_DIRECTORY_PATH, "snake_config.json")

#fonts
font_small_text = pygame.font.Sysfont ("arial", 20)
font_medium_text =  pygame.font.Sysfont ("arial", 32)
font_large_text = pygame.font.Sysfont ("arial", 50)

#set up of display
game_window_display = pygame.display.set_mode((window_width, window_width + header_height))
pygame.display.set_caption("snake")

game_timing_clock = pygame.time.Clock()

def draw_text_on_screen(text_string, chosen_font, text_color, x_position, y_position, is_centered=True):
    text_surface_image = chosen_font.render(text_string, True, text_color)
    text_boundary_rectangle = text_surface_image.get_rect()
    
    if is_centered:
        text_boundary_rectangle.center = (x_position, y_position)
    else:
        text_boundary_rectangle.topleft = (x_position, y_position)
        
    game_window_display.blit(text_surface_image, text_boundary_rectangle)


def get_random_grid_position(maximum_width, maximum_height):
    random_x_coordinate = random.randint(0, maximum_width - 1)
    random_y_coordinate = random.randint(0, maximum_height - 1)
    return (random_x_coordinate, random_y_coordinate)

def generate_new_apple(grid_width_limit, grid_height_limit, current_snake_body, list_of_current_apples):

    while True:
        random_position = get_random_grid_position(grid_width_limit, grid_height_limit)
        
        occupied_apple_positions = [apple_item['position'] for apple_item in list_of_current_apples]
        
        if random_position not in current_snake_body and random_position not in occupied_apple_positions:
            
            random_percentage_roll = random.random()
            
            if random_percentage_roll < apples_types_data['small']['spawn_chance']:
                selected_apple_data = apples_types_data['small']
            elif random_percentage_roll < apples_types_data['small']['spawn_chance'] + apples_types_data['medium']['spawn_chance']:
                selected_apple_data = apples_types_data['medium']
            else:
                selected_apple_data = apples_types_data['large']
            
            return {
                "position": random_position,
                "color": selected_apple_data["color"],
                "growth_value": selected_apple_data["growth_value"]
            }
        
def calculate_current_score(snake_length, grid_width, grid_height):
    total_available_cells = grid_width * grid_height
    percentage_filled = snake_length / total_available_cells
    return int(percentage_filled * 1000)

def load_user_settings_from_file():
    default_user_settings = {"grid_index": 0, "difficulty_index": 0, "wall_wrap_index": 0}
    
    if os.path.exists(CONFIGURATION_FILE_PATH):
        try:
            with open(CONFIGURATION_FILE_PATH, 'r') as configuration_file:
                loaded_data = json.load(configuration_file)
                if "wall_wrap_index" not in loaded_data: 
                    loaded_data["wall_wrap_index"] = 0
                return loaded_data
        except:
            return default_user_settings
    return default_user_settings

def save_user_settings_to_file(grid_choice_index, difficulty_choice_index, wall_wrap_choice_index):
    try:
        with open(CONFIGURATION_FILE_PATH, 'w') as configuration_file:
            json.dump({
                "grid_index": grid_choice_index, 
                "difficulty_index": difficulty_choice_index,
                "wall_wrap_index": wall_wrap_choice_index
            }, configuration_file)
    except:
        pass

def calculate_movement_delay_milliseconds(base_speed_milliseconds, current_snake_length, current_difficulty):
    if current_difficulty == "Easy":
        speed_reduction_amount = current_snake_length * 0.2
        calculated_delay = max(40, int(base_speed_milliseconds - speed_reduction_amount)) 
        return calculated_delay
    else: 
        speed_reduction_amount = current_snake_length * 0.5
        calculated_delay = max(25, int(base_speed_milliseconds - speed_reduction_amount))
        return calculated_delay

#Main Menu
def display_main_menu(starting_grid_index, starting_difficulty_index, starting_wrap_index):
    list_of_grid_options = [32, 64]
    list_of_difficulty_options = ["Easy", "Hard"]
    list_of_wall_options = ["Wrap", "Solid"]
    
    current_grid_index = starting_grid_index
    current_difficulty_index = starting_difficulty_index
    current_wrap_index = starting_wrap_index
    
    currently_highlighted_row = 0
    is_menu_running = True

    while is_menu_running:
        game_window_display.fill(color_background) 
        pygame.draw.rect(game_window_display, color_header_background, (0, 0, window_width, header_height))
        
        draw_text_on_screen("SNAKE", font_large_text, color_snake_body, window_width // 2, 120)
        draw_text_on_screen("WASD / Arrows to Move. Enter to Start.", font_small_text, (150, 150, 150), window_width // 2, 180)

        legend_y_position = 220
        pygame.draw.rect(game_window_display, apples_types_data['small']['color'], (200, legend_y_position, 20, 20))
        draw_text_on_screen("= +1", font_small_text, color_normal_text, 230, legend_y_position, is_centered=False)
        
        pygame.draw.rect(game_window_display, apples_types_data['medium']['color'], (280, legend_y_position, 20, 20))
        draw_text_on_screen("= +3", font_small_text, color_normal_text, 310, legend_y_position, is_centered=False)
        
        pygame.draw.rect(game_window_display, apples_types_data['large']['color'], (360, legend_y_position, 20, 20))
        draw_text_on_screen("= +5", font_small_text, color_normal_text, 390, legend_y_position, is_centered=False)

        row_color = color_normal_text if currently_highlighted_row == 0 else color_normal_text
        row_text = f"Grid Size: < {list_of_grid_options[current_grid_index]}x{list_of_grid_options[current_grid_index]} >"
        draw_text_on_screen(row_text, font_medium_text, row_color, window_width // 2, 290)
        
        row_color = color_normal_text if currently_highlighted_row == 1 else color_normal_text
        row_text = f"Difficulty: < {list_of_difficulty_options[current_difficulty_index]} >"
        draw_text_on_screen(row_text, font_medium_text, row_color, window_width // 2, 340)

        row_color = color_normal_text if currently_highlighted_row == 2 else color_normal_text
        row_text = f"Walls: < {list_of_wall_options[current_wrap_index]} >"
        draw_text_on_screen(row_text, font_medium_text, row_color, window_width // 2, 390)

        row_color = color_normal_text if currently_highlighted_row == 3 else color_normal_text
        draw_text_on_screen("START GAME", font_medium_text, row_color, window_width // 2, 460)

        pygame.display.flip()


        for user_event in pygame.event.get():
            if user_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if user_event.type == pygame.KEYDOWN:
                if user_event.key == pygame.K_UP or user_event.key == pygame.K_w:
                    currently_highlighted_row = (currently_highlighted_row - 1) % 4
                elif user_event.key == pygame.K_DOWN or user_event.key == pygame.K_s:
                    currently_highlighted_row = (currently_highlighted_row + 1) % 4
                
                elif user_event.key == pygame.K_LEFT or user_event.key == pygame.K_a:
                    if currently_highlighted_row == 0: 
                        current_grid_index = (current_grid_index - 1) % len(list_of_grid_options)
                    elif currently_highlighted_row == 1: 
                        current_difficulty_index = (current_difficulty_index - 1) % len(list_of_difficulty_options)
                    elif currently_highlighted_row == 2: 
                        current_wrap_index = (current_wrap_index - 1) % len(list_of_wall_options)
                
                elif user_event.key == pygame.K_RIGHT or user_event.key == pygame.K_d:
                    if currently_highlighted_row == 0: 
                        current_grid_index = (current_grid_index + 1) % len(list_of_grid_options)
                    elif currently_highlighted_row == 1: 
                        current_difficulty_index = (current_difficulty_index + 1) % len(list_of_difficulty_options)
                    elif currently_highlighted_row == 2: 
                        current_wrap_index = (current_wrap_index + 1) % len(list_of_wall_options)
                
                elif user_event.key == pygame.K_RETURN:
                    return current_grid_index, current_difficulty_index, current_wrap_index

def execute_game_loop(chosen_grid_size, chosen_difficulty, is_wall_wrap_enabled):

    grid_width_maximum = chosen_grid_size
    grid_height_maximum = chosen_grid_size
    pixel_size_per_cell = window_width // grid_width_maximum 
    

    base_delay_milliseconds = 100 if chosen_difficulty == "Easy" else 66
    maximum_apples_allowed = 5 if chosen_difficulty == "Easy" else 3


    starting_x_coordinate = grid_width_maximum // 2
    starting_y_coordinate = grid_height_maximum // 2

    snake_body_coordinates = [
        (starting_x_coordinate, starting_y_coordinate), 
        (starting_x_coordinate - 1, starting_y_coordinate), 
        (starting_x_coordinate - 2, starting_y_coordinate)
    ]
    
    current_moving_direction = (1, 0) # Moving Right
    player_input_buffer_queue = []    # Buffer to hold fast key presses
    pending_growth_segments = 0       # How much the snake still needs to grow after eating
    list_of_active_apples = []


    while len(list_of_active_apples) < maximum_apples_allowed:
        new_apple = generate_new_apple(grid_width_maximum, grid_height_maximum, snake_body_coordinates, list_of_active_apples)
        list_of_active_apples.append(new_apple)

    time_of_last_movement = pygame.time.get_ticks() 
    is_game_running = True
    is_game_over = False
    is_game_won = False
    
    while is_game_running:
        for user_event in pygame.event.get():
            if user_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if user_event.type == pygame.KEYDOWN:
                if user_event.key == pygame.K_UP or user_event.key == pygame.K_w:
                    currently_highlighted_row = (currently_highlighted_row - 1) % 4
                elif user_event.key == pygame.K_DOWN or user_event.key == pygame.K_s:
                    currently_highlighted_row = (currently_highlighted_row + 1) % 4

                elif user_event.key == pygame.K_LEFT or user_event.key == pygame.K_a:
                    if currently_highlighted_row == 0: 
                        current_grid_index = (current_grid_index - 1) % len(list_of_grid_options)
                    elif currently_highlighted_row == 1: 
                        current_difficulty_index = (current_difficulty_index - 1) % len(list_of_difficulty_options)
                    elif currently_highlighted_row == 2: 
                        current_wrap_index = (current_wrap_index - 1) % len(list_of_wall_options)

                elif user_event.key == pygame.K_RIGHT or user_event.key == pygame.K_d:
                    if currently_highlighted_row == 0: 
                        current_grid_index = (current_grid_index + 1) % len(list_of_grid_options)
                    elif currently_highlighted_row == 1: 
                        current_difficulty_index = (current_difficulty_index + 1) % len(list_of_difficulty_options)
                    elif currently_highlighted_row == 2: 
                        current_wrap_index = (current_wrap_index + 1) % len(list_of_wall_options)

                elif user_event.key == pygame.K_RETURN:
                    return current_grid_index, current_difficulty_index, current_wrap_index