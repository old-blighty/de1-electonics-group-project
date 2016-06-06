# Pilot script to control robot via bluetooth

print('Initialising Pilot Module')
print('Version 0.1')

from pyb import Pin, ADC, Timer

# Key global variables
direction = 'f'
speedL = 0
speedR = 0
critdistance = 30

# Defining the motor modules--------------------------------------
A1 = Pin('Y9',Pin.OUT_PP)
A2 = Pin('Y10',Pin.OUT_PP)
motor1 = Pin('X1')

B1 = Pin('Y11',Pin.OUT_PP)
B2 = Pin('Y12',Pin.OUT_PP)
motor2 = Pin('X2')

tim = Timer(2, freq = 1000)
ch1 = tim.channel(1, Timer.PWM, pin = motor1)
ch2 = tim.channel(2, Timer.PWM, pin = motor2)

# Ultrasound Echo Initialising -----------------------------------
Trigger = Pin('X3', Pin.OUT_PP)
Echo = Pin('X4',Pin.IN)
# Create a microseconds counter.
micros = pyb.Timer(5, prescaler=83, period=0x3fffffff)
micros.counter(0)
start = 0				# timestamp at rising edge of echo
end = 0					# timestamp at falling edge of echo

# -----------------------------------------------------------------

def direction(direction, speedL, speedR):
    # if speed is not zero then the car should stop first
    # slowdown not possible yet with L and R
    # we therefore call the stop function to stop for us
    (speedL, speedR) = stop()

    if direction == 'f':
    	A1.high()
    	A2.low()

    	B1.low()
    	B2.high()

        #return 'f'

    elif direction == 'b':
    	A1.low()
    	A2.high()

    	B1.high()
    	B2.low()

        #return 'b'

    print "Direction changed to: %s" % direction
    return (direction, speedL, speedR)

def speed(direction, mode, speedL, speedR):
    if direction == 'f':
        if mode == 'inc':
            if speedL < 96 and speedR < 96:
                speedL += 5
                speedR += 5

        elif mode == 'dec':
            if speedL > 4 and speedR > 4:
                speedL -= 5
                speedR -= 5

    elif direction == 'b':
        if mode == 'inc':
            if speedL > -96 and speedR > -96:
                speedL -= 5
                speedR -= 5

        elif mode == 'dec':
            if speedL < -4 and speedR < -4:
                speedL += 5
                speedR += 5

    setspeed(speedL,speedR)
    return (speedL,speedR)

def stop():
    speedL = 0
    speedR = 0
	A1.low()
	A2.low()
	B1.low()
	B2.low()

    setspeed(speedL,speedR)
    return (speedL, speedR)

def setspeed(speedL,speedR):
    	ch1.pulse_width_percent(speedL) # send a pulse of width 50% to motor1
    	ch2.pulse_width_percent(speedR) # send a pulse of width 50% to motor2

def turn(direction, speedL, speedR):
    if direction == 'l':
        if speedL > 4 and speedR <96:
            speedL -= 5
            speedR += 5

    elif direction == 'r':
        if speedL <96 and speedR >4:
            speedL += 5
            speedR -= 5

    setspeed(speedL,speedR)
    return (speedL,speedR)


# loop