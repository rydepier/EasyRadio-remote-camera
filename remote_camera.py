# Raspberry Pi remote camera unit using LPRS ERA Connect2Pi USB radio modules
# This python program runs on the Pi, acting as a slave unit.
# commands are sent from a PC base station running a control panel
# There are two User buttons and code can be added as required to this program
# plain text can be sent from the base station and this can easilly be interpreted as a command
# The text sent by the ERA module is limited to 180 characters.

# Chris Rouse February 2015


import serial
import os
import os.path

# Check to see if a string is a valid number
def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        print "This is not a number"
        ser.write("Wrong data entered")
        return False

# image varaibles
imagePath = ""
imageName = ""
imageCounter = 0
imageCounterFormatted = 0
# video variables
videoName = ""
videoPath = ""
videoRunTime = "5000" # 5 seconds
videoCounter=0
videoCounterFormatted = 0 
# time lapse variables
tlName = "timelapse_%04d.jpg"
tlPath = ""
runTime = "180000" # 3 minutes
interval = "30000" # 30 seconds
# general variables 
flip = False
osString  = ""
tempString = ""
a = 0

# image directory, change as required
imageDirectory = "/media/PI8GB/images/"
timelapseDirectory = "/media/PI8GB/timelapse/"
videoDirectory = "/media/PI8GB/video/"
#

# set up the serial port, this will be ttyUSB0 for the easy radio
ser = serial.Serial("/dev/ttyUSB0", 19200, timeout = 0.5)


print "Raspberry Pi Remote Camera Control using easyRadio ERA Connect2Pi Modules"
print ""
print ""
 
# main loop
while True:
    numbytes = ser.inWaiting()
    incomming = ""
    if numbytes >0: # wait for a singnal to come in
    # easyRadio sends up to 180 characters
        incomming = ser.read(180) # read in up to 180 characters
        if incomming != "":
            incomming = incomming.upper() # convert to uppercase
            print(incomming)

        # now check for commands

            if incomming == "PRINT":
                print("Takes a single picture")
                imageCounterFormatted = "%04d" % imageCounter
                imageName = "image_" + str(imageCounterFormatted) + ".jpg"
                print imageName
                imagePath = os.path.join(imageDirectory , imageName)
                if flip == True:
                    os.system("raspistill -vf -hf -o " + imagePath)
                else:
                    os.system("raspistill -o " + imagePath)
                
                ser.write("Single image recorded")
                print ("Single image recorded")
                imageCounter = imageCounter + 1

            if incomming == "VIDEO":
                print ("Takes a video")
                videoCounterFormatted = "%04d" % videoCounter
                videoName = "video_" + str(videoCounterFormatted) + ".h264"
                print videoName
                videoPath = os.path.join(videoDirectory , videoName)
                if flip == True:
                    os.system("raspivid -vf -hf -t " + videoRunTime + " -o " + videoPath)
                else:
                    os.system("raspivid  -t " + videoRunTime + " -o " + videoPath)
                ser.write("Video completed. ")
                print ("Video complete")
                videoCounter = videoCounter+ 1
                

            if incomming == "TIMELAPSE": 
               print ("Starting Time Lapse\n\rrun tme is " + runTime +"ms\r\ninterval is " + interval + "ms")
               ser.write("Starting Time Lapse\r\nrun time is " + runTime  + "ms\r\ninterval " + interval + "ms")
               tlPath = os.path.join(timelapseDirectory , tlName)
               if flip == True:
                   os.system("raspistill -vf -hf -o " + tlPath + " -t " + runTime + " -tl " + interval) 
               else:
                   os.system("raspistill -o " + tlpath + " -t " + runTime + " -tl " + interval)

               print ("Timelapse sequence finnished")
               ser.write("Time Lapse sequence finnished")
                
## these are the two User commands, add code as required             
                
            if incomming == "USER1":
                print("Starts User1 application")
                # place code here


            if incomming == "USER2":
                print("Starts User2 application")
                # place code here

# end User commands

# look for additional commands

            if incomming == "VFLIP0":
                print("Switching picture orientation to normal")
                ser.write("Normal picture orientation")
                flip = False

            if incomming == "VFLIP1":
                print("Switching picture orientation to inverted")
                ser.write("Inverted picture orientation")
                flip = True


            if incomming.startswith("RUNTIME"):
                tempString = str(incomming[7:])
                # check to see if this is a number      
                if is_numeric(tempString) == True: 
                    if int(float(tempString)) < 60000:
                        print "Value is too low, must be greater than 60000"
                        ser.write("Value too low, must be greater than 60,000")
                    else:
                        runTime = tempString
                        a = float(runTime) / 60000 # get time in minute
                        print "runTime value has been changed to " + runTime
                        ser.write ("runTime has been changed" + "\r\n" + "to about " + str(a) + " minute(s)")


            if incomming.startswith("INTERVAL"):
                tempString = str(incomming[8:])
                # check to see if this is a number
                if is_numeric(tempString) == True:
                    if int(float(tempString)) < 3000:
                        print "Value too low, must be greater than 3000"
                        ser.write("Value too low must be greater than 30000")
                    else:
                        interval = tempString
                        print "Interval has been changed to " + interval
                        ser.write("Interval has been changed" + '\r\n' + "to " + interval + "ms")

            if incomming.startswith("VIDEORUNTIME"):
                tempString = str(incomming[12:])
                # check to see if this is a number
                if is_numeric(tempString) == True:
                    if int(float(tempString)) < 60000:
                        print "Value too low, must be greater than 60000"
                        ser.write("Value too low, must be greater than 60000")
                    else:
                        videoRunTime = tempString
                        print "The video runtime has been changed to " + videoRunTime
                        ser.write("The video runtime has been changed to " + videoRunTime + "ms")
# end of commands

                                         
            incomming = "" # reset text string

        
