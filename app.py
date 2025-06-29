from idlelib.mainmenu import default_keydefs

import streamlit as st
import pickle
import pandas as pd
import requests
import streamlit.components.v1 as components
import joblib


########################################


# Page configuration
st.set_page_config(layout="wide")




st.markdown("""
    <style>
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 20px;
        padding: 10px;
    }
    /* REMOVE ALL BODY PADDING */
    .stButton>button {
        background-color: #E50914;
        color: white;
    }
    .block-container {
        background-color:rgb(14, 17, 23);
        padding: 0rem 20rem 0rem 4rem;
    }

    /* NAVBAR STYLE */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 9999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 30px;
        background-color: rgb(14, 17, 23);
        border-bottom: 1px solid #333;
        margin: 0;
    }

    .navbar-left {
        color: #E50914;
        font-weight: bold;
        font-size: 40px;
        font-family: 'Segoe UI', sans-serif;
    }

    .navbar-center a {
        margin: 0 15px;
        text-decoration: none;
        color: white;
        font-size: 16px;
    }

    .navbar-center a:hover {
        color: #E50914;
    }
</style>

<div class="navbar">
     <div class="navbar-left">MOVIE.Flix</div>
     <div class="navbar-center">
        <a href="#">Home</a>
        <a href="#">About</a>
        <a href="#">Movies</a>
        <a href="#">Contact</a>
     </div>
         
</div>
    <br><br><br><br><br>
""", unsafe_allow_html=True)

#Fetching data
API_KEY="a5b62deb"
def fetch_poster(movie_id):
    response=requests.get("https://www.omdbapi.com/?i={}&apikey=a5b62deb".format(movie_id) )
    data=response.json()
    return data['Poster']


#Recommending movie
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].imdb_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster


#Displaying recommended movies
def show_movie_cards(names, posters):
    html = """
    <style>
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            padding: 10px;
        }
        .movie-card {
            background-color: rgb(14, 17, 23);
            color:white;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            text-align: center;
            overflow: hidden;
            transition: transform 0.2s;
        }
        .movie-card:hover {
            transform: scale(1.03);
        }
        .movie-card img {
            width: 100%;
            height: 260px;
            object-fit: cover;
        }
        .movie-card p {
            font-weight: bold;
            font-size: 16px;
            color: white;
            margin: 10px;
            min-height: 40px;
        }
    </style>
    <div class="card-grid">
    """

    for i in range(5):
        poster_url = posters[i]
        if poster_url == "N/A" or poster_url.strip() == "":
            poster_url = default_poster
        html += f"""
        <div class="movie-card">
            <img src="{poster_url}" alt="{names[i]}">
            <p>{names[i]}</p>
        </div>
        """

    html += "</div>"
    html += """
                </div>
            </div>

            <footer style="
                text-align: center;
                padding: 20px;
                margin-top: 40px;
                color: #888;
                font-size: 14px;
                border-top: 1px solid #eee;
            ">
                Built with ❤️ by MOVIE.Flix · © 2025
            </footer>
            """
    components.html(html, height=1500, scrolling=False)

#Displaying loader at home page
def show_loader_animation():
    html = """
        <style>
        .loader-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 400px;
        }

        .balls {
            display: flex;
            justify-content: space-around;
            align-items: center;
            width: 400px;
        }

        .ball {
            width: 100px;
            height: 100px;
            background-color: #e50914;  
            border-radius: 50%;
            animation: bounce 0.6s infinite alternate;
        }

        .ball:nth-child(2) {
            animation-delay: 0.2s;
        }

        .ball:nth-child(3) {
            animation-delay: 0.4s;
        }

        @keyframes bounce {
            to {
                transform: translateY(-40px);
                opacity: 0.5;
            }
        }
        </style>

        <div class="loader-container">
            <div class="balls">
                <div class="ball"></div>
                <div class="ball"></div>
                <div class="ball"></div>
            </div>
        </div>
        """
    components.html(html, height=400)


#MAIN

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

#similarity = pickle.load(open('similarity.pkl','rb'))
import os
import gdown
import pickle

# Only download if file doesn't exist
try:
    if not os.path.exists("similarity_compressed.pkl"):
        file_id = "1oUt1qdvcMT8s8Ae6AWupkuXJKZWIHnrK"  # replace with your actual ID
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url,output="similarity_compressed.pkl", quiet=False)

    # Now load the file

    similarity = joblib.load("similarity_compressed.pkl")
except Exception as e:
    st.error(f"⚠️ Failed to download file: {e}")




st.title('Movie Recommender System')


#search-box
selected_movie_name = st.selectbox(
    'Which movie do you want to recommend?',
    movies['title'].values,
)



default_poster="https://thumbs.dreamstime.com/b/playful-graphic-words-inspiration-s-not-available-inside-lightbulb-shape-unique-style-whimsical-creative-design-379916567.jpg"

if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)
    cols = st.columns(5)
    show_movie_cards(names,posters)

else:
    st.markdown("### No Recommendations Yet")
    show_loader_animation()









