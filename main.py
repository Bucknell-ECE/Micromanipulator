##########################################################################
############################### Initialize ###############################
##########################################################################

from get_connection import get_connection
import RPi.GPIO as GPIO
import MFRC522
import signal
import time
from time import sleep
import os
import datetime
from shutdown import shutdown
from attemptAccess import attemptAccess
from LogSuccessAttempt import logAccessAttempt
from LogSuccessAttempt import logAccessCompletion
from notifyAdmin import notifyAdmin
from trainingRequest import trainingRequest
from neopixel import *
from ledanimations import *
import threading
from threading import Thread
MIFAREReader = MFRC522.MFRC522()			# Create an object of class MFRC522

continue_reading = True
resetReady = False

# LED strip configuration:
LED_COUNT      = 5                                      # Number of LED pixels.
LED_PIN        = 18                                     # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000                                 # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5                                      # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255                                    # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False                                  # True to invert the signal (when using NPN transistor level shift)
red            = Color(  0, 255,   0)
green          = Color(255,   0,   0)
yellow         = Color(255, 255,   0)
blue           = Color(  0,   0, 255)
orange         = Color( 30, 255,   0)
pink           = Color(  0, 255, 127)
white          = Color(255, 255, 255)
purple         = Color(146,  60, 244)
nocolor        = Color(  0,   0,   0)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()


## GPIO pin assignments and initializations
os.system('gpio mode 0 out')                            # Interlock
os.system('gpio mode 25 out')			            	# Solid State Relay
os.system('gpio mode 23 out')                           # Buzzer
os.system('gpio mode 24 down')                          # Button
os.system('gpio write 25 0')                            # Turn off power to SSR
os.system('gpio write 0 1')                             # Open interlock

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

##########################################################################
########################### Embedded Functions ###########################
##########################################################################

