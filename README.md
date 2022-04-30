## Musical 3D Printer
A fun easy script that turns a midi file into a GCode file which a 3D printer can execute/play


### How to use
A quick overview of how to use this script.
```
#Installing the required packages
pip install -e .

#Running the script
python musical_printer.py [input directory] [save to usb y/n] [output directory]

#Argument: Input directory
#Input midi file

#Argument: save to usb
#This argument is optional. If this argument is Y/yes 
#than the script will automatically detect a connected usb 
#storage device and save it to the first one it detects.

#Argument: Output directory
#This argument is also optional. This argument is for manually 
#depicting the output file location. Note that the "save to usb" 
#argument must be N/no for it to work properly.
```

### Backlog
A list of things i want to add in the future. The higher on the list the higher the priority of the item.
* Polyphony  with multiple steppers
* Bass notes with the Z stepper
* Middle notes with the Y stepper
* High notes with the X stepper
* Better CML arguments
* Support for gliscando notes.
* Rythmic/Drum kit with Z stepper
* Printer DAW (impossible dream)