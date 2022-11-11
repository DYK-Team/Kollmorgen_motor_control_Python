# Warning: May need to be started twice!
import requests
# import os
import time
import subprocess

p = subprocess.Popen(['run_controller.cmd'])
# Testing launch error catching
# if p.poll() is not None:
#     print ("failed to start!")
#     exit(1)
# else:
#     p = subprocess.Popen(['run_controller.cmd'])

time.sleep(5)

def Axis1SetZero():
    payload = {'Axis1SetZero': False}
    SetZero1 = requests.put('http://192.168.0.105/kas/plcvariables?format=text',data=payload)
    payload = {'Axis1SetZero': True}
    SetZero1 = requests.put('http://192.168.0.105/kas/plcvariables?format=text', data=payload)
    return SetZero1.status_code

def Axis2SetZero():
    payload = {'Axis2SetZero': False}
    SetZero2 = requests.put('http://192.168.0.105/kas/plcvariables?format=text',data=payload)
    payload = {'Axis2SetZero': True}
    SetZero2 = requests.put('http://192.168.0.105/kas/plcvariables?format=text', data=payload)
    return SetZero2.status_code

def ReadActualPosition12():
    ActualPos12 = requests.get('http://192.168.0.105/kas/plcvariables?variables=ActPos1,ActPos2&format=text')
    return ActualPos12.text  # two values separated with comma

# Returns only status codes; 200 - normal
def EnableMotors(retry_num = 3):
    retry_attempts = 0
    try:
        payload = "OpenButton=False"
        EnableMotorsS1 = requests.put('http://192.168.0.105/kas/plcvariables?format=text', data=payload)
        payload = "CloseButton=True"
        EnableMotorsS2 = requests.put('http://192.168.0.105/kas/plcvariables?format=text', data=payload)
        Stat1Enabled = requests.get('http://192.168.0.105/kas/plcvariables?variables=Stat1Enabled&format=text')
        Stat2Enabled = requests.get('http://192.168.0.105/kas/plcvariables?variables=Stat2Enabled&format=text')
        return EnableMotorsS1.status_code, EnableMotorsS2.status_code, Stat1Enabled.text, Stat2Enabled.text
    except:
        print("trying again")
        if (retry_attempts <= retry_num):
            time.sleep(retry_attempts)
            retry_attempts += 1
            EnableMotors()
        else:
            print ("Failed to enable motors")
            return False

# Returns only status codes; 200 - normal
def DisableMotors():
    payload = "CloseButton=False"
    EnableMotorsS1 = requests.put('http://192.168.0.105/kas/plcvariables?format=text',data=payload)
    payload = "OpenButton=True"
    EnableMotorsS2 = requests.put('http://192.168.0.105/kas/plcvariables?format=text',data=payload)
    Stat1Enabled = requests.get('http://192.168.0.105/kas/plcvariables?variables=Stat1Enabled&format=text')
    Stat2Enabled = requests.get('http://192.168.0.105/kas/plcvariables?variables=Stat2Enabled&format=text')
    return EnableMotorsS1.status_code, EnableMotorsS2.status_code, Stat1Enabled.text, Stat2Enabled.text

def checkMotorReadiness1():
    Stat1Enabled = requests.get('http://192.168.0.105/kas/plcvariables?variables=Stat1Enabled&format=text')
    #print(Stat1Enabled.text)
    return Stat1Enabled.text  # staus code; 200 - normal

def checkMotorReadiness2():
    Stat2Enabled = requests.get('http://192.168.0.105/kas/plcvariables?variables=Stat1Enabled&format=text')
    #print(Stat2Enabled.text)
    return Stat2Enabled.text  # staus code; 200 - normal

