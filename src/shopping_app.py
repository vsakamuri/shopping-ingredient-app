import tkinter as tk
from PIL import Image, ImageTk
from decouple import config
from io import BytesIO
import urllib
import urllib.request
import logging
import json
import base64

app = tk.Tk()

# Logging
logger = logging.getLogger()
logger.setLevel('INFO')

HEIGHT = 600
WIDTH = 700

def get_missing_ingredients_list(recipe):
    '''
    returns a string of missing ingredients from a recipe.
    '''
    missing_ingredients = []
    for missing_ingredient in recipe.get('missedIngredients'):      
        missing_ingredients.append(missing_ingredient.get('name'))
    
    return ', '.join(missing_ingredients)

def get_next_recipe(recipes):
    '''
    removes first item (which is not selected by user) from recipes.
    '''
    recipes.pop(0)
    get_liked_recipe(recipes)

def get_liked_recipe(recipes):
    '''
    gets the recipe image from spoonacular
    show the recipe image to user along with missing ingredients.
    '''
    recipe = recipes[0]
    try:
        image_request = urllib.request.Request(recipe.get('image'), headers={'User-Agent': 'Mozilla/5.0'})
        raw_data = urllib.request.urlopen(image_request).read()
        im = Image.open(BytesIO(raw_data))
        image = ImageTk.PhotoImage(im)       
        
        frame = tk.Frame(app, bg='black', bd=0)
        frame.place(relx=0.5, rely=0.06, relwidth=0.75, relheight=0.06, anchor='n')
        recipe_name = "Recipe Name: " + str(recipe.get('title'))
        label = tk.Label(frame, font='Consolas 10 bold', anchor='w', text=recipe_name)
        label.place(relheight=1, relwidth=1)

        image_frame = tk.Frame(app, bg='black', bd=0)
        image_frame.place(relx=0.5, rely=0.12, relwidth=0.75, relheight=0.4, anchor='n')
        label = tk.Label(image_frame, image=image)
        label.image = image
        label.place(relheight=1, relwidth=1)

        label_frame = tk.Frame(app, bd=0)
        label_frame.place(relx=0.5, rely=0.55, relwidth=0.75, relheight=0.1, anchor='n')

        if recipe.get('missedIngredientCount')  == 0:
            label = tk.Label(label_frame, font='Consolas 9 bold', anchor='w', text="You have all the ingredients for this recipe")
            label.place(relheight=1, relwidth=1)
        else:
            missing_str = get_missing_ingredients_list(recipe)
            if recipe.get('missedIngredientCount')  == 1:         
                missing_str_text = 'Missing ingredient for the recipe is: ' + missing_str
            else:
                missing_str_text = 'Missing ingredients for the recipe are: ' + missing_str
        
            label = tk.Label(label_frame, font='Consolas 9 bold', anchor='w', text=missing_str_text)
            label.place(relheight=.5, relwidth=1)
        
            select_button = tk.Button(label_frame, text="Get Shopping List", bg='#FEE585', font='Consolas 10 bold', command=lambda: get_missing_ingredients(recipe))
            select_button.place(relx=0.3, rely=0.5, relheight=.5, relwidth=.4)

        button_frame = tk.Frame(app, bd=0)
        button_frame.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.05, anchor='n')

        if (len(recipes) >= 2):
            next_button = tk.Button(button_frame, text="View another Recipe", bg='#FEE585', font='Consolas 10 bold', command=lambda: get_next_recipe(recipes))
            next_button.place(relheight=1, relwidth=1)

    except Exception as ex:
        logger.error("error occurred while getting the image." + str(ex))
        frame = tk.Frame(app, bg='black', bd=0)
        frame.place(relx=0.5, rely=0.06, relwidth=1, relheight=1, anchor='n')
        label = tk.Label(frame, font='Consolas 9 bold', anchor='w', text="Error Occurred while displaing the recipe. Please try again later")
        label.place(relheight=1, relwidth=1)

