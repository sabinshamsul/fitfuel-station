"""
FitFuel Station - Configuration File
All constants and configuration values for the application
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

class Config:
    # Display Settings
    WIDTH = 1100
    HEIGHT = 800
    
    # Color Scheme
    PRIMARY_COLOR = "#00c853"      # Bright green
    SECONDARY_COLOR = "#66ffb2"    # Light green
    TEXT_COLOR = "white"
    PANEL_BG = "#000000"           # Black
    PANEL_SECONDARY_BG = "#1a1a1a" # Dark gray
    SEPARATOR_COLOR = "#333333"    # Medium gray
    MUTED_TEXT = "#aaaaaa"         # Gray text
    
    # Timing (in milliseconds)
    SLIDE_DELAY = 3500             # Time between slideshow transitions
    FADE_STEPS = 10                # Number of steps in fade animation
    PULSE_DELAY = 500              # Pulse animation speed
    RESULT_DISPLAY_TIME = 4000     # How long to show results
    PROCESSING_DISPLAY_TIME = 1500 # Loading screen duration
    INACTIVITY_TIMEOUT = 30000     # Auto-reset after 30 seconds
    
    # Image Paths
    ASSETS_DIR = BASE_DIR / 'assets'
    SLIDE_IMAGES = [
        str(ASSETS_DIR / 'gym_bg_1.jpg'),
        str(ASSETS_DIR / 'gym_bg_2.jpg'),
        str(ASSETS_DIR / 'gym_bg_3.jpg')
    ]
    SELECTION_BG = str(ASSETS_DIR / 'gym_bg_3.jpg')
    
    # Font Settings
    FONT_FAMILY = "Helvetica"
    TITLE_FONT_SIZE = 28
    SUBTITLE_FONT_SIZE = 18
    BUTTON_FONT_SIZE = 15
    TEXT_FONT_SIZE = 13
    SMALL_TEXT_SIZE = 12
    LARGE_TITLE_SIZE = 36
    
    # Button Settings
    BUTTON_WIDTH = 16
    BUTTON_HEIGHT = 2
    BACK_BUTTON_WIDTH = 10
    BACK_BUTTON_HEIGHT = 1
    
    # Valid Options
    VALID_MODES = ['pre', 'post']
    VALID_BASES = ['maltodextrin', 'pumpkinrice']
    VALID_FLAVOURS = ['none', 'coffee', 'chocolate', 'matcha']
    
    # UI Steps
    STEPS = ["Scan", "Mode", "Base", "Flavour", "Refine", "Done"]
    
    # AI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")