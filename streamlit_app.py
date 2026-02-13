import requests
import streamlit as st

if 'show_category_recipes' not in st.session_state:
    st.session_state.show_category_recipes = False
if 'category_recipes' not in st.session_state:
    st.session_state.category_recipes = None


def get_recipe_from_api(recipe_name):
    response = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={recipe_name}")
    data = response.json()
    
    if data['meals'] is None:
        raise KeyError(recipe_name)

    meal = data['meals'][0]
    name = meal['strMeal']
    instructions =  meal['strInstructions']
    image_url = meal['strMealThumb']

    ingredients = []
    for i in range(1, 21):
        ingredient = meal[f'strIngredient{i}']
        measure = meal[f'strMeasure{i}']

        if ingredient and ingredient.strip():
            ingredients.append(f"{measure} {ingredient}")

    return(name, ingredients, instructions, image_url)

def get_random_recipe():
    response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
    data = response.json()
    
    meal = data['meals'][0]
    name = meal['strMeal']
    instructions =  meal['strInstructions']
    image_url = meal['strMealThumb']

    ingredients = []
    for i in range(1, 21):
        ingredient = meal[f'strIngredient{i}']
        measure = meal[f'strMeasure{i}']

        if ingredient and ingredient.strip():
            ingredients.append(f"{measure} {ingredient}")

    return(name, ingredients, instructions, image_url)

def get_categories():
    response = requests.get("https://www.themealdb.com/api/json/v1/1/list.php?c=list")
    data = response.json()

    categories = []
    for meal in data['meals']:
        category = meal['strCategory']
        categories.append(f"{category}")

    return(categories)

def get_recipes_by_category(category):
    response = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category}")
    data = response.json()

    meals = []
    meal_thumb =[]
    for meal in data['meals']:
        meal_name = meal['strMeal']
        meal_thumbnail = meal['strMealThumb']
        meals.append(f"{meal_name}")
        meal_thumb.append(f"{meal_thumbnail}")


    return(meals, meal_thumb)


st.title("🍳 Recipe Finder")

recipe_query = st.text_input("What recipe would you like to find?", placeholder="e.g., pasta, chicken, tacos")
if st.button("Search Recipe"):
    if recipe_query.strip():
        try:
            name, ingredients, instructions, image_url = get_recipe_from_api(recipe_query.title())
            st.success(f"RECIPE: {name.upper()}")
            st.image(image_url, caption=name)
            st.subheader("📝 Ingredients:")
            for ingredient in ingredients:
                st.write(f"  * {ingredient}")
            st.subheader("👨‍🍳 Instructions:")
            st.write(instructions)
        except KeyError:
            st.error(f"Sorry, {recipe_query} was not found. Try searching for something else.")
    else:
        st.warning("Please enter a recipe name!")

if st.button("🎲 Surprise Me!"):
    name, ingredients, instructions, image_url = get_random_recipe()
    st.success(f"RECIPE: {name.upper()}")
    st.image(image_url, caption=name, width=400)
    st.subheader("📝 Ingredients:")
    for ingredient in ingredients:
        st.write(f"  * {ingredient}")
    st.subheader("👨‍🍳 Instructions:")
    st.write(instructions)


st.sidebar.header("🍽️ Browse by Category")
categories = get_categories()
selected_category = st.sidebar.selectbox("Choose a category:", categories)
if st.sidebar.button("Show Recipes"):
    recipe_names, recipe_images = get_recipes_by_category(selected_category)
    st.session_state.category_recipes = (recipe_names, recipe_images, selected_category)
    st.session_state.show_category_recipes = True

if st.session_state.show_category_recipes and st.session_state.category_recipes:
    recipe_names, recipe_images, category = st.session_state.category_recipes
    st.subheader(f"{selected_category} recipes:")

    for name, image in zip(recipe_names, recipe_images):
        if st.button(f"🍽️ {name}", key=f"recipe_{name}"):
            recipe_name, recipe_ingredients, recipe_instructions, recipe_image = get_recipe_from_api(name)
            st.success(recipe_name)
            st.image(recipe_image, caption=name, width=400)
            st.subheader("📝 Ingredients:")
            for ingredient in recipe_ingredients:
                st.write(f"*  {ingredient}")
            st.subheader("👨‍🍳 Instructions:")
            st.write(recipe_instructions)
        st.image(image, width=200)