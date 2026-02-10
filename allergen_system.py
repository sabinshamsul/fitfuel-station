"""
Allergen Disclosure System
Displays allergen warnings before payment
"""

from typing import Dict, List, Set

# ═══════════════════════════════════════════════════════════
# ALLERGEN DATABASE
# ═══════════════════════════════════════════════════════════

INGREDIENT_ALLERGENS = {
    'pea_protein': {
        'allergens': ['Pea', 'Legume'],
        'severity': 'low',
        'note': 'May cause reaction in people with legume allergies'
    },
    'sunflower_seed': {
        'allergens': ['Sunflower seed'],
        'severity': 'medium',
        'note': 'Seed allergy - may cross-react with other seeds'
    },
    'pumpkin_seed_flour': {
        'allergens': ['Pumpkin seed', 'Potential nut cross-reactivity'],
        'severity': 'medium',
        'note': 'May cause reaction in people allergic to nuts, melons, or birch pollen'
    },
    'rice_syrup': {
        'allergens': [],
        'severity': 'none',
        'note': None
    },
    'glycerine': {
        'allergens': [],
        'severity': 'none',
        'note': None
    },
    'maltodextrin': {
        'allergens': [],
        'severity': 'none',
        'note': 'Derived from corn - safe for most people'
    },
    'brown_rice_flour': {
        'allergens': [],
        'severity': 'none',
        'note': 'Naturally gluten-free'
    },
    'leucine': {
        'allergens': [],
        'severity': 'none',
        'note': None
    },
    'guarana_extract': {
        'allergens': [],
        'severity': 'none',
        'note': 'Contains caffeine'
    },
    'salt': {
        'allergens': [],
        'severity': 'none',
        'note': None
    },
    'cocoa_powder': {
        'allergens': [],
        'severity': 'none',
        'note': 'Contains trace amounts of caffeine'
    },
    'instant_coffee': {
        'allergens': [],
        'severity': 'none',
        'note': 'Contains caffeine'
    },
    'matcha_powder': {
        'allergens': [],
        'severity': 'none',
        'note': 'Contains caffeine and L-theanine'
    },
    'vanilla': {
        'allergens': [],
        'severity': 'none',
        'note': None
    }
}

# Common allergens NOT in product
FREE_FROM_ALLERGENS = [
    'Gluten',
    'Dairy',
    'Soy',
    'Eggs',
    'Fish',
    'Shellfish',
    'Tree nuts',
    'Peanuts',
    'Wheat'
]


class AllergenAnalyzer:
    """Analyze formulation for allergens."""
    
    @staticmethod
    def get_allergens(formulation: Dict[str, float]) -> Dict:
        """
        Get allergen information from formulation.
        
        Returns dict with:
        - present_allergens: List of allergens in the bar
        - free_from: List of common allergens NOT in the bar
        - warnings: List of warning messages
        - has_caffeine: Boolean
        """
        present_allergens = set()
        warnings = []
        has_caffeine = False
        
        for ingredient, percentage in formulation.items():
            if percentage < 0.1:  # Ignore trace amounts
                continue
            
            if ingredient not in INGREDIENT_ALLERGENS:
                continue
            
            allergen_info = INGREDIENT_ALLERGENS[ingredient]
            
            # Collect allergens
            for allergen in allergen_info['allergens']:
                present_allergens.add(allergen)
            
            # Collect warnings
            if allergen_info['note'] and allergen_info['severity'] != 'none':
                warnings.append(allergen_info['note'])
            
            # Check for caffeine
            if ingredient in ['guarana_extract', 'instant_coffee', 'matcha_powder', 'cocoa_powder']:
                if percentage > 0.1:
                    has_caffeine = True
        
        return {
            'present_allergens': sorted(list(present_allergens)),
            'free_from': FREE_FROM_ALLERGENS,
            'warnings': warnings,
            'has_caffeine': has_caffeine
        }