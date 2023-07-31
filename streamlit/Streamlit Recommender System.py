import pickle
import streamlit as st
import pandas as pd
import numpy as np
import requests


def fetch_poster(movie_id):
    """
    getting poster path by movie id to display
    :param movie_id:
    :return poster path:
    """
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ac18249437531722f17508f69f817dda".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    print('Poster path fetched:', full_path)
    return full_path


@st.cache_resource
def initialize(state):
    """
    loading data and similarity matrix
    :param state:
    :return dataset, similarity matrix, indices matrix, movies list:
    """
    print('Start loading dependencies')
    data_dir = 'model/data.pkl'
    movies = pickle.load(open(data_dir, 'rb'))
    model_dir = 'model/similarity.pkl'
    similarity = pickle.load(open(model_dir, 'rb'))
    indices = pd.Series(movies.index, index=movies['title'])
    movie_list = movies['title'].values
    print('Loading dependencies completed')
    return movies, similarity, indices, movie_list


def recommend(title, rank):
    """
    Our main function to recommend movies
    :param titles:
    :param ranks:
    :return Top 5 movies:
    """
    idx = []
    for m in title:
        if type(indices[m]) == np.int64:
            idx.append(indices[m])
        else:
            idx.append(indices[m][0])
    lst = []
    counter = 0
    for i in idx:
        sim_scores = list(enumerate(similarity[i]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]

        # ranking
        l = [(ss[0], ss[1] * rank[counter] / 10) for ss in sim_scores]
        counter += 1
        sim_scores = l

        for j in sim_scores:
            if j[0] not in idx:
                lst.append(j)
    # sort
    lst.sort(key=lambda x: x[1], reverse=True)
    l = [i[0] for i in lst]
    movie_indices = l
    return movies['title'].iloc[list(dict.fromkeys(movie_indices))][0:5]


movies, similarity, indices, movie_list = initialize(0)
st.header('Movie Recommender System')
selected_movies = st.multiselect("Type or select movies from the dropdown", movie_list)
ranks = st.multiselect("Type or select rank for the movies", [str(i)[:3] for i in np.arange(0, 10.1, 0.1)])
ranks = [float(rank) for rank in ranks]

if st.button('Show Recommendation'):
    recommended_movie_names = []
    for i in recommend(selected_movies, ranks):
        recommended_movie_names.append(i)
    recommended_movie_posters = []
    for title in recommended_movie_names:
        id_m = int(movies[movies['title'] == title]['id'].values[0])
        recommended_movie_posters.append(fetch_poster(id_m))
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

