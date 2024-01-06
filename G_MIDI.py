"""
TEST DE ECRITURE/LECTURE D'UN FICHIER MIDI

velocity :  volume sonore (au debut / à la fin, variation du volume entre les deux)
time :      duree avant que la tache ne s'execute
program :   instrument (0-127)
note :      note MIDI  (0-127)

"""
import os
import time
import mido
from mido import Message, MidiFile, MidiTrack

# ---------------------
# FONCTIONS
# ---------------------
# enregistre le morceau dans un fichier midi, et renvoie la duree du morceau
def ecritureFichierMIDI(Morceau, nomFichier): 
    #---#
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', program=64, time=0))  # program=instrument
    track.append(Message('note_on', note = Morceau[0][0], velocity = 100, time = 0))  # On lance la première note
    #---#
    i=0
    currentTime =0
    nextDebutNote = 0
    NextAction = []
    #---#
    while i<=len(Morceau)-1 or NextAction!=[]:
        #---#
        if i<len(Morceau)-1: 
            NextAction += [ [nextDebutNote + Morceau[i][1], i, False] , [nextDebutNote + Morceau[i][2], i+1, True] ]
            NextAction = sorted( NextAction )
            nextDebutNote += Morceau[i][2]
            i+=1
        elif i==len(Morceau)-1:
            NextAction += [ [nextDebutNote + Morceau[i][1], i, False] ] 
            i+=1 # permet de sortir du cas i<=len(Morceau)-1
        #---#
        j=0
        NextActionTime = NextAction[0][0]
        #---#
        while j<len(NextAction) and NextActionTime==NextAction[j][0]:
            if NextAction[j][2]:
                track.append(Message('note_on', note = Morceau[NextAction[j][1]][0], velocity = 100, time = NextActionTime - currentTime ))
            else:
                track.append(Message('note_off', note = Morceau[NextAction[j][1]][0], velocity = 0, time = Morceau[NextAction[j][1]][1] ))
            j+=1
        #---#
        currentTime = NextActionTime
        NextAction = NextAction[j:]
        #---#
    mid.save(nomFichier) 
    return currentTime

# extrait pour chaque note sa valeur, durée , attente avant prochaine note
def lireParametresMIDI(midi_file_path):
    fichierDATA = []

    with mido.MidiFile(midi_file_path) as midi_file:
        for track in midi_file.tracks:
            listeTrack = []

            i = 0
            while i < len(track):
                if  (track[i].type == 'note_on' and track[i].velocity != 0): # S'il s'agit bien d'un début de note
                    note = [track[i].note, 0, 0]
                    bool1, bool2 = True, True # la note n'est pas arrété, la prochaine note n'a pas commencé
                    j = i + 1

                    temps_i_j = 0

                    while j < len(track) and (bool1 or bool2):
                        if bool1 and (track[j].type == 'note_off' or (track[j].type == 'note_on' and track[j].velocity == 0)) and (track[j].note == note[0]) :
                            note[1] = temps_i_j + track[j].time  # Durée de la note
                            bool1 = False
                        elif bool2 and (track[j].type == 'note_on' and track[j].velocity != 0):
                            note[2] = temps_i_j + track[j].time  # Durée avant la prochaine note
                            bool2 = False
                        try:
                            temps_i_j+=track[j].time
                        except Exception as e:
                            print("Il n'y a pas de donnée 'time' dans le message MIDI")
                        j += 1

                    listeTrack.append(note)
                i += 1

            fichierDATA.append(listeTrack)

    return fichierDATA


def jouerFichierMIDI(path):
    print("DebutLectureMIDI\n")
    periph_sortie = mido.get_output_names()
    print("ICIC ", periph_sortie)
    port = mido.open_output(periph_sortie[0])
    mid = MidiFile(path)
    for msg in mid.play():  # boucle de lecture du fichier Midi
        port.send(msg)      # envoi fichier Midi port MidO-OUT vers peripherique
    port.close()            # ferme proprement le port Midi
    print("\nFinLectureMIDI")
    return 0

def dureeFichierMIDI(path):
    mid = MidiFile(path)
    return time.strftime('%Hh:%Mm:%Ss', time.gmtime(mid.length))

def texteFichierMIDI(path):
    return MidiFile(path)
