"""
FitFuel Vending Machine - Streamlined Version
CSV sensor input → User selections → AI recommendations → 50g bar
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import itertools
import logging

from config import Config
from sensor_data_reader import SensorDataReader
from ai_ingredient_recommender import AIIngredientRecommender

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
    # Destroy all child widgets (Frames) to prevent memory leaks
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()
    canvas.delete("all")


def draw_background(image):
    """Draw background image - FIXED to prevent memory leak."""
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
        text=text,
        fill="white",
        font=(Config.FONT_FAMILY, Config.TITLE_FONT_SIZE, "bold")
    )
    if subtitle:
        canvas.create_text(
            Config.WIDTH // 2, 110,
            text=subtitle,
            fill="#dddddd",
            font=(Config.FONT_FAMILY, 14)
        )


def create_button(parent, text, command, bg_color=None, width=None):
    bg = bg_color or Config.PRIMARY_COLOR
    # Hover color: lighter if primary, else slightly lighter grey
    hover_bg = Config.SECONDARY_COLOR if bg == Config.PRIMARY_COLOR else "#888888"
    
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
    return btn


def create_back_button(parent, command, text="← Back"):
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
    return btn


def draw_progress_bar(step_index):
    """Draw the progress stepper at the top of the screen."""
    steps = Config.STEPS
    total_steps = len(steps)
    
    w = Config.WIDTH
    margin_x = 200
    y = 150
    available_w = w - (2 * margin_x)
    step_gap = available_w / (total_steps - 1)
    
    for i, step_name in enumerate(steps):
        x = margin_x + (i * step_gap)
        
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


def overlay_landing_text():
    canvas.delete("overlay")
    canvas.create_text(
        Config.WIDTH // 2, 170,
        text="FITFUEL STATION",
        fill="white",
        font=(Config.FONT_FAMILY, 36, "bold"),
        tags="overlay"
    )
    canvas.create_text(
        Config.WIDTH // 2, 220,
        text="AI-Powered Personalized Nutrition",
        fill="#dddddd",
        font=(Config.FONT_FAMILY, 18),
        tags="overlay"
    )


def pulse_text():
    if not app.slideshow_running:
        return
    
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


def stop_slideshow(event=None):
    """Stop slideshow and read sensor data."""
    if not app.slideshow_running:
        return
    app.slideshow_running = False
    canvas.delete("pulse")
    read_sensor_data()


# =============================
# SENSOR DATA READING
# =============================
def read_sensor_data():
    """Read body composition from CSV file."""
    clear_screen()
    draw_background(selection_bg_image)
    
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 - 50,
        text="📊 Reading Sensor Data...",
        fill="white",
        font=(Config.FONT_FAMILY, 24, "bold")
    )
    
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 10,
        text="Please step on the scale",
        fill="#dddddd",
        font=(Config.FONT_FAMILY, 14)
    )
    
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 50,
        text="●  ●  ●",
        fill=Config.PRIMARY_COLOR,
        font=(Config.FONT_FAMILY, 20)
    )
    
    root.update()
    root.after(2000, load_sensor_data)


def load_sensor_data():
    """Load data from CSV file."""
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
    create_back_button(button_frame, start_slideshow, "Cancel").pack(side="left", padx=10)
    create_button(button_frame, "Continue →", workout_mode_screen).pack(side="left", padx=10)


# =============================
# USER SELECTIONS
# =============================
def workout_mode_screen():
    """Select workout mode."""
    clear_screen()
    draw_background(selection_bg_image)
    draw_progress_bar(1)
    show_title("Choose Workout Mode")
    
    panel = tk.Frame(root, bg=Config.PANEL_BG, padx=30, pady=30,
                    highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 40, window=panel)
    
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


def select_mode(mode):
    app.mode = mode
    carb_mode_screen()


def carb_mode_screen():
    """Select carb base."""
    clear_screen()
    draw_background(selection_bg_image)
    draw_progress_bar(2)
    show_title("Select Energy Base")
    
    panel = tk.Frame(root, bg=Config.PANEL_BG, padx=30, pady=30,
                    highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 40, window=panel)
    
    for col, (label, value) in enumerate([
        ("Maltodextrin\n(Fast Energy)", 'maltodextrin'),
        ("Pumpkin & Rice\n(Whole Food)", 'pumpkinrice')
    ]):
        create_button(panel, label, lambda v=value: select_carb_mode(v)).grid(
            row=0, column=col, padx=25
        )
    
    create_back_button(panel, workout_mode_screen).grid(
        row=1, column=0, columnspan=2, pady=(30, 0)
    )


def select_carb_mode(carb_mode):
    app.carb_mode = carb_mode
    flavour_screen()


def flavour_screen():
    """Select flavour."""
    clear_screen()
    draw_background(selection_bg_image)
    draw_progress_bar(3)
    show_title("Choose Flavour")
    
    panel = tk.Frame(root, bg=Config.PANEL_BG, padx=30, pady=30,
                    highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 40, window=panel)
    
    options = [
        ("None", 'none'),
        ("Coffee", 'coffee'),
        ("Chocolate", 'chocolate'),
        ("Matcha", 'matcha')
    ]
    
    for i, (label, value) in enumerate(options):
        create_button(panel, label, lambda v=value: select_flavour(v)).grid(
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
    show_title("Ingredient Selection", "Do you want to choose specific ingredients?")
    
    panel = tk.Frame(root, bg=Config.PANEL_BG, padx=40, pady=30,
                    highlightbackground=Config.PRIMARY_COLOR, highlightthickness=1)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 40, window=panel)
    
    tk.Label(
        panel,
        text="Our AI will recommend the best ingredients\nbased on your body composition.",
        bg=Config.PANEL_BG,
        fg="#dddddd",
        font=(Config.FONT_FAMILY, 13),
        justify="center"
    ).pack(pady=20)
    
    btn_frame = tk.Frame(panel, bg=Config.PANEL_BG)
    btn_frame.pack(pady=10)
    
    create_button(btn_frame, "AI Recommendation", 
                 lambda: [setattr(app, 'user_selected_ingredients', None), generate_recommendation()],
                 bg_color=Config.PRIMARY_COLOR).pack(side="left", padx=10)
    
    create_button(btn_frame, "Choose Ingredients", 
                 show_ingredient_selection,
                 bg_color="#666666").pack(side="left", padx=10)
    
    create_back_button(panel, flavour_screen).pack(pady=(20, 0))


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
    types = {}
    for ing in ingredients:
        ing_type = ing['type']
        if ing_type not in types:
            types[ing_type] = []
        types[ing_type].append(ing)
    
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


# =============================
# AI RECOMMENDATION
# =============================
def generate_recommendation():
    """Generate AI-powered ingredient recommendation."""
    clear_screen()
    draw_background(selection_bg_image)
    
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 - 30,
        text="🤖 AI Analyzing...",
        fill="white",
        font=(Config.FONT_FAMILY, 24, "bold")
    )
    
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 20,
        text="Optimizing ingredients for your body composition",
        fill="#dddddd",
        font=(Config.FONT_FAMILY, 13)
    )
    
    root.update()
    root.after(2000, calculate_formulation)


def calculate_formulation():
    """Calculate final formulation using AI - FIXED VERSION."""
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

    create_button(btn_frame, "Exit App", lambda: root.destroy(), bg_color="#ff4444", width=15).pack(side="left", padx=5)
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
    sorted_ings = sorted(result['formulation_grams'].items(), key=lambda x: -x[1])
    for i, (ing, grams) in enumerate(sorted_ings[:10]):
        ing_name = ing.replace('_', ' ').title()
        # Ingredient Name
        tk.Label(
            ing_frame,
            text=ing_name,
            bg=Config.PANEL_BG,
            fg="#dddddd",
            font=(Config.FONT_FAMILY, 11),
        ).grid(row=i+1, column=0, sticky="w", pady=2)
        # Ingredient Amount
        tk.Label(
            ing_frame,
            text=f"{grams:.2f}g",
            bg=Config.PANEL_BG,
            fg="white",
            font=(Config.FONT_FAMILY, 11, "bold"),
        ).grid(row=i+1, column=1, sticky="e", padx=(40, 0))
    
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
    
    start_slideshow()
    root.mainloop()


if __name__ == "__main__":
    main()