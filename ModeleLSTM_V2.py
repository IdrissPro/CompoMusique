"""
READ ME

data=JDD()

exemple d'utilisation de la classe LSTM

reseau = LSTM(profondeurLSTM, data.nombreDeNotesPrecedentes, data.formatNote,dropout, batchNormalisation)
#ou 
#reseau = LSTM(profondeurLSTM) # par defaut nombreDeNotesPrecedentes=7, formatNote=2, dropout=False, batchNormalisation=False 

reseau.architecture()

reseau.entrainement(data, batch, epoch, epochPatience)
#ou
#reseau.entrainement(data, batch, epoch) # par defaut epochPatience=0 , il n'y a pas d'EarlyStopping

reseau.courbe_apprentissage()

RESULTAT=reseau.generation(X_initial, longueur)
"""
from Guillaume_JeuDeDonnees_V1 import JDD

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import InputLayer, LSTM, Dense, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping

def creationModele(profondeurLSTM, nombreDeNotesPrecedentes, formatNote, dropout, batchNormalisation):
        model = Sequential()
        model.add( InputLayer(input_shape=(nombreDeNotesPrecedentes, formatNote)) )
        model.add( LSTM(profondeurLSTM, activation='relu') )
        if dropout:
            model.add( Dropout(0.2) ) 
        if batchNormalisation:
            model.add( BatchNormalization() )
        model.add( Dense(formatNote) )
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model

class LSTM:
    def __init__(self, profondeurLSTM, nombreDeNotesPrecedentes=7, formatNote=2, dropout=False, batchNormalisation=False):
        self.profondeurLSTM = profondeurLSTM
        self.nombreDeNotesPrecedentes = nombreDeNotesPrecedentes
        self.formatNote = formatNote
        self.modele = creationModele(profondeurLSTM, nombreDeNotesPrecedentes, formatNote, dropout, batchNormalisation)
        self.historique = []
    
    def architecture(self):
        self.modele.summary()

    def entrainement(self, data, nombreDeBatch, nombreDeEpoch, nombreDeEpochPatient=0):
        if nombreDeEpochPatient!=0:
            early_stopping = EarlyStopping(
                min_delta=0.001, # quantité minimale considérable comme une amélioration
                patience=nombreDeEpochPatient,
                restore_best_weights=True,
            )
            history = self.modele.fit(
                data.X_train, data.y_train,
                validation_data=(data.X_test, data.y_test),
                batch_size=nombreDeBatch,
                epochs=nombreDeEpoch,
                callbacks=[early_stopping],
            )
        else:
            history = self.modele.fit(
                data.X_train, data.y_train,
                validation_data=(data.X_test, data.y_test),
                batch_size=nombreDeBatch,
                epochs=nombreDeEpoch,
            )
        self.historique = history
        return history
    
    def courbe_apprentissage(self):
        if ([]!=self.historique):
            history_df = pd.DataFrame(self.historique.history)
            history_df.loc[:, ['loss', 'val_loss']].plot()
            print("Erreur minimale atteinte : {}".format(history_df['val_loss'].min()))
        return 0

    def generation(self, X_initial, longueur):
        res=[ k for k in X_initial]
        for i in range(longueur):
            predictions = self.modele.predict(np.array(X_initial))
            res.append(predictions)
            X_initial = res[-self.nombreDeNotesPrecedentes:]
        return res
    
    def __str__(self):
        return "LSTM(profondeurLSTM={}, nombreDeNotesPrecedentes={}, formatNote={})".format(self.profondeurLSTM, self.nombreDeNotesPrecedentes, self.formatNote)