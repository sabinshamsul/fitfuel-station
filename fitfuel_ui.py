"""
FitFuel Vending Machine - Streamlined Version
CSV sensor input → User selections → AI recommendations → 50g bar
"""

import tkinter as tk
from tkinter import messagebox
<<<<<<< HEAD
import tkinter.font as tkfont
from PIL import Image, ImageTk
import itertools
import logging
import math
=======
from PIL import Image, ImageTk
import itertools
import logging
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86

from config import Config
from sensor_data_reader import SensorDataReader
from ai_ingredient_recommender import AIIngredientRecommender
<<<<<<< HEAD
from allergen_system import AllergenAnalyzer
# from payment_system import PricingCalculator
=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='fitfuel_station.log'
)


class FitFuelVendingMachine:
    """Streamlined vending machine application."""
    
    def __init__(self):
        self.slideshow_running = False
        self.pulse_state = True
        self.current_slide = None
        self.next_slide = None
<<<<<<< HEAD
        self.loading_animation_job = None
        self.fade_job = None
        self.pulse_job = None
=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
        
        # Components
        self.sensor_reader = SensorDataReader()
        self.ai_recommender = AIIngredientRecommender()
        
        # User data
        self.sensor_data = None
        self.mode = None
        self.carb_mode = None
        self.flavour = None
        self.user_selected_ingredients = None
        self.final_recommendation = None
        self.inactivity_timer = None
<<<<<<< HEAD
        self.ingredient_images = {}
=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86


# Initialize
root = tk.Tk()
root.title("FitFuel Vending Machine")
root.attributes('-fullscreen', True)
Config.WIDTH = root.winfo_screenwidth()
Config.HEIGHT = root.winfo_screenheight()
root.geometry(f"{Config.WIDTH}x{Config.HEIGHT}")
root.resizable(False, False)
root.configure(bg='black')
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

app = FitFuelVendingMachine()

<<<<<<< HEAD
def on_close():
    """Handle window closing event."""
    app.slideshow_running = False
    
    # Cancel all pending jobs to prevent "invalid command name" errors
    for job_attr in ['loading_animation_job', 'inactivity_timer', 'fade_job', 'pulse_job']:
        job = getattr(app, job_attr, None)
        if job:
            try:
                root.after_cancel(job)
            except Exception:
                pass
    
    try:
        root.destroy()
    except Exception:
        pass

root.protocol("WM_DELETE_WINDOW", on_close)

=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
canvas = tk.Canvas(
    root, 
    width=Config.WIDTH, 
    height=Config.HEIGHT, 
    highlightthickness=0,
    bg='black'
)
canvas.pack(fill="both", expand=True)


# Image loading
def load_image(path):
    try:
        return Image.open(path).resize((Config.WIDTH, Config.HEIGHT))
    except Exception as e:
        logging.error(f"Failed to load image {path}: {e}")
        return Image.new('RGB', (Config.WIDTH, Config.HEIGHT), color='#1a1a1a')


slide_images = [load_image(path) for path in Config.SLIDE_IMAGES]
selection_bg_image = load_image(Config.SELECTION_BG)
slide_cycle = itertools.cycle(slide_images)
app.current_slide = next(slide_cycle)
app.next_slide = next(slide_cycle)


def clear_screen():
<<<<<<< HEAD
    try:
        if not root.winfo_exists():
            return
        # Destroy all child widgets (Frames) to prevent memory leaks
        for widget in root.winfo_children():
            if widget != canvas:
                widget.destroy()
        canvas.delete("all")
    except Exception:
        pass
=======
    # Destroy all child widgets (Frames) to prevent memory leaks
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()
    canvas.delete("all")
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86


def draw_background(image):
    """Draw background image - FIXED to prevent memory leak."""
<<<<<<< HEAD
    try:
        if not root.winfo_exists(): return
        photo = ImageTk.PhotoImage(image, master=root)
        
        # Delete old background to prevent memory leak
        canvas.delete("background")
        
        # Create new background with tag
        canvas.create_image(0, 0, image=photo, anchor="nw", tags="background")
        canvas.tag_lower("background")  # Ensure background stays behind other elements
        
        # Store reference (required by tkinter)
        canvas.bg_photo = photo
    except Exception:
        pass


def show_title(text, subtitle=None):
    # New: Add a semi-transparent backdrop for readability
    title_font = tkfont.Font(family=Config.FONT_FAMILY, size=Config.TITLE_FONT_SIZE, weight="bold")
    title_width = title_font.measure(text)
    
    subtitle_width = 0
    if subtitle:
        subtitle_font = tkfont.Font(family=Config.FONT_FAMILY, size=14)
        subtitle_width = subtitle_font.measure(subtitle)
    
    backdrop_width = max(title_width, subtitle_width) + 80
    backdrop_height = 100 if subtitle else 60
    
    x = Config.WIDTH // 2
    y = 85 # Center of the backdrop
    
    # Backdrop
    canvas.create_rectangle(
        x - backdrop_width / 2, y - backdrop_height / 2,
        x + backdrop_width / 2, y + backdrop_height / 2,
        fill=Config.TEXT_BACKDROP_COLOR,
        outline="",
        stipple="gray75" # Hack for semi-transparency
    )
    
    canvas.create_text(
        Config.WIDTH // 2, y - (15 if subtitle else 0),
=======
    photo = ImageTk.PhotoImage(image)
    
    # Delete old background to prevent memory leak
    canvas.delete("background")
    
    # Create new background with tag
    canvas.create_image(0, 0, image=photo, anchor="nw", tags="background")
    canvas.tag_lower("background")  # Ensure background stays behind other elements
    
    # Store reference (required by tkinter)
    canvas.bg_photo = photo


def show_title(text, subtitle=None):
    canvas.create_text(
        Config.WIDTH // 2, 70,
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
        text=text,
        fill="white",
        font=(Config.FONT_FAMILY, Config.TITLE_FONT_SIZE, "bold")
    )
    if subtitle:
        canvas.create_text(
<<<<<<< HEAD
            Config.WIDTH // 2, y + 20,
=======
            Config.WIDTH // 2, 110,
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
            text=subtitle,
            fill="#dddddd",
            font=(Config.FONT_FAMILY, 14)
        )

<<<<<<< HEAD
class RoundedButton(tk.Canvas):
    """Custom rounded button using Canvas."""
    def __init__(self, parent, text, command, width=220, height=60, corner_radius=20, 
                 bg_color=Config.PRIMARY_COLOR, fg_color="black", hover_color=Config.SECONDARY_COLOR, 
                 font_size=None, icon=None):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.fg_color = fg_color
        self.text = text
        self.icon = icon
        self.corner_radius = corner_radius
        self.font_size = font_size or Config.BUTTON_FONT_SIZE
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        # Bind to children (text) as well so clicking text works
        self.bind_all_children("<Button-1>", self._on_click)
        
        self.draw()
        self.configure(cursor="hand2")

    def bind_all_children(self, event, callback):
        pass

    def draw(self, fill_color=None):
        self.delete("all")
        color = fill_color or self.bg_color
        
        r = self.corner_radius
        w = int(self['width'])
        h = int(self['height'])
        
        # Draw rounded shape
        self.create_arc(0, 0, 2*r, 2*r, start=90, extent=90, fill=color, outline=color)
        self.create_arc(w-2*r, 0, w, 2*r, start=0, extent=90, fill=color, outline=color)
        self.create_arc(w-2*r, h-2*r, w, h, start=270, extent=90, fill=color, outline=color)
        self.create_arc(0, h-2*r, 2*r, h, start=180, extent=90, fill=color, outline=color)
        self.create_rectangle(r, 0, w-r, h, fill=color, outline=color)
        self.create_rectangle(0, r, w, h-r, fill=color, outline=color)
        
        # Draw text
        font_spec = (Config.FONT_FAMILY, self.font_size, "bold")
        
        if self.icon:
            # Measure text and icon to center them together
            f = tkfont.Font(family=Config.FONT_FAMILY, size=self.font_size, weight="bold")
            
            lines = self.text.split('\n')
            text_w = max(f.measure(line) for line in lines)
            icon_w = f.measure(self.icon)
            gap = 15
            
            total_w = text_w + gap + icon_w
            start_x = (w - total_w) / 2
            
            # Draw text (centered relative to its own width)
            text_center_x = start_x + (text_w / 2)
            self.create_text(text_center_x, h/2, text=self.text, fill=self.fg_color, 
                           font=font_spec, justify="center")
            
            # Draw icon
            icon_center_x = start_x + text_w + gap + (icon_w / 2)
            self.create_text(icon_center_x, h/2, text=self.icon, fill=self.fg_color, 
                           font=font_spec)
        else:
            self.create_text(w/2, h/2, text=self.text, fill=self.fg_color, 
                           font=font_spec, justify="center")

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_enter(self, event):
        self.draw(fill_color=self.hover_color)

    def _on_leave(self, event):
        self.draw(fill_color=self.bg_color)


def create_button(parent, text, command, bg_color=None, width=None, icon=None):
=======

def create_button(parent, text, command, bg_color=None, width=None):
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    bg = bg_color or Config.PRIMARY_COLOR
    # Hover color: lighter if primary, else slightly lighter grey
    hover_bg = Config.SECONDARY_COLOR if bg == Config.PRIMARY_COLOR else "#888888"
    
<<<<<<< HEAD
    # Convert width logic: Config.BUTTON_WIDTH is 16 chars.
    # If width is provided (in chars), scale it. If not, use default pixel width.
    # 1 char approx 14px.
    
    pixel_width = 220
    if width:
        pixel_width = width * 14
    elif len(text) > 15:
        pixel_width = 280  # Auto-expand for long text
        
    if icon:
        pixel_width += 40
        
    btn = RoundedButton(
        parent,
        text=text,
        command=command,
        width=pixel_width,
        height=60,
        bg_color=bg,
        hover_color=hover_bg,
        fg_color="black" if bg == Config.PRIMARY_COLOR else "white",
        icon=icon
    )
=======
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=(Config.FONT_FAMILY, Config.BUTTON_FONT_SIZE, "bold"),
        bg=bg,
        fg="black",
        activebackground=hover_bg,
        relief="flat",
        width=width or Config.BUTTON_WIDTH,
        height=Config.BUTTON_HEIGHT,
        cursor="hand2"
    )
    
    # Add hover effect
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    return btn


