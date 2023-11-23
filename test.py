import pickle
from keras.utils import pad_sequences
import numpy as np
from keras.models import load_model




def generate_title(seed_text, sentiment, tokenizer, model, max_sequence_length):
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


model = load_model('title_builder.h5')

with open('tokenizer.pkl', 'rb') as file:
    tokenizer = pickle.load(file)


# Preparar el texto semilla y el valor de sentimiento
seed_text = "TOP"
sentiment_value = 0.9  # Asumiendo que los sentimientos están normalizados entre 0 y 1
max_sequence_length = 20
# Generar el título
generated_title = generate_title(seed_text, sentiment_value, tokenizer, model, max_sequence_length)

# Imprimir el título generado
print("Título generado:", generated_title)