def alertAuth(makerid, rid):
    '''
    Flashes red LED when a user is not authorized
        and waits until ID is removed.
        Can submit training requests from this state.
    :param makerid: User ID for current card
    :param rid: Resource ID
    :return: Void
    '''

    colorFlash(strip, red)
    colorSet(strip, red)

    buttonCount = 0
    buttonPressed = False
    pressedSinceLastUser = False
    global resetReady

    while True:
        CardPresent = 1  # Card is now present at scanner
        miss = 0  # Set consecutive missed reads to 0

        while CardPresent:
            stillthere = 0  # Assume card is not present
            while ~stillthere:

                cur_time = datetime.datetime.now()  # Check time to see if ready for daily reset (UTC)
                if cur_time.hour == 8 and cur_time.minute == 0:
                    resetReady = True

                # Scan for cards
                (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                # Get the UID of the card
                (status, uid) = MIFAREReader.MFRC522_Anticoll()

                # If we have the UID, generate unsigned integer
                if status == MIFAREReader.MI_OK:  # If we read a UID
                    finalUID = 0
                    for i in range(4):
                        finalUID = finalUID + (uid[i] << (8 * (3 - i)))
                    currentid = finalUID

                else:  # If we did not read a UID
                    miss += 1  # Increment consecutive misses
                    currentid = 0  # Clear previously read ID

                if currentid == makerid:  # If the ID read == unauthorized ID
                    stillthere = 1  # The ID is still at the scanner
                    colorSet(strip, red)
                    miss = 0

                elif miss > 5:  # If we miss 5 or more consecutive reads
                    return # Assume ID removed; Go back to waiting

                    ########## Check if button is being held #####################

                # Checking for long button press for training request
                if pressedSinceLastUser == False and buttonCount < 25:  # If no training requests since last user
                    p = subprocess.Popen(['gpio read 24'], stdout=subprocess.PIPE, shell=True)
                    (buttonPress, errors) = p.communicate()

                    if (buttonPress == "1\n"):
                        buttonCount += 1
                        buttonPressed = True
                    elif buttonPressed == True:  # Allows a one loop buffer
                        buttonPressed = False
                    else:
                        buttonCount = 0

                    p.wait()

                    if buttonCount == 25:  # Check for long button press to report issue
                        miss = 0  # Clear consecutive misses
                        buttonCount = 0
                        pressedSinceLastUser = True

                        setBuzzer(True)
                        sleep(0.2)
                        setBuzzer(False)
                        colorFlash(strip, white, 200, 5)
                        colorSet(strip, white)

                        success = trainingRequest(rid, makerid)  # Generate training request
                        if success == 1:
                            colorFlash(strip, green, 100, 5)
                        elif success == 0:
                            colorFlash(strip, red, 200, 3)

	
def poweron(readid, makerid, interlock, rid):
    '''
    Activates the relay when a maker has been authorized
       and continues to ensure the MakerID has not been
       removed from the scanner. If it has, this function
       calls the shutdown protocol.
    :param readid:
    :param makerid:
    :param interlock: Defines whether to use interlock or relay
    :param rid: Resource ID
    :return: calls power_down() if card removed
    '''

    buttonCount = 0
    buttonPressed = False
    pressedSinceLastUser = False
    global resetReady

    while True:
        if interlock == 1:
            os.system('gpio write 25 1')	                # Energize the relay
        else:
            os.system('gpio write 0 0')                         # Close the interlock
        CardPresent = 1				                # Card is now present at scanner
        miss = 0					        # Set consecutive missed reads to 0

        while CardPresent:         
            stillthere = 0				        # Assume card is not present
            while ~stillthere:

                cur_time = datetime.datetime.now()  # Check time to see if ready for daily reset (UTC)
                if cur_time.hour == 8  and cur_time.minute == 0:
                    resetReady = True
			
                # Scan for cards    
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)                
                # Get the UID of the card
                (status,uid) = MIFAREReader.MFRC522_Anticoll() 
				
                # If we have the UID, generate unsigned integer
                if status == MIFAREReader.MI_OK:	        # If we read a UID
                    finalUID = 0
                    for i in range(4):
                        finalUID = finalUID + (uid[i] << (8 * (3 - i)))
                    currentid = finalUID

                else:					        # If we did not read a UID
                    miss += 1				        # Increment consecutive misses
                    currentid = 0				# Clear previously read ID
                                    
                if currentid == makerid:			# If the ID read == authorized ID
                    stillthere = 1			        # The ID is still at the scanner
                    colorSet(strip, green)
                    miss = 0
                
                elif currentid == readid:
                    stillthere = 1
                    colorSet(strip, orange)
                    miss = 0
                
                elif miss > 5:				        # If we miss 5 or more consecutive reads
                    colorSet(strip, yellow)
                    return power_down(makerid, interlock, rid)	# Assume ID removed; begin shutdown

            ########## Check if button is being held #####################

                if pressedSinceLastUser == False and buttonCount < 25:  # If no issues reported since last user
                    p = subprocess.Popen(['gpio read 24'], stdout=subprocess.PIPE, shell=True)
                    (buttonPress, errors) = p.communicate()

                    if (buttonPress == "1\n"):
                        buttonCount += 1
                        buttonPressed = True
                    elif buttonPressed == True:  # Allows a one loop buffer
                        buttonPressed = False
                    else:
                        buttonCount = 0

                    p.wait()

                    if buttonCount == 25:  # Check for long button press to report issue
                        miss = 0  # Clear consecutive misses
                        buttonCount = 0
                        pressedSinceLastUser = True

                        setBuzzer(True)
                        sleep(0.1)
                        setBuzzer(False)
                        colorFlash(strip, white, 200, 5)
                        colorSet(strip, white)

                        notifyAdmin(rid, makerid)  # Generate incident report email

def setBuzzer(onOff):
    '''
    :param onOff: True -> Buzzer On; False -> Buzzer Off
    :return: None
    '''

    if onOff:
        # Set on
        os.system("gpio write 23 1")
    else:
        # Set off
        os.system("gpio write 23 0")

import subprocess 
                                
