import win32file
from gcode_compiler import  GetGCodePrinterSetup, GCodePlayFrequencies
from music import MidoMidiFileToNotes
import sys


def locate_usb():
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


if __name__ == "__main__":

    inputMidiFileDirectory = ""
    outputDirectory = ""
    saveToUsb = False
    notes = []

    if len(sys.argv) == 0:
        print("Please give an input directory")
        exit()

    for i, arg in enumerate(sys.argv):
        if arg == "help":
            print("Usage: musical_printer.py [input directory] [save to usb] [output directory]")
            exit()
        if i == 0:
            inputMidiFileDirectory = arg
            if inputMidiFileDirectory == "":
                print("Please give an input directory")
                exit()
            notes = MidoMidiFileToNotes(inputMidiFileDirectory)
        elif i == 1:
            if i in ["true", "True", "TRUE", "1", "yes", "Yes", "YES", "y", "Y", "t", "T"]:
                saveToUsb = True
        elif i == 2:
            outputDirectory = arg

    
    if saveToUsb == True:
        usbDrives = locate_usb()
        saveDirectory = usbDrives[0] + outputDirectory if len(usbDrives) > 0 else ""
        if(saveDirectory  == ""):
            print("No USB drive found")
            exit()    
    else:
        saveDirectory = outputDirectory

    
   
    
    try:
        gcodeFile = open(saveDirectory + "test.gcode", "x")
    except FileExistsError:
        gcodeFile = open(saveDirectory +  "test.gcode", "w")

    gcodeFile.write(GetGCodePrinterSetup() + GCodePlayFrequencies())
    gcodeFile.close()