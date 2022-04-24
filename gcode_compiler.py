from gcode_utilities import *
import music

#GLOBALS
lastAxis = "X"
lastDir = 1
#END GLOBALS    

def GCodeGenerateStepperFrequency(frequency: float, position: Position) -> str:
    setFrequencyLength = position.toGCode(frequency)
    return setFrequencyLength
        
def GeneratePositionForNoteDuration(duration: float, currentPosition: Position, frequency: float) -> Position:
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
    noteTable = music.GenerateTwelveToneRange(baseFrequency=55)
    outputFrequenciesAndLengths = []
    
    for name, duration in notes:
        outputFrequenciesAndLengths.append((noteTable[name], duration))

    return GCodePlayFrequencies(notes)


def GCodePlayFrequencies(frequencies: list[tuple[float, float]]) -> str:
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
    scale = list(zip(list(music.GenerateTwelveToneRangeNames(nrOfNotes=47)), [1] * 47))
    return GCodePlayFrequencies(scale)