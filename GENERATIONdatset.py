import G_DATA

# PREND DU TEMPS A COMPILER, NE PAS LANCER POUR RIEN !!!!!!!!!!!!!!!!!

#Lecture des parametres depuis un dossier Midi
liste=G_DATA.lister_fichiersMIDI("./datasetMidi","datasetMidi")
listeMorceauxDATA = G_DATA.extractionMorceaux(liste)

# Enregistrement dans un fichier texte des morceaux et dans un fichier CSV des sequences lisibles par le reseau de neurones
G_DATA.creer_ecrire_fichier("datasetParMusiques.txt", str(listeMorceauxDATA))
G_DATA.enregistrementDatasetCSV( "dataset_16notes.csv", listeMorceauxDATA, longueurSequence=16 )

# jeu de données lisible par le reseau de neurones
G_DATA.conversionCSVtoCSV("./dataset_16notes.csv", "LSTM_16notes.csv")

# Création d'un MINI jeu de données (fichier texte de certains morceaux + fichier CSV d'un pourcentage de l'ensemble des données CSV)
# 10% du jeu de données
MINI_10_listeMorceauxDATA = G_DATA.pourcentageDeLaListe(listeMorceauxDATA, pourcentage=10, seed=42)
G_DATA.creer_ecrire_fichier("MINI_10_datasetParMusiques.txt", str(MINI_10_listeMorceauxDATA))
G_DATA.pourcentageFichierCSV("dataset_16notes.csv", "MINI_10_dataset_16notes.csv", pourcentage=10, seed=42)
G_DATA.pourcentageFichierCSV("./LSTM_16notes.csv", "MINI_10_LSTM_16notes.csv", pourcentage=10, seed=42)

# 1% du jeu de données
MINI_1_listeMorceauxDATA = G_DATA.pourcentageDeLaListe(listeMorceauxDATA, pourcentage=1, seed=42)
G_DATA.creer_ecrire_fichier("MINI_1_datasetParMusiques.txt", str(MINI_1_listeMorceauxDATA))
G_DATA.pourcentageFichierCSV("dataset_16notes.csv", "MINI_1_dataset_16notes.csv", pourcentage=1, seed=42)
G_DATA.pourcentageFichierCSV("./LSTM_16notes.csv", "MINI_1_LSTM_16notes.csv", pourcentage=1, seed=42)