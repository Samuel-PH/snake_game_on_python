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
    "large": {"color": (150, 112, 221), "growth_value": 5, "spawn-chance": 0.10}
}

#fonts
font_small_text = pygame.font.Sysfont ("arial", 20)
font_medium_text =  pygame.font.Sysfont ("arial", 32)
font_large_text = pygame.font.Sysfont ("arial", 50)

#Set up of display
game_window_display = pygame.display.set_mode((window_width, window_width + header_height))
pygame.display.set_caption("snake")

game_timing_clock = pygame.time.Clock()