def power_down(makerid, interlock, rid):
    '''
    :param makerid: User ID that needs to be replaced to trigger power_on()
    :param interlock: interlock setting
    :param rid: Resource ID
    :return: None
    '''

    # Make new connection to server in case power_on ran longer than server timeout period
    cnx = get_connection()

    miss = 0						# Clear consecutive misses
    readid = 0						# Clear read ID number
    while miss < 15:					# While we have fewer than 5 consecutive misses
	p = subprocess.Popen(['gpio read 24'], stdout=subprocess.PIPE,shell=True)
	(buttonPress, errors) = p.communicate()
	print("button press", buttonPress)
        if (buttonPress == "1\n"):
	    print('read button press')
	    miss = 15

        colorSet(strip, yellow)                         # Set LEDs to yellow
        setBuzzer(True)
        sleep(0.25)                                     # Wait.
        colorSet(strip, nocolor)                        # turn off LEDs
        setBuzzer(False)

	p = subprocess.Popen(['gpio read 24'], stdout=subprocess.PIPE,shell=True)
	(buttonPress, errors) = p.communicate()
	print("button press", buttonPress)
        if (buttonPress == "1\n"):
	    print('read button press')
	    miss = 15

        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
               
        # If we have the UID, generate unsigned integer
        if status == MIFAREReader.MI_OK:		# If we read a UID
            finalUID = 0
	    for i in range(4):
	    	finalUID = finalUID + (uid[i] << (8 * (3 - i)))
            readid = finalUID

        else:						# If we did not read a UID
            readid = 0 
                 
        
		if isProxyResource(cnx, rid):# if the resouce is allowed to use proxy cards
			if readid == isProxyCard(cnx, readid): #if the ID is a  proxy card
				cnx.close()
				return poweron(readid, makerid, interlock, rid)	# Abort shutdown and return power
		
		elif readid == makerid :	# If the ID was returned to the reader 
			cnx.close()
            return poweron(readid, makerid, interlock, rid)	# Abort shutdown and return power

        elif readid == 0:
            miss += 1
        
        elif readid != makerid:
            miss += 1
            colorSet(strip, nocolor)
            colorSet(strip, red)
            sleep(0.25)
            colorSet(strip, nocolor)
	    
    if interlock == 1:                
        os.system('gpio write 25 0')		        # Once we have more than 15 misses, remove power
    else:
        os.system('gpio write 0 1')
    cnx.close()
    return				                # Return to waiting for an ID
##################################################################################
#Checks to see whether the resouce is authorized to use a proxy card
#####################################################################################
def isProxyResource(cnx, rid):
	query = ('SELECT rid FROM ms_resources WHERE rid=' + str(rid) ' AND proxyEnable = 1 ')
     proxyResource = False
    cursor = cnx.cursor()
    cursor.execute(query)
    for (rid) in cursor:
        proxyResource = True
    cursor.close()
    return proxyResource
def isProxyCard(cnx, uid):
    '''
    Checks to see if a given user ID is that of an proxy (aka admin) card.
    :param cnx: connection to SQL server
    :param uid: user ID to be checked
    :return: True if is a proxy card
    '''
    query = ('SELECT cardId FROM ms_adminCards WHERE cardId=' + str(uid))
    proxyExists = False
    cursor = cnx.cursor()
    cursor.execute(query)
    for (cardId) in cursor:
        proxyExists = True
    cursor.close()
    return proxyExists
###########################################################################
########################### Check for RFID chip ###########################
###########################################################################

