//PROGRAM FOR LIFT 

#!/usr/bin/python 

 
import sys
import time
import select



LED_1	=	(0 * 32) + 3		
LED_2	=	(0 * 32) + 23		
LED_3	=	(0 * 32) + 2		
LED_4	=	(0 * 32) + 26		

LED_5	=	(1 * 32) + 17		
LED_6	=	(1 * 32) + 15		
LED_7	=	(0 * 32) + 15		
LED_8	=	(1 * 32) + 14		

LED_9	=	(0 * 32) + 30
LED_10	=	(2 * 32) + 2
LED_11	=	(1 * 32) + 28
LED_12	=	(2 * 32) + 3
LED_13	=	(0 * 32) + 31
LED_14	=	(2 * 32) + 5
LED_15	=	(1 * 32) + 18

SW_1	=	(0 * 32) + 14		
SW_2	=	(0 * 32) + 27		
SW_3	=	(0 * 32) + 22		
SW_4	=	(2 * 32) + 1	



# DIRECTIN LEDS: to represent lift direction (up or down) 
LIFT_DIR_1   =    LED_9
LIFT_DIR_2   =    LED_10
LIFT_DIR_3   =    LED_11
LIFT_DIR_4   =    LED_12
LIFT_DIR_5   =    LED_13
LIFT_DIR_6   =    LED_14
LIFT_DIR_7   =    LED_15


# POSITION LEDS: LEDs to indicate the current position of Lift 
LIFT_POS_0   =    LED_5
LIFT_POS_1   =    LED_6
LIFT_POS_2   =    LED_7
LIFT_POS_3   =    LED_8


# LIFT BUTTONS: corresponding to each floor of the Lift 
LIFT_BUTTON_0   =    SW_1
LIFT_BUTTON_1   =    SW_2
LIFT_BUTTON_2   =    SW_3
LIFT_BUTTON_3   =    SW_4

# LIFT LEDS: indication for BUTTON Press on each floor 
LIFT_LED_0   =    LED_1
LIFT_LED_1   =    LED_2
LIFT_LED_2   =    LED_3
LIFT_LED_3   =    LED_4


# An array of DIRECTIN LEDS 
dir_leds = [ 	LIFT_DIR_1,
		LIFT_DIR_2,
		LIFT_DIR_3,
		LIFT_DIR_4,
		LIFT_DIR_5,
		LIFT_DIR_6,
		LIFT_DIR_7
	   ]	

# An array of POSITION LEDS 
pos_leds = [
		LIFT_POS_0,
		LIFT_POS_1,
		LIFT_POS_2,
		LIFT_POS_3
	   ]

# An array of BUTTON PRESS LEDS
lift_leds = [
		LIFT_LED_0,
		LIFT_LED_1,
		LIFT_LED_2,
		LIFT_LED_3
	   ]

# An array of lift BUTTONs
lift_buttons = [
		 LIFT_BUTTON_0,
		 LIFT_BUTTON_1,
		 LIFT_BUTTON_2,
		 LIFT_BUTTON_3
	   ]


NO_OF_FLOORS	  =	4		
NO_OF_DIR_LEDS	  =	7		
DEFAULT_LIFT_POS =	0		


# Array associated with each floor having 4 elements; each again having 3 elements fd, button and led
floor_set = [
		{"fd":-1, "button":LIFT_BUTTON_0, "led":LIFT_LED_0},		
		{"fd":-1, "button":LIFT_BUTTON_1, "led":LIFT_LED_1},		
		{"fd":-1, "button":LIFT_BUTTON_2, "led":LIFT_LED_2},		       
		{"fd":-1, "button":LIFT_BUTTON_3, "led":LIFT_LED_3}		

             ]
             
# PATH of a GPIO specific sysfs interfce directory on Linux system             
SYSFS_GPIO_DIR = "/sys/class/gpio"


             	

def gpioExport (gpio): 
	try:
   		fo = open(SYSFS_GPIO_DIR + "/export","w")  			
   		fo.write(gpio)
   		fo.close()
   		return
   	except IOError:
                return


def gpioUnexport (gpio):
	try: 
   		fo = open(SYSFS_GPIO_DIR + "/unexport","w")  
   		fo.write(gpio)
   		fo.close()
   		return
   	except IOError:
 		return




def gpioSetDir (gpio, flag):
	try: 
	   	fo = open(SYSFS_GPIO_DIR + "/gpio" + gpio + "/direction" ,"w")  
	   	fo.write(flag)
	   	fo.close()
	   	return
 	except IOError:
                return



def gpioSetVal (gpio, val):
	try: 
		fo = open(SYSFS_GPIO_DIR + "/gpio" + gpio + "/value" ,"w")  
		fo.write(val)
		fo.close()
		return
	except IOError:
                return


def gpioSetEdge (gpio, flag): 
	try:
		fo = open(SYSFS_GPIO_DIR + "/gpio" + gpio + "/edge" ,"w")  
		fo.write(flag)
		fo.close()
   		return
	except IOError:
                return


def liftLEDExit (gpio):
	gpioSetVal(gpio, val="0")
	gpioUnexport(gpio)
	return 



	
def liftLEDInit (gpio):
	gpioExport(gpio)
	gpioSetDir(gpio, flag="out")
 	gpioSetVal(gpio, val="0")
 	return



 	
def liftLEDOn (gpio):
	gpioSetVal(gpio, val="1")
	return 



def liftLEDOff (gpio):
	gpioSetVal(gpio, val="0")
	return 


