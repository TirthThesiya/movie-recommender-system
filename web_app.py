import streamlit as st
import pickle
import requests

movies = pickle.load(open('movies.pkl','rb'))
movies_list1 = movies['title'].values
similarity = pickle.load(open('similarity.pkl','rb'))

def poster(movie_id):
  response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=12804ad378a8ba3bd3da09faac00798a&language=en-US'.format(movie_id))
  data = response.json()
  return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]

    recomended_movies = []
    recomended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fecthing poster from API
        recomended_movies_posters.append(poster(movie_id))
        recomended_movies.append (movies_list1) 
    return recomended_movies,recomended_movies_posters

# movies = pd.DataFrame(movies_dict)

st.title("Movie Recomender System 👉")

Selected_movies_name = st.selectbox('Search',movies_list1)

if st.button('RECOMMEND'):
    names,posters = recommend(Selected_movies_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    col_list = [col1,col2,col3,col4,col5]
  
    for i in col_list:
        with i:
            st.image(posters[col_list.index(i)])
