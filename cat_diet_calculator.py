def get_basic_info():
    """Get basic cat information from user input."""
    print("\n=== Cat Calorie Calculator ===\n")
    
    # Get weight with validation
    while True:
        weight_str = input("Enter your cat's weight in pounds: ").strip()
        if weight_str.startswith('-'):
            print("Weight must be greater than 0.")
            continue
        try:
            weight_lbs = float(weight_str)
            if weight_lbs <= 0:
                print("Weight must be greater than 0.")
                continue
            weight_kg = weight_lbs * 0.453592
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Get age with validation
    while True:
        age_str = input("Enter your cat's age in years: ").strip()
        if age_str.startswith('-'):
            print("Age cannot be negative.")
            continue
        try:
            age_years = float(age_str)
            if age_years < 0:
                print("Age cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Get spay/neuter status
    while True:
        spay_neuter = input("Is your cat spayed or neutered? (yes/no): ").lower()
        if spay_neuter in ['yes', 'no', 'y', 'n']:
            is_spayed_neutered = spay_neuter.startswith('y')
            break
        print("Please enter 'yes' or 'no'.")
    
    # Get body condition
    while True:
        print("\nSelect your cat's body condition:")
        print("1. Underweight")
        print("2. Ideal weight")
        print("3. Overweight")
        condition = input("Enter number (1-3): ")
        if condition in ['1', '2', '3']:
            body_condition = {
                '1': 'underweight',
                '2': 'ideal',
                '3': 'overweight'
            }[condition]
            break
        print("Please enter 1, 2, or 3.")
    
    return weight_kg, age_years, is_spayed_neutered, body_condition

def get_food_info():
    """Get information about food proportions and caloric density."""
    # Get wet/dry food ratio
    while True:
        wet_input = input("\nWhat percentage of the diet should be wet food? (0-100): ").strip()
        try:
            if '%' in wet_input:
                print("Please do not include the % sign - enter just the number.")
                continue
            wet_percent = int(wet_input)
            if 0 <= wet_percent <= 100:
                break
            print("Please enter a number between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get optional caloric density for wet food
    print("\nDo you know the caloric density of your wet food?")
    print("(Usually listed as kcal/kg or kcal/can on the label)")
    while True:
        response = input("Enter calories per gram, or press Enter to use standard value (0.9 kcal/g): ").strip()
        if response == "":
            wet_kcal_per_g = 0.9  # Default value
            break
        try:
            value = float(response)
            if value <= 0:
                print("Caloric density must be greater than 0.")
                continue
            wet_kcal_per_g = value
            break
        except ValueError:
            print("Please enter a valid number or press Enter to skip.")
    
    # Get optional caloric density for dry food
    print("\nDo you know the caloric density of your dry food?")
    print("(Usually listed as kcal/kg or kcal/cup on the label)")
    while True:
        response = input("Enter calories per gram, or press Enter to use standard value (4.0 kcal/g): ").strip()
        if response == "":
            dry_kcal_per_g = 4.0  # Default value
            break
        try:
            value = float(response)
            if value <= 0:
                print("Caloric density must be greater than 0.")
                continue
            dry_kcal_per_g = value
            break
        except ValueError:
            print("Please enter a valid number or press Enter to skip.")
    
    return wet_percent, wet_kcal_per_g, dry_kcal_per_g

def calculate_cat_calories(weight_kg, age_years, is_spayed_neutered=True, body_condition="ideal", 
                         wet_food_percentage=50, wet_kcal_per_g=0.9, dry_kcal_per_g=4.0):
    """Calculate daily caloric needs for cats with mixed wet and dry food diet."""
    # Base Resting Energy Requirement (RER)
    RER = 70 * (weight_kg ** 0.75)
    
    # Age factor adjustments
    age_factors = {
        "kitten": 2.5,      # < 1 year
        "adult": 1.0,       # 1-7 years
        "senior": 0.9       # > 7 years
    }
    
    if age_years < 1:
        age_category = "kitten"
    elif age_years > 7:
        age_category = "senior"
    else:
        age_category = "adult"
    
    # Spay/neuter adjustment
    spay_neuter_factor = 0.8 if is_spayed_neutered else 1.0
    
    # Body condition adjustments
    body_condition_factors = {
        "underweight": 1.2,
        "ideal": 1.0,
        "overweight": 0.8
    }
    
    # Calculate daily calories
    daily_calories = (
        RER *
        age_factors[age_category] *
        spay_neuter_factor *
        body_condition_factors[body_condition]
    )
    
    # Calculate wet and dry food portions
    wet_calories = daily_calories * (wet_food_percentage / 100)
    dry_calories = daily_calories * ((100 - wet_food_percentage) / 100)
    
    wet_food_grams = wet_calories / wet_kcal_per_g
    dry_food_grams = dry_calories / dry_kcal_per_g
    
    meals_per_day = 2 if age_years >= 1 else 3
    
    return {
        "daily_calories": round(daily_calories),
        "wet_food": {
            "calories": round(wet_calories),
            "grams_per_day": round(wet_food_grams),
            "grams_per_meal": round(wet_food_grams / meals_per_day),
            "kcal_per_g": wet_kcal_per_g
        },
        "dry_food": {
            "calories": round(dry_calories),
            "grams_per_day": round(dry_food_grams),
            "grams_per_meal": round(dry_food_grams / meals_per_day),
            "kcal_per_g": dry_kcal_per_g
        },
        "meals_per_day": meals_per_day,
        "age_category": age_category
    }

def convert_to_volume(grams, food_type="dry"):
    """
    Convert grams to cups and tablespoons.
    Approximate conversions:
    - Dry food: 1 cup ≈ 120g, 1 tablespoon ≈ 7.5g
    - Wet food: 1 cup ≈ 250g, 1 tablespoon ≈ 15g
    """
    if food_type == "dry":
        cups = grams / 120
        tbsp = grams / 7.5
    else:  # wet food
        cups = grams / 250
        tbsp = grams / 15
    
    return cups, tbsp

def display_results(results):
    """Display calculation results in a formatted way."""
    print("\n=== Feeding Recommendations ===")
    print(f"\nTotal daily calories: {results['daily_calories']} kcal")
    print(f"Recommended meals per day: {results['meals_per_day']}")
    print(f"Age category: {results['age_category'].capitalize()}")
    
    # Convert wet food measurements
    wet_cups_daily, wet_tbsp_daily = convert_to_volume(results['wet_food']['grams_per_day'], "wet")
    wet_cups_per_meal, wet_tbsp_per_meal = convert_to_volume(results['wet_food']['grams_per_meal'], "wet")
    
    print("\nWet Food:")
    print(f"- Daily calories: {results['wet_food']['calories']} kcal")
    print(f"- Food caloric density: {results['wet_food']['kcal_per_g']:.2f} kcal/g")
    print("- Amount per day:")
    print(f"  • {results['wet_food']['grams_per_day']} grams")
    print(f"  • {wet_cups_daily:.2f} cups")
    print(f"  • {wet_tbsp_daily:.1f} tablespoons")
    print("- Amount per meal:")
    print(f"  • {results['wet_food']['grams_per_meal']} grams")
    print(f"  • {wet_cups_per_meal:.2f} cups")
    print(f"  • {wet_tbsp_per_meal:.1f} tablespoons")
    
    # Convert dry food measurements
    dry_cups_daily, dry_tbsp_daily = convert_to_volume(results['dry_food']['grams_per_day'], "dry")
    dry_cups_per_meal, dry_tbsp_per_meal = convert_to_volume(results['dry_food']['grams_per_meal'], "dry")
    
    print("\nDry Food:")
    print(f"- Daily calories: {results['dry_food']['calories']} kcal")
    print(f"- Food caloric density: {results['dry_food']['kcal_per_g']:.2f} kcal/g")
    print("- Amount per day:")
    print(f"  • {results['dry_food']['grams_per_day']} grams")
    print(f"  • {dry_cups_daily:.2f} cups")
    print(f"  • {dry_tbsp_daily:.1f} tablespoons")
    print("- Amount per meal:")
    print(f"  • {results['dry_food']['grams_per_meal']} grams")
    print(f"  • {dry_cups_per_meal:.2f} cups")
    print(f"  • {dry_tbsp_per_meal:.1f} tablespoons")

def main():
    """Main program function."""
    try:
        # Get all user inputs in two steps
        weight_kg, age_years, is_spayed_neutered, body_condition = get_basic_info()
        wet_percent, wet_kcal_per_g, dry_kcal_per_g = get_food_info()
        
        # Calculate results
        results = calculate_cat_calories(
            weight_kg=weight_kg,
            age_years=age_years,
            is_spayed_neutered=is_spayed_neutered,
            body_condition=body_condition,
            wet_food_percentage=wet_percent,
            wet_kcal_per_g=wet_kcal_per_g,
            dry_kcal_per_g=dry_kcal_per_g
        )
        
        # Display results
        display_results(results)
        
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()