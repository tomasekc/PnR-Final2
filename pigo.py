# STUDENTS SHOULD NOT EDIT THIS FILE. IT WILL MAKE UPDATING MORE DIFFICULT

from gopigo import *
import time


##########################################################
#################### PIGO PARENT CLASS
#### (students will make their own class & inherit this)

class Pigo(object):
    MIDPOINT = 77
    STOP_DIST = 20
    RIGHT_SPEED = 200
    LEFT_SPEED = 200
    scan = [None] * 180

    def __init__(self):
        # this makes sure the parent handler doesn't take over student's
        if __name__ == "__main__":
            print('-----------------------')
            print('------- PARENT --------')
            print('-----------------------')
            # let's use an event-driven model, make a handler of sorts to listen for "events"
            self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)
            while True:
                self.stop()
                self.handler()

    ########################################
    #### FUNCTIONS REPLACED IN CHILD CHILD
    # Parent's handler is replaced by child's
    def handler(self):
        menu = {"1": ("Navigate forward", self.nav),
                "2": ("Rotate", self.rotate),
                "3": ("Dance", self.dance),
                "4": ("Calibrate", self.calibrate),
                "5": ("Forward", self.encF),
                "6": ("Open House Demo", self.openHouse),
                "q": ("Quit", quit)
                }
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])

        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()

    def openHouse(self):
        choice = input("1) Shy;  2) Spin.. ")
        if choice == "1":
            while True:
                if not self.isClear():
                    self.beShy()
        else:
            while True:
                if not self.isClear():
                    for x in range(5):
                        self.encR(2)
                        self.encL(2)
                    self.encR(15)

    def beShy(self):
        set_speed(80)
        self.encB(5)
        for x in range(3):
            servo(20)
            time.sleep(.1)
            servo(120)
            time.sleep(.1)
        self.encL(2)
        self.encR(2)
        self.encF(5)

    def nav(self):
        print("Parent nav")
        while True:
            choice = self.choosePath()
            if choice == "fwd":
                self.encF(18)
                while self.isClear():
                    self.encF(18)
            elif choice == "right":
                self.encR(6)
            elif choice == "left":
                self.encL(6)
            else:
                print("Can't find a path ahead.")
                break

    ##DANCING IS FOR THE CHILD CLASS
    def dance(self):
        print('Parent dance is lame.')
        for x in range(self.MIDPOINT - 20, self.MIDPOINT + 20, 5):
            servo(x)
            time.sleep(.1)
        self.encB(5)
        self.encR(5)
        self.encL(5)
        self.encF(5)
        for x in range(self.MIDPOINT - 20, self.MIDPOINT + 20, 10):
            servo(x)
            time.sleep(.1)

    ########################################
    ##### FUNCTIONS NOT INTENDED TO BE OVERWRITTEN
    def setSpeed(self, left, right):
        set_left_speed(left)
        set_right_speed(right)
        self.LEFT_SPEED = left
        self.RIGHT_SPEED = right
        print('Left speed set to: ' + str(left) + ' // Right set to: ' + str(right))

    def encF(self, enc):
        print('Moving ' + str((enc / 18)) + ' rotation(s) forward')
        enc_tgt(1, 1, enc)
        fwd()
        time.sleep((enc / 18) * 1.8)
        stop()

    def encR(self, enc):
        print('Moving ' + str((enc / 18)) + ' rotation(s) right')
        enc_tgt(1, 1, enc)
        right_rot()
        time.sleep((enc / 18) * 1.8)
        stop()

    def encL(self, enc):
        print('Moving ' + str((enc / 18)) + ' rotation(s) left')
        enc_tgt(1, 1, enc)
        left_rot()
        time.sleep((enc / 18) * 1.8)
        stop()

    def encB(self, enc):
        print('Moving ' + str((enc / 18)) + ' rotations(s) backwards')
        enc_tgt(1, 1, enc)
        bwd()
        time.sleep((enc / 18) * 1.8)
        stop()

    # HELP STUDENTS LEARN HOW TO PORTION TURN/SLEEP VALUES
    def rotate(self):
        print("We tell our robot to rotate then pause the app.")
        print("The longer the pause, the longer the turn.")
        print("We also like to slow our robot down for the turn.")
        while True:
            speed_adj = float(input("What modifier would you like to apply to your speed?"))
            set_left_speed(int(self.LEFT_SPEED * speed_adj))
            set_right_speed(int(self.RIGHT_SPEED * speed_adj))
            turn_time = float(input("How many seconds would you like to turn? "))
            right_rot()
            time.sleep(turn_time)
            self.stop()

    ##DUMP ALL VALUES IN THE SCAN ARRAY
    def flushScan(self):
        self.scan = [None] * 180

    # SEARCH 120 DEGREES COUNTING BY 2's
    def wideScan(self):
        # dump all values
        self.flushScan()
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, +2):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
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
            time.sleep(.01)

    def isClear(self) -> bool:
        for x in range((self.MIDPOINT - 15), (self.MIDPOINT + 15), 5):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            # double check the distance
            scan2 = us_dist(15)
            time.sleep(.1)
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

    # DECIDE WHICH WAY TO TURN
    def choosePath(self) -> str:
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
        if avgRight > avgLeft:
            return "right"
        else:
            return "left"

    def stop(self):
        print('All stop.')
        for x in range(3):
            stop()
        servo(self.MIDPOINT)
        time.sleep(0.05)
        disable_servo()

    def calibrate(self):
        print("Calibrating...")
        servo(self.MIDPOINT)
        response = input("Am I looking straight ahead? (y/n): ")
        if response == 'n':
            while True:
                response = input("Turn right, left, or am I done? (r/l/d): ")
                if response == "r":
                    self.MIDPOINT += 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                elif response == "l":
                    self.MIDPOINT -= 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                else:
                    print("Midpoint now saved to: " + str(self.MIDPOINT))
                    break
        response = input("Do you want to check if I'm driving straight? (y/n)")
        if response == 'y':

            while True:
                set_left_speed(self.LEFT_SPEED)
                set_right_speed(self.RIGHT_SPEED)
                print("Left: " + str(self.LEFT_SPEED) + "//  Right: " + str(self.RIGHT_SPEED))
                self.encF(9)
                response = input("Reduce left, reduce right or done? (l/r/d): ")
                if response == 'l':
                    self.LEFT_SPEED -= 10
                elif response == 'r':
                    self.RIGHT_SPEED -= 10
                else:
                    break

    # PRINTS THE CURRENT STATUS OF THE ROBOT
    def status(self):
        print("My power is at " + str(volt()) + " volts")
        print('Left speed set to: ' + str(self.LEFT_SPEED) + ' // Right set to: ' + str(self.RIGHT_SPEED))
        print('My MIDPOINT is set to: ' + str(self.MIDPOINT))
        print('I get scared when things are closer than ' + str(self.STOP_DIST) + 'cm')


########################
#### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


p = Pigo()