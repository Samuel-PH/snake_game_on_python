import pygame 
import sys
import random
import json
import os

pygame.init()

#global constants (must be writen in upper case)
WINDOW_WIDTH = 832
HEADER_HEIGHT = 60   

COLOR_BACKGROUND = (20, 20, 20)
COLOR_HEADER_BACKGROUND = (10, 10, 10)
COLOR_NORMAL_TEXT = (255, 255, 255)
COLOR_SELECTED_TEXT = (255, 215, 0)
COLOR_SNAKE_BODY = (50, 205, 50)
COLOR_SNAKE_HEAD = (0, 155, 0)

#apple power ups (mechanics)
APPLE_TYPES_DATA = {
    "small": {"color": (255, 60, 60), "growth_value": 1, "spawn_chance": 0.70},
    "medium": {"color": (255, 165, 0), "growth_value": 3, "spawn_chance": 0.20},
    "large": {"color": (147, 112, 219), "growth_value": 5, "spawn_chance": 0.10}
}

BASE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIGURATION_FILE_PATH = os.path.join(BASE_DIRECTORY_PATH, "snake_config.json")

#fonts
font_small_text = pygame.font.SysFont ("arial", 20)
font_medium_text =  pygame.font.SysFont ("arial", 32)
font_large_text = pygame.font.SysFont ("arial", 50)

