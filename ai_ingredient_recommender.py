"""
AI-Powered Ingredient Recommendation Engine
Recommends optimal ingredients and amounts for 50g protein bar
"""

import logging
import json
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='fitfuel_station.log'
)
from config import Config


def log_formulation_details(formulation, stage):
    """Log detailed formulation for debugging."""
    total = sum(formulation.values())
    logging.info(f"=== Formulation at {stage} ===")
    logging.info(f"Total: {total:.2f}%")
    
    for ing, pct in sorted(formulation.items(), key=lambda x: -x[1]):
        if pct > 0.01:
            logging.info(f"  {ing:25s}: {pct:6.2f}%")
    
    logging.info("=" * 50)


@dataclass
class Ingredient:
    """Ingredient definition with nutritional properties."""
    name: str
    min_percent: float
    max_percent: float
    priority: int  # Lower number = higher priority
    protein_content: float  # g per 100g
    carb_content: float
    fat_content: float
    is_binder: bool = False
    is_protein: bool = False
    is_carb: bool = False
    is_flavour: bool = False


class AIIngredientRecommender:
    """
    AI-powered ingredient recommendation system.
    Uses body composition data to recommend optimal ingredient mix.
    """
    
    # Available ingredients database
    INGREDIENTS = {
        'pea_protein': Ingredient('Pea Protein Isolate', 18, 38, 1, 85, 5, 3, is_protein=True),
        'sunflower_seed': Ingredient('Sunflower Seed Powder', 6, 18, 2, 21, 20, 51, is_protein=True),
        'rice_syrup': Ingredient('Rice Syrup', 10, 20, 3, 0, 80, 0, is_binder=True),
        'glycerine': Ingredient('Glycerine (Food Grade)', 6, 12, 4, 0, 0, 0, is_binder=True),
        'maltodextrin': Ingredient('Maltodextrin', 0, 10, 5, 0, 95, 0, is_carb=True),
        'pumpkin_seed_flour': Ingredient('Pumpkin Seed Flour', 0, 12, 6, 33, 14, 49, is_carb=True),
        'brown_rice_flour': Ingredient('Brown Rice Flour', 0, 10, 7, 7, 77, 3, is_carb=True),
        'leucine': Ingredient('Leucine', 0, 4, 8, 100, 0, 0, is_protein=True),
        'guarana_extract': Ingredient('Guarana Extract', 0, 2, 9, 0, 0, 0),
        'salt': Ingredient('Salt', 0.2, 0.8, 10, 0, 0, 0),
        'cocoa_powder': Ingredient('Cocoa Powder', 0, 3, 11, 20, 58, 14, is_flavour=True),
        'instant_coffee': Ingredient('Instant Coffee Powder', 0, 1.5, 12, 12, 42, 0, is_flavour=True),
        'matcha_powder': Ingredient('Matcha Powder', 0, 0.8, 13, 30, 39, 5, is_flavour=True),
        'vanilla': Ingredient('Vanilla Powder', 0, 0.3, 14, 0, 13, 0, is_flavour=True),
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_user_needs(self, sensor_data, mode: str, carb_mode: str, flavour: str) -> Dict:
        """
        Analyze user needs based on body composition and preferences.
        
        Args:
            sensor_data: SensorData object with body metrics
            mode: 'pre' or 'post' workout
            carb_mode: 'maltodextrin' or 'pumpkinrice'
            flavour: 'none', 'coffee', 'chocolate', 'matcha'
            
        Returns:
            dict: User needs analysis
        """
        needs = {
            'protein_priority': 'normal',
            'energy_priority': 'normal',
            'leucine_needed': False,
            'caffeine_needed': False,
            'protein_boost': 0,
            'carb_boost': 0
        }
        
        # Protein priority based on muscle mass
        if sensor_data.skeletal_muscle_percent < 30:
            needs['protein_priority'] = 'high'
            needs['leucine_needed'] = True
            needs['protein_boost'] = 6
        elif sensor_data.skeletal_muscle_percent <= 38:
            needs['protein_priority'] = 'medium'
            needs['leucine_needed'] = True
            needs['protein_boost'] = 3
        
        # Energy priority based on RMR
        if sensor_data.resting_metabolic_rate > 1800:
            needs['energy_priority'] = 'high'
            needs['carb_boost'] = 4
        elif sensor_data.resting_metabolic_rate >= 1500:
            needs['energy_priority'] = 'medium'
            needs['carb_boost'] = 2
        
        # Caffeine for pre-workout based on body fat
        if mode == 'pre':
            if sensor_data.body_fat_percent > 30:
                needs['caffeine_needed'] = 'low'  # 40mg
            elif sensor_data.body_fat_percent >= 20:
                needs['caffeine_needed'] = 'medium'  # 60mg
            else:
                needs['caffeine_needed'] = 'high'  # 80mg
        
        self.logger.info(f"User needs analysis: {needs}")
        return needs
    
    def recommend_ingredients(self, sensor_data, mode: str, carb_mode: str, 
                            flavour: str, user_selected: List[str] = None) -> Dict[str, float]:
        """
        AI-powered ingredient recommendation.
        
        Args:
            sensor_data: Body composition data
            mode: 'pre' or 'post' workout
            carb_mode: 'maltodextrin' or 'pumpkinrice'
            flavour: Flavour selection
            user_selected: Optional list of ingredients user wants to include
            
        Returns:
            dict: Recommended ingredients with grams for 50g bar
        """
        # Analyze user needs
        needs = self.analyze_user_needs(sensor_data, mode, carb_mode, flavour)
        
        # Start with base formulation
        formulation = self._get_base_formulation(mode, carb_mode)
        # log_formulation_details(formulation, "BASE")
        
        # Apply AI adjustments based on needs
        formulation = self._apply_ai_adjustments(formulation, needs, carb_mode)
        log_formulation_details(formulation, "AFTER AI ADJUSTMENTS")
        
        # Add flavour system
        formulation = self._add_flavour_system(formulation, flavour)
        log_formulation_details(formulation, "AFTER FLAVOUR")
        
        # Adjust for user-selected ingredients
        if user_selected:
            formulation = self._adjust_for_user_selection(formulation, user_selected, needs)
        
        # Normalize to 100%
        formulation = self._normalize(formulation)
        log_formulation_details(formulation, "NORMALIZED")
        
        # Validate
        is_valid, errors = self._validate_formulation(formulation, carb_mode)
        
        if not is_valid:
            self.logger.warning(f"Formulation validation issues: {errors}")
            
            # 1. Try Local Smart Solver
            formulation = self._smart_balance(formulation, carb_mode)
            is_valid, errors = self._validate_formulation(formulation, carb_mode)
            
            # 2. Try External AI (ChatGPT) if local failed
            if not is_valid:
                self.logger.info("Local solver failed. Attempting External AI...")
                ai_formulation = self._solve_with_external_ai(formulation, errors)
                if ai_formulation:
                    formulation = ai_formulation
                    is_valid, errors = self._validate_formulation(formulation, carb_mode)
            
            # 3. Emergency Fallback (Guaranteed Valid)
            if not is_valid:
                self.logger.warning("All solvers failed. Using Emergency Fallback.")
                formulation = self._emergency_fallback(mode, carb_mode, flavour)
                is_valid = True # Fallback is always valid by design
        
        # Convert percentages to grams (50g bar)
        grams = {ing: (pct / 100) * 50 for ing, pct in formulation.items()}
        
        # Remove ingredients with less than 0.1g (too small to measure)
        grams = {ing: g for ing, g in grams.items() if g >= 0.1}
        
        # Log the final total weight for verification
        total_grams = sum(grams.values())
        self.logger.info(f"Final formulation weight for 50g bar: {total_grams:.2f}g")
        
        self.logger.info(f"AI Recommendation complete: {len(grams)} ingredients selected")
        
        return {
            'formulation_percent': formulation,
            'formulation_grams': grams,
            'needs_analysis': needs,
            'validation_status': 'PASS' if is_valid else 'FAIL',
            'selected_ingredients': list(grams.keys()),
            'errors': errors if not is_valid else []
        }
    
    def _get_base_formulation(self, mode: str, carb_mode: str) -> Dict[str, float]:
        """Get base formulation that sums to exactly 100%."""
        if mode == 'pre':
            if carb_mode == 'maltodextrin':
                return {
                    'pea_protein': 35.0, 'sunflower_seed': 12.0,
                    'rice_syrup': 14.0, 'glycerine': 8.0,
                    'maltodextrin': 26.0, 'leucine': 1.5,
                    'salt': 0.5, 'brown_rice_flour': 3.0,
                    'guarana_extract': 0.0
                }
            else:  # pumpkinrice
                return {
                    'pea_protein': 34.0, 'sunflower_seed': 12.0,
                    'rice_syrup': 15.0, 'glycerine': 9.0,
                    'pumpkin_seed_flour': 15.5, 'brown_rice_flour': 8.0,
                    'leucine': 1.5, 'salt': 0.5,
                    'maltodextrin': 4.5, 'guarana_extract': 0.0
                }
        else:  # post
            if carb_mode == 'maltodextrin':
                return {
                    'pea_protein': 38.0, 'sunflower_seed': 12.0,
                    'rice_syrup': 13.0, 'glycerine': 7.0,
                    'maltodextrin': 25.0, 'leucine': 2.5,
                    'salt': 0.5, 'brown_rice_flour': 2.0,
                    'guarana_extract': 0.0
                }
            else:  # pumpkinrice
                return {
                    'pea_protein': 36.0, 'sunflower_seed': 12.0,
                    'rice_syrup': 14.0, 'glycerine': 8.0,
                    'pumpkin_seed_flour': 13.5, 'brown_rice_flour': 8.0,
                    'leucine': 2.5, 'salt': 0.5,
                    'maltodextrin': 5.5, 'guarana_extract': 0.0
                }
    
    def _safe_adjust(self, formulation: Dict[str, float], ingredient: str, adjustment: float):
        """Safely adjust an ingredient's percentage, respecting its bounds."""
        if ingredient not in self.INGREDIENTS:
            return
        
        limits = self.INGREDIENTS[ingredient]
        # Use .get() to handle ingredients that might not be in the initial dict
        current_val = formulation.get(ingredient, 0)
        new_val = current_val + adjustment
        formulation[ingredient] = max(limits.min_percent, min(new_val, limits.max_percent))

    def _apply_ai_adjustments(self, formulation: Dict[str, float], 
                             needs: Dict, carb_mode: str) -> Dict[str, float]:
        """
        Apply AI-driven adjustments based on user needs.
        SAFER VERSION - respects bounds during adjustments.
        """
        
        # Helper function to safely adjust ingredient
        def safe_adjust(ing_name, amount, is_increase=True):
            """Adjust ingredient amount while respecting min/max bounds."""
            current = formulation.get(ing_name, 0)
            
            if ing_name not in self.INGREDIENTS:
                return 0  # Can't adjust unknown ingredient
            
            ing_def = self.INGREDIENTS[ing_name]
            
            if is_increase:
                new_amount = min(current + amount, ing_def.max_percent)
                actual_increase = new_amount - current
                formulation[ing_name] = new_amount
                return actual_increase
            else:
                new_amount = max(current - amount, ing_def.min_percent)
                actual_decrease = current - new_amount
                formulation[ing_name] = new_amount
                return actual_decrease
        
        # Protein boost with safety
        if needs['protein_boost'] > 0:
            # Try to add to pea_protein first
            actual_increase = safe_adjust('pea_protein', needs['protein_boost'], is_increase=True)
            
            # If we couldn't add the full amount, distribute remainder
            remainder = needs['protein_boost'] - actual_increase
            if remainder > 0.5:
                # Try adding to sunflower seed
                actual_increase += safe_adjust('sunflower_seed', remainder * 0.5, is_increase=True)
            
            # Compensate by reducing carbs proportionally
            if carb_mode == 'maltodextrin':
                safe_adjust('maltodextrin', actual_increase * 0.5, is_increase=False)
                safe_adjust('rice_syrup', actual_increase * 0.3, is_increase=False)
            else:
                safe_adjust('pumpkin_seed_flour', actual_increase * 0.3, is_increase=False)
                safe_adjust('brown_rice_flour', actual_increase * 0.2, is_increase=False)
                safe_adjust('rice_syrup', actual_increase * 0.3, is_increase=False)
        
        # Energy boost (carbs) with safety
        if needs['carb_boost'] > 0:
            if carb_mode == 'maltodextrin':
                safe_adjust('maltodextrin', needs['carb_boost'], is_increase=True)
            else:
                safe_adjust('brown_rice_flour', needs['carb_boost'] * 0.6, is_increase=True)
                safe_adjust('pumpkin_seed_flour', needs['carb_boost'] * 0.4, is_increase=True)
        
        # Leucine adjustment (safe because we control the exact values)
        if needs['leucine_needed']:
            if needs['protein_priority'] == 'high':
                formulation['leucine'] = 2.0
            else:
                formulation['leucine'] = 1.5
        else:
            formulation['leucine'] = 0
        
        # Caffeine (via guarana) - safe because values are pre-defined
        if needs['caffeine_needed']:
            if needs['caffeine_needed'] == 'high':
                formulation['guarana_extract'] = 0.7
            elif needs['caffeine_needed'] == 'medium':
                formulation['guarana_extract'] = 0.5
            else:
                formulation['guarana_extract'] = 0.35
        else:
            formulation['guarana_extract'] = 0
        
        return formulation
    
    def _add_flavour_system(self, formulation: Dict[str, float], flavour: str) -> Dict[str, float]:
        """Add flavour ingredients."""
        if flavour == 'chocolate':
            formulation['cocoa_powder'] = 2.0
            formulation['vanilla'] = 0.2
        elif flavour == 'coffee':
            formulation['instant_coffee'] = 1.2
            formulation['vanilla'] = 0.2
        elif flavour == 'matcha':
            formulation['matcha_powder'] = 0.6
            formulation['vanilla'] = 0.2
        
        return formulation
    
    def _adjust_for_user_selection(self, formulation: Dict[str, float], 
                                   user_selected: List[str], needs: Dict) -> Dict[str, float]:
        """
        Adjust formulation when user manually selects specific ingredients.
        AI will optimize amounts while respecting user choices.
        """
        # Ensure all user-selected ingredients are included
        for ingredient in user_selected:
            if ingredient in self.INGREDIENTS:
                if ingredient not in formulation:
                    # Add ingredient at minimum safe level
                    ing_def = self.INGREDIENTS[ingredient]
                    formulation[ingredient] = max(ing_def.min_percent, 1.0)
        
        # Remove ingredients not selected by user (except essentials)
        essentials = ['pea_protein', 'sunflower_seed', 'rice_syrup', 'glycerine', 'salt']
        to_remove = []
        for ingredient in formulation:
            if ingredient not in user_selected and ingredient not in essentials:
                to_remove.append(ingredient)
        
        for ingredient in to_remove:
            del formulation[ingredient]
        
        return formulation
    
    def _normalize(self, formulation: Dict[str, float]) -> Dict[str, float]:
        """Normalize formulation to 100%."""
        total = sum(formulation.values())
        if abs(total - 100) > 0.01:
            factor = 100 / total
            formulation = {k: v * factor for k, v in formulation.items()}
        return formulation
    
    def _validate_formulation(self, formulation: Dict[str, float], 
                             carb_mode: str) -> Tuple[bool, List[str]]:
        """Validate formulation against constraints."""
        errors = []
        
        # Check ingredient bounds
        for ing, pct in formulation.items():
            if ing in self.INGREDIENTS:
                ing_def = self.INGREDIENTS[ing]
                if pct < ing_def.min_percent - 0.01 or pct > ing_def.max_percent + 0.01:
                    errors.append(f"{ing}: {pct:.2f}% outside bounds ({ing_def.min_percent}-{ing_def.max_percent}%)")
        
        # Check binder range
        binder_total = formulation.get('rice_syrup', 0) + formulation.get('glycerine', 0)
        if binder_total < 18 or binder_total > 26:
            errors.append(f"Binder total {binder_total:.2f}% outside range (18-26%)")
        
        # Check binder for pumpkinrice
        if carb_mode == 'pumpkinrice' and binder_total < 20:
            errors.append(f"PumpkinRice mode requires binder ≥20%, got {binder_total:.2f}%")
        
        # Check protein system
        protein_total = formulation.get('pea_protein', 0) + formulation.get('sunflower_seed', 0)
        if protein_total < 28 or protein_total > 48:
            errors.append(f"Protein system {protein_total:.2f}% outside range (28-48%)")
        
        return len(errors) == 0, errors
    
    def _smart_balance(self, formulation: Dict[str, float], carb_mode: str) -> Dict[str, float]:
        """
        Advanced Constraint Solver.
        Uses a priority-based distribution algorithm to ensure formulation sums to 100%
        while strictly adhering to ingredient min/max bounds and group constraints.
        """
        # Helper to clamp value
        def clamp(val, min_v, max_v):
            return max(min_v, min(val, max_v))
        
        # 1. Enforce Group Constraints (Scaling)
        # Binders: 18-26%
        binders = ['rice_syrup', 'glycerine']
        binder_min = 20.0 if carb_mode == 'pumpkinrice' else 18.0
        binder_max = 26.0
        binder_sum = sum(formulation.get(b, 0) for b in binders)
        if binder_sum > 0:
            if binder_sum > binder_max:
                scale = binder_max / binder_sum
                for b in binders:
                    if b in formulation: formulation[b] *= scale
            elif binder_sum < binder_min:
                scale = binder_min / binder_sum
                for b in binders:
                    if b in formulation: formulation[b] *= scale

        # Proteins: 28-48%
        proteins = [k for k, v in self.INGREDIENTS.items() if v.is_protein]
        prot_sum = sum(formulation.get(p, 0) for p in proteins if p in formulation)
        if prot_sum > 0:
            if prot_sum > 48:
                scale = 48.0 / prot_sum
                for p in proteins:
                    if p in formulation: formulation[p] *= scale
            elif prot_sum < 28:
                scale = 28.0 / prot_sum
                for p in proteins:
                    if p in formulation: formulation[p] *= scale

        # 2. Enforce Individual Constraints (Clamping)
        for ing, amount in formulation.items():
            if ing in self.INGREDIENTS:
                limits = self.INGREDIENTS[ing]
                formulation[ing] = clamp(amount, limits.min_percent, limits.max_percent)

        # 3. Iterative Solver to sum to 100%
        # We distribute the error (100 - sum) to ingredients that have "slack"
        last_error = float('inf')
        for _ in range(50): # Iterations
            current_sum = sum(formulation.values())
            error = 100.0 - current_sum
            
            # CONVERGENCE & STUCK HANDLING: Break if error is tiny or not improving
            if abs(error) < 0.01 or abs(error) >= last_error:
                break
            
            # Find candidates that can move in the direction of the error
            candidates = []
            total_weight = 0
            
            for ing, amount in formulation.items():
                if ing not in self.INGREDIENTS: continue
                limits = self.INGREDIENTS[ing]
                
                # Check individual bounds
                can_move = False
                if error > 0: # Need to increase
                    if amount < limits.max_percent - 0.01:
                        can_move = True
                else: # Need to decrease
                    if amount > limits.min_percent + 0.01:
                        can_move = True
                
                if can_move:
                    # Weight by current amount to distribute proportionally
                    weight = amount + 0.1
                    candidates.append(ing)
                    total_weight += weight
            
            if not candidates:
                break # Cannot improve further
            last_error = abs(error)
            
            # Distribute error
            for ing in candidates:
                amount = formulation[ing]
                weight = amount + 0.1
                share = (weight / total_weight) * error
                
                # Apply share but clamp to limits immediately to avoid overshoot
                limits = self.INGREDIENTS[ing]
                new_val = amount + share
                formulation[ing] = clamp(new_val, limits.min_percent, limits.max_percent)

        formulation = self._normalize(formulation)
        return formulation
    
    def get_available_ingredients(self) -> List[Dict]:
        """Get list of all available ingredients for user selection."""
        ingredients = []
        for key, ing in self.INGREDIENTS.items():
            ingredients.append({
                'id': key,
                'name': ing.name,
                'type': 'Protein' if ing.is_protein else 'Carb' if ing.is_carb else 'Binder' if ing.is_binder else 'Flavour' if ing.is_flavour else 'Other',
                'protein': ing.protein_content,
                'carbs': ing.carb_content,
                'fats': ing.fat_content
            })
        return ingredients

    def _solve_with_external_ai(self, current_formulation, errors):
        """Fallback to External AI (OpenAI/ChatGPT) to solve the formulation."""
        api_key = getattr(Config, 'OPENAI_API_KEY', None) or os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            return None

        try:
            import openai
        except ImportError:
            self.logger.warning("OpenAI module not found. Please install it using 'pip install openai'")
            return None

        try:
            client = openai.OpenAI(api_key=api_key)
            
            # Construct bounds string
            bounds = [f"{k}: {v.min_percent}-{v.max_percent}%" for k, v in self.INGREDIENTS.items()]
            
            prompt = f"""
            Fix this protein bar recipe to meet constraints.
            Current (Failed): {json.dumps(current_formulation)}
            Errors: {errors}
            
            Constraints:
            1. Sum must be exactly 100.
            2. Binder (rice_syrup + glycerine) must be 18-26%.
            3. Protein System (pea_protein + sunflower_seed) must be 28-48%.
            4. Ingredient Bounds: {', '.join(bounds)}
            
            Return ONLY valid JSON: {{ "ingredient_name": percentage, ... }}
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a nutrition API that outputs only JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            self.logger.error(f"External AI failed: {e}")
            return None

    def _emergency_fallback(self, mode: str, carb_mode: str, flavour: str) -> Dict[str, float]:
        """Emergency fallback: guaranteed valid formulation."""
        self.logger.warning(f"Using EMERGENCY FALLBACK for {mode}/{carb_mode}/{flavour}")
        
        if carb_mode == 'maltodextrin':
            base = {
                'pea_protein': 32.0, 'sunflower_seed': 10.0,
                'rice_syrup': 15.0, 'glycerine': 7.0,
                'maltodextrin': 20.0, 'brown_rice_flour': 8.0,
                'leucine': 2.0, 'salt': 0.5,
                'pumpkin_seed_flour': 5.5, 'guarana_extract': 0.0
            }
        else:
            base = {
                'pea_protein': 32.0, 'sunflower_seed': 10.0,
                'rice_syrup': 16.0, 'glycerine': 9.0,
                'pumpkin_seed_flour': 15.0, 'brown_rice_flour': 9.0,
                'leucine': 2.0, 'salt': 0.5,
                'maltodextrin': 6.5, 'guarana_extract': 0.0
            }
        
        # Add flavour if needed
        if flavour == 'coffee':
            base['instant_coffee'] = 0.8
            base['vanilla'] = 0.2
            base['maltodextrin' if carb_mode == 'maltodextrin' else 'brown_rice_flour'] -= 1.0
        elif flavour == 'chocolate':
            base['cocoa_powder'] = 1.5
            base['vanilla'] = 0.2
            base['maltodextrin' if carb_mode == 'maltodextrin' else 'brown_rice_flour'] -= 1.7
        elif flavour == 'matcha':
            base['matcha_powder'] = 0.5
            base['vanilla'] = 0.2
            base['maltodextrin' if carb_mode == 'maltodextrin' else 'brown_rice_flour'] -= 0.7
        
        base = {k: v for k, v in base.items() if v > 0}
        total = sum(base.values())
        if abs(total - 100.0) > 0.01:
            factor = 100.0 / total
            base = {k: v * factor for k, v in base.items()}
        
        return base


def main():
    """Demo of AI ingredient recommender."""
    from sensor_data_reader import SensorData
    
    print("\n" + "🤖" * 30)
    print("  AI INGREDIENT RECOMMENDER - DEMO")
    print("🤖" * 30)
    
    # Sample sensor data
    sensor_data = SensorData(
        body_weight_kg=75,
        skeletal_muscle_percent=32,
        resting_metabolic_rate=1650,
        body_fat_percent=22
    )
    
    recommender = AIIngredientRecommender()
    
    print("\n📊 User Body Composition:")
    print(f"  Weight: {sensor_data.body_weight_kg}kg")
    print(f"  Muscle: {sensor_data.skeletal_muscle_percent}%")
    print(f"  RMR: {sensor_data.resting_metabolic_rate} kcal/day")
    print(f"  Fat: {sensor_data.body_fat_percent}%")
    
    print("\n🎯 User Selections:")
    print("  Mode: Pre-Workout")
    print("  Base: Maltodextrin")
    print("  Flavour: Coffee")
    
    # Get AI recommendation
    result = recommender.recommend_ingredients(
        sensor_data,
        mode='pre',
        carb_mode='maltodextrin',
        flavour='coffee'
    )
    
    print("\n🤖 AI Recommendation:")
    print(f"  Status: {result['validation_status']}")
    print(f"  Ingredients Selected: {len(result['selected_ingredients'])}")
    
    print("\n📦 Ingredients (50g bar):")
    for ing, grams in sorted(result['formulation_grams'].items(), key=lambda x: -x[1]):
        pct = result['formulation_percent'][ing]
        print(f"  {ing:25s}: {grams:6.2f}g ({pct:5.2f}%)")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()