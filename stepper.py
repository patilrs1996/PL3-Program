#!/usr/bin/python 
##########################################################
# * Python code for Driving a Stepper Motor Card using
# * Beaglebone Black running Debian 7 Linux distribution
##########################################################
# *
##########################################################
 
# Import standard python libraries
import sys
import os
import time

##############################################################
# GPIO Pin definitions for Stepper Motor Interfacing Board 
# Please refer "MicroEmbedded_BBB_Interfacing Details_New.pdf" 
# for all the PIN details
##############################################################

STEPPER_1	=	(0 * 32) + 30		#GPIO0_30
STEPPER_2	=	(2 * 32) + 2		#GPIO2_2
STEPPER_3	=	(1 * 32) + 28		#GPIO1_28
STEPPER_4	=	(2 * 32) + 3		#GPIO2_3

# PATH of a GPIO specific sysfs interfce directory on Linux system 
SYSFS_GPIO_DIR = "/sys/class/gpio"

################################################################################
# Description 	: Write the GPIO PIN value on "/sys/class/gpio/export" file.
# 		 This will export (make visible) the directory associated
#		 with particular GPIO pin under sysfs interface.
#		 e.g. if value of GPIO PIN is "23" then "/sys/class/gpio/gpio23"
#		 directory will be exported (will become visible)
# Input   	: @gpio = Value of GPIO PIN (in the form of string)
# Return	: None
# Note		: Must be called for a particular GPIO PIN before using that PIN.
################################################################################

def gpioExport (gpio): 
	try:
   		fo = open(SYSFS_GPIO_DIR + "/export","w")  
   		fo.write(gpio)
   		fo.close()
   		return
   	except IOError:
                return

#################################################################################
# Description : Exactly opposite of export() function above.
# 		 Write the GPIO PIN value on "/sys/class/gpio/unexport" file.
# 		 This will un-export (make invisible) the directory associated
#		 with particular GPIO pin under sysfs interface.
#		 e.g. if value of GPIO PIN is "23" then "/sys/class/gpio/gpio23"
#		 directory will be unexported (will become invisible)
# Input		: @gpio = Value of GPIO PIN (in the form of string)
# Return	: None
# Note		: Must be called for a particular GPIO PIN after it is used
# 		  This makes a PIN free from GPIO functionality
#################################################################################

def gpioUnexport (gpio):
	try: 
   		fo = open(SYSFS_GPIO_DIR + "/unexport","w")  
   		fo.write(gpio)
   		fo.close()
   		return
   	except IOError:
 		return

################################################################################################
# Description : Write the direction ("in"/"out") on "/sys/class/gpio/gpioN/direction"
#               where "gpioN" stands for the directory already exported.
# 		 This will configure a particular GPIO PIN as an input or output pin.
# Input		: @gpio = Value of GPIO PIN (in the form of string)
# 		  @flag  = Value of direction either "in" or "out"
# Return	: None
# Note		: Make sure to export a GPIO PIN (using gpioExport) before calling this function
#################################################################################################
             	
def gpioSetDir (gpio, flag):
	try: 
	   	fo = open(SYSFS_GPIO_DIR + "/gpio" + gpio + "/direction" ,"w")  
	   	fo.write(flag)
	   	fo.close()
	   	return
 	except IOError:
                return

################################################################################################
# Description  : Write the value ("0"/"1") on "/sys/class/gpio/gpioN/value"
#                where "gpioN" stands for the directory already exported.
# 		  This will make particular GPIO PIN as LOW or HIGH (CLEAR or SET).
# Input   	: @gpio = Value of GPIO PIN (in the form of string)
# 		  @val  = Value of GPIO either "0" or "1"
# Return	: None
# Note		: Make sure to export a GPIO PIN (using gpioExport) and
# 		  set the direction as "out" (using gpioSetDir) before calling this function
#################################################################################################

def gpioSetVal (gpio, val):
	try: 
		fo = open(SYSFS_GPIO_DIR + "/gpio" + gpio + "/value" ,"w")  
		fo.write(val)
		fo.close()
		return
	except IOError:
                return

##################################################################################
# Description  : Function to clean up a particular stepper pin
#		 Means Clear and unexport the GPIO PIN
# Input        : @gpio = Value of GPIO PIN (in the form of string)
# Return       : None
# Note	       : This function is called for every pin on stepper interfacing card
##################################################################################

def stepperExit (gpio):
	gpioSetVal(gpio, val="0")
	gpioUnexport(gpio)
	return 

###################################################################################
# Description  : Function to initialize a particular stepper pin
#		 Means export the GPIO PIN for pin, Set its direction as "out"
#		 and Clear the stepper pin (Make it "OFF").
# Input 	: @gpio = Value of GPIO PIN (in the form of string)
# Return	: None
# Note		: This function is called for every stepper pin
###################################################################################
	
def stepperInit (gpio):
	gpioExport(gpio)
	gpioSetDir(gpio, flag="out")
 	gpioSetVal(gpio, val="0")
 	return

###################################################################################
# Description   : Function to make a particular stepper pin ON
#		  Means make the stepper pin "ON", by writing "1" to it's GPIO PIN
# Input  	: @gpio = Value of GPIO PIN (in the form of string)
# Return   	: None
# Note		: Make sure to initialize a particular stepper pin using
# 		  stepperInit() before calling this function
###################################################################################

def stepperOn (gpio):
	gpioSetVal(gpio, val="1")
	return 


