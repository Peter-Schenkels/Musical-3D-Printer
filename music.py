import math
from pickle import TRUE
from mido import MidiFile


def ParseMidiFileToNotes(midiFile:MidiFile) -> list[tuple[str, float]]:
    """Parses a midi file to a list of notes and their durations

    Args:
        midiFile (MidiFile): The midi file to parse

    Returns:
        list[tuple[str, float]]: List of notes and their duration
    """    
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

def MidoMidiFileToNotes(fileDirectory: str) -> list[tuple[str, float]]:
    """Converts a midi file to a list of notes and their durations

    Args:
        fileDirectory (str): The directory of the midi file

    Returns:
        list[tuple[str, float]]: List of notes and their duration
    """    
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


def GenerateTwelveToneRange(nrOfNotes:int=47, baseFrequency:float=55, names:bool=False) -> list[float] or dict[float, str]:
    """Generates a list of frequencies for the twelve tones in the western harmonic system

    Args:
        nrOfNotes (int, optional): Nr of notes to generate form the base frequency. Defaults to 47.
        baseFrequency (float, optional): Starting frequency. Defaults to 55.
        names (bool, optional): Wether names shoudl be included in the list of frequencues. Defaults to False.

    Returns:
        list[float]: List of frequencies
        dict[float, str]: Dictionary of frequencies and names
    """    
    frequencies = []
    notenames = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    for noteNr in range(0, nrOfNotes):
        noteFrequency = baseFrequency * math.pow(2, noteNr/len(notenames))
        if(names is True):
            octaveNr = int(noteNr / len(notenames))
            currentNote = notenames[noteNr % len(notenames)]
            generatedNoteName = currentNote + str(octaveNr)
            frequencies.append((noteFrequency, generatedNoteName))
        else:
            frequencies.append(noteFrequency)

    if names is True:
        return dict(frequencies)
    else:
        return frequencies
    
