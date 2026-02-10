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
    PRIMARY_COLOR = "#00b0ff"      # Bright blue
    SECONDARY_COLOR = "#80e2ff"    # Light blue (for hover)
    TEXT_COLOR = "white"
    PANEL_BG = "#000000"           # Black
    PANEL_SECONDARY_BG = "#1c1c1e" # Dark gray (almost black)
    SEPARATOR_COLOR = "#38383a"    # Medium gray
    MUTED_TEXT = "#a0a0a5"         # Lighter gray text
    TEXT_BACKDROP_COLOR = "#101012" # Very dark, for text readability
    
    # Timing (in milliseconds)
    SLIDE_DELAY = 3500             # Time between slideshow transitions
    FADE_STEPS = 10                # Number of steps in fade animation
    PULSE_DELAY = 500              # Pulse animation speed
    RESULT_DISPLAY_TIME = 20000    # How long to show results
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
    TITLE_FONT_SIZE = 32
    SUBTITLE_FONT_SIZE = 18
    BUTTON_FONT_SIZE = 16
    TEXT_FONT_SIZE = 14
    SMALL_TEXT_SIZE = 12
    LARGE_TITLE_SIZE = 48
    
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
    STEP_ICONS = ["🧍", "🎯", "🌾", "🎨", "🔧", "🏁"]
    
    # Payment Settings
    ENABLE_PAYMENT = True
    PAYMENT_METHODS = ['qr', 'card']
    
    # Pricing
    BASE_PRICE = 12.00
    CURRENCY = 'MYR'
    
    # Payment Gateway (add your keys)
    REVENUE_MONSTER_API_KEY = os.getenv("RM_API_KEY", "")
    STRIPE_API_KEY = os.getenv("STRIPE_KEY", "")
    
    # AI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")