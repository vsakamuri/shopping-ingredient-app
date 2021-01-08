import unittest
from src import shopping_app

class TestMissingIngredients(unittest.TestCase):
        
    def test_get_missing_ingredients_list(self):
        recipe = {'id': 47942, 'title': 'Easy Glonola Stuffed Baked Apples', 'missedIngredientCount': 2, 
            'missedIngredients': [{'id': 1001, 'amount': 1.0, 'aisle': 'Milk, Eggs, Other Dairy', 'name': 'butter'}, 
            {'id': 1012010, 'amount': 0.5, 'aisle': 'Spices and Seasonings', 'name': 'ground cinnamon'}]}

        self.assertEqual(shopping_app.get_missing_ingredients_list(recipe), 'butter, ground cinnamon')

if __name__ == '__main__':
    unittest.main()