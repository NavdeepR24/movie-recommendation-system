import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import streamlit.components.v1 as components

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
    match = movies[movies['title'] == movie_title]
    if match.empty:
        return [], [], []
    idx = match.index[0]
    dists = sorted(enumerate(similarity[idx]), reverse=True, key=lambda x: x[1])
    names, posters, ids = [], [], []
    for i, _ in dists[1:6]:
        row = movies.iloc[i]
        mid = row['movie_id']
        names.append(row['title'])
        posters.append(fetch_poster(mid))
        ids.append(mid)
    return names, posters, ids

# Session State
if 'selected_movie_id' not in st.session_state:
    st.session_state.selected_movie_id    = None
if 'selected_movie_title' not in st.session_state:
    st.session_state.selected_movie_title = None

def go_back():
    st.session_state.selected_movie_id = None
    st.session_state.selected_movie_title = None

# Details Page
def show_detail_page(movie_id: int, movie_title: str):
    st.button("← Back to Search", on_click=go_back)

    details = fetch_movie_details(movie_id)
    poster_path = details.get("poster_path")
    poster = (POSTER_BASE + poster_path) if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"

    col_poster, col_info = st.columns([1, 2])

    with col_poster:
        st.image(poster, use_container_width=True)

    with col_info:
        st.title(details.get("title", movie_title))

        tagline = details.get("tagline", "")
        if tagline:
            st.markdown(f"*{tagline}*")

        # Rating + meta row
        vote = details.get("vote_average", 0)
        votes_n = details.get("vote_count", 0)
        runtime = details.get("runtime", 0)
        release_date = details.get("release_date", "")
        date = release_date[:4] if release_date else "N/A"
        lang = details.get("original_language", "").upper()

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("⭐ Rating", f"{vote:.1f}/10")
        m2.metric("🗳️ Votes", f"{votes_n:,}")
        m3.metric("🕐 Runtime", f"{runtime} min" if runtime else "N/A")
        m4.metric("📅 Released", date)
        m5.metric("🌐 Language", lang if lang else "N/A")

        # Genres
        genres = [g["name"] for g in details.get("genres", [])]
        if genres:
            st.markdown("**Genres:** " + "  ".join([f"`{g}`" for g in genres]))

        # Languages / countries
        countries = [c["name"] for c in details.get("production_countries", [])]
        if countries:
            st.markdown("**Countries:** " + ", ".join(countries))

        # Overview
        st.markdown("### Overview")
        st.write(details.get("overview", "No overview available."))

        # Cast
        movie_credits = details.get("credits", {})
        cast = movie_credits.get("cast", [])[:8]
        if cast:
            cast_str = ", ".join([c["name"] for c in cast])
            st.markdown(f"**Cast:** {cast_str}")

        # Director
        crew = movie_credits.get("crew", [])
        director = next((p["name"] for p in crew if p["job"] == "Director"), None)
        if director:
            st.markdown(f"**Director:** {director}")

        # Trailer
        videos = details.get("videos", {}).get("results", [])
        trailer = next((v for v in videos if v["type"] == "Trailer" and v["site"] == "YouTube"), None)
        if trailer:
            st.markdown(
                f'<a href="https://www.youtube.com/watch?v={trailer["key"]}" target="_blank">'
                f'▶️ Watch Trailer</a>',
                unsafe_allow_html=True
            )

    st.divider()

    # ── Budget / Revenue ──────────────────────────────────────────────────────
    budget = details.get("budget", 0)
    revenue = details.get("revenue", 0)
    if budget or revenue:
        b1, b2 = st.columns(2)
        if budget:
            b1.metric("💰 Budget", f"${budget:,.0f}")
        if revenue:
            b2.metric("💵 Revenue", f"${revenue:,.0f}")
        st.divider()

    # ── Recommendations based on THIS movie ──────────────────────────────────
    st.markdown("## 🎬 You Might Also Like")

    # Look up this movie in our local dataset by tmdb id or title
    match = movies[movies['movie_id'] == movie_id]
    if match.empty:
        match = movies[movies['title'].str.lower() == movie_title.lower()]

    if not match.empty:
        rec_title = match.iloc[0]['title']
        rec_names, rec_posters, rec_ids = recommend(rec_title)

        cols = st.columns(5)
        for col, name, poster, rid in zip(cols, rec_names, rec_posters, rec_ids):
            with col:
                st.image(poster, use_container_width=True)
                st.button(
                    name,
                    key=f"rec_{rid}",
                    on_click=select_movie,
                    args=(rid, name),
                    use_container_width=True
                )
    else:
        st.info("Recommendations not available for this movie in the local dataset.")

def select_movie(movie_id, movie_title):
    st.session_state.selected_movie_id = movie_id
    st.session_state.selected_movie_title = movie_title

def show_main_page():
    st.title("🎬 Movie Recommender System")

    selected = st.selectbox(
        "Type or select a movie",
        movies['title'].values,
        index=None,
        placeholder="Search for a movie…"
    )

    if st.button("Recommend") and selected:
        names, posters, ids = recommend(selected)

        st.markdown("### Recommended Movies")
        st.markdown("*Click on any movie to see its full details and more recommendations*")

        cols = st.columns(5)
        for col, name, poster, mid in zip(cols, names, posters, ids):
            with col:
                st.image(poster, use_container_width=True)
                st.button(
                    name,
                    key=f"main_{mid}",
                    on_click=select_movie,
                    args=(mid, name),
                    use_container_width=True
                )


if st.session_state.selected_movie_id:
    show_detail_page(
        st.session_state.selected_movie_id,
        st.session_state.selected_movie_title
    )
else:
    show_main_page()