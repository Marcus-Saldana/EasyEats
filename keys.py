import streamlit as st
import requests

# YouTube API credentials
YOUTUBE_API_KEY = ""  # Replace with your YouTube API key

# Edamam API credentials
EDAMAM_APP_ID = "29d395d3"  # Replace with your Edamam app ID
EDAMAM_APP_KEY = "81d1f11d53570c150a29393dd774cf4e"  # Replace with your Edamam app key

st.title('Easy Eats with Recipe Videos')

ingredients = st.text_input("Enter ingredients you have (comma separated):")

def get_recipes(ingredients):
    ingredients_query = ','.join([ing.strip() for ing in ingredients.split(',')])
    url = f"https://api.edamam.com/api/recipes/v2?type=public&q={ingredients_query}&app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}"

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

def search_youtube_videos(query):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return []

if st.button('Find Recipes'):
    if ingredients:
        exact_recipes, possible_recipes = get_recipes(ingredients)
        
        if exact_recipes:
            st.subheader("Recipes you can make with your ingredients:")
            for recipe in exact_recipes:
                st.write(f"**{recipe['label']}**")
                st.markdown(f"[Recipe Link]({recipe['url']})")

                # Search for YouTube videos related to the recipe
                youtube_videos = search_youtube_videos(recipe['label'])
                if youtube_videos:
                    st.write("**YouTube Videos:**")
                    for video in youtube_videos[:3]:  # Show the top 3 videos
                        video_title = video['snippet']['title']
                        video_id = video['id']['videoId']
                        st.markdown(f"- [{video_title}](https://www.youtube.com/watch?v={video_id})")
                else:
                    st.write("No YouTube videos found for this recipe.")

        else:
            st.write("No exact recipes found that match your ingredients.")
        
        if possible_recipes:
            st.subheader("Possible recipes if you get a few more ingredients:")
            for recipe, missing in possible_recipes:
                st.write(f"**{recipe['label']}** - Missing ingredients: {', '.join(missing)}")
                st.markdown(f"[Recipe Link]({recipe['url']})")

                # Search for YouTube videos related to the recipe
                youtube_videos = search_youtube_videos(recipe['label'])
                if youtube_videos:
                    st.write("**YouTube Videos:**")
                    for video in youtube_videos[:3]:  # Show the top 3 videos
                        video_title = video['snippet']['title']
                        video_id = video['id']['videoId']
                        st.markdown(f"- [{video_title}](https://www.youtube.com/watch?v={video_id})")
                else:
                    st.write("No YouTube videos found for this recipe.")
        
        else:
            st.write("No possible recipes found with a few more ingredients.")
    else:
        st.write("Please enter some ingredients to find recipes.")
