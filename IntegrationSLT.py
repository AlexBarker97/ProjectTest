import time, RPi.GPIO as gpio, numpy as np, matplotlib, serial, binascii, threading, math
matplotlib.use('Agg')
import matplotlib.pyplot as plt

hex2dec = {"0": 0,  "1": 1,  "2": 2,  "3": 3,
           "4": 4,  "5": 5,  "6": 6,  "7": 7,
           "8": 8,  "9": 9,  "a": 10, "b": 11,
           "c": 12, "d": 13, "e": 14, "f": 15}

def Mapping():
    x=[]
    y=[]
    i=0
    while i < len(theta):
        if theta[i] < 90:
            x.append((-r[i])*(math.cos(theta[i]*math.pi/180)))
            y.append(r[i]*(math.sin(theta[i]*math.pi/180)))
        else:
            x.append(r[i]*math.sin((theta[i]-90)*math.pi/180))
            y.append(r[i]*math.cos((theta[i]-90)*math.pi/180))
        print(x[i],y[i])
        i += 1
    plt.scatter(x, y)
    plt.savefig('map.png')

def lidarReadings():
    global value
    global res0
    global res1
    while True:
        result = binascii.hexlify(ser.read(8))
        result = str(result)
        res0 = hex2dec[result[2]]
        res1 = hex2dec[result[3]]
        res2 = hex2dec[result[4]]
        res3 = hex2dec[result[5]]
        res4 = hex2dec[result[6]]
        res5 = hex2dec[result[7]]
        res6 = hex2dec[result[8]]
        res7 = hex2dec[result[9]]
        value = 0
        value = value + (res2*(16**5)) + (res3*(16**4)) + (res4*(16**3)) + (res5*(16**2)) + (res6*(16**1)) + (res7*(16**0))
        value = ((value-35811)/2446.1)
        if duty <= 17:
            Mapping()
            break
    
def setDuty():
    global duty
    global p
    duty = 85
    time.sleep(0.2)
    p = gpio.PWM(18, 366)
    p.start(duty)
    while True:
        duty -= 1
        p.ChangeDutyCycle(duty)
        if duty >= 18:
            r.append(value)
            theta.append(((duty-10)*180)/67)
            time.sleep(0.1)
        else:
            break

global r
global theta
r = []
theta = []

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(18, gpio.OUT) #pin 18 (panservo) set to output

while True:       
    ser = serial.Serial()
    ser.close()
    ser.port = '/dev/ttyUSB0'
    ser.baudrate = 115200
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = serial.EIGHTBITS
    ser.timeout = 10
    ser.open()
    ser.write(bytes('P', 'UTF-8'))
    ser.write(bytes('T', 'UTF-8'))
    result = binascii.hexlify(ser.read(8))
    result = str(result)
    res0 = hex2dec[result[2]]
    res1 = hex2dec[result[3]]
    res2 = hex2dec[result[4]]
    res3 = hex2dec[result[5]]
    res4 = hex2dec[result[6]]
    res5 = hex2dec[result[7]]
    res6 = hex2dec[result[8]]
    res7 = hex2dec[result[9]]
    if ((str(res0) == "5") and (str(res1) == "4")):
        thread1 = threading.Thread(target=lidarReadings)
        thread1.start()
        thread2 = threading.Thread(target=setDuty)
        thread2.start()
        break
    else:
        ser.close()
        ser.port = '/dev/ttyUSB0'
        ser.baudrate = 115200
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.bytesize = serial.EIGHTBITS
        ser.timeout = 10
        ser.open()
        ser.write(bytes('P', 'UTF-8'))
        ser.write(bytes('T', 'UTF-8'))
