import math

def GCodePosition(x: float, y: float, z: float, fast: bool) -> str:
    if(fast is True):
        return "G0 X" + str(x) + " Y" + str(y) + " Z" + str(z) + "\n"
    else:
        return "G1 X" + str(x) + " Y" + str(y) + " Z" + str(z) + "\n"

def GCodeWait(time: float) -> str:
    return "G4 P" + str(time) + "\n"

def GetGCodePrinterSetup() -> str:
    resetExtruder = "G92 E0\n"
    resetToHome = "G28\n"
    setSpeed = "G1 Z2.0 F3000\n"
    setExtruder = "M104 S" + str(0) + "\n"
    setRelativePositioning = "G90\n"
    setBed = "M140 S" + str(0) + "\n"
    return resetExtruder + resetToHome + setSpeed + setExtruder + setRelativePositioning + setBed
    
    
def GCodeMoveCircle(x: float, y: float, z: float, radius: float, speed: float, fast: bool, numberOfCorners: int) -> str:
    outputGcode = ""
    
    #Generate Movements with stops in between
    for i in range(0, numberOfCorners):
        angle = i * (360 / numberOfCorners)
        xMovement = radius * math.cos(math.radians(angle))
        yMovement = radius * math.sin(math.radians(angle))
        outputGcode += GCodePosition(x + xMovement, y + yMovement, z, fast)
    
    return outputGcode


if __name__ == "__main__":
    try:
        gcodeFile = open("test.gcode", "x")
    except FileExistsError:
        gcodeFile = open("test.gcode", "w")
    
    gcodeFile.write(GetGCodePrinterSetup() + GCodeMoveCircle(125,125,10,62,3000,True,12 * 8))
    gcodeFile.close()