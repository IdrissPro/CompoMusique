"""
READ ME
Dans ce fichier nous retrouvons :
    - les paramètres du dataset
    - la création du modèle LSTM
    - l'entrainement du modèle
    - la génération de 20 notes qui suivent les 7 notes données en entrée du modèle entrainé
"""

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import InputLayer, LSTM, Dense, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping
import G_DATA

# ------------------------------
# Paramètres du Dataset
# ------------------------------
"""
dataset = G_DATA.csvToList("MINI_1_dataset_16notes.csv")

pourcentage_entrainement = 70
seed = 42

dataset_entrainement = G_DATA.pourcentageDeLaListe(dataset, pourcentage_entrainement, seed)
dataset_test = [x for x in dataset if x not in dataset_entrainement]

X_train=np.array([x[:-1] for x in dataset_entrainement])
y_train=np.array([x[-1] for x in dataset_entrainement])

X_test=np.array([x[:-1] for x in dataset_test])
y_test=np.array([x[-1] for x in dataset_test])

input_shape = [X_train.shape[1]]

nombreDeNotesPrecedentes = len(X_train[0]) # nombre de notes précédentes à prendre en compte
formatNote = len(X_train[0][0]) # valeur de la note, durée, durée avant prochaine note"""

# ------------------------------
# Paramètres du Dataset
# ------------------------------

G_DATA.conversionCSVtoCSV("./dataset_16notes.csv", "LSTM_16notes.csv")
dataset = pd.read_csv("./LSTM_16notes.csv")
df = dataset.copy()

df_train = df.sample(frac=0.7, random_state=0)
df_valid = df.drop(df_train.index)

X_train = df_train['X']
X_test = df_valid['X']
y_train = df_train['Y']
y_test = df_valid['Y']

nombreDeNotesPrecedentes = len(X_train[0]) # nombre de notes précédentes à prendre en compte
formatNote = len(X_train[0][0]) # valeur de la note, durée, durée avant prochaine note

# ------------------------------
# Création du modèle
# ------------------------------
nombreDeNeurones = 20       # nombre de neurones dans la couche LSTM
nombreDeBatch = 1           # nombre de subdivisions du jeu de données
nombreDeEpoch = 1           # nombre de fois que l'on va parcourir le jeu de données
nombreDeEpochPatient = 5    # nombre d'epoch sans amélioration avant d'arrêter l'apprentissage
dropout=False
batchNormalisation=False

# Création d'un modèle séquentiel
model = Sequential()

# Couche d'entrée
model.add( InputLayer(input_shape=(nombreDeNotesPrecedentes, formatNote)) )
# Couche LSTM
model.add( LSTM(nombreDeNeurones, activation='relu') )
# Dropout de 20% qui sert à éviter le surapprentissage
if dropout:
    model.add( Dropout(0.2) ) 
# Batch Normalisation qui sert à normaliser les données d'entrée dans les différents batchs
if batchNormalisation:
    model.add( BatchNormalization() )
# Couche de sortie
model.add( Dense(formatNote) )
# Compilation du modèle avec 
#   - la fonction de perte d'erreur quadratique moyenne
#   - l'optimiseur 'adam' qui est une descente de gradient stochastique à pas adaptatif
model.compile(loss='mean_squared_error', optimizer='adam')


# Afficher le résumé du modèle
model.summary()


# ------------------------------
# Apprentissage sur nos données
# ------------------------------
# Callback pour arrêter l'apprentissage si la perte ne diminue plus
early_stopping = EarlyStopping(
    min_delta=0.001, # quantité minimale considérable comme une amélioration
    patience=nombreDeEpochPatient,
    restore_best_weights=True,
)

# Entrainement du modèle
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    batch_size=nombreDeBatch,
    epochs=nombreDeEpoch,
    callbacks=[early_stopping],
)


# Afficher la courbe d'apprentissage
history_df = pd.DataFrame(history.history)
history_df.loc[:, ['loss', 'val_loss']].plot()
print("Erreur minimale atteinte : {}".format(history_df['val_loss'].min()))


"""
# Sauvegarder le modèle dans un fichier HDF5
model.save('modele_lstm.h5')

from keras.models import load_model

# Charger le modèle à partir du fichier HDF5
loaded_model = load_model('modele_lstm.h5')


# ------------------------------
# Génération de 20 notes à partir de nombreDeNotesPrecedentes = 7 notes
# ------------------------------
X_prediction = [] # len(X_prediction) = nombreDeNotesPrecedentes
res=[ k for k in X_prediction]
for i in range(20):
    predictions = loaded_model.predict(np.array(X_prediction))
    res.append(predictions)
    X_prediction = res[-nombreDeNotesPrecedentes:]
print(res)"""