###################################################################################
# Description  : Function to make a particular stepper pin OFF
#		  Means make the stepper pin "OFF", by writing "0" to it's GPIO PIN
# Input   	: @gpio = Value of GPIO PIN (in the form of string)
# Return	: None
# Note		: Make sure to initialize a particular stepper pin using
# 		  stepperInit() before calling this function
#####################################################################################
	
	
def stepperOff (gpio):
	gpioSetVal(gpio, val="0")
	return 


###################################################################################
# Description  : Initialize all the stepper pins
#		 Observe that each time stepperInit()  is called, stepper pin
#		 value is converted from integer number to a string
#		 and then it is passed as a parameter.
# Input       	: None
# Return	: None
###################################################################################

def stepperInitAll():
	stepperInit(str(STEPPER_1))
	stepperInit(str(STEPPER_2))
	stepperInit(str(STEPPER_3))
	stepperInit(str(STEPPER_4))

###################################################################################
# Description  : Cleanup all the stepper pins
#		 Observe that each time stepperInit()  is called, stepper pin
#		 value is converted from integer number to a string
#		 and then it is passed as a parameter.
# Input       	: None
# Return	: None
###################################################################################

def stepperExitAll():
	stepperExit(str(STEPPER_1))
	stepperExit(str(STEPPER_2))
	stepperExit(str(STEPPER_3))
	stepperExit(str(STEPPER_4))
	print "\n=== Demonstration END ===\n"
	return	


##############################################################
# Description 	: This function writes the sequence 5 
# 		  (5 in binary "0101") on stepper motor pins
#		  While writing start from LSB, hence LSB
#		  goes to stepper pin #1 	 
# Input		: None	 
# Return	: None	 
##############################################################
def stepperSeq5():
	stepperOn(str(STEPPER_1))
	time.sleep(0.0001)
	stepperOff(str(STEPPER_2))
	time.sleep(0.0001)
	stepperOn(str(STEPPER_3))
	time.sleep(0.0001)
	stepperOff(str(STEPPER_4))
	time.sleep(0.0001)
	return 


##############################################################
# Description 	: This function writes the sequence 9 
# 		  (9 in binary "1001") on stepper motor pins
#		  While writing start from LSB, hence LSB
#		  goes to stepper pin #1 	 
# Input		: None	 
# Return	: None	 
##############################################################

def stepperSeq9():
	stepperOn(str(STEPPER_1))
	time.sleep(0.0001)
	stepperOff(str(STEPPER_2))
	time.sleep(0.0001)
	stepperOff(str(STEPPER_3))
	time.sleep(0.0001)
	stepperOn(str(STEPPER_4))
	time.sleep(0.0001)
	return 

##############################################################
# Description 	: This function writes the sequence 10 
# 		  (10 in binary "1010") on stepper motor pins
#		  While writing start from LSB, hence LSB
#		  goes to stepper pin #1 	 
# Input		: None	 
# Return	: None	 
##############################################################
def stepperSeq10():
	stepperOff(str(STEPPER_1))
	time.sleep(0.0001)
	stepperOn(str(STEPPER_2))
	time.sleep(0.0001)
	stepperOff(str(STEPPER_3))
	time.sleep(0.0001)
	stepperOn(str(STEPPER_4))
	time.sleep(0.0001)
	return 


##############################################################
# Description 	: This function writes the sequence 6 
# 		  (6 in binary "0110") on stepper motor pins
#		  While writing start from LSB, hence LSB
#		  goes to stepper pin #1 	 
# Input		: None	 
# Return	: None	 
##############################################################

def stepperSeq6():
	stepperOff(str(STEPPER_1))
	time.sleep(0.0001)
	stepperOn(str(STEPPER_2))
	time.sleep(0.0001)
	stepperOn(str(STEPPER_3))
	time.sleep(0.0001)
	stepperOff(str(STEPPER_4))
	time.sleep(0.0001)
	return 


##############################################################
# Description 	: This function rotates the stepper motor one 
# 		  step in left direction (anti-clockwise)
# Input		: None	 
# Return	: None	 
##############################################################
	
def stepperDirLeft():
	stepperSeq5()
	time.sleep(0.01)
	stepperSeq9()
	time.sleep(0.01)
	stepperSeq10()
	time.sleep(0.01)
	stepperSeq6()
	time.sleep(0.01)
	return


##############################################################
# Description 	: This function rotates the stepper motor one 
# 		  step in right direction (clockwise)
# Input		: None	 
# Return	: None	 
##############################################################

def stepperDirRight():
	stepperSeq6()
	time.sleep(0.01)
	stepperSeq10()
	time.sleep(0.01)
	stepperSeq9()
	time.sleep(0.01)
	stepperSeq5()
	time.sleep(0.01)
	return

			
######################## 
# Program starts here
########################	

try:
	print "\nStepper Motor Driver using Python\n"
	print  "-----------------------------------------------\n" 	
	stepperInitAll()
	while True:
		for i in range(0, 12):				# Loop for 12 times (to comeplete on revolution)
			stepperDirLeft()			# Rotate stepper left 
		time.sleep(3)					# Sleep for 3 seconds 
		for i in range(0, 12):				# Loop for 12 times (to comeplete on revolution)
			stepperDirRight()			# Rotate stepper right
		time.sleep(3)					# Sleep for 3 seconds
		
	stepperExitAll						# Cleanup all the stepper pins
	exit()							# Exit from Program
except KeyboardInterrupt:					# CTRL-C Exception Handler to cleanup and exit safely from program
	stepperExitAll()	
	print "Program Exit due to CTRL-C"
	exit()
    	sys.exit(0)


