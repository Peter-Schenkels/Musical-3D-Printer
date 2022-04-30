def GCodePosition(x: float, y: float, z: float, fast: bool) -> str:
    if(fast is True):
        return "G0 X" + str(x) + " Y" + str(y) + " Z" + str(z) + "\n"
    else:
        return "G1 X" + str(x) + " Y" + str(y) + " Z" + str(z) + "\n"
    
def GCodePositionSpeed(x: float, y: float, z: float, speed: float) -> str:
    return "G0 X" + str(x) + " Y" + str(y) + " Z" + str(z) + " F" + str(speed) + "\n"

def GCodeWait(time: float) -> str:
    return "G4 P" + str(time*1000) + "\n"

def GetGCodePrinterSetup() -> str:
    # resetExtruder = "G92 E0\n"
    # resetToHome = "G28\n"
    # setSpeed = "G1 Z2.0 F3000\n"
    # setExtruder = "M104 S" + str(0) + "\n"
    # setAbsolutePositioning = "G90\n"
    # setBed = "M140 S" + str(0) + "\n"
    # return resetExtruder + resetToHome + setSpeed + setExtruder + setAbsolutePositioning + setBed
    return "G92 E0\nG28\nG1 Z2.0 F3000\nM104 S0 \nG90\nM140 S0\n"
 
class Position:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z    

    def toGCode(self, speed) -> str:
        return GCodePositionSpeed(self.x, self.y, self.z, speed)
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)