def get_missing_ingredients(liked_recipe):
    '''
    displays shopping list for missing ingredients
    '''
    total_amount = 0.00
    lower_frame = tk.Frame(app, bd=0)
    lower_frame.place(relx=0.5, rely=0.06, relwidth=0.75, relheight=1, anchor='n')
    ingredient_str = "{:<30} {:<30} {:<20}".format('Name','Aisle','Estimated Amount')
    rely = .1
    label = tk.Label(lower_frame, font='Consolas 10 bold', anchor='w', text=ingredient_str)
    label.place(rely=rely, relheight=0.02, relwidth=1)
    
    ingredient_str = "{:<30} {:<30} {:<20}".format('****','*****','**************')
    rely = rely + .02
    label = tk.Label(lower_frame, font='Consolas 10 bold', anchor='w', text=ingredient_str)
    label.place(rely=rely, relheight=0.02, relwidth=1)

    for missing_ingredient in liked_recipe.get('missedIngredients'):      
        ingredient_str = "{:<30} {:<30} {:<20}".format(str(missing_ingredient.get('name')), str(missing_ingredient.get('aisle')), str(missing_ingredient.get('amount')))
        rely = rely + .02
        label = tk.Label(lower_frame, font='Consolas 10', anchor='w', text=ingredient_str)
        label.place(rely=rely, relheight=0.02, relwidth=1)

        total_amount = total_amount + float(missing_ingredient.get('amount'))
    
    total_estimated_str = "Total estimated cost of your shopping list is: " + str (total_amount)
    label = tk.Label(lower_frame, font='Consolas 11 bold', text=total_estimated_str)
    label.place(rely=.06, relheight=0.02, relwidth=1)

def get_recipes(ingredients):
    '''
    if no recipe found with the ingredients, displys message
    '''
    
    if (ingredients == ""):
        lower_frame = tk.Frame(app, bg='black', bd=5)
    
        lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

        label = tk.Label(lower_frame, font=40, text="Please enter ingredients before clicking Get Recipes button")
        label.place(relheight=1, relwidth=1)        

    else:        
        recipes = get_recipes_for_ingredients(ingredients)

        if len(recipes) == 0:
            lower_frame = tk.Frame(app, bg='black', bd=5)
        
            lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

            label = tk.Label(lower_frame, font=40, text="No recipes found with the provided ingredients")
            label.place(relheight=1, relwidth=1)        
        else: 
            get_liked_recipe(recipes)

def get_recipes_for_ingredients(ingredients):
    '''
    calls spoonacular api to get recipes for the provided ingredents
    '''
    ingredients_list = ingredients.split(",")
    ingredients_list = [x.strip(' ') for x in ingredients_list]
    ingredients_list_str = ",+".join(ingredients_list)
    api_key_encoded = config('KEY')
    API_KEY = base64.b64decode(api_key_encoded).decode("ascii")

    BASE_URL = "https://api.spoonacular.com/recipes/findByIngredients?"
    uri =  BASE_URL + "apiKey=" + API_KEY + "&ingredients=" + ingredients_list_str + "&ranking=1&number=10"
    try:
        request = urllib.request.Request(uri, headers={'User-Agent': 'Mozilla/5.0'})
        url = urllib.request.urlopen(request)
        response = json.loads(url.read().decode('utf-8'))
        return response
    except Exception as ex:
        logger.error('Unknown error while calling spoonacular API.')
        logger.error('Reason:' + str(ex))
        frame = tk.Frame(app, bg='black', bd=0)
        frame.place(relx=0.5, rely=0.06, relwidth=0.75, relheight=0.06, anchor='n')
        label = tk.Label(frame, font='Consolas 9 bold', anchor='w', text="Error Occurred while getting recipes. Please try again later")
        label.place(relheight=1, relwidth=1)

def main():

    app.title('Shopping Ingredients')
    
    canvas = tk.Canvas(app, height=HEIGHT, width=WIDTH)
    canvas.pack()

    frame = tk.Frame(app, bg='black', bd=0)
    frame.place(relx=0.5, rely=0.06, relwidth=0.75, relheight=0.06, anchor='n')

    label = tk.Label(frame, font='Consolas 12 bold', anchor='w', text="Enter the Ingredients in the below text box separated by ,")
    label.place(relheight=1, relwidth=1)

    frame2 = tk.Frame(app, bg='black', bd=1)
    frame2.place(relx=0.5, rely=0.12, relwidth=0.75, relheight=0.06, anchor='n')

    entry = tk.Entry(frame2, font='Consolas 10')
    entry.place(relwidth=0.68, relheight=1)
    
    button = tk.Button(frame2, text="Get Recipes", font='Consolas 10 bold', bg='#FEE585', command=lambda: get_recipes(entry.get()))
    button.place(relx=0.7, relheight=1, relwidth=0.3)

    app.mainloop()

if __name__ == '__main__':
    main()
