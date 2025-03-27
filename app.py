import pickle
import streamlit as st
import requests

# Replace with your own OMDb API Key (Get it from https://www.omdbapi.com/apikey.aspx)
OMDB_API_KEY = "6b1718f6"


def fetch_omdb_poster(movie_name):
    """Fetch movie poster from OMDb API"""
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "Poster" in data and data["Poster"] != "N/A":
            return data["Poster"], f"https://www.imdb.com/title/{data.get('imdbID', '')}"

    return "https://via.placeholder.com/300x450?text=No+Poster+Found", "#"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title
        poster_url, imdb_url = fetch_omdb_poster(movie_title)
        recommended_movies.append((movie_title, poster_url, imdb_url))

    return recommended_movies


# --- Streamlit UI ---
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Custom CSS for better design
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .title {
            font-size: 30px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .movie-card {
            background: #222;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
        }
        img {
            border-radius: 10px;
        }
        .movie-title {
            font-size: 20px;  /* Increased size */
            font-weight: bold;
            color: #FFFFFF;  /* Bright white */
            margin-top: 10px;
            padding: 5px;
            background: rgba(255, 255, 255, 0.1); /* Light background */
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎬 Movie Recommender System</div>", unsafe_allow_html=True)

movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movie_list = movies['title'].values
selected_movie = st.selectbox("🔍 Type or Select a movie from the dropdown", movie_list)

if st.button('🔮 Show Recommendations'):
    recommended_movies = recommend(selected_movie)

    cols = st.columns(5)
    for i, (title, poster, imdb_url) in enumerate(recommended_movies):
        with cols[i]:
            st.markdown(f"""
                <div class='movie-card'>
                    <a href="{imdb_url}" target="_blank">
                        <img src="{poster}" width="180">
                    </a>
                    <div class='movie-title'>{title}</div>  <!-- Improved visibility -->
                </div>
            """, unsafe_allow_html=True)
st.markdown("""
    <hr style="border:1px solid white;">
    <div style="text-align:center; font-size:16px; color:#CCCCCC;">
        Created by <b>Yuvraj Singh</b>
    </div>
""", unsafe_allow_html=True)
