import pigo
import time
import random
from gopigo import *

'''
This class INHERITS your teacher's Pigo class. That means Mr. A can continue to
improve the parent class and it won't overwrite your work.
'''


class  GoPiggy(pigo.Pigo):
    # CUSTOM INSTANCE VARIABLES GO HERE. You get the empty self.scan array from Pigo
    # You may want to add a variable to store your default speed
    MIDPOINT = 83
    STOP_DIST = 20
    RIGHT_SPEED = 200
    LEFT_SPEED = 171



    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward
        #self.calibrate()
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        set_right_speed(self.RIGHT_SPEED)
        set_left_speed(self.LEFT_SPEED)
        servo(self.MIDPOINT)
        while True:
            self.stop()
            self.handler()



    ##### HANDLE IT
    def handler(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like
        menu = {"1": ("Navigate forward", self.nav),
                "2": ("Rotate", self.rotate),
                "3": ("Dance", self.dance),
                "4": ("Calibrate servo", self.calibrate),
                "5": ("Status", self.currentStatus),
                "q": ("Quit", quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        #
        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()


    def currentStatus(self):
        print("My power is at:" + str(volt()) + "volts")
        print('My MIDPOINT is set to: ' + str(self.MIDPOINT))
        print('I get scared when things are closer than ' + str(self.STOP_DIST) + 'cm')
        print('Left speed set to: ' + str(self.LEFT_SPEED) + ' // Right set to: ' + str(self.RIGHT_SPEED))
        servo(self.MIDPOINT)
        time.sleep(.1)
        return us_dist(15)


    # A SIMPLE DANCE ALGORITHM
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE
        #Check if its clear using superClear method
        print("Is it clear?")
        if(self.superClear()):
            print("Let's dance!")
        #Time to dance
        for x in range(3):
            x = 100
            print("Speed is set to:" + str(x))
            set_speed(x)
            servo(20)
            self.encB(10)
            self.encR(4)
            self.encL(4)
            self.encF(15)
            self.encR(4)
            self.encL(4)
            self.encB(5)
            servo(120)
            time.sleep(.1)



    def superClear(self):
        #Check front distance
        servo(self.MIDPOINT)
        time.sleep(.1)
        scan1 = us_dist(15)
        time.sleep(.5)
        print("Front Distance:" + str(us_dist(15)))
        #Check right distance
        servo(self.MIDPOINT - 60)
        time.sleep(.1)
        scan2 = us_dist(15)
        time.sleep(.5)
        print("Right Distance:" + str(us_dist(15)))
        #Check left distance
        servo(self.MIDPOINT + 60)
        time.sleep(.1)
        scan3 = us_dist(15)
        time.sleep(.5)
        print("Left Distance:" + str(us_dist(15)))
        #Average the 3 scans
        scan0 = (scan1 + scan2 +scan3) / 3
        time.sleep(.1)
        servo(self.MIDPOINT)
        time.sleep(.5)
        #If its safe or not to dance:
        if scan0 < self.STOP_DIST:
            print("There is something in the way, so I'll back up")
            time.sleep(.5)
            self.encB(20)
            return False
        if scan0 > self.STOP_DIST:
            print("It looks pretty clear")
        return True


    def frontClear(self) -> bool:
        for x in range((self.MIDPOINT - 5), (self.MIDPOINT + 5), 5):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            # double check the distance
            scan2 = us_dist(15)
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            if scan1 < self.STOP_DIST:
                print("Doesn't look clear to me")
                return False
        return True


    def superChoosePath(self) -> str:
        print('Considering options...')
        if self.isClear():
            return "fwd"
        else:
            self.wideScan()
        avgRight = 0
        avgLeft = 0
        for x in range(self.MIDPOINT - 60, self.MIDPOINT):
            if self.scan[x]:
                avgRight += self.scan[x]
        avgRight /= 60
        print('The average dist on the right is ' + str(avgRight) + 'cm')
        for x in range(self.MIDPOINT, self.MIDPOINT + 60):
            if self.scan[x]:
                avgLeft += self.scan[x]
        avgLeft /= 60
        print('The average dist on the left is ' + str(avgLeft) + 'cm')
        if avgRight > avgLeft and avgRight > self.STOP_DIST:
            return "right"
        if avgLeft > avgRight and avgLeft > self.STOP_DIST:
            return "left"
        elif avgRight < self.STOP_DIST or avgLeft < self.STOP_DIST:
            return "There is no where to go"


    #Moving slowly forever but still scanning
    def cruise(self):
        self.setSpeed(75, 100)
        #Have the robot drive forward without end
        while self.frontClear():
            print("It is clear. Time to fly!")
            fwd()
            if self.frontClear() is False:
                self.stop()


    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE
        #TODO: If while loop fails, check for other paths
        #loop: check that it's clear
        while self.isClear():
            #Let's go forward a lot
            self.cruise()
            if False:
                self.stop()
                self.superChoosePath()
        #Choosing the direction
                answer = self.superChoosePath()
                if answer == "left":
                    self.encL(9)
                elif answer == "right":
                    self.encR(9)
                elif answer == "There is no where to go":
                    print("Since there's no where to go, I'll back up")
                    self.encB(20)
                    self.encL(15)
                self.nav()



####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