# Change Axis1 parameters
def Axis1Parameters(angle, velocity, acceleration):
    payload1 = {'Axis1RelDistance': angle}
    payload2 = {'Axis1Vel': velocity}
    payload3 = {'Axis1Accel': acceleration}
    r1 = requests.put('http://192.168.0.105/kas/plcvariables?format=text',data=payload1)
    r2 = requests.put('http://192.168.0.105/kas/plcvariables?format=text', data=payload2)
    r2 = requests.put('http://192.168.0.105/kas/plcvariables?format=text', data=payload3)
    s1 = requests.get('http://192.168.0.105/kas/plcvariables?variables=Axis1RelDistance&format=text')
    s2 = requests.get('http://192.168.0.105/kas/plcvariables?variables=Axis1Vel&format=text')
    s3 = requests.get('http://192.168.0.105/kas/plcvariables?variables=Axis1Accel&format=text')
    if angle == float(s1.text):
        s1 = 1
    else:
        s1 = 0
    if velocity == float(s2.text):
        s2 = 1
    else:
        s2 = 0
    if acceleration == float(s3.text):
        s3 = 1
    else:
        s3 = 0
    return s1, s2, s3  # statuses: 1 - normal, 0 - fault

# Change Axis2 parameters
def Axis2Parameters(angle, velocity, acceleration):
    payload1 = {'Axis2RelDistance': angle}
    payload2 = {'Axis2Vel': velocity}
    payload3 = {'Axis2Accel': acceleration}
    r1 = requests.put('http://192.168.0.105/kas/plcvariables?format=text',data=payload1)
    r2 = requests.put('http://192.168.0.105/kas/plcvariables?format=text', data=payload2)
    r2 = requests.put('http://192.168.0.105/kas/plcvariables?format=text', data=payload3)
    s1 = requests.get('http://192.168.0.105/kas/plcvariables?variables=Axis2RelDistance&format=text')
    s2 = requests.get('http://192.168.0.105/kas/plcvariables?variables=Axis2Vel&format=text')
    s3 = requests.get('http://192.168.0.105/kas/plcvariables?variables=Axis2Accel&format=text')
    if angle == float(s1.text):
        s1 = 1
    else:
        s1 = 0
    if velocity == float(s2.text):
        s2 = 1
    else:
        s2 = 0
    if acceleration == float(s3.text):
        s3 = 1
    else:
        s3 = 0
    return s1, s2, s3  # statuses: 1 - normal, 0 - fault

def runMotors(axis):
    if axis == 1:
        payload = {'TestDrive1': True}
        DriveMotors = requests.put('http://192.168.0.105/kas/plcvariables?format=text', data=payload)
    elif axis == 2:
        payload = {'TestDrive2': True}
        DriveMotors = requests.put('http://192.168.0.105/kas/plcvariables?format=text', data=payload)
    return DriveMotors.status_code

def positionWaiter(timeout, threshold, rel_motion, prev_angle):
    # for i in range(0,10):
    print('control = ', float((ReadActualPosition12()).split(",")[0]))
    print ("outcome", ((abs(float((ReadActualPosition12()).split(",")[0])) - (prev_angle + rel_motion))))
    while ((abs(float((ReadActualPosition12()).split(",")[0]) - (prev_angle + rel_motion))) > threshold):
        actual_angle = ReadActualPosition12()
        time.sleep(timeout)
        print(actual_angle)

    print("match!")
    return True

# Motor tests
EnableMotors()
time.sleep(2)
Axis1SetZero()
Axis2SetZero()
time.sleep(2)

or_reading = ReadActualPosition12()
print("Initial position is: ", or_reading)
prev_angle = float((or_reading).split(",")[0])
print(prev_angle)
# Go to actual angle required
angle1 = 360.0  # dgrees
velocity = 150.0  # degree/second
acceleration = 600.0  # degree/second^2
#print(Axis2Parameters(angle2, velocity, acceleration))
print(Axis1Parameters(angle1, velocity, acceleration))

print(runMotors(1))
#print(runMotors(2))
#time.sleep(5)
positionWaiter(0.1, 0.5, angle1, prev_angle)

DisableMotors()
