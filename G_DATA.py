from os import listdir
from os import path
import csv
import G_MIDI 
import random

# permet de lister les elements d'un dossier
def lister_fichiersMIDI(cheminDossierMIDI, nomDossierMIDI):
    try:
        # Obtient la liste des fichiers dans le dossier
        fichiers = [ "./"+nomDossierMIDI+"/"+f for f in listdir( cheminDossierMIDI ) if path.isfile( path.join( cheminDossierMIDI, f ) ) ]
        return fichiers
    except FileNotFoundError:
        print(f"Le dossier {nomDossierMIDI} n'existe pas.")
        return []

# depuis une liste de chemins vers des fichiers, midi, on extrait des parametres voulus de chaque morceaux
def extractionMorceaux(ListefichiersMIDI):
    ListeMorceaux = []
    i=1
    l=len(ListefichiersMIDI)
    for titre in ListefichiersMIDI:
        ListeMorceaux.append(  G_MIDI.lireParametresMIDI(titre)  )
        print("Fichier "+str(i)+"/"+str(l)+" extrait")
        i+=1
    return ListeMorceaux

# permet d'avoir une liste de N notes qui se suivent a partir d'une liste de notes de longueur quelconque
def extractionSequenceNotes(listeNotes, longueurSequence):
    tailleListe = len(listeNotes)
    i=0
    res = []

    while i+longueurSequence<=tailleListe:
        res.append( [ listeNotes[i:i+longueurSequence][j][k] for j in range(longueurSequence) for k in range(3) ] )
        i += random.randint(1,longueurSequence//2)

    return res

# a partir des parametres voulus de chaque morceaux, on extrait une liste de sequence de N notes consecutives
def generationDATASET(listeMorceauxDATA, longueurSequence):
    dataset = []
    for morceau in listeMorceauxDATA:
        for track in morceau:
            sequence =extractionSequenceNotes(track, longueurSequence) 
            if sequence != []:
                dataset+= sequence 
    return dataset

# a partir des parametres voulus de chaque morceaux, on enregistre dans un CSV une liste de sequence de N notes consecutives
def enregistrementDatasetCSV(nomFichierDataset, listeMorceauxDATA, longueurSequence):
    donnees = [["note_"+str(i+1)+"_"+str(j+1) for i in range(longueurSequence) for j in range(3) ]]
    donnees += generationDATASET(listeMorceauxDATA, longueurSequence)
    
    try:
        with open(nomFichierDataset, 'w', newline='') as fichier_csv:
            # Créer un objet writer CSV
            writer = csv.writer(fichier_csv)

            # Écrire les données dans le fichier CSV
            writer.writerows(donnees)

        print(f"Le fichier CSV '{nomFichierDataset}' a été créé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création du fichier CSV : {e}")
    return 0

# Permet d'enregistrer du texte dans un fichier texte
def creer_ecrire_fichier(nom_fichier, contenu):
    try:
        with open(nom_fichier, 'w') as fichier:
            fichier.write(contenu)
        print(f"Le fichier '{nom_fichier}' a été créé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création du fichier : {e}")

# permet de renvoyer N pourcent d'une liste, en initialisant une seed
def pourcentageDeLaListe(liste, pourcentage, seed=None):
    if seed is not None:
        random.seed(seed)

    nb_elements_a_selectionner = int(len(liste) * (pourcentage / 100.0))
    indices_selectionnes = random.sample(range(len(liste)), nb_elements_a_selectionner)
    elements_selectionnes = [liste[i] for i in indices_selectionnes]

    return elements_selectionnes

# permet de creer un CSV de N pourcent d'un autre CSV , en initialisant une seed
def pourcentageFichierCSV(nom_fichier_initial, nom_fichier_n_pourcent, pourcentage, seed=None):
    if seed is not None:
        random.seed(seed)

    # Lire le fichier CSV initial
    with open(nom_fichier_initial, 'r') as fichier_initial:
        lecteur_csv = csv.reader(fichier_initial)
        contenu_initial = list(lecteur_csv)

    # Sélectionner un pourcentage d'éléments aléatoires
    elements_selectionnes = [contenu_initial[0]] + pourcentageDeLaListe(contenu_initial[1:], pourcentage, seed)

    # Écrire les éléments sélectionnés dans le nouveau fichier CSV
    with open(nom_fichier_n_pourcent, 'w', newline='') as fichier_n_pourcent:
        ecrivain_csv = csv.writer(fichier_n_pourcent)
        ecrivain_csv.writerows(elements_selectionnes)

# permet de convertir un CSV de données en parametre X, Y pour le reseau de neurones
def conversionCSVtoCSV(fichierAlire, fichierAcreer):
    donnees = [['X', 'Y']]
    # Lire le fichier CSV
    with open(fichierAlire, 'r') as fichier_csv:
        lecteur_csv = csv.reader(fichier_csv)
        contenu_csv = list(lecteur_csv)
    # Regrouper les parametres d'une seule note
    for ligne in contenu_csv[1:]:  # Ignorer l'en-tête
        ligne = [int(x) for x in ligne]
        sequence_notes = [ligne[i:i+3] for i in range(0, len(ligne), 3)]
        donnees.append([sequence_notes[:-1],sequence_notes[-1]])
    try:
        with open(fichierAcreer, 'w', newline='') as fichier_csv:
            # Créer un objet writer CSV
            writer = csv.writer(fichier_csv)
            # Écrire les données dans le fichier CSV
            writer.writerows(donnees)

        print(f"Le fichier CSV '{fichierAcreer}' a été créé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création du fichier CSV : {e}")
    return 0