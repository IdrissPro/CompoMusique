"""
TEST DE ECRITURE/LECTURE D'UN FICHIER MIDI

velocity :  volume sonore (au debut / à la fin, variation du volume entre les deux)
time :      duree avant que la tache ne s'execute
program :   instrument (0-127)
note :      note MIDI  (0-127)

"""

import mido
import time
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


def lireParametresMIDI(midi_file_path):
    #---#
    fichierDATA = []
    #---#
    with mido.MidiFile(midi_file_path) as midi_file:
        #---#
        for track in midi_file.tracks: 
            #---#
            listeTrack=[]
            i=0
            while (i<len(track)):
                #---#
                j=i+1
                if track[i].type == 'note_on':
                    Note = [track[i].note, 0, 0]
                    bool1, bool2 = True,True
                    while ( j<len(track) and (bool1 or bool2) ):
                        #---#
                        if bool1 and track[j].type == 'note_off' and track[j].note == Note[0]:
                            Note[1]=track[j].time  #duree de la note
                            bool1=False
                        elif bool2 and track[j].type == 'note_on':
                            Note[2]=track[j].time + Note[1] #duree avant la prochaine note 
                            bool2=False
                        j+=1
                        #---#
                    listeTrack.append(Note)
                #---#
                i+=1
            #---#
            fichierDATA.append(listeTrack)
        #---#
    return fichierDATA

def jouerFichierMIDI(path):
    print("DebutLectureMIDI\n")
    periph_sortie = mido.get_output_names()
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

# ---------------------
# DATA
# ---------------------

# Jeu d'Exemple [valeurNote, dureeNote, AttenteAvantProchaineNote]
#Morceau = [[70, 256, 0], [71, 256, 257],[72, 256, 257], [73, 256, 0]]

valeurNote = [74,71,67,69,71,67,69,
              74,71,67,69,67,71,69,
              74,72,71,69,67,69,72,71,69,
              74,71,69,67,69,71,67,74]

dureeNote = [1.0,1.0,2.0,1.0,0.5,0.5,2.0,
             1.0,1.0,2.0,1.0,0.5,0.5,2.0,
             1.0,1.0,1.0,0.5,0.5,1.0,1.0,1.0,1.0,
             0.5,0.5,0.5,0.5,1.0,1.0,2.0,2.0] # 4x8 temps

Morceau = [[valeurNote[i], int(256 *dureeNote[i]), int(256 *dureeNote[i])+1] for i in range(len(valeurNote))]
Morceau[-1][2]=0

# ---------------------
# TESTS
# ---------------------
path = './V3.mid'
ecritureFichierMIDI(Morceau, path)
print("verif    :", Morceau==lireParametresMIDI(path)[0])