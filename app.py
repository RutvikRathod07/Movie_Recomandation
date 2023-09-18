import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict1.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)

def fetch_poster(movie_id):
    responce=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e1081f4a49f44134e421cdef27614d25&language=en-US'.format(movie_id))
    data=responce.json()
    return 'https://image.tmdb.org/t/p/w500'+data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    movie_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
    recommanded_movies = []
    recommanded_movies_posters = []
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommanded_movies.append(movies.iloc[i[0]].title)
         #fetch poster from api
        recommanded_movies_posters.append(fetch_poster(movie_id))
    return recommanded_movies,recommanded_movies_posters


if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1,col2,col3,col4,col5=st.columns(5)
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
