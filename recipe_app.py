import requests

def get_recipe_from_api(recipe_name):
    response = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={recipe_name}")
    data = response.json()
    
    if data['meals'] is None:
        raise KeyError(recipe_name)

    meal = data['meals'][0]
    name = meal['strMeal']
    instructions =  meal['strInstructions']

    ingredients = []
    for i in range(1, 21):
        ingredient = meal[f'strIngredient{i}']
        measure = meal[f'strMeasure{i}']

        if ingredient and ingredient.strip():
            ingredients.append(f"{measure} {ingredient}")

    return(name, ingredients, instructions)


while True:
    print("Welcome to Recipe Finder")
    user_query = input("What recipe would you like to find today? ")
    user_query = user_query.title()
    print(f"Finding recipes for {user_query}")

    try:
        name, ingredients, instructions = get_recipe_from_api(user_query)
        print(f"\n{'='*50}")
        print(f"RECIPE: {name.upper()}")
        print(f"{'='*50}\n")
        print("INGREDIENTS:")
        for ingredient in ingredients:
            print(f"  * {ingredient}")
        print("\nINSTRUCTIONS:")
        print(instructions)

    except KeyError:
        print(f"Sorry, {user_query} was not found. Try searching for something else.")
    
    continue_search = input("Search for another recipe? (yes/no)")
    if continue_search.lower() in ["no", "n", "quit", "exit"]:
        print("Thanks for trying the app. Happy Cooking!")
        break