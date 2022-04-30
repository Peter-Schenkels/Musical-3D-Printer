def GCodePosition(x: float, y: float, z: float, fast: bool) -> str:
    """ Returns a GCode string that moves the printer to the given position.

    Args:
        x (float): The x position to move to.
        y (float): The y position to move to.
        z (float): The z position to move to.
        fast (bool): Whether to move fast or slow.

    Returns:
        str: The GCode string that moves the printer to the given position.
    """    
    if(fast is True):
        return "G0 X" + str(x) + " Y" + str(y) + " Z" + str(z) + "\n"
    else:
        return "G1 X" + str(x) + " Y" + str(y) + " Z" + str(z) + "\n"
    
def GCodePositionSpeed(x: float, y: float, z: float, speed: float) -> str:
    """ Returns a GCode string that moves the printer to the given position.

    Args:
        x (float): The x position to move to.
        y (float): The y position to move to.
        z (float): The z position to move to.
        speed (float): The speed to move at in mm/s.

    Returns:
        str: The GCode string that moves the printer to the given position.
    """    
    return "G0 X" + str(x) + " Y" + str(y) + " Z" + str(z) + " F" + str(speed) + "\n"

def GCodeWait(time: float) -> str:
    """ Returns a GCode string that waits for the given amount of time.

    Args:
        time (float): The amount of time to wait in seconds.

    Returns:
        str: The GCode string that waits for the given amount of time.
    """    
    return "G4 P" + str(time*1000) + "\n"

def GetGCodePrinterSetup() -> str:
    """ Returns the GCode string that sets up the printer.

    Returns:
        str: The GCode string that sets up the printer.
    """    
    # resetExtruder = "G92 E0\n"
    # resetToHome = "G28\n"
    # setSpeed = "G1 Z2.0 F3000\n"
    # setExtruder = "M104 S" + str(0) + "\n"
    # setAbsolutePositioning = "G90\n"
    # setBed = "M140 S" + str(0) + "\n"
    # return resetExtruder + resetToHome + setSpeed + setExtruder + setAbsolutePositioning + setBed
    return "G92 E0\nG28\nG1 Z2.0 F3000\nM104 S0 \nG90\nM140 S0\n"
 
class Position:
    """ Positions class that contains the x, y, and z coordinates of a position. """ 
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z    

    def toGCode(self, speed: float) -> str:
        """ Converts the position to a GCode string.

        Args:
            speed (float): The speed to move at in mm/s.

        Returns:
            str: The GCode string that moves the printer to the given position.
        """        
        return GCodePositionSpeed(self.x, self.y, self.z, speed)
    
    def __add__(self, other):
        """ Adds two positions together.

        Args:
            other (Position): The other position to add to this position.

        Returns:
            Position: The new position.
        """        
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)
        