"""
made by : PowerPizza or SciHack
description : my AI project. which track hand movement and move game character.
begin date : 11-09-2022
end data :16-09-2022
project : GyroController
"""

import serial
import serial.tools.list_ports as lp
from pynput.keyboard import Controller
from pynput.keyboard import Key
import time, json

configs = json.load(open("configs.json"))
isHardwareFound = False
s = serial.Serial()

def automate_serial():
    global isHardwareFound, s
    for ports in lp.comports():
        try:
            print(f"Testing connection at : {ports}")
            testSerial = serial.Serial(port=ports.name, baudrate=115200)
            if testSerial.readline() == b"BEGIN\r\n":
                isHardwareFound = True
                s = testSerial
                print("Hardware found at COM port :", ports.name)
        except BaseException as e:
            print(f"Connecting to COM port {ports.name} failed.\n\tError", e)
            input("Press enter to quit : ")
    if not isHardwareFound:
        print("No Hardware found for this driver!")
        input("Press enter to quit : ")

com_port = input("Enter COM port (hit enter to automate) : ")
if len(com_port) > 1:
    s = serial.Serial(port=com_port, baudrate=115200)
    if s.readline() == b"BEGIN\r\n":
        isHardwareFound = True
        print("Hardware found at COM port :", com_port)
else:
    automate_serial()

kb = Controller()
ct = time.perf_counter()  # current time counted

counterBtn = 0
counterBtn2 = 0

senstivityX = configs["sensitivity-X"]
senstivityY = configs["sensitivity-Y"]
sensorCooldown = configs["sensorCoolDown"]  # seconds

if isHardwareFound:
    while 1:
        data_ = s.readline().decode("utf-8").replace("\r\n", "").split(",")
        if len(data_) < 3:
            continue

        nt = time.perf_counter()  # new time counted

        if float(data_[0]) > senstivityX and (nt - ct) >= sensorCooldown:
            print("right")
            kb.press(Key.right)
            kb.release(Key.right)
            ct = nt
        elif float(data_[0]) < -senstivityX and (nt - ct) >= sensorCooldown:
            print("left")
            kb.press(Key.left)
            kb.release(Key.left)
            ct = nt

        if float(data_[1]) > senstivityY and (nt - ct) >= sensorCooldown:
            print("sneak")
            kb.press(Key.down)
            kb.release(Key.down)
            ct = nt
        elif float(data_[1]) < -senstivityY and (nt - ct) >= sensorCooldown:
            print("jump")
            kb.press(Key.up)
            kb.release(Key.up)
            ct = nt

        if int(data_[3]) == 0 and counterBtn == 0:
            print("escape")
            kb.press(Key.esc)
            kb.release(Key.esc)
            counterBtn = 1

        elif int(data_[4]) == 0 and counterBtn == 0:
            print("space")
            kb.press(Key.space)
            kb.release(Key.space)
            counterBtn = 1

        elif int(data_[4]) and int(data_[3]) and counterBtn:
            counterBtn = 0
