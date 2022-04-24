import math
from pickle import TRUE
from mido import MidiFile


def ParseMidiFileToNotes(midiFile:MidiFile) -> list[tuple[str, float]]:
    notes = []
    currentTime = 0
    MidiNoteState = {}
    noNotesPlayingTime = 0
    noNotesPlaying = True
    
    for message in midiFile:  
        
        currentTime += message.time
        
        #If no notes are playing
        if len(MidiNoteState) == 0:
            noNotesPlayingTime += message.time
            noNotesPlaying = True        
        else:
            if noNotesPlaying is True:
                if noNotesPlayingTime > 0:
                    notes.append(("sleep", noNotesPlayingTime))
            noNotesPlaying = False
            noNotesPlayingTime = 0
        
        #Which notes are playing?
        if message.type == "note_on":   
            MidiNoteState[message.note] = currentTime
        elif message.type == "note_off":
            notes.append((message.note, (currentTime - MidiNoteState[message.note])))
            del MidiNoteState[message.note]
    
    return notes

def MidoMidiFileToNotes(fileDirectory) -> list[tuple[str, float]]:
    
    midiFile = MidiFile(fileDirectory)
    notes = ParseMidiFileToNotes(midiFile)
    lookupNoteFrequencies = GenerateTwelveToneRange(nrOfNotes=47)
    outputNotes = []
    
    for note in notes:
        if(note[0] == "sleep"):
            outputNotes.append(("sleep", note[1]))
        else:
            outputNotes.append((lookupNoteFrequencies [note[0]] , note[1]))
    return outputNotes


def GenerateTwelveToneRange(nrOfNotes:int=47, baseFrequency:float=55) -> list[float]:
    frequencies = []
    for noteNr in range(0, nrOfNotes):
        noteFrequency = baseFrequency * math.pow(2, noteNr/12)
        frequencies.append(noteFrequency)

    return frequencies
    
def GenerateTwelveToneRangeNames(nrOfNotes:int=47, baseFrequency:float=55) -> dict[float, str]:
    frequencies = []
    notenames = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    for noteNr in range(0, nrOfNotes):
        noteFrequency = baseFrequency * math.pow(2, noteNr/len(notenames))
        octaveNr = int(noteNr / len(notenames))
        currentNote = notenames[noteNr % len(notenames)]
        generatedNoteName = currentNote + str(octaveNr)
        frequencies.append((noteFrequency, generatedNoteName))
 
    return dict(frequencies)