def create_back_button(parent, command, text="← Back"):
<<<<<<< HEAD
    btn = RoundedButton(
        parent,
        text=text,
        command=command,
        width=120,
        height=40,
        bg_color="#333333",
        hover_color="#555555",
        fg_color="white",
        font_size=Config.SMALL_TEXT_SIZE,
        corner_radius=15
    )
=======
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=(Config.FONT_FAMILY, Config.SMALL_TEXT_SIZE),
        bg="#333333",
        fg="white",
        activebackground="#555555",
        relief="flat",
        width=Config.BACK_BUTTON_WIDTH,
        height=Config.BACK_BUTTON_HEIGHT,
        cursor="hand2"
    )
    
    # Add hover effect
    btn.bind("<Enter>", lambda e: btn.config(bg="#555555"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#333333"))
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    return btn


def draw_progress_bar(step_index):
    """Draw the progress stepper at the top of the screen."""
    steps = Config.STEPS
<<<<<<< HEAD
    step_icons = Config.STEP_ICONS
=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    total_steps = len(steps)
    
    w = Config.WIDTH
    margin_x = 200
<<<<<<< HEAD
    y = 160 # Moved down to avoid title
=======
    y = 150
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    available_w = w - (2 * margin_x)
    step_gap = available_w / (total_steps - 1)
    
    for i, step_name in enumerate(steps):
        x = margin_x + (i * step_gap)
        
<<<<<<< HEAD
        # Draw connecting line (will be underneath the next circle)
        if i < total_steps - 1:
            next_x = margin_x + ((i + 1) * step_gap)
            color = Config.PRIMARY_COLOR if i < step_index else "#333333"
            canvas.create_line(x, y, next_x, y, fill=color, width=5)
            
        # Draw node circle
        r = 25 if i == step_index else 16
        outline = Config.PRIMARY_COLOR if i <= step_index else "#333333"
        fill = "black"
        canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline=outline, width=4)
        
        # Draw icon and label
        icon = step_icons[i]
        icon_color = Config.PRIMARY_COLOR if i <= step_index else "#666666"
        icon_font_size = 22 if i == step_index else 14
        canvas.create_text(x, y, text=icon, fill=icon_color, font=("Arial", icon_font_size))

        if i == step_index:
            canvas.create_text(x, y + r + 20, text=step_name, fill="white", font=(Config.FONT_FAMILY, 14, "bold"))
=======
        # Draw connecting line
        if i < total_steps - 1:
            next_x = margin_x + ((i + 1) * step_gap)
            color = Config.PRIMARY_COLOR if i < step_index else "#333333"
            canvas.create_line(x, y, next_x, y, fill=color, width=3)
            
        # Draw node circle
        r = 10 if i == step_index else 6
        outline = Config.PRIMARY_COLOR if i <= step_index else "#333333"
        fill = Config.PRIMARY_COLOR if i <= step_index else "black"
        
        canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline=outline, width=2)
        
        # Draw label
        if i == step_index:
            canvas.create_text(x, y+25, text=step_name, fill="white", font=(Config.FONT_FAMILY, 11, "bold"))
        else:
            canvas.create_text(x, y+25, text=step_name, fill="#666666", font=(Config.FONT_FAMILY, 10))
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86


def reset_inactivity_timer(event=None):
    """Reset the inactivity timer on user interaction - FIXED VERSION."""
    if app.inactivity_timer:
        root.after_cancel(app.inactivity_timer)
        app.inactivity_timer = None
    
    # Only set timer if we are NOT in slideshow mode (i.e., user is interacting)
    if not app.slideshow_running:
        app.inactivity_timer = root.after(Config.INACTIVITY_TIMEOUT, timeout_reset)


def timeout_reset():
    """Reset application due to inactivity."""
    if not app.slideshow_running:
        logging.info("Inactivity timeout - resetting application")
        start_slideshow()


# =============================
# LANDING SCREEN
# =============================
def start_slideshow():
    """Start landing screen slideshow."""
    app.slideshow_running = True
    app.sensor_data = None
    app.mode = None
    app.carb_mode = None
    app.flavour = None
    app.user_selected_ingredients = None
    
    # Cancel any existing inactivity timer
    if app.inactivity_timer:
        root.after_cancel(app.inactivity_timer)
        app.inactivity_timer = None
<<<<<<< HEAD
        
    # Cancel existing slideshow jobs if any
    if app.fade_job:
        try: root.after_cancel(app.fade_job)
        except: pass
        app.fade_job = None
    if app.pulse_job:
        try: root.after_cancel(app.pulse_job)
        except: pass
        app.pulse_job = None
=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    
    clear_screen()
    fade_transition()
    pulse_text()
    
    # Maintenance Button (Top-Left Corner)
    # 1. Draw background (Circle for better aesthetics)
    canvas.create_oval(10, 10, 60, 60, fill="#222222", outline="#444444", width=2, tags="maintenance_trigger")
    # 2. Draw icon
    canvas.create_text(35, 36, text="⚙️", font=("Arial", 24), fill="#aaaaaa", tags="maintenance_trigger")
    
    def on_maintenance_click(event):
        show_pin_entry()
        return "break"

    canvas.tag_bind("maintenance_trigger", "<Button-1>", on_maintenance_click)
    # Ensure it stays on top
    canvas.tag_raise("maintenance_trigger")


def fade_transition(alpha=0.0):
    """Handle the fade animation between slides."""
    if not app.slideshow_running:
        return

<<<<<<< HEAD
    try:
        # Blend current and next images
        blended_image = Image.blend(app.current_slide, app.next_slide, alpha)
        draw_background(blended_image)
        overlay_landing_text()  # Redraw text on top of the blended image

        alpha += 1.0 / Config.FADE_STEPS
        if alpha <= 1.0:
            # Continue fading in the next frame
            # A smaller delay here (e.g., 30ms) creates a smoother animation
            app.fade_job = root.after(30, fade_transition, alpha)
        else:
            # Fade complete, set up for the next cycle
            app.current_slide = app.next_slide
            app.next_slide = next(slide_cycle)
            # Wait for the slide delay, then start the next fade from alpha=0
            app.fade_job = root.after(Config.SLIDE_DELAY, fade_transition, 0.0)
    except Exception:
        pass