#set up of display
game_window_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH + HEADER_HEIGHT))
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
            
            if random_percentage_roll < APPLE_TYPES_DATA['small']['spawn_chance']:
                selected_apple_data = APPLE_TYPES_DATA['small']
            elif random_percentage_roll < APPLE_TYPES_DATA['small']['spawn_chance'] + APPLE_TYPES_DATA['medium']['spawn_chance']:
                selected_apple_data = APPLE_TYPES_DATA['medium']
            else:
                selected_apple_data = APPLE_TYPES_DATA['large']
            
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
        game_window_display.fill(COLOR_BACKGROUND) 
        pygame.draw.rect(game_window_display, COLOR_HEADER_BACKGROUND, (0, 0, WINDOW_WIDTH, HEADER_HEIGHT))
        
        draw_text_on_screen("SNAKE", font_large_text, COLOR_SNAKE_BODY, WINDOW_WIDTH // 2, 120)
        draw_text_on_screen("WASD / Arrows to Move. Enter to Start.", font_small_text, (150, 150, 150), WINDOW_WIDTH // 2, 180)

        legend_y_position = 220
        center_x = WINDOW_WIDTH // 2
        
        pygame.draw.rect(game_window_display, APPLE_TYPES_DATA['small']['color'], (center_x - 120, legend_y_position, 20, 20))
        draw_text_on_screen("= +1", font_small_text, COLOR_NORMAL_TEXT, center_x - 90, legend_y_position, is_centered=False)
        
        pygame.draw.rect(game_window_display, APPLE_TYPES_DATA['medium']['color'], (center_x - 40, legend_y_position, 20, 20))
        draw_text_on_screen("= +3", font_small_text, COLOR_NORMAL_TEXT, center_x - 10, legend_y_position, is_centered=False)
        
        pygame.draw.rect(game_window_display, APPLE_TYPES_DATA['large']['color'], (center_x + 40, legend_y_position, 20, 20))
        draw_text_on_screen("= +5", font_small_text, COLOR_NORMAL_TEXT, center_x + 70, legend_y_position, is_centered=False)

        row_color = COLOR_SELECTED_TEXT if currently_highlighted_row == 0 else COLOR_NORMAL_TEXT
        row_text = f"Grid Size: < {list_of_grid_options[current_grid_index]}x{list_of_grid_options[current_grid_index]} >"
        draw_text_on_screen(row_text, font_medium_text, row_color, WINDOW_WIDTH // 2, 290)
        

        row_color = COLOR_SELECTED_TEXT if currently_highlighted_row == 1 else COLOR_NORMAL_TEXT
        row_text = f"Difficulty: < {list_of_difficulty_options[current_difficulty_index]} >"
        draw_text_on_screen(row_text, font_medium_text, row_color, WINDOW_WIDTH // 2, 340)

        row_color = COLOR_SELECTED_TEXT if currently_highlighted_row == 2 else COLOR_NORMAL_TEXT
        row_text = f"Walls: < {list_of_wall_options[current_wrap_index]} >"
        draw_text_on_screen(row_text, font_medium_text, row_color, WINDOW_WIDTH // 2, 390)

        row_color = COLOR_SELECTED_TEXT if currently_highlighted_row == 3 else COLOR_NORMAL_TEXT
        draw_text_on_screen("START GAME", font_medium_text, row_color, WINDOW_WIDTH // 2, 460)

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
    pixel_size_per_cell = WINDOW_WIDTH // grid_width_maximum 
    
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
                if not is_game_over:

                    if player_input_buffer_queue: 
                        last_planned_direction = player_input_buffer_queue[-1]
                    else: 
                        last_planned_direction = current_moving_direction

                    new_planned_direction = None
                    
                    if (user_event.key == pygame.K_UP or user_event.key == pygame.K_w) and last_planned_direction != (0, -1): 
                        new_planned_direction = (0, -1)
                    elif (user_event.key == pygame.K_DOWN or user_event.key == pygame.K_s) and last_planned_direction != (0, -1): 
                        new_planned_direction = (0, 1)
                    elif (user_event.key == pygame.K_LEFT or user_event.key == pygame.K_a) and last_planned_direction != (1, 0): 
                        new_planned_direction = (-1, 0)
                    elif (user_event.key == pygame.K_RIGHT or user_event.key == pygame.K_d) and last_planned_direction != (-1, 0): 
                        new_planned_direction = (1, 0)
                    
                    # Store up to 3 rapid keystrokes to prevent input loss
                    if new_planned_direction and len(player_input_buffer_queue) < 3:
                        player_input_buffer_queue.append(new_planned_direction)
                else:
                    if user_event.key == pygame.K_r: return "restart"
                    elif user_event.key == pygame.K_m: return "menu"
                    elif user_event.key == pygame.K_q: pygame.quit(); sys.exit()

        current_time_milliseconds = pygame.time.get_ticks()
        required_delay_before_move = calculate_movement_delay_milliseconds(base_delay_milliseconds, len(snake_body_coordinates), chosen_difficulty)

        if not is_game_over and not is_game_won:

            if current_time_milliseconds - time_of_last_movement > required_delay_before_move:
                time_of_last_movement = current_time_milliseconds
                if player_input_buffer_queue:
                    current_moving_direction = player_input_buffer_queue.pop(0)
                current_head_x, current_head_y = snake_body_coordinates[0]
                direction_x, direction_y = current_moving_direction
                raw_new_head_x = current_head_x + direction_x
                raw_new_head_y = current_head_y + direction_y
                
                # Check Wall Settings
                if is_wall_wrap_enabled:
                    final_new_head_position = (raw_new_head_x % grid_width_maximum, raw_new_head_y % grid_height_maximum)
                else:
                    final_new_head_position = (raw_new_head_x, raw_new_head_y)
                    if not (0 <= final_new_head_position[0] < grid_width_maximum) or not (0 <= final_new_head_position[1] < grid_height_maximum):
                        is_game_over = True

                # Check Self-Collision
                if not is_game_over:
                    if final_new_head_position in snake_body_coordinates:
                        is_game_over = True
                    else:

                        snake_body_coordinates.insert(0, final_new_head_position)
                        
                        eaten_apple_data = None
                        for active_apple in list_of_active_apples:
                            if active_apple['position'] == final_new_head_position:
                                eaten_apple_data = active_apple
                                break
                        
                        if eaten_apple_data:
                            list_of_active_apples.remove(eaten_apple_data)
                            
                            pending_growth_segments += (eaten_apple_data['growth_value'] - 1)
                            
                            if len(snake_body_coordinates) >= grid_width_maximum * grid_height_maximum:
                                is_game_won = True
                            else:
                                while len(list_of_active_apples) < maximum_apples_allowed:
                                    spawned_apple = generate_new_apple(grid_width_maximum, grid_height_maximum, snake_body_coordinates, list_of_active_apples)
                                    list_of_active_apples.append(spawned_apple)
                        else:
                            if pending_growth_segments > 0:
                                pending_growth_segments -= 1
                            else:
                                snake_body_coordinates.pop()

#Drawings
        game_window_display.fill(COLOR_BACKGROUND)
        
        pygame.draw.rect(game_window_display, COLOR_HEADER_BACKGROUND, (0, 0, WINDOW_WIDTH, HEADER_HEIGHT))
        pygame.draw.line(game_window_display, (50, 50, 50), (0, HEADER_HEIGHT), (WINDOW_WIDTH, HEADER_HEIGHT), 2)

        for active_apple in list_of_active_apples:
            apple_x_coordinate, apple_y_coordinate = active_apple['position']
            apple_color = active_apple['color']
            apple_rectangle = (apple_x_coordinate * pixel_size_per_cell, apple_y_coordinate * pixel_size_per_cell + HEADER_HEIGHT, pixel_size_per_cell, pixel_size_per_cell)
            pygame.draw.rect(game_window_display, apple_color, apple_rectangle)

        for segment_index, snake_segment_coordinates in enumerate(snake_body_coordinates):
            segment_color = COLOR_SNAKE_HEAD if segment_index == 0 else COLOR_SNAKE_BODY
            segment_rectangle = (snake_segment_coordinates[0] * pixel_size_per_cell, snake_segment_coordinates[1] * pixel_size_per_cell + HEADER_HEIGHT, pixel_size_per_cell, pixel_size_per_cell)
            pygame.draw.rect(game_window_display, segment_color, segment_rectangle)

        current_score = calculate_current_score(len(snake_body_coordinates), grid_width_maximum, grid_height_maximum)
        draw_text_on_screen(f"Score: {current_score}", font_medium_text, COLOR_NORMAL_TEXT, WINDOW_WIDTH // 2, HEADER_HEIGHT // 2)
        
        walls_status_text = "Wrap" if is_wall_wrap_enabled else "Solid"
        draw_text_on_screen(f"{chosen_difficulty} | Walls: {walls_status_text}", font_small_text, (150, 150, 150), 100, HEADER_HEIGHT // 2)
        
        if pending_growth_segments > 0:
            draw_text_on_screen(f"Growing...", font_small_text, (50, 205, 50), WINDOW_WIDTH - 60, HEADER_HEIGHT // 2)

        center_y_coordinate_for_text = (WINDOW_WIDTH // 2) + HEADER_HEIGHT
        
        if is_game_over:
            draw_text_on_screen("GAME OVER", font_large_text, (255, 50, 50), WINDOW_WIDTH // 2, center_y_coordinate_for_text - 60)
            draw_text_on_screen(f"Final Score: {current_score}", font_medium_text, COLOR_NORMAL_TEXT, WINDOW_WIDTH // 2, center_y_coordinate_for_text)
            draw_text_on_screen("Press 'R' to Restart", font_small_text, COLOR_NORMAL_TEXT, WINDOW_WIDTH // 2, center_y_coordinate_for_text + 40)
            draw_text_on_screen("Press 'M' for Menu", font_small_text, COLOR_NORMAL_TEXT, WINDOW_WIDTH // 2, center_y_coordinate_for_text + 70)
        
        if is_game_won:
            draw_text_on_screen("YOU WIN!", font_large_text, (50, 255, 215), WINDOW_WIDTH // 2, center_y_coordinate_for_text - 60)
            draw_text_on_screen("Perfect Score: 1000", font_medium_text, COLOR_NORMAL_TEXT, WINDOW_WIDTH // 2, center_y_coordinate_for_text)
            draw_text_on_screen("Press 'R' to Restart", font_small_text, COLOR_NORMAL_TEXT, WINDOW_WIDTH // 2, center_y_coordinate_for_text + 40)
            draw_text_on_screen("Press 'M' for Menu", font_small_text, COLOR_NORMAL_TEXT, WINDOW_WIDTH // 2, center_y_coordinate_for_text + 70)

        pygame.display.flip() 
        game_timing_clock.tick(60) # Lock the game engine to 60 Frames Per Second

#Ignition States
if __name__ == "__main__":
    loaded_user_settings = load_user_settings_from_file()
    saved_grid_index = loaded_user_settings["grid_index"]
    saved_difficulty_index = loaded_user_settings["difficulty_index"]
    saved_wrap_index = loaded_user_settings["wall_wrap_index"]
    
    actual_grid_options = [32, 64]
    actual_difficulty_options = ["Easy", "Hard"]
    actual_wrap_options = [True, False] 

    current_game_state = "MENU"
    
    while True:
        if current_game_state == "MENU":
            saved_grid_index, saved_difficulty_index, saved_wrap_index = display_main_menu(saved_grid_index, saved_difficulty_index, saved_wrap_index)
            
            save_user_settings_to_file(saved_grid_index, saved_difficulty_index, saved_wrap_index)
            
            current_game_state = "GAME"
        
        elif current_game_state == "GAME" or current_game_state == "RESTART":
            chosen_grid_value = actual_grid_options[saved_grid_index]
            chosen_difficulty_value = actual_difficulty_options[saved_difficulty_index]
            chosen_wrap_value = actual_wrap_options[saved_wrap_index]
            
            gameplay_result = execute_game_loop(chosen_grid_value, chosen_difficulty_value, chosen_wrap_value)
            
            if gameplay_result == "restart": 
                current_game_state = "RESTART"
            elif gameplay_result == "menu": 
                current_game_state = "MENU"
