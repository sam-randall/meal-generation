
import json

with open('recipes.json', 'r') as f:
    recipes = json.load(f)


with open('food_categories.json', 'r') as f:
    categories_dict = json.load(f)

categories = categories_dict['categories']


for meal in recipes:
    for ingredient in recipes[meal]:
        prompt = f"Ingredient {ingredient}\n"
        for i, cat in enumerate(categories):
            prompt += f"{i} for {cat}" + '\n'

        response = input(prompt)

        try:
            response = int(response)
            entry = f'{ingredient},{categories[response]},\n'
        except Exception as e:
            entry = f'{ingredient},{response},\n'

        print(entry)
        

        with open('ingredient_categories.txt', 'a') as f:
            f.write(entry)