=======
    # Blend current and next images
    blended_image = Image.blend(app.current_slide, app.next_slide, alpha)
    draw_background(blended_image)
    overlay_landing_text()  # Redraw text on top of the blended image

    alpha += 1.0 / Config.FADE_STEPS
    if alpha <= 1.0:
        # Continue fading in the next frame
        # A smaller delay here (e.g., 30ms) creates a smoother animation
        root.after(30, fade_transition, alpha)
    else:
        # Fade complete, set up for the next cycle
        app.current_slide = app.next_slide
        app.next_slide = next(slide_cycle)
        # Wait for the slide delay, then start the next fade from alpha=0
        root.after(Config.SLIDE_DELAY, fade_transition, 0.0)
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86


def overlay_landing_text():
    canvas.delete("overlay")
<<<<<<< HEAD
    
    # Backdrop for better readability
    canvas.create_rectangle(
        Config.WIDTH // 2 - 400, 120, Config.WIDTH // 2 + 400, 310,
        fill=Config.TEXT_BACKDROP_COLOR,
        outline="",
        stipple="gray75",
        tags="overlay"
    )
    
=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    canvas.create_text(
        Config.WIDTH // 2, 170,
        text="FITFUEL STATION",
        fill="white",
<<<<<<< HEAD
        font=(Config.FONT_FAMILY, Config.LARGE_TITLE_SIZE, "bold"),
        tags="overlay"
    )
    canvas.create_text(
        Config.WIDTH // 2, 230,
        text="Fresh Protein Bars, Scientifically Optimized for You",
        fill="#dddddd",
        font=(Config.FONT_FAMILY, Config.SUBTITLE_FONT_SIZE),
        tags="overlay"
    )
    canvas.create_text(
        Config.WIDTH // 2, 275,
        text="Get a protein bar customized for your body and goals in minutes.",
        fill=Config.MUTED_TEXT,
        font=(Config.FONT_FAMILY, 14),
=======
        font=(Config.FONT_FAMILY, 36, "bold"),
        tags="overlay"
    )
    canvas.create_text(
        Config.WIDTH // 2, 220,
        text="AI-Powered Personalized Nutrition",
        fill="#dddddd",
        font=(Config.FONT_FAMILY, 18),
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
        tags="overlay"
    )


def pulse_text():
    if not app.slideshow_running:
        return
    
<<<<<<< HEAD
    try:
        color = Config.PRIMARY_COLOR if app.pulse_state else Config.SECONDARY_COLOR
        app.pulse_state = not app.pulse_state
        
        canvas.delete("pulse")
        canvas.create_text(
            Config.WIDTH // 2, Config.HEIGHT - 80,
            text="Touch to Begin",
            fill=color,
            font=(Config.FONT_FAMILY, 16, "bold"),
            tags="pulse"
        )
        app.pulse_job = root.after(Config.PULSE_DELAY, pulse_text)
    except Exception:
        pass
=======
    color = Config.PRIMARY_COLOR if app.pulse_state else Config.SECONDARY_COLOR
    app.pulse_state = not app.pulse_state
    
    canvas.delete("pulse")
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT - 80,
        text="Touch to Begin",
        fill=color,
        font=(Config.FONT_FAMILY, 16, "bold"),
        tags="pulse"
    )
    root.after(Config.PULSE_DELAY, pulse_text)
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86


def stop_slideshow(event=None):
    """Stop slideshow and read sensor data."""
    if not app.slideshow_running:
        return
    app.slideshow_running = False
<<<<<<< HEAD
    
    # Cancel slideshow jobs
    if app.fade_job:
        try: root.after_cancel(app.fade_job)
        except: pass
        app.fade_job = None
    if app.pulse_job:
        try: root.after_cancel(app.pulse_job)
        except: pass
        app.pulse_job = None
        
=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    canvas.delete("pulse")
    read_sensor_data()


# =============================
# SENSOR DATA READING
# =============================
<<<<<<< HEAD
def animate_sensor_scanning(step=0):
    """Animate a pulsing ring for sensor reading."""
    canvas.delete("loading_anim")
    
    cx, cy = Config.WIDTH // 2, Config.HEIGHT // 2 + 80
    
    # Pulse effect
    scale = 1.0 + 0.15 * math.sin(step * 0.1)
    r = 30 * scale
    
    # Outer ring
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, 
                       outline=Config.PRIMARY_COLOR, width=3, tags="loading_anim")
    
    # Inner scanning line
    scan_range = 20
    scan_y = cy + (step % (scan_range * 2)) - scan_range
    if step % (scan_range * 4) > (scan_range * 2):
        scan_y = cy + scan_range - (step % (scan_range * 2))
        
    canvas.create_line(cx-20, scan_y, cx+20, scan_y, fill="white", width=2, tags="loading_anim")
    
    app.loading_animation_job = root.after(30, animate_sensor_scanning, step + 1)


=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
def read_sensor_data():
    """Read body composition from CSV file."""
    clear_screen()
    draw_background(selection_bg_image)
    
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 - 50,
<<<<<<< HEAD
        text="📊 Scanning Body Composition...",
=======
        text="📊 Reading Sensor Data...",
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
        fill="white",
        font=(Config.FONT_FAMILY, 24, "bold")
    )
    
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 10,
        text="Please step on the scale",
        fill="#dddddd",
        font=(Config.FONT_FAMILY, 14)
    )
    
<<<<<<< HEAD
    # Start the animation
    animate_sensor_scanning()
=======
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 50,
        text="●  ●  ●",
        fill=Config.PRIMARY_COLOR,
        font=(Config.FONT_FAMILY, 20)
    )
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    
    root.update()
    root.after(2000, load_sensor_data)


def load_sensor_data():
    """Load data from CSV file."""
<<<<<<< HEAD
    # Stop the animation
    if app.loading_animation_job:
        root.after_cancel(app.loading_animation_job)
        app.loading_animation_job = None

=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    try:
        # Try to read sensor data
        app.sensor_data = app.sensor_reader.read_latest_data()
        
        logging.info("Sensor data loaded successfully")
        show_sensor_confirmation()
        
    except FileNotFoundError:
        # No CSV file - create sample for demo
        logging.warning("CSV file not found, creating sample")
        app.sensor_reader.create_sample_csv()
        
        # Try again
        try:
            app.sensor_data = app.sensor_reader.read_latest_data()
            show_sensor_confirmation()
        except Exception as e:
            show_error(f"Failed to read sensor data: {e}")
    
    except Exception as e:
        logging.error(f"Error reading sensor data: {e}")
        show_error(str(e))


def show_sensor_confirmation():
    """Show loaded sensor data for confirmation."""
    clear_screen()
    draw_background(selection_bg_image)
    
    draw_progress_bar(0)
    show_title("✅ Body Scan Complete", "Your measurements have been recorded")
    
    # Display data
    panel = tk.Frame(root, bg=Config.PANEL_BG, padx=40, pady=30, 
                    highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 20, window=panel)
    
    data_points = [
        ("Body Weight:", f"{app.sensor_data.body_weight_kg:.1f} kg"),
        ("Skeletal Muscle:", f"{app.sensor_data.skeletal_muscle_percent:.1f}%"),
        ("Metabolic Rate:", f"{app.sensor_data.resting_metabolic_rate:.0f} kcal/day"),
        ("Body Fat:", f"{app.sensor_data.body_fat_percent:.1f}%"),
    ]

    for i, (label, value) in enumerate(data_points):
        tk.Label(
            panel,
            text=label,
            bg=Config.PANEL_BG,
            fg=Config.MUTED_TEXT,
            font=(Config.FONT_FAMILY, 14),
            anchor="w"
        ).grid(row=i, column=0, sticky="w", pady=4)

        tk.Label(
            panel,
            text=value,
            bg=Config.PANEL_BG,
            fg="white",
            font=(Config.FONT_FAMILY, 14, "bold"),
            anchor="e"
        ).grid(row=i, column=1, sticky="e", padx=(20, 0))
    
    # Add a frame for the button to give it space
    button_frame = tk.Frame(panel, bg=Config.PANEL_BG)
    button_frame.grid(row=len(data_points), column=0, columnspan=2, pady=(25, 0))
