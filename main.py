import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Page config.
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Access your API key
tmdb_api_key = os.getenv("TMDB_API_KEY")

TMDB_BASE    = "https://api.themoviedb.org/3"
POSTER_BASE  = "https://image.tmdb.org/t/p/w500"

# Load data
movies_list=pickle.load(open('movie_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_list)
similarity=pickle.load(open('similarity.pkl', 'rb'))

# def fetch_poster(movie_id):
#     response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id,tmdb_api_key))
#     data=response.json()
#     return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def fetch_poster(movie_id: int) -> str:
    url = f"{TMDB_BASE}/movie/{movie_id}?api_key={tmdb_api_key}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        path = data.get("poster_path")
        if path:
            return POSTER_BASE + path
    return "https://via.placeholder.com/500x750?text=No+Poster"

def fetch_movie_details(movie_id: int) -> dict:
    """Return full movie details + credits + videos from TMDb."""
    details = requests.get(
        f"{TMDB_BASE}/movie/{movie_id}",
        params={"api_key": tmdb_api_key, "append_to_response": "credits,videos,keywords"}
    ).json()
    return details

#Recommender logic
def recommend(movie_title):
    """Return 5 (name, poster_url, tmdb_id) tuples."""
    idx   = movies[movies['title'] == movie_title].index[0]
    dists = sorted(enumerate(similarity[idx]), reverse=True, key=lambda x: x[1])
    names, posters, ids = [], [], []
    for i, _ in dists[1:6]:
        row = movies.iloc[i]
        mid = row['movie_id']
        names.append(row['title'])
        posters.append(fetch_poster(mid))
        ids.append(mid)
    return names, posters, ids

# def recommend (movie):
#     movie_index=movies[movies['title'] == movie].index[0]
#     distances=similarity [movie_index]
#     movies_list_sorted = sorted(list(enumerate (distances)), reverse=True, key=lambda x: x[1]) [1:6]
#
#     recommended_movies=[]
#     recommended_movies_poster=[]
#     for i in movies_list_sorted:
#         movie_id=movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_movies_poster.append(fetch_poster(movie_id))
#     return recommended_movies,recommended_movies_poster

st.title('Movie Recommender System')
selected_movie_name=st.selectbox(
    'Enter the movie name',
    movies['title'].values)

if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)

    col1, col2, col3,col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
