print('Initialising Autodrive Module')
print('Version 1.0')

from pyb import Pin, ADC, Timer

# Key variables --------------------------------------------------
speed = 50 # standard driving speed
critdistance = 40 # critical stopping distance in cm


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

def stop():
	ch1.pulse_width_percent(0) # send a pulse of width 50% to motor1
	ch2.pulse_width_percent(0) # send a pulse of width 50% to motor2

def drive(speed): # Set direction to forward

	A1.high()
	A2.low()

	B1.low()
	B2.high()

	ch1.pulse_width_percent(speed) # send a pulse of width 50% to motor1
	ch2.pulse_width_percent(speed) # send a pulse of width 50% to motor2

def preventCollision(speed):

	# slowdown
	while speed > 0:
		speed = speed - 5
		ch1.pulse_width_percent(speed)
	 	ch2.pulse_width_percent(speed)
		pyb.delay(50) # delay for 50 millisec

	stop() # stop

	# reverse both motor direction
	A1.low()
	A2.high()

	B1.high()
	B2.low()

	# reversing
	ch1.pulse_width_percent(40)
	ch2.pulse_width_percent(40)
	pyb.delay(750) # run to allow reverse
	stop()
	pyb.delay(750)

	# reverse one motor direction
	B1.low()
	B2.high()

	# turn on the spot
	ch1.pulse_width_percent(40)
	ch2.pulse_width_percent(40)
	pyb.delay(500) # run to allow the turn

	stop() # stop
	pyb.delay(500)


drive(speed) # begin the drive

while True: # Distance feedback loop
	# Send a 20usec pulse every 10ms
	Trigger.high()
	pyb.udelay(20) #udelay uses argument in microseconds
	Trigger.low()

	# Wait until echo pulse goes from low to high
	while Echo.value() == 0:
		start = micros.counter()	# record start time of pulse

	# Wait until echo pulse goes from high to low
	while Echo.value() == 1:   # do nothing
		end = micros.counter()		# record end time of pulse

	# Calculate distance from delay duration
	distance = int(((end - start) / 2) / 29) # distance in cm
	print('Distance: ', distance, ' cm')

	if distance <= critdistance:
		preventCollision(speed)
	else:
		drive(50) # run drive(at 50%) func (which should correct the motor direction)

	pyb.delay(250) # delay 500 millisec before repeating loop
