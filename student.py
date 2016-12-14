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
    LEFT_SPEED = 180

    # NEW TURN DETAILS
    turn_track = 0.0
    TIME_PER_DEGREE = 0.010278
    TURN_MODIFIER = .5



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
                "6": ("Cruise", self.cruise),
                "q": ("Quit", quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        #
        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()



    ###########
    ####MY NEW TURN METHODS because others just don't make the cut
    ###########
    #takes number of degrees and turns right accordingly
    def turnR(self, deg):
        #adjust the tracker so we know how many degrees our exit is
        self.turn_track += deg
        print("The exit is " + str(self.turn_track) + " degrees away.")
        self.setSpeed(self.RIGHT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        #do turn stuff
        right_rot()
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        #set speed back to normal:
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)

    #takes number of degrees and turns left accordingly
    def turnL(self, deg):
        #adjust the tracker so we know how many degrees our exit is
        self.turn_track -= deg
        print("The exit is " + str(self.turn_track) + " degrees away.")
        self.setSpeed(self.RIGHT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        #do turn stuff
        left_rot()
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        #set speed back to normal:
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)



    # REPLACEMENT TURN METHOD. Find the best option to turn
    def kenny(self):
        # Activate our scanner!
        self.wideScan()
        # count will keep track of contigeous positive readings
        count = 0
        # list of all the open paths we detect
        option = [0]
        # YOU DECIDE: What do we add to STOP_DIST when looking for a path fwd?
        SAFETY_BUFFER = 15
        # YOU DECIDE: what increment do you have your wideScan set to?
        INC = 3

        ###########################
        ######### BUILD THE OPTIONS
        # loop from the 60 deg right of our middle to 60 deg left of our middle
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60):
            # ignore all blank spots in the list
            if self.scan[x]:
                # add 30 if you want, this is an extra safety buffer
                if self.scan[x] > (self.STOP_DIST + SAFETY_BUFFER):
                    count += 1
                # if this reading isn't safe...
                else:
                    # aww nuts, I have to reset the count, this path won't work
                    count = 0
                # YOU DECIDE: Is 16 degrees the right size to consider as a safe window?
                if count > (16 / INC) - 1:
                    # SUCCESS! I've found enough positive readings in a row
                    print("---FOUND OPTION: from " + str(x - 16) + " to " + str(x))
                    # set the counter up again for next time
                    count = 0
                    # add this option to the list
                    option.append(x - 8)

        ####################################
        ############## PICK FROM THE OPTIONS - experimental

        # The biggest angle away from our midpoint we could possibly see is 90
        bestoption = 90
        # the turn it would take to get us aimed back toward the exit - experimental
        ideal = -self.turn_track
        print("\nTHINKING. Ideal turn: " + str(ideal) + " degrees\n")
        # x will iterate through all the angles of our path options
        for x in option:
            # skip our filler option
            if x != 0:
                # the change to the midpoint needed to aim at this path
                turn = self.MIDPOINT - x
                # state our logic so debugging is easier
                print("\nPATH at  " + str(x) + " degrees means a turn of " + str(turn))
                # if this option is closer to our ideal than our current best option...
                if abs(ideal - bestoption) > abs(ideal - turn):
                    # store this turn as the best option
                    bestoption = turn
        if bestoption > 0:
            # CHANGE AS NEEDED. Can either use input (for tests), or print (for timed runs)
            input("\nABOUT TO TURN RIGHT BY: " + str(bestoption) + " degrees")
        else:
            input("\nABOUT TO TURN LEFT BY: " + str(abs(bestoption)) + " degrees")
        return bestoption



    def setSpeed(self, left, right):
        print("\nLeft speed: " + str(left) + "// Right speed: " + str(right))
        set_left_speed(int(left))
        time.sleep(.05)
        set_right_speed(int(right))
        time.sleep(.05)



    # A SAFETY PRECAUTION
    def backUp(self):
        if us_dist(15) < 2:
            print("I don't think it's safe. Backing up for .3 second")
            bwd()
            time.sleep(.3)
            self.stop()



    # HOW'S THE ROBOT DOING?
    def currentStatus(self):
        print("My power is at:" + str(volt()) + "volts")
        print('My MIDPOINT is set to: ' + str(self.MIDPOINT))
        print('I get scared when things are closer than ' + str(self.STOP_DIST) + 'cm')
        print('Left speed set to: ' + str(self.LEFT_SPEED) + ' // Right set to: ' + str(self.RIGHT_SPEED))
        # Return the headset back to midpoint and return the distance
        servo(self.MIDPOINT)
        time.sleep(.1)
        scan = us_dist(15)
        print("The distance is: " + str(us_dist(15)))




    # A SIMPLE DANCE ALGORITHM
    def dance(self):
        print("Piggy dance")
        # Check if its clear using superClear method
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



    # SCANNING TO THE FRONT, RIGHT, AND THEN LEFT
    def superClear(self):
        # Check front distance
        servo(self.MIDPOINT)
        time.sleep(.1)
        scan1 = us_dist(15)
        time.sleep(.5)
        print("Front Distance:" + str(us_dist(15)))
        # Check right distance
        servo(self.MIDPOINT - 60)
        time.sleep(.1)
        scan2 = us_dist(15)
        time.sleep(.5)
        print("Right Distance:" + str(us_dist(15)))
        # Check left distance
        servo(self.MIDPOINT + 60)
        time.sleep(.1)
        scan3 = us_dist(15)
        time.sleep(.5)
        print("Left Distance:" + str(us_dist(15)))
        # Average the 3 scans
        scan0 = (scan1 + scan2 +scan3) / 3
        time.sleep(.1)
        servo(self.MIDPOINT)
        time.sleep(.5)
        # If its safe or not to dance:
        if scan0 < self.STOP_DIST:
            print("There is something in the way, so I'll back up")
            time.sleep(.5)
            self.encB(20)
            return False
        if scan0 > self.STOP_DIST:
            print("It looks pretty clear")
        return True



    # ONLY CHECKING THE VERY FRONT AND NOTHING ELSE
    def frontClear(self) -> bool:
        for x in range((self.MIDPOINT - 2), (self.MIDPOINT + 2), 4):
            servo(x)
            time.sleep(.05)
            scan1 = us_dist(15)
            # double check the distance
            scan2 = us_dist(15)
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.01)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            if scan1 < self.STOP_DIST:
                print("Doesn't look clear to me")
                return False
        return True



    # CHOOSING A PATH THAT ACCOUNTS FOR STOP DISTANCES
    def superChoosePath(self) -> str:
        print('Considering options...')
        if self.isClear():
            return "fwd"
        else:
            self.wideScan()
        # Attempt to use four different options instead of two
        avgFarRight = 0
        avgRight = 0
        avgLeft = 0
        avgFarLeft = 0
        # This is for the far right
        for x in range(self.MIDPOINT - 60, self.MIDPOINT - 29):
            if self.scan[x]:
                avgFarRight += self.scan[x]
        avgFarRight /= 30
        print('The average dist on the far right is ' + str(avgFarRight) + 'cm')
        # This is for the near right
        for x in range(self.MIDPOINT - 30, self.MIDPOINT):
            if self.scan[x]:
                avgRight += self.scan[x]
        avgRight /= 30
        print('The average dist on the near right is ' + str(avgRight) + ' cm')
        # This is for the near left
        for x in range(self.MIDPOINT, self.MIDPOINT + 30):
            if self.scan[x]:
                avgLeft += self.scan[x]
        avgLeft /= 30
        print('The average dist on the near left is ' + str(avgLeft) + ' cm')
        # This is for the far Left
        for x in range(self.MIDPOINT + 31, self.MIDPOINT + 60):
            if self.scan[x]:
                avgFarLeft += self.scan[x]
        avgFarLeft /= 30
        print('The average dist on the far left is ' + str(avgFarLeft) + 'cm')
        # Time to call whatever is the best choice
        if avgFarRight > avgFarLeft and avgFarRight > avgRight and avgFarRight > avgLeft:
            return "far right"
        if avgRight > avgFarRight and avgRight > avgLeft and avgRight > avgFarLeft:
            return "near right"
        if avgLeft > avgFarLeft and avgLeft > avgRight and avgLeft > avgFarRight:
            return "near left"
        if avgFarLeft > avgFarRight and avgFarLeft > avgRight and avgFarLeft > avgLeft:
            return "far left"
        else:
            return "stuck"



    #  MOVING SLOWLY FOREVER BUT STILL SCANNING
    def cruise(self):
        self.setSpeed(91, 110)
        # Have the robot drive forward without end
        fwd()
        while self.frontClear():
            print("It is clear. Time to fly!")
        self.stop()



    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        while True:
            # cruise forward
            if self.isClear():
                self.cruise()
            self.backUp()
            # if I had to stop, pick a better path
            #turn_target = self.kenny()
            #if turn_target < 0:
                #self.turnR(abs(turn_target))
            #else:
                #self.turnL(turn_target)

                ###################################################
                ######THIS IS THE OLD STUFF
                #######################################################

            # Choosing the direction
            answer = self.superChoosePath()
            print("\n---------------------------")
            print("\nI'M GOING TO THE TURN TO THE: " + answer)
            print("\n---------------------------")
            if answer == "far left":
                self.turnL(90)
                #self.turnL(turn_target)
            if answer == "near left":
                self.turnL(45)
                #self.turnL(turn_target)
            if answer == "near right":
                self.turnR(45)
                #self.turnR(turn_target)
            if answer == "far right":
                self.turnR(90)
            if answer == "stuck":
                self.encB(10)
                #self.turnR(turn_target)
                # If the robot goes into a tight space and cannot turn
                #elif answer == "There is no where to go":
                    #print("Since there's no where to go, I'll back up")
                    #self.encB(20)
                    #self.encL(15)
                #self.nav()




####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
