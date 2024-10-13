import streamlit as st
import requests

st.title('Easy Eats')

ingredients = st.text_input("Enter ingredients you have (comma separated):")

def get_recipes(ingredients):
    app_id = "29d395d3"
    app_key = "81d1f11d53570c150a29393dd774cf4e"

    ingredients_query = ','.join([ing.strip() for ing in ingredients.split(',')])
    url = f"https://api.edamam.com/api/recipes/v2?type=public&q={ingredients_query}&app_id={app_id}&app_key={app_key}"

    response = requests.get(url)
    exact_matches = []
    partial_matches = []
    if response.status_code == 200:
        recipes = response.json().get('hits', [])
        for recipe in recipes:
            recipe_ingredients = set([ingredient['food'] for ingredient in recipe['recipe']['ingredients']])
            user_ingredients_set = set(ingredients_query.split(','))
            if recipe_ingredients == user_ingredients_set:
                exact_matches.append(recipe['recipe'])
            elif user_ingredients_set.issubset(recipe_ingredients):
                missing_ingredients = recipe_ingredients - user_ingredients_set
                partial_matches.append((recipe['recipe'], missing_ingredients))
        return exact_matches, partial_matches
    else:
        return [], []

if st.button('Find Recipes'):
    if ingredients:
        exact_recipes, possible_recipes = get_recipes(ingredients)
        if exact_recipes:
            st.subheader("Recipes you can make with your ingredients:")
            for recipe in exact_recipes:
                st.write(f"**{recipe['label']}**")
                st.markdown(f"[Recipe Link]({recipe['url']})")
        else:
            st.write("No exact recipes found that match your ingredients.")
        
        if possible_recipes:
            st.subheader("Possible recipes if you get a few more ingredients:")
            for recipe, missing in possible_recipes:
                st.write(f"**{recipe['label']}** - Missing ingredients: {', '.join(missing)}")
                st.markdown(f"[Recipe Link]({recipe['url']})")
        else:
            st.write("No possible recipes found with a few more ingredients.")

    else:
        st.write("Please enter some ingredients to find recipes.")