<<<<<<< HEAD
    create_back_button(button_frame, start_slideshow, "Restart").pack(side="left", padx=10)
    create_button(button_frame, "Edit", lambda: edit_sensor_data_screen(app.sensor_data), 
                  bg_color="#666666", width=8).pack(side="left", padx=10)
    create_button(button_frame, "Continue →", workout_mode_screen).pack(side="left", padx=10)


def edit_sensor_data_screen(current_data):
    """Screen to manually edit sensor data."""
    clear_screen()
    draw_background(selection_bg_image)
    show_title("Edit Body Scan Data", "Adjust the values as needed")

    panel = tk.Frame(root, bg=Config.PANEL_BG, padx=40, pady=30,
                    highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 40, window=panel)

    entries = {}
    data_points = {
        "Body Weight (kg)": (current_data.body_weight_kg, 'body_weight_kg'),
        "Skeletal Muscle (%)": (current_data.skeletal_muscle_percent, 'skeletal_muscle_percent'),
        "Metabolic Rate (kcal)": (current_data.resting_metabolic_rate, 'resting_metabolic_rate'),
        "Body Fat (%)": (current_data.body_fat_percent, 'body_fat_percent'),
    }

    for i, (label, (value, key)) in enumerate(data_points.items()):
        tk.Label(panel, text=label, bg=Config.PANEL_BG, fg=Config.MUTED_TEXT, font=(Config.FONT_FAMILY, 14)).grid(row=i, column=0, sticky="w", pady=8)
        
        entry_var = tk.StringVar(value=f"{value:.1f}")
        entry = tk.Entry(panel, textvariable=entry_var, font=(Config.FONT_FAMILY, 14, "bold"), width=8, bg=Config.PANEL_SECONDARY_BG, fg="white", insertbackground="white", justify="right")
        entry.grid(row=i, column=1, sticky="e", padx=(20, 0))
        entries[key] = entry_var

    def save_edited_data():
        try:
            # Update app's sensor data object from entries
            app.sensor_data.body_weight_kg = float(entries['body_weight_kg'].get())
            app.sensor_data.skeletal_muscle_percent = float(entries['skeletal_muscle_percent'].get())
            app.sensor_data.resting_metabolic_rate = float(entries['resting_metabolic_rate'].get())
            app.sensor_data.body_fat_percent = float(entries['body_fat_percent'].get())
            app.sensor_data.validate() # Re-validate the new data

            logging.info(f"User manually edited sensor data: {app.sensor_data}")
            show_sensor_confirmation() # Go back to confirmation screen

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter valid numbers.\n\nDetails: {e}")

    button_frame = tk.Frame(panel, bg=Config.PANEL_BG)
    button_frame.grid(row=len(data_points), column=0, columnspan=2, pady=(25, 0))
    create_back_button(button_frame, show_sensor_confirmation, "Cancel").pack(side="left", padx=10)
    create_button(button_frame, "Save Changes", save_edited_data).pack(side="left", padx=10)


=======
    create_back_button(button_frame, start_slideshow, "Cancel").pack(side="left", padx=10)
    create_button(button_frame, "Continue →", workout_mode_screen).pack(side="left", padx=10)


>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
# =============================
# USER SELECTIONS
# =============================
def workout_mode_screen():
    """Select workout mode."""
    clear_screen()
    draw_background(selection_bg_image)
    draw_progress_bar(1)
<<<<<<< HEAD
    show_title("Choose Workout Mode", "Select based on your current activity")
=======
    show_title("Choose Workout Mode")
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    
    panel = tk.Frame(root, bg=Config.PANEL_BG, padx=30, pady=30,
                    highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 40, window=panel)
    
<<<<<<< HEAD
    for col, (label, value, icon) in enumerate([
        ("Pre-Workout", 'pre', "⚡"),
        ("Post-Workout", 'post', "🔄")
    ]):
        create_button(panel, label, lambda v=value: select_mode(v), icon=icon).grid(
            row=0, column=col, padx=25
        )
        
    # Add descriptions
    tk.Label(panel, text="For an energy boost before you train", 
             bg=Config.PANEL_BG, fg=Config.MUTED_TEXT, font=(Config.FONT_FAMILY, 11), 
             wraplength=200, justify="center").grid(row=1, column=0, pady=(5,15))
    
    tk.Label(panel, text="To refuel muscles and aid recovery after", 
             bg=Config.PANEL_BG, fg=Config.MUTED_TEXT, font=(Config.FONT_FAMILY, 11), 
             wraplength=200, justify="center").grid(row=1, column=1, pady=(5,15))
    
    create_back_button(panel, show_sensor_confirmation).grid(
        row=2, column=0, columnspan=2, pady=(15, 0)
    )





=======
    for col, (label, value) in enumerate([
        ("Pre-Workout", 'pre'),
        ("Post-Workout", 'post')
    ]):
        create_button(panel, label, lambda v=value: select_mode(v)).grid(
            row=0, column=col, padx=25
        )
    
    create_back_button(panel, show_sensor_confirmation).grid(
        row=1, column=0, columnspan=2, pady=(30, 0)
    )


>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
def select_mode(mode):
    app.mode = mode
    carb_mode_screen()


def carb_mode_screen():
    """Select carb base."""
    clear_screen()
    draw_background(selection_bg_image)
    draw_progress_bar(2)
<<<<<<< HEAD
    show_title("Select Energy Base", "Choose your preferred carbohydrate source")
=======
    show_title("Select Energy Base")
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    
    panel = tk.Frame(root, bg=Config.PANEL_BG, padx=30, pady=30,
                    highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 40, window=panel)
    
<<<<<<< HEAD
    for col, (label, value, icon) in enumerate([
        ("Maltodextrin\n(Fast Energy)", 'maltodextrin', "⚡"),
        ("Pumpkin & Rice\n(Whole Food)", 'pumpkinrice', "🎃")
    ]):
        create_button(panel, label, lambda v=value: select_carb_mode(v), icon=icon).grid(
            row=0, column=col, padx=25
        )
        
    # Add descriptions
    tk.Label(panel, text="Fast-acting carbs for quick energy", 
             bg=Config.PANEL_BG, fg=Config.MUTED_TEXT, font=(Config.FONT_FAMILY, 11), 
             wraplength=200, justify="center").grid(row=1, column=0, pady=(5,15))
    
    tk.Label(panel, text="Slower-releasing, whole-food carbs", 
             bg=Config.PANEL_BG, fg=Config.MUTED_TEXT, font=(Config.FONT_FAMILY, 11), 
             wraplength=200, justify="center").grid(row=1, column=1, pady=(5,15))
    
    create_back_button(panel, workout_mode_screen).grid(
        row=2, column=0, columnspan=2, pady=(15, 0)
=======
    for col, (label, value) in enumerate([
        ("Maltodextrin\n(Fast Energy)", 'maltodextrin'),
        ("Pumpkin & Rice\n(Whole Food)", 'pumpkinrice')
    ]):
        create_button(panel, label, lambda v=value: select_carb_mode(v)).grid(
            row=0, column=col, padx=25
        )
    
    create_back_button(panel, workout_mode_screen).grid(
        row=1, column=0, columnspan=2, pady=(30, 0)
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    )


def select_carb_mode(carb_mode):
    app.carb_mode = carb_mode
    flavour_screen()


def flavour_screen():
    """Select flavour."""
    clear_screen()
    draw_background(selection_bg_image)
    draw_progress_bar(3)
<<<<<<< HEAD
    show_title("Choose Flavour", "Add a natural flavour to your bar")
=======
    show_title("Choose Flavour")
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    
    panel = tk.Frame(root, bg=Config.PANEL_BG, padx=30, pady=30,
                    highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 40, window=panel)
    
    options = [
<<<<<<< HEAD
        ("None", 'none', "🚫"),
        ("Coffee", 'coffee', "☕"),
        ("Chocolate", 'chocolate', "🍫"),
        ("Matcha", 'matcha', "🍵")
    ]
    
    for i, (label, value, icon) in enumerate(options):
        create_button(panel, label, lambda v=value: select_flavour(v), icon=icon).grid(
=======
        ("None", 'none'),
        ("Coffee", 'coffee'),
        ("Chocolate", 'chocolate'),
        ("Matcha", 'matcha')
    ]
    
    for i, (label, value) in enumerate(options):
        create_button(panel, label, lambda v=value: select_flavour(v)).grid(
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
            row=i // 2, column=i % 2, padx=25, pady=15
        )
    
    create_back_button(panel, carb_mode_screen).grid(
        row=2, column=0, columnspan=2, pady=(30, 0)
    )


def select_flavour(flavour):
    app.flavour = flavour
    ask_custom_ingredients()


# =============================
# CUSTOM INGREDIENT SELECTION
# =============================
def ask_custom_ingredients():
    """Ask if user wants to customize ingredients."""
    clear_screen()
    draw_background(selection_bg_image)
    
    draw_progress_bar(4)
<<<<<<< HEAD
    show_title("Refine Your Bar", "Use our AI recommendation or choose your own ingredients")
=======
    show_title("Ingredient Selection", "Do you want to choose specific ingredients?")
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    
    panel = tk.Frame(root, bg=Config.PANEL_BG, padx=40, pady=30,
                    highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 40, window=panel)
    
    tk.Label(
        panel,
<<<<<<< HEAD
        text="Our AI optimizes ingredients for your body composition and goals.\nOr, you can take full control and select them yourself.",
=======
        text="Our AI will recommend the best ingredients\nbased on your body composition.",
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
        bg=Config.PANEL_BG,
        fg="#dddddd",
        font=(Config.FONT_FAMILY, 13),
        justify="center"
    ).pack(pady=20)
    
    btn_frame = tk.Frame(panel, bg=Config.PANEL_BG)
    btn_frame.pack(pady=10)
    
    create_button(btn_frame, "AI Recommendation", 
                 lambda: [setattr(app, 'user_selected_ingredients', None), generate_recommendation()],
<<<<<<< HEAD
                 bg_color=Config.PRIMARY_COLOR, icon="🤖").pack(side="left", padx=10)
    
    create_button(btn_frame, "Choose Ingredients", 
                 show_ingredient_selection,
                 bg_color="#666666", icon="📝").pack(side="left", padx=10)
=======
                 bg_color=Config.PRIMARY_COLOR).pack(side="left", padx=10)
    
    create_button(btn_frame, "Choose Ingredients", 
                 show_ingredient_selection,
                 bg_color="#666666").pack(side="left", padx=10)
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    
    create_back_button(panel, flavour_screen).pack(pady=(20, 0))


