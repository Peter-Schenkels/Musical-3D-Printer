from re import S
import win32file
from gcode_compiler import  GetGCodePrinterSetup, GCodePlayFrequencies
from music import MidoMidiFileToNotes
import sys


def locate_usb() -> list[str]:
    """Locates all USB storage devices and returns their mount points

    Returns:
        list[str]: A list of all USB storage devices
    """    
    drive_list = []
    drivebits = win32file.GetLogicalDrives()
    for d in range(1, 26):
        mask = 1 << d
        if drivebits & mask:
            # here if the drive is at least there
            drname = '%c:\\' % chr(ord('A') + d)
            t = win32file.GetDriveType(drname)
            
            if t == win32file.DRIVE_REMOVABLE:
                drive_list.append(drname)
    return drive_list


def handle_args() -> tuple[str, str, bool]:
    """Handles the command line arguments

    Returns:
        tuple[str, str, bool]: The input file directory, output file directory, and whether to save to USB without knowing an output directory
    """
    
    inputMidiFileDirectory = ""
    outputDirectory = ""
    saveToUsb = False
    
    if len(sys.argv) == 1:
        print("Please give an input directory")
        exit()

    for i, arg in enumerate(sys.argv):
        if arg == "--help":
            print("Usage: musical_printer.py [input directory] [save to usb y/n] [output directory]")
            exit()
        if i == 1:
            inputMidiFileDirectory = arg
            if inputMidiFileDirectory == "":
                print("Please give an input directory")
                exit()
            
        elif i == 2:
            if arg in ["true", "True", "TRUE", "1", "yes", "Yes", "YES", "y", "Y", "t", "T"]:
                saveToUsb = True
        elif i == 3:
            outputDirectory = arg
            
   
        
    return inputMidiFileDirectory, outputDirectory, saveToUsb

def SaveToUsb(outputDirectory: str) -> str:
    """Saves the output file to a USB storage device

    Args:
        outputDirectory (str): The directory of the output file

    Returns:
        str: The path where the output file should be saved
    """    
    usbDrives = locate_usb()
    saveDirectory = usbDrives[0] + outputDirectory if len(usbDrives) > 0 else ""
    if(saveDirectory  == ""):
        print("No USB drive found")
        exit()    

    return saveDirectory


def MidiFileToGCodeFile(inputFileDirectory: str, outputFileDirectory: str) -> bool:
    """Converts a midi file from the input file directory to a gcode file and saves it to the output directory

    Args:
        inputFileDirectory (str): The directory of the input midi file
        outputFileDirectory (str): The directory of the output gcode file

    Returns:
        bool: Whether the operation was successful
    """    
    
    notes = MidoMidiFileToNotes(inputFileDirectory)
    try:
        gcodeFile = open(outputFileDirectory + "out.gcode", "x")
    except FileExistsError:
        gcodeFile = open(outputFileDirectory +  "out.gcode", "w")

    gcodeFile.write(GetGCodePrinterSetup() + GCodePlayFrequencies(notes))
    return gcodeFile.close()


if __name__ == "__main__":

    inputMidiFileDirectory, outputDirectory, saveToUsb = handle_args()
    
    if(saveToUsb is True):
        saveDirectory = SaveToUsb(outputDirectory)
    else:
        saveDirectory = outputDirectory   
    
    MidiFileToGCodeFile(inputMidiFileDirectory, saveDirectory)
