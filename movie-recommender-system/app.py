import streamlit as st
import pickle
import requests

movie_df = pickle.load(open('movies.pkl', 'rb'))
similarities = pickle.load(open('similarities.pkl', 'rb'))


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=0e6c7e085d4001cc7b14093ec37aca85&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie_name):
    idx = movie_df[movie_df['title'] == movie_name].index[0]
    # sorting the distances and taking top 5 movies except the 0th as it will be the same movie
    recommended_list = sorted(list(enumerate(similarities[idx])), reverse=True, key=lambda x: x[1])[1:6]
    movie_list = []
    movie_posters = []
    for i in recommended_list:
        movie_list.append(movie_df.iloc[i[0]]['title'])
        # fetch movie poster
        movie_posters.append(fetch_poster(movie_df.iloc[i[0]]['id']))
    return movie_list, movie_posters


st.set_page_config(page_title='Movie Recommender', layout='wide', initial_sidebar_state='auto')
st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Select a movie?',
    movie_df['title'].values)

if st.button('Recommend me Matching movies'):
    recommended_movies, recommended_movie_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movies[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movies[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movies[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movies[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movies[4])
        st.image(recommended_movie_posters[4])