<<<<<<< HEAD
def show_ingredient_selection(): # REVAMPED
    """Show ingredient selection screen with descriptions."""
    clear_screen()
    draw_background(selection_bg_image)
    draw_progress_bar(4)
    show_title("Select Ingredients", "Hover over an item to see its benefits")

    # Main container frame
    main_frame = tk.Frame(root, bg=Config.PANEL_BG, padx=20, pady=20,
                         highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 80, window=main_frame, 
                         width=Config.WIDTH * 0.75, height=Config.HEIGHT * 0.6)

    # --- Logic & Vars (Defined early for button access) ---
    ingredients = app.ai_recommender.get_available_ingredients()
    
    # Filter carbs and flavours based on previous selections
    filtered_ingredients = []
    for ing in ingredients:
        # Carb filtering: Only show compatible carbs
        if ing['type'] == 'Carb':
            if app.carb_mode == 'maltodextrin':
                continue  # Skip all carbs in maltodextrin mode
            if app.carb_mode == 'pumpkinrice' and ing['id'] == 'maltodextrin':
                continue  # Skip maltodextrin in whole-food mode

        # Flavour filtering: If a flavour is already chosen, don't show flavour options here
        if ing['type'] == 'Flavour' and app.flavour != 'none':
            continue

        filtered_ingredients.append(ing)
    ingredients = filtered_ingredients

    category_vars = {
        'Protein': tk.StringVar(value=""),
        'Carb': tk.StringVar(value=""),
        'Binder': tk.StringVar(value=""),
        'Flavour': tk.StringVar(value=""),
        'Other': tk.StringVar(value="")
    }

    def submit_selection():
        selected = []
        for var in category_vars.values():
            value = var.get()
            if value: # If not an empty string
                selected.append(value)
        
        if not selected:
            messagebox.showwarning("No Selection", "Please select at least one ingredient or use AI recommendation")
            return
        app.user_selected_ingredients = selected
        generate_recommendation()

    # Left side: Scrollable list of ingredients
    list_container = tk.Frame(main_frame, bg=Config.PANEL_SECONDARY_BG)
    list_container.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    list_canvas = tk.Canvas(list_container, bg=Config.PANEL_SECONDARY_BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(list_container, orient="vertical", command=list_canvas.yview)
    
    list_frame = tk.Frame(list_canvas, bg=Config.PANEL_SECONDARY_BG, padx=10, pady=10)
    
    list_frame.bind(
        "<Configure>",
        lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
    )
    
    list_window = list_canvas.create_window((0, 0), window=list_frame, anchor="nw")
    
    def on_canvas_configure(event):
        list_canvas.itemconfig(list_window, width=event.width)
        
    list_canvas.bind("<Configure>", on_canvas_configure)
    list_canvas.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side="right", fill="y")
    list_canvas.pack(side="left", fill="both", expand=True)

    # --- Touch/Swipe to Scroll ---
    def scroll_start(event):
        # canvasx/y converts screen coordinates to canvas coordinates
        list_canvas.scan_mark(int(list_canvas.canvasx(event.x_root)), int(list_canvas.canvasy(event.y_root)))

    def scroll_move(event):
        list_canvas.scan_dragto(int(list_canvas.canvasx(event.x_root)), int(list_canvas.canvasy(event.y_root)), gain=1)

    def _on_mousewheel(event):
        list_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Bind to the canvas itself, and the frame placed inside it
    list_canvas.bind("<ButtonPress-1>", scroll_start)
    list_canvas.bind("<B1-Motion>", scroll_move)
    list_canvas.bind("<MouseWheel>", _on_mousewheel)
    list_frame.bind("<ButtonPress-1>", scroll_start)
    list_frame.bind("<B1-Motion>", scroll_move)
    list_frame.bind("<MouseWheel>", _on_mousewheel)

    # Right side: Description panel
    desc_frame = tk.Frame(main_frame, bg=Config.PANEL_BG, padx=25, pady=20)
    desc_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    # Buttons at the bottom of the description panel (Packed FIRST to ensure visibility)
    btn_frame = tk.Frame(desc_frame, bg=Config.PANEL_BG)
    btn_frame.pack(side="bottom", fill="x", pady=20)
    create_back_button(btn_frame, ask_custom_ingredients).pack(side="left", padx=10)
    create_button(btn_frame, "Generate Bar", submit_selection, icon="🚀").pack(side="left", padx=10)

    # --- Description Panel Widgets (created once) ---
    desc_title = tk.Label(desc_frame, text="Ingredient Information", bg=Config.PANEL_BG, fg=Config.PRIMARY_COLOR, font=(Config.FONT_FAMILY, 16, "bold"))
    desc_title.pack(anchor="w", pady=(0, 15))

    desc_text = tk.Label(desc_frame, text="Select an ingredient on the left to learn more about it.", 
                         bg=Config.PANEL_BG, fg="white", font=(Config.FONT_FAMILY, 13), 
                         wraplength=int(Config.WIDTH * 0.75 * 0.5 - 50), justify="left", anchor="nw")
    desc_text.pack(anchor="w", fill="x")

    # Image placeholder
    desc_image_label = tk.Label(desc_frame, bg=Config.PANEL_BG)
    desc_image_label.pack(pady=20, anchor="center", expand=True)

    # --- Populate Ingredient List ---
    def update_description(ing_data):
        desc_title.config(text=ing_data['name'])
        desc_text.config(text=ing_data['description'])

        image_file = ing_data.get('image_file')
        photo = None
        if image_file:
            if image_file in app.ingredient_images:
                photo = app.ingredient_images[image_file]
            else:
                try:
                    img_path = Config.ASSETS_DIR / image_file
                    img = Image.open(img_path)
                    img = img.resize((350, 350), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    app.ingredient_images[image_file] = photo # Cache it
                except FileNotFoundError:
                    logging.warning(f"Ingredient image not found: {image_file}")
                    photo = None # No image to show
        
        desc_image_label.config(image=photo)
        desc_image_label.image = photo # Keep reference

    # Group ingredients by type for organized display
=======
def show_ingredient_selection():
    """Show ingredient selection screen."""
    clear_screen()
    draw_background(selection_bg_image)
    
    draw_progress_bar(4)
    show_title("Select Ingredients", "Choose ingredients you want in your bar")
    
    # Get available ingredients
    ingredients = app.ai_recommender.get_available_ingredients()
    
    # Create scrollable frame
    main_frame = tk.Frame(root, bg=Config.PANEL_BG, padx=20, pady=20,
                         highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 50, window=main_frame)
    
    # Checkboxes for ingredients
    selected_vars = {}
    
    # Group by type
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    types = {}
    for ing in ingredients:
        ing_type = ing['type']
        if ing_type not in types:
            types[ing_type] = []
        types[ing_type].append(ing)
<<<<<<< HEAD

    for ing_type in ['Protein', 'Carb', 'Binder', 'Flavour', 'Other']:
        if ing_type not in types: continue
        ing_list = types[ing_type]

        type_label = tk.Label(
            list_frame,
            text=f"{ing_type}:",
            bg=Config.PANEL_SECONDARY_BG,
            fg=Config.PRIMARY_COLOR,
            font=(Config.FONT_FAMILY, 13, "bold")
        )
        type_label.pack(anchor="w", pady=(10, 5))
        type_label.bind("<ButtonPress-1>", scroll_start)
        type_label.bind("<B1-Motion>", scroll_move)
        type_label.bind("<MouseWheel>", _on_mousewheel)

        # Get the shared variable for this category
        category_var = category_vars.get(ing_type)
        if not category_var: continue

        for ing in ing_list:
            rb = tk.Radiobutton(
                list_frame,
                text=ing['name'],
                variable=category_var,
                value=ing['id'],
                indicatoron=0,  # This makes it a button-style radio button
                bg="#33373a",   # Unselected background
                fg="white",
                selectcolor=Config.PRIMARY_COLOR, # Selected background
                activebackground=Config.SECONDARY_COLOR, # Hover background
                activeforeground="black", # Text color on hover
                font=(Config.FONT_FAMILY, 12, "bold"),
                relief="flat",
                padx=20,
                pady=12,
                bd=0,
                justify="left",
                anchor="w",
                command=lambda data=ing: update_description(data)
            )
            rb.pack(fill="x", expand=True, pady=2, padx=5)
            
            # Bind scroll events. We add '+' to not override the default button behavior
            rb.bind("<ButtonPress-1>", scroll_start, add='+')
            rb.bind("<B1-Motion>", scroll_move)
            rb.bind("<MouseWheel>", _on_mousewheel)
=======
    
    row = 0
    for ing_type, ing_list in types.items():
        tk.Label(
            main_frame,
            text=f"{ing_type}:",
            bg=Config.PANEL_BG,
            fg=Config.PRIMARY_COLOR,
            font=(Config.FONT_FAMILY, 12, "bold")
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 5))
        row += 1
        
        for ing in ing_list:
            var = tk.BooleanVar()
            selected_vars[ing['id']] = var
            
            cb = tk.Checkbutton(
                main_frame,
                text=ing['name'],
                variable=var,
                bg=Config.PANEL_BG,
                fg="white",
                selectcolor="#2a2a2a",
                activebackground=Config.PANEL_BG,
                activeforeground="white",
                font=(Config.FONT_FAMILY, 11)
            )
            cb.grid(row=row, column=0, columnspan=2, sticky="w", pady=2)
            row += 1
    
    # Submit button
    def submit_selection():
        selected = [ing_id for ing_id, var in selected_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("No Selection", "Please select at least one ingredient or use AI recommendation")
            return
        app.user_selected_ingredients = selected
        generate_recommendation()
    
    create_button(main_frame, "Generate Bar", submit_selection).grid(
        row=row, column=0, columnspan=2, pady=20
    )
    
    create_back_button(main_frame, ask_custom_ingredients).grid(
        row=row+1, column=0, columnspan=2, pady=(0, 20)
    )

>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86

# =============================
# AI RECOMMENDATION
# =============================
<<<<<<< HEAD
def animate_ai_processing(step=0):
    """Animate a rotating spinner for AI."""
    canvas.delete("loading_anim")
    
    cx, cy = Config.WIDTH // 2, Config.HEIGHT // 2
    radius = 60
    num_dots = 12
    
    for i in range(num_dots):
        angle = (i * (360 / num_dots)) + (step * 8)
        rad = math.radians(angle)
        
        x = cx + radius * math.cos(rad)
        y = cy + radius * math.sin(rad)
        
        # Size modulation for dynamic effect
        size = 5 + 3 * math.sin(math.radians(angle * 3))
        
        canvas.create_oval(x-size, y-size, x+size, y+size, 
                           fill=Config.PRIMARY_COLOR, outline="", tags="loading_anim")

    app.loading_animation_job = root.after(30, animate_ai_processing, step + 1)

=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
def generate_recommendation():
    """Generate AI-powered ingredient recommendation."""
    clear_screen()
    draw_background(selection_bg_image)
    
    canvas.create_text(
<<<<<<< HEAD
        Config.WIDTH // 2, Config.HEIGHT // 2 - 100,
=======
        Config.WIDTH // 2, Config.HEIGHT // 2 - 30,
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
        text="🤖 AI Analyzing...",
        fill="white",
        font=(Config.FONT_FAMILY, 24, "bold")
    )
    
    canvas.create_text(
<<<<<<< HEAD
        Config.WIDTH // 2, Config.HEIGHT // 2 + 100,
=======
        Config.WIDTH // 2, Config.HEIGHT // 2 + 20,
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
        text="Optimizing ingredients for your body composition",
        fill="#dddddd",
        font=(Config.FONT_FAMILY, 13)
    )
    
<<<<<<< HEAD
    animate_ai_processing()
=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    root.update()
    root.after(2000, calculate_formulation)


def calculate_formulation():
    """Calculate final formulation using AI - FIXED VERSION."""
<<<<<<< HEAD
    # Stop animation
    if app.loading_animation_job:
        root.after_cancel(app.loading_animation_job)
        app.loading_animation_job = None

=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    try:
        app.final_recommendation = app.ai_recommender.recommend_ingredients(
            app.sensor_data,
            app.mode,
            app.carb_mode,
            app.flavour,
            app.user_selected_ingredients
        )
        
        # NEW: Check if formulation actually failed
        if app.final_recommendation['validation_status'] == 'FAIL':
            error_msg = "Unable to create safe formulation with selected options."
            if 'errors' in app.final_recommendation:
                error_msg += "\n\nIssues:\n" + "\n".join(app.final_recommendation['errors'][:3])
            show_error(error_msg)
            logging.error(f"Formulation failed validation: {app.final_recommendation.get('errors', [])}")
            return
        
        show_results()
        
    except Exception as e:
        logging.error(f"Error generating recommendation: {e}", exc_info=True)
        show_error(f"System error: {str(e)}\n\nPlease try different selections or restart.")


# =============================
# MAINTENANCE MODE
# =============================
def show_pin_entry():
    """Show PIN entry screen for maintenance mode."""
    app.slideshow_running = False
    if app.inactivity_timer:
        root.after_cancel(app.inactivity_timer)
        app.inactivity_timer = None
        
    clear_screen()
    # Use a dark solid background
    canvas.create_rectangle(0, 0, Config.WIDTH, Config.HEIGHT, fill="#1a1a1a")
    
    show_title("🔒 Security Check")
    
    panel = tk.Frame(root, bg="black", padx=40, pady=30, 
                    highlightbackground="#666666", highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2, window=panel)
    
    # PIN Display
    pin_var = tk.StringVar()
    pin_display = tk.Label(panel, textvariable=pin_var, font=("Courier", 32, "bold"), 
                          bg="#111111", fg=Config.PRIMARY_COLOR, width=8, relief="sunken")
    pin_display.grid(row=0, column=0, columnspan=3, pady=(0, 30), ipady=10)
    
    current_pin = []
    
    def update_display():
        pin_var.set(" ".join("•" * len(current_pin)))
        
    def add_digit(digit):
        if len(current_pin) < 4:
            current_pin.append(str(digit))
            update_display()
            if len(current_pin) == 4:
                root.after(200, check_pin)
    
    def check_pin():
        if "".join(current_pin) == "1234":
            show_maintenance_mode()
        else:
            messagebox.showerror("Access Denied", "Incorrect PIN")
            current_pin.clear()
            update_display()
            
    def clear_pin():
        current_pin.clear()
        update_display()

    # Keypad
    keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'C', '0', '←']
    for i, key in enumerate(keys):
        cmd = lambda k=key: clear_pin() if k == 'C' else (start_slideshow() if k == '←' else add_digit(k))
        btn_bg = "#ff4444" if key == '←' else ("#444444" if key == 'C' else "#333333")
        
        tk.Button(panel, text=key, font=(Config.FONT_FAMILY, 18, "bold"),
                 width=5, height=2, bg=btn_bg, fg="white", activebackground="#555555",
                 relief="flat", command=cmd).grid(row=(i//3)+1, column=i%3, padx=5, pady=5)


def show_maintenance_mode():
    """Show hidden maintenance screen."""
    app.slideshow_running = False
    if app.inactivity_timer:
        root.after_cancel(app.inactivity_timer)
        app.inactivity_timer = None
        
    clear_screen()
    # Use a dark solid background
    canvas.create_rectangle(0, 0, Config.WIDTH, Config.HEIGHT, fill="#1a1a1a")
    
    show_title("🛠️ Maintenance Mode")
    
    panel = tk.Frame(root, bg="black", padx=20, pady=20, 
                    highlightbackground="#666666", highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2, window=panel, width=800, height=500)
    
    # System Stats
    stats_frame = tk.Frame(panel, bg="black")
    stats_frame.pack(fill="x", pady=10)
    
    tk.Label(stats_frame, text="System Status: ONLINE", fg=Config.PRIMARY_COLOR, bg="black", font=(Config.FONT_FAMILY, 12)).pack(anchor="w")
    tk.Label(stats_frame, text=f"Screen Resolution: {Config.WIDTH}x{Config.HEIGHT}", fg="white", bg="black", font=(Config.FONT_FAMILY, 12)).pack(anchor="w")
    
    # Log Viewer
    tk.Label(panel, text="Recent Logs:", fg="white", bg="black", font=(Config.FONT_FAMILY, 12, "bold")).pack(anchor="w", pady=(20, 5))
    
    log_text = tk.Text(panel, height=12, bg="#111111", fg="#cccccc", font=("Consolas", 10), relief="flat")
    log_text.pack(fill="both", expand=True)
    
    # Read last 20 lines of log
    try:
        with open('fitfuel_station.log', 'r') as f:
            lines = f.readlines()
            last_lines = lines[-20:]
            log_text.insert("1.0", "".join(last_lines))
    except Exception:
        log_text.insert("1.0", "No log file found.")
    
    log_text.config(state="disabled")
    
    # Actions
    btn_frame = tk.Frame(panel, bg="black")
    btn_frame.pack(pady=20)
    
    def clear_logs():
        if messagebox.askyesno("Clear Logs", "Are you sure you want to clear the system logs?"):
            try:
                with open('fitfuel_station.log', 'w') as f:
                    f.write("Log cleared by user.\n")
                
                log_text.config(state="normal")
                log_text.delete("1.0", "end")
                log_text.insert("1.0", "Log cleared by user.\n")
                log_text.config(state="disabled")
            except Exception as e:
                messagebox.showerror("Error", f"Could not clear logs: {e}")

<<<<<<< HEAD
=======
    create_button(btn_frame, "Exit App", lambda: root.destroy(), bg_color="#ff4444", width=15).pack(side="left", padx=5)
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    create_button(btn_frame, "Clear Logs", clear_logs, bg_color="#4444ff", width=15).pack(side="left", padx=5)
    create_button(btn_frame, "Return", start_slideshow, width=15).pack(side="left", padx=5)


# =============================
# RESULTS
# =============================
def show_results():
    """Display final formulation results."""
    clear_screen()
    draw_background(selection_bg_image)
    
    draw_progress_bar(5)
    show_title("✅ Your Custom Bar Ready!")
    
    result = app.final_recommendation
    
<<<<<<< HEAD
    # Safety check for None result
    if result is None:
        logging.error("show_results called with None result")
        show_error("No recommendation data found. Please try again.")
        return
    
=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    # Summary
    summary_frame = tk.Frame(root, bg=Config.PANEL_SECONDARY_BG, padx=20, pady=15,
                            highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, 220, window=summary_frame)
    
    tk.Label(
        summary_frame,
        text=f"50g Bar  |  {len(result['selected_ingredients'])} Ingredients  |  {result['validation_status']}",
        bg=Config.PANEL_SECONDARY_BG,
        fg=Config.PRIMARY_COLOR,
        font=(Config.FONT_FAMILY, 13, "bold")
    ).pack()
    
    # Ingredients list
    ing_frame = tk.Frame(root, bg=Config.PANEL_BG, padx=30, pady=20,
                        highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 60, window=ing_frame)
    
    tk.Label(
        ing_frame,
        text="Ingredients (grams):",
        bg=Config.PANEL_BG,
        fg="white",
        font=(Config.FONT_FAMILY, 14, "bold")
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
    
    # Show top 10 ingredients
<<<<<<< HEAD
    sorted_ings = sorted(result['formulation_grams'].items(), key=lambda x: -x[1])[:10]
    for i, (ing, grams) in enumerate(sorted_ings):
=======
    sorted_ings = sorted(result['formulation_grams'].items(), key=lambda x: -x[1])
    for i, (ing, grams) in enumerate(sorted_ings[:10]):
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
        ing_name = ing.replace('_', ' ').title()
        # Ingredient Name
        tk.Label(
            ing_frame,
            text=ing_name,
<<<<<<< HEAD
            bg=Config.PANEL_BG, # Changed from PANEL_BG
=======
            bg=Config.PANEL_BG,
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
            fg="#dddddd",
            font=(Config.FONT_FAMILY, 11),
        ).grid(row=i+1, column=0, sticky="w", pady=2)
        # Ingredient Amount
        tk.Label(
            ing_frame,
            text=f"{grams:.2f}g",
<<<<<<< HEAD
            bg=Config.PANEL_BG, # Changed from PANEL_BG
=======
            bg=Config.PANEL_BG,
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
            fg="white",
            font=(Config.FONT_FAMILY, 11, "bold"),
        ).grid(row=i+1, column=1, sticky="e", padx=(40, 0))
    
<<<<<<< HEAD
    # Allergen preview removed to make it a separate screen as requested.
    # It will be shown in full in the next step.
    
    # Calculate pricing
    # pricing = PricingCalculator.calculate_price(
    #     result['formulation_percent'],
    #     customization_type='ai_optimized'
    # )
    pricing = {'total': 0.00} # Dummy pricing since payment is disabled
    app.pricing = pricing
    
    # Continue to allergen disclosure then payment
    btn_frame = tk.Frame(root, bg=Config.PANEL_BG)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT - 80, window=btn_frame)

    create_back_button(
        btn_frame,
        ask_custom_ingredients,
        "← Back"
    ).pack(side="left", padx=10)

    def on_continue():
        try:
            show_allergen_disclosure(result, pricing)
        except Exception as e:
            logging.error(f"Failed to open allergen screen: {e}", exc_info=True)
            show_error(f"Error opening allergen screen: {e}")

    create_button(
        btn_frame,
        "Continue →",
        on_continue
    ).pack(side="left", padx=10)

    logging.info(f"Results displayed - {len(result['selected_ingredients'])} ingredients")


def show_allergen_disclosure(result, pricing):
    """
    Show allergen disclosure screen.
    User must acknowledge before proceeding.
    """
    try:
        logging.info("Displaying Allergen Disclosure Screen")
        clear_screen()
        draw_background(selection_bg_image)
        
        # Title
        canvas.create_text(
            Config.WIDTH // 2, 70,
            text="⚠️ ALLERGEN INFORMATION",
            fill=Config.PRIMARY_COLOR,
            font=(Config.FONT_FAMILY, Config.TITLE_FONT_SIZE, "bold")
        )
        
        canvas.create_text(
            Config.WIDTH // 2, 110,
            text="Please review before purchasing",
            fill="#dddddd",
            font=(Config.FONT_FAMILY, 13)
        )
        
        # Get allergen information
        allergen_info = AllergenAnalyzer.get_allergens(result['formulation_percent'])
        
        # Main panel
        panel = tk.Frame(root, bg=Config.PANEL_BG, padx=40, pady=30,
                        highlightbackground=Config.PRIMARY_COLOR, highlightthickness=2)
        canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 20, window=panel)
        
        # ─────────────────────────────────────────────────────
        # Section 1: Contains (Allergens Present)
        # ─────────────────────────────────────────────────────
        if allergen_info['present_allergens']:
            tk.Label(
                panel,
                text="⚠️  THIS BAR CONTAINS:",
                bg=Config.PANEL_BG,
                fg="#ff9800",  # Orange warning color
                font=(Config.FONT_FAMILY, 14, "bold"),
                anchor="w"
            ).pack(fill="x", pady=(0, 5))
            
            contains_frame = tk.Frame(panel, bg=Config.PANEL_SECONDARY_BG, padx=15, pady=10)
            contains_frame.pack(fill="x", pady=(0, 15))
            
            for allergen in allergen_info['present_allergens']:
                tk.Label(
                    contains_frame,
                    text=f"• {allergen}",
                    bg=Config.PANEL_SECONDARY_BG,
                    fg="white",
                    font=(Config.FONT_FAMILY, 12),
                    anchor="w"
                ).pack(fill="x", pady=2)
        else:
            tk.Label(
                panel,
                text="✅ No common allergens detected",
                bg=Config.PANEL_BG,
                fg="#4CAF50",
                font=(Config.FONT_FAMILY, 14, "bold")
            ).pack(pady=(0, 15))
        
        # ─────────────────────────────────────────────────────
        # Section 2: Free From
        # ─────────────────────────────────────────────────────
        tk.Label(
            panel,
            text="✓  FREE FROM:",
            bg=Config.PANEL_BG,
            fg="#4CAF50",
            font=(Config.FONT_FAMILY, 14, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        free_frame = tk.Frame(panel, bg=Config.PANEL_SECONDARY_BG, padx=15, pady=10)
        free_frame.pack(fill="x", pady=(0, 15))
        
        # Display free-from allergens in 3 columns
        num_cols = 3
        for i, allergen in enumerate(allergen_info['free_from']):
            row = i // num_cols
            col = i % num_cols
            
            tk.Label(
                free_frame,
                text=f"• {allergen}",
                bg=Config.PANEL_SECONDARY_BG,
                fg="#aaaaaa",
                font=(Config.FONT_FAMILY, 11),
                anchor="w"
            ).grid(row=row, column=col, sticky="w", padx=10, pady=2)
        
        # ─────────────────────────────────────────────────────
        # Section 3: Special Warnings
        # ─────────────────────────────────────────────────────
        if allergen_info['warnings']:
            tk.Frame(panel, bg=Config.SEPARATOR_COLOR, height=1).pack(fill="x", pady=10)
            
            tk.Label(
                panel,
                text="⚠️  IMPORTANT NOTICES:",
                bg=Config.PANEL_BG,
                fg="#ff9800",
                font=(Config.FONT_FAMILY, 13, "bold"),
                anchor="w"
            ).pack(fill="x", pady=(0, 5))
            
            for warning in allergen_info['warnings']:
                warning_frame = tk.Frame(panel, bg="#332200", padx=10, pady=5)
                warning_frame.pack(fill="x", pady=3)
                
                tk.Label(
                    warning_frame,
                    text=f"• {warning}",
                    bg="#332200",
                    fg="#ffcc00",
                    font=(Config.FONT_FAMILY, 11),
                    anchor="w",
                    wraplength=500,
                    justify="left"
                ).pack(fill="x")
        
        # ─────────────────────────────────────────────────────
        # Acknowledgment Checkbox
        # ─────────────────────────────────────────────────────
        acknowledged = tk.BooleanVar(value=False)
        # Attach to panel to prevent garbage collection
        panel.acknowledged = acknowledged
        
        check_frame = tk.Frame(panel, bg=Config.PANEL_BG)
        check_frame.pack(pady=(20, 10))
        
        checkbox = tk.Checkbutton(
            check_frame,
            text="I have read and understand the allergen information above",
            variable=acknowledged,
            bg=Config.PANEL_BG,
            fg="white",
            selectcolor=Config.PANEL_SECONDARY_BG,
            activebackground=Config.PANEL_BG,
            activeforeground="white",
            font=(Config.FONT_FAMILY, 12),
            cursor="hand2"
        )
        checkbox.pack()
        
        # ─────────────────────────────────────────────────────
        # Buttons
        # ─────────────────────────────────────────────────────
        btn_frame = tk.Frame(panel, bg=Config.PANEL_BG)
        btn_frame.pack(pady=(10, 0))
        
        create_back_button(
            btn_frame,
            show_results
        ).pack(side="left", padx=10)
        
        def on_finish():
            try:
                if not acknowledged.get():
                    messagebox.showwarning(
                        "Acknowledgment Required",
                        "Please confirm that you have read the allergen information."
                    )
                    return
                
                # Return to landing page
                start_slideshow()
            except Exception as e:
                logging.error(f"Error in on_finish: {e}", exc_info=True)
                show_error(f"Error proceeding: {e}")
        
        create_button(
            btn_frame,
            "Finish",
            on_finish
        ).pack(side="left", padx=10)

    except Exception as e:
        logging.error(f"Error displaying allergen disclosure: {e}", exc_info=True)
        show_error(f"Error loading allergen info: {e}")


def show_error(message):
    """Show error message - ENHANCED VERSION."""
    # Stop any running animations
    if app.loading_animation_job:
        root.after_cancel(app.loading_animation_job)
        app.loading_animation_job = None

=======
    # Status message
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT - 60,
        text="✓ Dispensing your bar...",
        fill=Config.PRIMARY_COLOR,
        font=(Config.FONT_FAMILY, 14, "bold")
    )
    
    root.after(5000, start_slideshow)
    
    logging.info(f"Results displayed - {len(result['selected_ingredients'])} ingredients")


def show_error(message):
    """Show error message - ENHANCED VERSION."""
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    clear_screen()
    draw_background(selection_bg_image)
    
    # Error icon
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 - 100,
        text="⚠️",
        fill="#ff6b6b",
        font=(Config.FONT_FAMILY, 48)
    )
    
    # Error title
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 - 30,
        text="Oops! Something went wrong",
        fill="white",
        font=(Config.FONT_FAMILY, 22, "bold")
    )
    
    # Error message
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 40,
        text=message,
        fill="#dddddd",
        font=(Config.FONT_FAMILY, 14),
        width=600,
        justify="center"
    )
    
    # Buttons panel
    retry_panel = tk.Frame(root, bg=Config.PANEL_BG)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 150, window=retry_panel)
    
    # NEW: Give user options
    create_button(retry_panel, "Try Again", start_slideshow).grid(row=0, column=0, padx=10)
    create_button(retry_panel, "Change Selections", workout_mode_screen, bg_color="#666666").grid(row=0, column=1, padx=10)
    create_button(retry_panel, "🛠️", show_pin_entry, bg_color="#333333", width=4).grid(row=0, column=2, padx=10)


# =============================
# START APP
# =============================
def main():
    logging.info("FitFuel Vending Machine started (streamlined version)")
    print("\n" + "="*60)
    print("  FITFUEL VENDING MACHINE")
    print("="*60)
    print("\nStarted successfully!")
    print("Expected CSV format: sensor_data.csv")
    print("Columns: body_weight_kg, skeletal_muscle_percent,")
    print("         resting_metabolic_rate, body_fat_percent, timestamp")
    print("="*60 + "\n")
    
    # Bind slideshow elements to stop_slideshow instead of global canvas
    canvas.tag_bind("background", "<Button-1>", stop_slideshow)
    canvas.tag_bind("overlay", "<Button-1>", stop_slideshow)
    canvas.tag_bind("pulse", "<Button-1>", stop_slideshow)
    
    # Bind global events for inactivity tracking
    root.bind_all("<Button-1>", reset_inactivity_timer)
    root.bind_all("<Key>", reset_inactivity_timer)
<<<<<<< HEAD
    root.bind_all("<Key>", reset_inactivity_timer)
=======
>>>>>>> 1c173a5094a15923e865d946c0126d3a4fdc3c86
    
    start_slideshow()
    root.mainloop()


if __name__ == "__main__":
    main()