

### Identificadores

- track_id (string)
- track_album_id (string)	
- playlist_id (string)

### Características

- track_artist (string)
- language (string)

### Características especiales
- track_popularity (numerico)
- track_album_release_date (date)

### Atributos de análisis de sentimientos

- track_name (string)
- track_album_name	(string)


### Características para K-means

- playlist_genre (string)
- playlist_subgenre (string)
- energy (numeric)
- key(numeric)  - The estimated overall key of the track. Integers map to pitches using standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.
- loudness(numeric) - double

- mode(numeric) - Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.

- speechiness (numeric)
- acousticness (numeric)
- instrumentalness (numeric)
- valence (numeric) - A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
- tempo (numeric)


### Aparentemente poco utiles
- liveness