def liftButtonExit (gpio):
	gpioUnexport(gpio)
	return 
	

def liftButtonInit (gpio):
	gpioExport(gpio)
	gpioSetDir(gpio, flag="in")
 	gpioSetEdge(gpio, flag="falling")
 	return



def liftInitAll():
	for i in range(0, NO_OF_DIR_LEDS):
		liftLEDInit(str(dir_leds[i]))
			
	for i in range(0, NO_OF_FLOORS):
		liftLEDInit(str(pos_leds[i]))
		liftLEDInit(str(lift_leds[i]))
		liftButtonInit(str(lift_buttons[i]))
	return	



def liftExitAll():
	for i in range(0, NO_OF_DIR_LEDS):
		liftLEDExit(str(dir_leds[i]))
			
	for i in range(0, NO_OF_FLOORS):
		liftLEDExit(str(pos_leds[i]))
		liftLEDExit(str(lift_leds[i]))
		liftButtonExit(str(lift_buttons[i]))
	print "\n=== Demonstration END ===\n"
	return	


def liftDefaultPos():
	liftLEDOn(str(pos_leds[DEFAULT_LIFT_POS]))
	return 

def liftDirUp():
	for i in range(0, NO_OF_DIR_LEDS):
		liftLEDOn(str(dir_leds[i]))
		time.sleep(0.5)
	for i in range(0, NO_OF_DIR_LEDS):
		liftLEDOff(str(dir_leds[i]))
	return


def liftDirDown():
	for i in range(NO_OF_DIR_LEDS, 0, -1):
		liftLEDOn(str(dir_leds[i-1]))
		time.sleep(0.5)
	for i in range(0, NO_OF_DIR_LEDS):
		liftLEDOff(str(dir_leds[i]))
	return



def GetButtonVal(): 
	try:		
		fo0 = open(SYSFS_GPIO_DIR + "/gpio" + str(LIFT_BUTTON_0) + "/value" ,"r") 
		fo0.read(2)								  	
		floor_set[0]["fd"] = fo0						  	
		
		fo1 = open(SYSFS_GPIO_DIR + "/gpio" + str(LIFT_BUTTON_1) + "/value" ,"r") 
		fo1.read(2)								 
		floor_set[1]["fd"] = fo1						  
		
		fo2 = open(SYSFS_GPIO_DIR + "/gpio" + str(LIFT_BUTTON_2) + "/value" ,"r") 
		fo2.read(2)								  
		floor_set[2]["fd"] = fo2						  
		
		fo3 = open(SYSFS_GPIO_DIR + "/gpio" + str(LIFT_BUTTON_3) + "/value" ,"r") 
		fo3.read(2)								   	
		floor_set[3]["fd"] = fo3						  
		
		print "\nWaiting for button press ..."
		
		
		r, w, ex = select.select([], [], [fo0, fo1, fo2, fo3])			
						
		# Detect on which floor button is pressed						
		for i in range(len(floor_set)):								
			if floor_set[i]["fd"] in ex:					  	
				print "LIFT button is pressed for floor #%d" % i	
				liftLEDOn(str(floor_set[i] ["led"]))			
				time.sleep(1)						
				but = i							
				fo = floor_set[i]["fd"]					
				fo.seek(0, 0);						
				str1 = fo.read(1)					
	
		fo0.close()								
		fo1.close()								
		fo2.close()								
		fo3.close()								
		return but
	
	except IOError:
                return


try:
	print "\nLift Operation Simulation using Python\n"
	print  "-----------------------------------------------\n" 	
	liftInitAll()							
	liftDefaultPos()						
	cur_flr = DEFAULT_LIFT_POS					
	
	while True:
		new_flr = GetButtonVal()		
		if new_flr > cur_flr:					
			tmp = cur_flr						
			print "LIFT going UP to floor #%d" %new_flr		
			while (tmp != new_flr):					
				liftDirUp()					
				time.sleep(0.01)				
				liftLEDOff(str(pos_leds[tmp]))			
				tmp += 1					
				liftLEDOn(str(pos_leds[tmp]))			
				time.sleep(0.5)					
		elif new_flr < cur_flr:				
			tmp = cur_flr						
			print "LIFT going DOWN to floor #%d" %new_flr		
			while (tmp != new_flr):					
				liftDirDown()					
				time.sleep(0.01)				
				liftLEDOff(str(pos_leds[tmp]))			
				tmp -= 1					
				liftLEDOn(str(pos_leds[tmp]))			
				time.sleep(0.5)					
		
		cur_flr = new_flr			
		liftLEDOff(str(lift_leds[new_flr]))	
		time.sleep(1)				
		 
	liftExitAll()					
	exit()						
except KeyboardInterrupt:				 
	liftExitAll()	
	print "Program Exit due to CTRL-C"
	exit()
    	sys.exit(0)

//OUTPUT:-
/*root@beaglebone:/home# python elevator.py

Lift Operation Simulation using Python

-----------------------------------------------


Waiting for button press ...
LIFT button is pressed for floor #1
LIFT going UP to floor #1

Waiting for button press ...
LIFT button is pressed for floor #3
LIFT going UP to floor #3

Waiting for button press ...
LIFT button is pressed for floor #0
LIFT going DOWN to floor #0

Waiting for button press ...
^C
=== Demonstration END ===

Program Exit due to CTRL-C
root@beaglebone:/home# 
Broadcast message from root@beaglebone (Wed Apr 23 21:36:04 2014):

Power button pressed 
The system is going down for system halt NOW!
*/
