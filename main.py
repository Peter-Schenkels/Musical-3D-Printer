import win32file
from gcode_compiler import  GetGCodePrinterSetup, GCodePlayFrequencies
from music import MidoMidiFileToNotes


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
    
    usbDrives = locate_usb()
    dir = usbDrives[0] if len(usbDrives) > 0 else "C:\\"
    
    megalovania = MidoMidiFileToNotes("megalovania.mid")

    
    if(dir == "C:\\"):
        raise Exception("No USB drive found")
    else:
        print("USB drive found: " + dir)
        try:
            gcodeFile = open(dir + "test.gcode", "x")
        except FileExistsError:
            gcodeFile = open(dir +  "test.gcode", "w")

        gcodeFile.write(GetGCodePrinterSetup() + GCodePlayFrequencies(megalovania))
        gcodeFile.close()