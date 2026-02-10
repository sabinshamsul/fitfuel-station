"""
Manual CSV Data Creator
Easily create test sensor data without real sensors
"""

import csv
from datetime import datetime


def write_csv(weight, muscle, rmr, fat):
    """Write data to CSV file."""
    with open('sensor_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['body_weight_kg', 'skeletal_muscle_percent', 
                        'resting_metabolic_rate', 'body_fat_percent', 'timestamp'])
        writer.writerow([weight, muscle, rmr, fat, datetime.now().isoformat()])


def create_csv_interactive():
    """Interactive mode - prompts for values."""
    print("\n" + "="*60)
    print("  FITFUEL - MANUAL TEST DATA CREATOR")
    print("="*60)
    print("\nEnter body composition values:")
    print("(Press Enter for default values shown in brackets)")
    
    # Get input with defaults
    weight = input("\nBody Weight (kg) [75]: ").strip() or "75"
    muscle = input("Skeletal Muscle (%) [35]: ").strip() or "35"
    rmr = input("Resting Metabolic Rate (kcal/day) [1650]: ").strip() or "1650"
    fat = input("Body Fat (%) [22]: ").strip() or "22"
    
    # Convert to float and validate
    try:
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
        write_csv(weight, muscle, rmr, fat)
        
        print("\n✅ CSV file created successfully!")
        print("📄 File: sensor_data.csv")
        print(f"\nValues saved:")
        print(f"  Body Weight:        {weight} kg")
        print(f"  Skeletal Muscle:    {muscle}%")
        print(f"  RMR:                {rmr} kcal/day")
        print(f"  Body Fat:           {fat}%")
        print("\n✅ Ready to run vending machine!")
        print("   Run: python main.py")
        
    except ValueError:
        print("❌ Error: Please enter valid numbers")
        return


def create_csv_preset(preset_name):
    """Create CSV from preset profile."""
    presets = {
        'beginner_male': (75, 32, 1700, 25),
        'beginner_female': (60, 28, 1400, 32),
        'athletic_male': (80, 42, 2000, 15),
        'athletic_female': (65, 38, 1750, 20),
        'advanced_male': (85, 45, 2200, 12),
        'average': (70, 35, 1650, 22)
    }
    
    if preset_name in presets:
        weight, muscle, rmr, fat = presets[preset_name]
        write_csv(weight, muscle, rmr, fat)
        
        print(f"\n✅ Created CSV with {preset_name.replace('_', ' ').title()} profile")
        print(f"   Weight: {weight}kg, Muscle: {muscle}%, RMR: {rmr}kcal, Fat: {fat}%")
        return True
    return False


def show_presets():
    """Show available presets."""
    print("\n" + "="*60)
    print("  AVAILABLE PRESETS")
    print("="*60)
    
    presets = [
        ("beginner_male", "75kg, 32% muscle, 1700 RMR, 25% fat"),
        ("beginner_female", "60kg, 28% muscle, 1400 RMR, 32% fat"),
        ("athletic_male", "80kg, 42% muscle, 2000 RMR, 15% fat"),
        ("athletic_female", "65kg, 38% muscle, 1750 RMR, 20% fat"),
        ("advanced_male", "85kg, 45% muscle, 2200 RMR, 12% fat"),
        ("average", "70kg, 35% muscle, 1650 RMR, 22% fat")
    ]
    
    for i, (name, desc) in enumerate(presets, 1):
        print(f"\n{i}. {name.replace('_', ' ').title()}")
        print(f"   {desc}")
    
    print("\n" + "="*60)


def main():
    """Main menu."""
    print("\n" + "🔬" * 30)
    print("  FITFUEL TEST DATA CREATOR")
    print("🔬" * 30)
    
    print("\nChoose an option:")
    print("1. Enter custom values (interactive)")
    print("2. Use preset profile")
    print("3. Quick default (70kg, 35% muscle, 1650 RMR, 22% fat)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        create_csv_interactive()
    
    elif choice == '2':
        show_presets()
        print("\nEnter preset number (1-6) or name:")
        preset_input = input("> ").strip().lower()
        
        # Map number to name
        preset_map = {
            '1': 'beginner_male',
            '2': 'beginner_female',
            '3': 'athletic_male',
            '4': 'athletic_female',
            '5': 'advanced_male',
            '6': 'average'
        }
        
        preset_name = preset_map.get(preset_input, preset_input)
        
        if create_csv_preset(preset_name):
            print("\n✅ Ready to run vending machine!")
            print("   Run: python main.py")
        else:
            print("❌ Invalid preset name")
    
    elif choice == '3':
        write_csv(70, 35, 1650, 22)
        print("\n✅ Created CSV with default values")
        print("   Weight: 70kg, Muscle: 35%, RMR: 1650kcal, Fat: 22%")
        print("\n✅ Ready to run vending machine!")
        print("   Run: python main.py")
    
    else:
        print("❌ Invalid choice")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()