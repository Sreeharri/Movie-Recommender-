

import streamlit as st
import joblib
import pandas as pd
import requests

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ---------- GLOBAL STYLES ----------
st.markdown("""
    <style>
        .title-center {
            text-align: center;
            padding-bottom: 0.5rem;
        }
        .movie-title {
            text-align: center;
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 0.5rem;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------- DATA / FUNCTIONS ----------
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7ca8ed1364f5b31bd66c8b69f3c50a93&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = joblib.load('movies_dict.joblib')
movies = pd.DataFrame(movies_dict)
similarity = joblib.load('similarity.joblib')

# ---------- HEADER ----------
st.markdown("<h1 class='title-center'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color: gray;'>"
    "Pick a movie you like and we’ll suggest 5 similar ones."
    "</p>",
    unsafe_allow_html=True,
)

st.write("")  # small spacer

# ---------- INPUT ROW (ALIGNED LIKE OLD VERSION) ----------
with st.form("movie_form"):
    col_left, col_right = st.columns([4, 1])

    with col_left:
        selected_movie = st.selectbox(
            "Pick a movie you like:",
            movies["title"].values
        )

    with col_right:
        # add top margin so the button lines up vertically with the selectbox
        st.markdown("<div style='margin-top: 1.9rem'></div>", unsafe_allow_html=True)
        recommend_clicked = st.form_submit_button("Recommend", use_container_width=True)

st.write("")

# ---------- RESULTS ----------
if recommend_clicked:
    names, posters = recommend(selected_movie)

    st.subheader("We think you'll like:")
    cols = st.columns(5)

    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster, use_container_width=True)
            st.markdown(f"<div class='movie-title'>{name}</div>", unsafe_allow_html=True)
