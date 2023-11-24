import numpy as np
import pandas as pd
from keras.models import load_model
from spotify import Spotify
import pickle
from keras.utils import pad_sequences

def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))


def preprocess_cluster(cluster):
    return cluster.fillna(0).apply(pd.to_numeric)


def sort_clusters_by_proximity(df, cluster_id):
    target_cluster = df[df['cluster'] == cluster_id].iloc[0]
    distances = []

    for i, row in df.iterrows():
        if row['cluster'] != cluster_id:
            distance = euclidean_distance(target_cluster[1:], row[1:])  # Excluimos la columna 'cluster'
            distances.append((row['cluster'], distance))

    # Ordenar por la distancia
    distances.sort(key=lambda x: x[1])

    return distances


def generate_title(seed_text, sentiment):
    max_sequence_length=20
    model = load_model('title_builder.h5')

    with open('tokenizer.pkl', 'rb') as file:
        tokenizer = pickle.load(file)

    for _ in range(max_sequence_length):
        sequence = tokenizer.texts_to_sequences([seed_text])[0]
        sequence_padded = pad_sequences([sequence], maxlen=max_sequence_length, padding='post')
        
        # Predicción
        prediction = model.predict([sequence_padded, np.array([sentiment]).reshape(1, -1)])
        predicted_word_index = np.argmax(prediction, axis=-1)[0]
        predicted_word = tokenizer.index_word.get(predicted_word_index, '')

        # Verificar si el índice predicho corresponde a una palabra real
        if predicted_word:
            seed_text += " " + predicted_word
        else:
            break
        
        # Si se alcanza el final o el padding
        if predicted_word == 'end' or len(seed_text.split()) >= max_sequence_length:
            break
    
    return seed_text


# Cargar los datos
cluster_center = pd.read_csv("./data/cluster_center.csv")
clustered_data = pd.read_csv("./data/spotify_songs_clustered.csv")
songs_info = pd.read_csv("./data/spotify_songs_clustered_with_additional_info.csv")


unique_clusters = songs_info['cluster'].unique()


cluster_dataframes = {}
for cluster in unique_clusters:
    cluster_dataframes[cluster] = songs_info[songs_info['cluster'] == cluster]
    if cluster == -1:
        print(len(songs_info[songs_info['cluster'] == cluster]))

clustered_data.drop("cluster", inplace=True, axis=1)
clustered_data = preprocess_cluster(clustered_data)
for col in ['genre_edm', 'genre_latin', 'genre_pop', 'genre_r&b', 'genre_rap', 'genre_rock']:
    clustered_data[col] = clustered_data[col].astype('float32')

model = load_model('cluster_prediction.h5')

sample_data = clustered_data.sample(1)
print(sample_data)


prediction = model.predict(sample_data)


predicted_class = np.argmax(prediction)

original_sentiment = sample_data["lyrics_sentiment"]

cluster_belongs: pd.DataFrame = cluster_dataframes.get(predicted_class)
samples_songs = cluster_belongs.sample(15)
tracks_ids = samples_songs["track_id"].tolist()

token = input("Ingresa token de autenticación: ")
seed_text = input("Ingrese palabra para crear título playlist: ")
playlist_name = generate_title(seed_text, original_sentiment)


spotify: Spotify = Spotify()



spotify.create_playlist(token, playlist_name, tracks_ids) 