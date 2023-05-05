#!/usr/bin/env python
# coding: utf-8

# In[5]:


#importing the required dependencies
import pandas as pd 
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[6]:


movies_data=pd.read_csv('C:/Users/ankit/Downloads/movies.csv')


# In[7]:


#selecting relevent features from the dataset for recommendation 
selected_features = ['genres','keywords','tagline','cast','director']
print(selected_features)


# In[8]:


#replacing null values with null string for the required columns
for features in selected_features:
  movies_data[features] = movies_data[features].fillna('')


# In[9]:


combined_features=movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']


# In[10]:


vectorizer = TfidfVectorizer()


# In[11]:


feature_vectors=vectorizer.fit_transform(combined_features)


# In[12]:


similarity = cosine_similarity(feature_vectors)


# In[13]:


movie_name = input(' Enter the movie you want to watch :')


# In[14]:


list_of_all_titles=movies_data['title'].tolist()
print(list_of_all_titles)


# In[15]:


find_close_match = difflib.get_close_matches(movie_name,list_of_all_titles)
print(find_close_match)


# In[16]:


close_match = find_close_match[0]
print(close_match)


# In[17]:


index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
print(index_of_the_movie)


# In[18]:


similarity_score = list(enumerate(similarity[index_of_the_movie]))
print(similarity_score)


# In[19]:


#sorting movies based on similarity score
sorted_similar_movies = sorted(similarity_score,key = lambda x:x[1],reverse = True)


# In[20]:


#printing names of similar movies based on the index 
print('Movies suggested for you : \n')
i = 1

for movie in sorted_similar_movies:
  index = movie[0]
  title_from_index = movies_data[movies_data.index==index]['title'].values[0]
  if(i<30):
    print(i,'.',title_from_index)
    i+=1


# In[21]:


movie_name = input(' Enter the movie you want to watch :')
list_of_all_titles = movies_data['title'].tolist()
find_close_match = difflib.get_close_matches(movie_name,list_of_all_titles)
close_match = find_close_match[0]
index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
similarity_score = list(enumerate(similarity[index_of_the_movie]))
sorted_similar_movies = sorted(similarity_score,key = lambda x:x[1],reverse = True)
print('Movies suggested for you : \n')
i = 1

for movie in sorted_similar_movies:
  index = movie[0]
  title_from_index = movies_data[movies_data.index==index]['title'].values[0]
  if(i<30):
    print(i,'.',title_from_index)
    i+=1


# In[ ]:




