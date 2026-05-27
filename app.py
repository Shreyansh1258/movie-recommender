import pickle
import streamlit as st
import requests
import pandas as pd

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Movie Recommender System",
    layout="wide"
)

# -----------------------------------
# TMDB API KEY
# -----------------------------------
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

# -----------------------------------
# Load Pickle Files
# -----------------------------------
# Make sure these files are in the same folder as app.py
movies = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Convert dictionary to DataFrame
movies = pd.DataFrame(movies)

# Movie titles for dropdown
movie_list = movies['title'].values


# -----------------------------------
# Fetch Movie Poster
# -----------------------------------
def fetch_poster(movie_id):

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

        response = requests.get(url, timeout=10)

        # If API fails
        if response.status_code != 200:
            return "https://via.placeholder.com/300x450?text=No+Poster"

        data = response.json()

        poster_path = data.get('poster_path')

        # If poster not found
        if poster_path is None:
            return "https://via.placeholder.com/300x450?text=No+Poster"

        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

        return full_path

    except Exception as e:
        print(e)
        return "https://via.placeholder.com/300x450?text=Error"


# -----------------------------------
# Recommendation Function
# -----------------------------------
def recommend(movie):

    # Get selected movie index
    movie_index = movies[movies['title'] == movie].index[0]

    # Get similarity scores
    distances = similarity[movie_index]

    # Sort movies based on similarity
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    # Fetch recommended movies
    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title

        recommended_movie_names.append(title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# -----------------------------------
# Streamlit UI
# -----------------------------------
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Button
if st.button("Show Recommendation"):

    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0], use_container_width=True)

    with col2:
        st.text(names[1])
        st.image(posters[1], use_container_width=True)

    with col3:
        st.text(names[2])
        st.image(posters[2], use_container_width=True)

    with col4:
        st.text(names[3])
        st.image(posters[3], use_container_width=True)

    with col5:
        st.text(names[4])
        st.image(posters[4], use_container_width=True)