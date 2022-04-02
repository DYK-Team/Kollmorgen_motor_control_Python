import requests
# import os
import time
import subprocess
p = subprocess.Popen(['run_controller.cmd'])
time.sleep(5)

def Axis1SetZero():
    payload = {'Axis1SetZero': True}
    SetZero1 = requests.put('http://192.168.0.105/kas/plcvariables?format=text',data=payload)
    return SetZero1.status_code

def Axis2SetZero():
    payload = {'Axis2SetZero': True}
    SetZero2 = requests.put('http://192.168.0.105/kas/plcvariables?format=text',data=payload)
    return SetZero2.status_code

def ReadActualPosition12():
    ActualPos12 = requests.get('http://192.168.0.105/kas/plcvariables?variables=ActPos1,ActPos2&format=text')
    return ActualPos12.text  # two values separated with comma

# Returns only status codes; 200 - normal
def EnableMotors():
    payload = "OpenButton=False"
    EnableMotorsS1 = requests.put('http://192.168.0.105/kas/plcvariables?format=text', data=payload)
    payload = "CloseButton=True"
    EnableMotorsS2 = requests.put('http://192.168.0.105/kas/plcvariables?format=text', data=payload)
    Stat1Enabled = requests.get('http://192.168.0.105/kas/plcvariables?variables=Stat1Enabled&format=text')
    Stat2Enabled = requests.get('http://192.168.0.105/kas/plcvariables?variables=Stat2Enabled&format=text')
    return EnableMotorsS1.status_code, EnableMotorsS2.status_code, Stat1Enabled.text, Stat2Enabled.text

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

angle = 360.0  # dgrees
velocity = 150.0  # degree/second
acceleration = 900.0  # degree/second^2
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

print(ReadActualPosition12())

a = Axis1SetZero()
b = Axis2SetZero()
time.sleep(1)

print(Axis2Parameters(angle, velocity, acceleration))
print(Axis1Parameters(angle, velocity, acceleration))
a = EnableMotors()
time.sleep(2)
print(runMotors(1))
print(runMotors(2))