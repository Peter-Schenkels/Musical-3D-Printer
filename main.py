from ast import operator
import math

def GCodePosition(x: float, y: float, z: float, fast: bool) -> str:
    if(fast is True):
        return "G0 X" + str(x) + " Y" + str(y) + " Z" + str(z) + "\n"
    else:
        return "G1 X" + str(x) + " Y" + str(y) + " Z" + str(z) + "\n"
    
def GCodePositionSpeed(x: float, y: float, z: float, speed: float) -> str:
    return "G0 X" + str(x) + " Y" + str(y) + " Z" + str(z) + " F" + str(speed) + "\n"

def GCodeWait(time: float) -> str:
    return "G4 P" + str(time) + "\n"

def GetGCodePrinterSetup() -> str:
    resetExtruder = "G92 E0\n"
    resetToHome = "G28\n"
    setSpeed = "G1 Z2.0 F3000\n"
    setExtruder = "M104 S" + str(0) + "\n"
    setAbsolutePositioning = "G90\n"
    setBed = "M140 S" + str(0) + "\n"
    return resetExtruder + resetToHome + setSpeed + setExtruder + setAbsolutePositioning + setBed
    
class Position:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z    

    def toGCode(self, speed) -> str:
        return GCodePositionSpeed(self.x, self.y, self.z, speed)
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)

def GCodeGenerateStepperFrequency(frequency: float, length: int, position: Position) -> str:
    newPosition = position + Position(length, 0, 0)
    setFrequencyLength = newPosition.toGCode(frequency)
    return setFrequencyLength, newPosition

def GCodeTestRange(startPosition: Position, nrOfOctaves:int) -> str:
    startFrequency = 8
    gcodeOutput = "" 
    position = startPosition
    
    for i in range(0, nrOfOctaves):
        startFrequency *= 2
        newGCode, position = GCodeGenerateStepperFrequency(startFrequency, 2, position)
        gcodeOutput += newGCode
    
    return gcodeOutput
        

def GenerateTwelveToneRange(nrOfNotes:int=47, baseFrequency:float=55) -> list[float]:
    baseFrequency = 27.5
    outputFrequencies = []
    for i in range(0, nrOfNotes):
        outputFrequencies.append(baseFrequency * math.pow(2, i/12))
    return outputFrequencies

def GCodePlayFrequencies(frequencies: list[float]) -> str:
    gcodeOutput = "" 
    position = Position(0, 0, 0)
    
    for frequency in frequencies:
        returnGcode, position = GCodeGenerateStepperFrequency(frequency, 1, position)
        gcodeOutput += returnGcode
    
    return gcodeOutput

def GCodeMoveCircle(x: float, y: float, z: float, radius: float, speed: float, fast: bool, numberOfCorners: int) -> str:
    outputGcode = ""
    
    #Generate Movements with stops in between
    for i in range(0, numberOfCorners):
        angle = i * (360 / numberOfCorners)
        xMovement = radius * math.cos(math.radians(angle))
        yMovement = radius * math.sin(math.radians(angle))
        outputGcode += GCodePosition(x + xMovement, y + yMovement, z, fast)
    
    return outputGcode 

def GCodeGenerateMultipleCircles(x: float, y: float, z: float, radius: float, speed: float, fast: bool, numberOfCircles: int) -> str:   
    circleGcode = ""
    
    for i in range(0, numberOfCircles):
        circleGcode += GCodeMoveCircle(x, y, z, i, speed, fast, 24)
        circleGcode += GCodeWait(0.5)

    return circleGcode


if __name__ == "__main__":
    for i in GenerateTwelveToneRange():
        print(i)
    
    try:
        gcodeFile = open("test.gcode", "x")
    except FileExistsError:
        gcodeFile = open("test.gcode", "w")
    
    gcodeFile.write(GetGCodePrinterSetup() + GCodePlayFrequencies(GenerateTwelveToneRange(120)))
    gcodeFile.close()