def wait_for_maker(resourceType, needsTraining, rid, interlock):
    '''
    The state that the device remains in while not being used.
    :param resourceType: Resource Type
    :param needsTraining: Whether the resource needs training
    :param rid: Resource ID
    :param interlock: Interlock or Relay
    :return: None
    '''
    miss = 0                                            # Clear miss counter
    count = 0                                           # Clear read count
    readid = 0                                          # Clear read ID value
    lastid = 0                                          # Clear stored ID value
    makerid = 0                                         # Clear stored ID value
    standby = 0
    buttonCount = 0
    buttonPressed = False
    pressedSinceLastUser = False
    rejected = False
    global sleepMode
    sleepMode = False
    global resetReady
    resetReady = False
    colorFlash(strip, green, 100, 3)
    colorWipe(strip, blue, 5)
    colorWipe(strip, orange, 10)
    colorWipe(strip, red, 15)

    while continue_reading: # Remains in this loop while at rest
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)            
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # Recently turned on or had a card removed
        if miss < 50:
            colorSet(strip, blue)                        # Set LEDs to blue

        # Hasn't read card for a while, go into sleep mode.
        # All sleep mode entails is that sleep_display() will run in a new thread,
        #       simply changing the display color to rainbow and allowing the
        #       device to reboot if it is the right time.
        elif miss == 50:
            sleepMode = True
            sleepThread = Thread(target = sleepDisplay, args=(strip, 20, 1))
            sleepThread.daemon = True
            sleepThread.start()
        
        # If we have the UID, generate unsigned integer
        if status == MIFAREReader.MI_OK:		# If we read an ID
            sleepMode = False
            miss = 0					# Clear consecutive misses
	    finalUID = 0
	    for i in range(4):
	    	finalUID = finalUID + (uid[i] << (8 * (3 - i)))
            readid = finalUID           # This is the user ID in the card reader
        
        # Check if we have read ID before
            if lastid == 0:				# If we have no stored ID
                miss = 0				# Clear consecutive misses
                lastid = readid				# Store read ID value 
                count = 1				# Increment the read count
            elif lastid == readid:		        # If we have read the ID previously
                count += 1				# Increment the read count
                miss = 0				# Clear misses
            else:				        # If we read an ID that is not the stored ID
                lastid = 0				# Clear stored ID
                count = 0      				# Clear the read count
        else:						# If we did not read an ID
            miss += 1					# Increment the miss counter
            
	
        if count >= 3:					# If we read the same ID 3 times consecutively
            makerid = lastid				# Make this ID the MakerID
            colorSet(strip, yellow)                       # Set LEDs to white
            print(makerid)
            count = 3                 # Just so count doesn't get too big
            print("Connected to server")

        # Check if maker is authorized
            isAuthorized = attemptAccess(makerid, resourceType, needsTraining, rid)
            if isAuthorized==1:			# If MakerID is authorized:
                logAccessAttempt(makerid, rid, True)
                poweron(readid, makerid, interlock, rid)		# Deliver power to the resource
                logAccessCompletion(makerid, rid)
                makerid = 0
                readid = 0
                lastid = 0
                miss = 0
                count = 0
                pressedSinceLastUser = False
            elif isAuthorized == 2:    # If read shutdown card:
                makerid = 0
                readid = 0
                lastid = 0
                miss = 0
                count = 0
                colorSet(strip, pink)
                shutdown()
            elif rejected == False:					# If not authorized:
                logAccessAttempt(makerid, rid, False)
                alertAuth(makerid, rid)  # Reject card and remain red until card is removed
                makerid = 0
                readid = 0
                lastid = 0
                miss = 0
                count = 0
                rejected = True
            
        elif miss > 2:				        # If we miss more than 2 consecutive reads, assume card is gone
            lastid = 0					# Clear previously read ID
            makerid = 0					# Clear MakerID
            rejected = False
            count = 0

        # Check for button press for incident reporting
        if pressedSinceLastUser == False and buttonCount < 25:   # If no issues reported since last user
            p = subprocess.Popen(['gpio read 24'], stdout=subprocess.PIPE, shell=True)
            (buttonPress, errors) = p.communicate()

            if (buttonPress == "1\n"):    # If button is pressed
                buttonCount +=1
                buttonPressed = True
            elif buttonPressed == True:    # Allows a one loop buffer
                buttonPressed = False
            else:
                buttonCount = 0

            p.wait()

            if buttonCount == 25:     #Check for long button press to report issue (~5 sec)
                sleepMode = False
                miss = 0  # Clear consecutive misses
                buttonCount = 0
                pressedSinceLastUser = True

                setBuzzer(True)
                sleep(0.1)
                setBuzzer(False)
                colorFlash(strip, white, 200, 5)
                colorSet(strip, white)           # White indicates communicating with server

                notifyAdmin(rid)   # Generate incident report email


        cur_time = datetime.datetime.now()   # Check time to see if ready for daily reset (UTC)
        if cur_time.hour == 8  and cur_time.minute == 0:    # 8:00 UTC = 4:00am EST
            resetReady = True

            
def sleepDisplay(strip, wait_ms=10, iterations=1):
    '''
    Sets LED display to a pulsating rainbow and executes daily reboot if the time is right
    :param strip: LED strip
    :param wait_ms: factor in rainbow pattern speed
    :param iterations: factor in rainbow pattern speed
    :return: None
    '''
    i=0
    #six_hours = 21600
    while sleepMode:
        for j in range(256*iterations): #5.12 seconds if iterations = 1
            if sleepMode:
                for i in range(strip.numPixels()):
                        strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
                strip.show()
                time.sleep(wait_ms/1000.0)

        i = i+1

        if (resetReady == True and sleepMode == True):    # If resetReady and in sleep mode
            print("Rebooting...")
            colorFlash(strip, pink, 100, 2)
            colorSet(strip, pink)
            os.system("sudo reboot")     # (Daily) Reboot

