"""
FitFuel Vending Machine - Smart Launcher
Automatically handles CSV creation and launches vending machine
"""

import sys
import os
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='fitfuel_station.log'
)


def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        from PIL import Image
        return True
    except ImportError:
        print("\n❌ ERROR: Required package 'Pillow' not found")
        print("\nPlease install it with:")
        print("   pip install Pillow")
        return False


def check_csv_file():
    """Check if sensor_data.csv exists."""
    return Path('sensor_data.csv').exists()


def create_csv_menu():
    """Show menu to create CSV file."""
    print("\n" + "="*60)
    print("  SENSOR DATA NOT FOUND")
    print("="*60)
    print("\nNo sensor_data.csv file found.")
    print("How would you like to create test data?\n")
    print("1. Quick Default (70kg, 35% muscle, 1650 RMR, 22% fat)")
    print("2. Choose Preset Profile")
    print("3. Enter Custom Values")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    return choice


def create_quick_default():
    """Create CSV with quick default values."""
    from sensor_data_reader import SensorDataReader
    
    reader = SensorDataReader()
    reader.create_sample_csv()
    
    print("\n✅ Created sensor_data.csv with default values:")
    print("   Weight: 75.5kg")
    print("   Muscle: 35.2%")
    print("   RMR: 1650 kcal/day")
    print("   Fat: 22.3%")


def create_preset():
    """Create CSV from preset profile."""
    print("\n" + "="*60)
    print("  PRESET PROFILES")
    print("="*60)
    
    presets = {
        '1': ('beginner_male', 75, 32, 1700, 25, "Beginner Male"),
        '2': ('beginner_female', 60, 28, 1400, 32, "Beginner Female"),
        '3': ('athletic_male', 80, 42, 2000, 15, "Athletic Male"),
        '4': ('athletic_female', 65, 38, 1750, 20, "Athletic Female"),
        '5': ('advanced_male', 85, 45, 2200, 12, "Advanced Male"),
        '6': ('average', 70, 35, 1650, 22, "Average User")
    }
    
    print("\nAvailable Profiles:")
    for key, (_, w, m, r, f, name) in presets.items():
        print(f"{key}. {name:20s} ({w}kg, {m}% muscle, {r} RMR, {f}% fat)")
    
    choice = input("\nSelect profile (1-6): ").strip()
    
    if choice in presets:
        _, weight, muscle, rmr, fat, name = presets[choice]
        
        from create_test_data import write_csv
        write_csv(weight, muscle, rmr, fat)
        
        print(f"\n✅ Created sensor_data.csv with {name} profile")
        print(f"   Weight: {weight}kg, Muscle: {muscle}%, RMR: {rmr} kcal/day, Fat: {fat}%")
        return True
    else:
        print("❌ Invalid choice")
        return False


def create_custom():
    """Create CSV with custom values."""
    print("\n" + "="*60)
    print("  CUSTOM VALUES")
    print("="*60)
    print("\nEnter body composition values:")
    print("(Press Enter to use default value shown in brackets)\n")
    
    try:
        weight = input("Body Weight (kg) [75]: ").strip() or "75"
        muscle = input("Skeletal Muscle (%) [35]: ").strip() or "35"
        rmr = input("Resting Metabolic Rate (kcal/day) [1650]: ").strip() or "1650"
        fat = input("Body Fat (%) [22]: ").strip() or "22"
        
        # Convert to float
        weight = float(weight)
        muscle = float(muscle)
        rmr = float(rmr)
        fat = float(fat)
        
        # Validate ranges
        if not (30 <= weight <= 200):
            print("⚠️  Warning: Weight should be 30-200 kg")
        if not (10 <= muscle <= 60):
            print("⚠️  Warning: Muscle should be 10-60%")
        if not (800 <= rmr <= 3500):
            print("⚠️  Warning: RMR should be 800-3500 kcal/day")
        if not (5 <= fat <= 60):
            print("⚠️  Warning: Body fat should be 5-60%")
        
        # Create CSV
        from create_test_data import write_csv
        write_csv(weight, muscle, rmr, fat)
        
        print("\n✅ Created sensor_data.csv with custom values:")
        print(f"   Weight: {weight}kg")
        print(f"   Muscle: {muscle}%")
        print(f"   RMR: {rmr} kcal/day")
        print(f"   Fat: {fat}%")
        return True
        
    except ValueError:
        print("❌ Invalid input. Please enter numbers only.")
        return False


def launch_vending_machine():
    """Launch the vending machine application."""
    print("\n" + "="*60)
    print("  LAUNCHING FITFUEL VENDING MACHINE")
    print("="*60)
    print("\nStarting application...")
    print("Touch the screen to begin!\n")
    
    try:
        from fitfuel_ui import main as vending_main
        vending_main()
    except Exception as e:
        logging.error(f"Error launching vending machine: {e}")
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure all required files are present:")
        print("  - config.py")
        print("  - sensor_data_reader.py")
        print("  - ai_ingredient_recommender.py")
        print("  - fitfuel_ui.py")
        sys.exit(1)


def main():
    """Main launcher function."""
    print("\n" + "🏋️" * 30)
    print("  FITFUEL VENDING MACHINE - LAUNCHER")
    print("🏋️" * 30)
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ Dependencies OK")
    
    # Check for CSV file
    print("\n🔍 Checking for sensor data...")
    if not check_csv_file():
        print("⚠️  No sensor_data.csv found")
        
        # Show menu to create CSV
        while True:
            choice = create_csv_menu()
            
            if choice == '1':
                create_quick_default()
                break
            elif choice == '2':
                if create_preset():
                    break
            elif choice == '3':
                if create_custom():
                    break
            elif choice == '4':
                print("\nExiting...")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please try again.")
    else:
        print("✅ Found sensor_data.csv")
        
        # Show what's in the file
        try:
            from sensor_data_reader import SensorDataReader
            reader = SensorDataReader()
            data = reader.read_latest_data()
            print(f"\nCurrent sensor data:")
            print(f"  Weight: {data.body_weight_kg}kg")
            print(f"  Muscle: {data.skeletal_muscle_percent}%")
            print(f"  RMR: {data.resting_metabolic_rate} kcal/day")
            print(f"  Fat: {data.body_fat_percent}%")
            
            # Ask if user wants to use existing or create new
            print("\n" + "-"*60)
            use_existing = input("\nUse this data? (y/n) [y]: ").strip().lower()
            
            if use_existing == 'n':
                while True:
                    choice = create_csv_menu()
                    
                    if choice == '1':
                        create_quick_default()
                        break
                    elif choice == '2':
                        if create_preset():
                            break
                    elif choice == '3':
                        if create_custom():
                            break
                    elif choice == '4':
                        print("\nExiting...")
                        sys.exit(0)
                    else:
                        print("❌ Invalid choice. Please try again.")
        except Exception as e:
            print(f"⚠️  Could not read existing CSV: {e}")
            print("Creating new CSV file...")
            create_quick_default()
    
    # Launch vending machine
    input("\nPress Enter to launch vending machine...")
    launch_vending_machine()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Launcher error: {e}", exc_info=True)
        print(f"\n❌ Unexpected error: {e}")
        print("Check fitfuel_station.log for details")
        sys.exit(1)