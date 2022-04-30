from gcode_utilities import *
import music

#GLOBALS
lastAxis = "X"
lastDir = 1
#END GLOBALS    

def GCodeGenerateStepperFrequency(frequency: float, position: Position) -> str:
    """Generates a gcode file that moves the stepper to the given frequency and position

    Args:
        frequency (float): The frequency of the note
        position (Position): The position of the stepper

    Returns:
        str: GCode for the given frequency and position
    """    
    setFrequencyLength = position.toGCode(frequency)
    return setFrequencyLength
        
def GeneratePositionForNoteDuration(duration: float, currentPosition: Position, frequency: float) -> Position:
    """Generates a new position for the given note and its duration to match the duration of the note

    Args:
        duration (float): The duration of the note
        currentPosition (Position): The current position of the stepper
        frequency (float): The frequency of the note

    Returns:
        Position: The new position of the stepper
    """    
    
    global lastAxis
    global lastDir
    
    #Note Length in units?
    MagicNumberSeconds = 50
    offset = (duration * frequency) / MagicNumberSeconds
    
    if(lastAxis == "X"):
        generatedPosition = currentPosition + Position(offset * lastDir, 0, 0)
        if generatedPosition.x >= 150 or generatedPosition.x <= 0:
            lastDir *= -1
            generatedPosition = currentPosition + Position(offset * lastDir, 0, 0)
    else:

        generatedPosition = currentPosition + Position(0, offset * lastDir, 0)
        if generatedPosition.y >= 150 or generatedPosition.y <= 0:
            lastDir *= -1
            generatedPosition = currentPosition + Position(0, offset * lastDir, 0)
            
    
    return generatedPosition

def GCodePlayNotes(notes: list[tuple[str, float]]) -> str:
    """Generates a gcode file that plays the given notes and their durations

    Args:
        notes (list[tuple[str, float]]): List of notes and their durations

    Returns:
        str: GCode for the given notes and their durations
    """    
    noteTable = music.GenerateTwelveToneRange(baseFrequency=55)
    outputFrequenciesAndLengths = []
    
    for name, duration in notes:
        outputFrequenciesAndLengths.append((noteTable[name], duration))

    return GCodePlayFrequencies(notes)


def GCodePlayFrequencies(frequencies: list[tuple[float, float]]) -> str:
    """Generates a gcode file that plays the given frequencies and their durations

    Args:
        frequencies (list[tuple[float, float]]): List of frequencies and their durations
    Returns:
        str: GCode for the given frequencies and their durations
    """    
    gcodeOutput = "" 
    position = Position(0, 0, 0)
    
    for frequency, duration in frequencies:
        if(frequency == "sleep"):
            gcodeOutput += GCodeWait(duration)
        else:
            position = GeneratePositionForNoteDuration(duration, position, frequency)
            returnGcode = GCodeGenerateStepperFrequency(frequency, position)
            gcodeOutput += returnGcode
    
    return gcodeOutput


def GCodePlayScale() -> str:
    """Generates a gcode file that plays the chromatic scale for 47 notes

    Returns:
        str: GCode for the chromatic scale
    """    
    scale = list(zip(list(music.GenerateTwelveToneRange(nrOfNotes=47, names=True)), [1] * 47))
    return GCodePlayFrequencies(scale)