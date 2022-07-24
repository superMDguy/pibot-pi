from Adafruit_MotorHAT import Adafruit_MotorHAT
import socket
from threading import Thread
from queue import Queue

mh = Adafruit_MotorHAT()
steer = mh.getMotor(1)
drive = mh.getMotor(4)
SPEED = 255
TURN_AMT = 210

current_drive = 1 # 0 = back, 1 = none, 2 = forward
current_turn = 1  # 0 = left, 1 = none, 2 = right

def forward(speed=SPEED):
    global current_drive
    drive.run(Adafruit_MotorHAT.FORWARD)
    drive.setSpeed(speed)
    current_drive = 2


def backward(speed=SPEED):
    global current_drive
    drive.run(Adafruit_MotorHAT.BACKWARD)
    drive.setSpeed(speed)
    current_drive = 0


def stop_driving():
    global current_drive
    drive.run(Adafruit_MotorHAT.RELEASE)
    current_drive = 1


def stop_turning():
    global current_turn
    steer.run(Adafruit_MotorHAT.RELEASE)
    current_turn = 1

def left():
    global current_turn
    steer.run(Adafruit_MotorHAT.BACKWARD)
    steer.setSpeed(TURN_AMT)
    current_turn = 0


def right():
    global current_turn
    steer.run(Adafruit_MotorHAT.FORWARD)
    steer.setSpeed(TURN_AMT)
    current_turn = 2

def runQueryServer():
    HOST = '0.0.0.0'
    PORT = 9001

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    conn, addr = s.accept()
    print(addr[0], 'connected')

    while True:
        data = conn.recv(1024)
        conn.sendall(bytes((current_drive, current_turn)))

queryServer = Thread(target=runQueryServer)
queryServer.start()

commandMap = {"go": forward, "back": backward,
              "left": left, "right": right, "stop_drive": stop_driving, "stop_turn": stop_turning}
if __name__ == "__main__":
    while True:
        cmd = input_nowait()
        commandMap[cmd]()
