import pandas as pd
import pickle
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# fetching anime dataset
anime_d = pd.read_csv('anime.csv')


# Selecting columns that are needed
anime_dataset = anime_d[['MAL_ID', 'Name', 'Score', 'Genres', 'English name', 'Type', 'Episodes',
                         'Aired', 'Studios', 'Duration', 'Rating', 'Watching', 'Img_url', 'Link', 'Synopsis']]

# ==============================Data Cleaning============================
# drop null values
anime_dataset.dropna(inplace=True)

# fetching popular anime
popular_anime = anime_dataset.sort_values('Watching', ascending=False)[0:16]


# Machine learning concept starts
# first converting usable column to tags
# ==========================Data Preprocessing==========================
# Removing Commas
anime_dataset['Genres1'] = anime_dataset['Genres'].apply(
    lambda x: x.replace(",", ""))
anime_dataset['Studios1'] = anime_dataset['Studios'].apply(
    lambda x: x.replace(",", ""))
anime_dataset['Synopsis1'] = anime_dataset['Synopsis'].apply(
    lambda x: x.replace(",", ""))

# Converting string to list
anime_dataset['Genres1'] = anime_dataset['Genres1'].apply(
    lambda x: x.split(" "))
anime_dataset['Studios1'] = anime_dataset['Studios1'].apply(
    lambda x: x.split(" "))
anime_dataset['Synopsis1'] = anime_dataset['Synopsis1'].apply(
    lambda x: x.split(" "))

# Removing Spaces
anime_dataset['Genres1'] = anime_dataset['Genres1'].apply(
    lambda x: [i.replace(" ", "") for i in x])
anime_dataset['Studios1'] = anime_dataset['Studios1'].apply(
    lambda x: [i.replace(" ", "") for i in x])
anime_dataset['Synopsis1'] = anime_dataset['Synopsis1'].apply(
    lambda x: [i.replace(" ", "") for i in x])


# making tags with selected columns
anime_dataset['Tags'] = anime_dataset['Synopsis1'] + \
    anime_dataset['Genres1'] + anime_dataset['Studios1']

# making new dataframe
new_anime_dataframe = anime_dataset[['MAL_ID', 'Name', 'English name', 'Tags', 'Score',
                                     'Genres', 'Type', 'Episodes', 'Aired', 'Duration', 'Rating', 'Img_url', 'Link', 'Synopsis']]
new_anime_dataframe = new_anime_dataframe.sort_values('MAL_ID', ascending=True)

# anime_tv = new_anime_dataframe[new_anime_dataframe['Type'] == 'TV']


# converting tags to string format
new_anime_dataframe['Tags'] = new_anime_dataframe['Tags'].apply(
    lambda x: " ".join(x))

# converting to lower case
new_anime_dataframe['Tags'] = new_anime_dataframe['Tags'].apply(
    lambda x: x.lower())

# removing similer words
ps = PorterStemmer()


def stem(tags):
    L = []
    for i in tags.split():
        L.append(ps.stem(i))
    return " ".join(L)


new_anime_dataframe['Tags'] = new_anime_dataframe['Tags'].apply(stem)


# ==========================Training Model==========================
# converting tags to vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_anime_dataframe['Tags']).toarray()

# calculate similarity between vectors
similarity = cosine_similarity(vectors)

# ==========================Function==========================
# Function for anime recommendation


def recommend_anime(anime):
    anime = anime.lower()
    anime_index = new_anime_dataframe[(new_anime_dataframe['Name'].str.lower() == anime) | (
        new_anime_dataframe['English name'].str.lower() == anime)].index[0]

    distance_a = similarity[anime_index]
    anime_list = sorted(list(enumerate(distance_a)),
                        reverse=True, key=(lambda x: x[1]))[1:31]

    for i in anime_list:
        print(new_anime_dataframe.iloc[i[0]].Name)


# recommend_anime('one piece')

# ==========================Saving Model==========================

pickle.dump(new_anime_dataframe, open('anime_data.pkl', 'wb'))
pickle.dump(similarity, open('similarities.pkl', 'wb'))
pickle.dump(popular_anime, open('popular_anime.pkl', 'wb'))
