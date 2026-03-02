import pygame 
import sys
import random
import json
import os

pygame.init()

#Global Constants
window_width = 640
header_height = 60

color_background = (20, 20, 20)
color_header_background = (10, 10, 10)
color_normal_text = (255,255, 255)
color_selected_text = (255,215,0)
color_snake_body = (50, 205, 50)
color_snake_head = (0, 155, 0)

#Apple Power ups
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

#Set up of display
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
