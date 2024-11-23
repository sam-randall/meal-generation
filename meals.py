
import fire
import numpy as np
import json
import pandas as pd
import warnings

from password import APP_PASSWORD

dinners = [
    'shakshuka',
    'eggs and potatoes',
    'pasta',
    'thai',
    'greek salad',
    'chickpea salad',
    'mexican',
    'soup and salad',
    'fried rice',
    'pasta salad',
    'choose-a-recipe',
]


def send_email(content: str):
    import smtplib
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login('sam.randall5@gmail.com', APP_PASSWORD)
    # message to be sent
    message = content
    # sending the mail
    s.sendmail('sam.randall5@gmail.com', "shreyanarayan@gmail.com", message)
    # terminating the session
    s.quit()



def main():

    with open('recipes.json', 'r') as f:
        recipes = json.load(f)
    
    # No Replacent for no repeats!
    random_choices = np.random.choice(dinners, 7, replace = False, )

    days = ['Su', 'M', "T", "W", "Th", "F", "Sa"]

    schedule = "Schedule:\n"

    for d, ch in zip(days, random_choices):
        schedule += f'{d}: {ch}\n'

    print(schedule)

    
    response = input(f'''
Look OK? y to generate shopping list, 'D: Meal' to edit meals.
I know these meals: {list(recipes.keys()) + ["out"]}.
''')

    while response != 'y':

        day, meal = response.split(':')
        meal = meal.strip()

        index = days.index(day)
        random_choices[index] = meal

        schedule = "Schedule:\n"

        for d, ch in zip(days, random_choices):
            schedule += f'{d}: {ch}\n'

        print("Updated Schedule:")
        print(schedule)


        # TODO: Apply Changes
        response = input("Look OK? y to generate shopping list, 'D: Meal' to edit meals. ")

    schedule += '\n'

    master_dict = {}

    # The next two for loops are just initializing each element to 0, 
    # then incrementing.
    for ch in random_choices:

        if ch in recipes:

            if isinstance(recipes[ch], dict):

                for ingredient, quantity in recipes[ch].items():
                    master_dict[ingredient] = 0

        else: 
            if ch == 'out':
                pass
            else:
                warnings.warn(f"Meal {ch} selected, no recipe.")

    for ch in random_choices:

        if ch in recipes:
            if isinstance(recipes[ch], dict):

                for ingredient, quantity in recipes[ch].items():
                    master_dict[ingredient] += quantity



    store_item_to_quantity = dict(sorted(master_dict.items()))
    shopping_list = "Shopping List:\n"

    df = pd.read_csv('ingredient_categories.txt', header = None)
    df.columns = ["ingredient", "aisle", "none"]
    df = df[['ingredient', 'aisle']]

    # Iterate through your aisles, so as to organize the items.
    aisle_group_by = df.groupby('aisle')
    for aisle_val, subset in aisle_group_by:

        # Need to do `unique` because ingredients in the aisle are not unique.

        items_in_aisle = [item for item in subset.ingredient.unique() if item in store_item_to_quantity]
        if len(items_in_aisle):
            shopping_list += f'The {aisle_val.upper()} Aisle\n'
            for item in items_in_aisle:
                shopping_list += f'{item} ({store_item_to_quantity[item]})\n'

            shopping_list += '\n'

    print(shopping_list)
    print(schedule)

    email_response = input("Send email to Shreya.")



    if email_response == '':
        send_email(schedule)
        send_email(shopping_list)
        

if __name__ == '__main__':
    fire.Fire(main)