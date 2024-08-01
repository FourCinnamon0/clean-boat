from machine import Pin, PWM
from time import sleep
from math import floor
import network
import socket
from MPU6050 import MPU6050 #https://github.com/Lezgend/MPU6050-MicroPython


ap_if = network.WLAN(network.AP_IF)
ap_if.active(True)
ap_if.config(essid="DebriSweeper", password="CleanBoat11")

frequency = 500
ESC_LEFT = PWM(Pin(13), frequency)
def thrust_left(val):# -1 < val < 1
  ESC_LEFT.duty(floor((0.25*val+0.75) * 1023))
 
ESC_RIGHT = PWM(Pin(12), frequency)
mpu = MPU6050()
def thrust_right(val):# -1 < val < 1
  ESC_RIGHT.duty(floor((0.25*val+0.75) * 1023))
  
def go(fwd,rot):
	# fwd => gas pedal
	# rot => steering wheel
	thrust_left((fwd+rot)/(1+abs(rot)))
	thrust_left((fwd-rot)/(1+abs(rot)))

#thrust_left(0)
#thrust_right(0)


while ap_if.active() == False:
  pass

print('Connection successful')
print(ap_if.ifconfig())
#led=Pin(2,Pin.OUT)

from machine import UART


def web_page():
  #if led.value() == 1:
  #  gpio_state="ON"
  #else:
  #  gpio_state="OFF"
  
  html = """<html><head> <title>BOAT</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body><script>l = document.getElementById("l");r = document.getElementById("r");function thrust(){window.location = `http://192.168.4.1/?${l.value}&${r.value}`}</script>
  <input type="range" min="-1" max="1" value="0" id="l" onchange="thrust()" step="0.0009775171"><br><input type="range" min="-1" max="1" value="0" id="r" onchange="thrust()" step="0.0009775171"><script>l = document.getElementById("l");r = document.getElementById("r");function thrust(){window.location = `/?${l.value}&${r.value}`}</script>
  </body></html>"""
  #html = f"{accel}"
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 83))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  url_stat = request.split(" ")[1][2:].split("&")
  if(len(url_stat)==2):
    print(url_stat)
    desired_l = float(url_stat[0])
    desired_r = float(url_stat[1])
    print(desired_l)
    print(desired_r)
    thrust_left(desired_l)
    thrust_right(desired_r)
  
  #accel = mpu.read_accel_data()
  #gyro = mpu.read_gyro_data()
  #print(floor(accel["x"]),floor(accel["y"]),floor(accel["z"]),floor(mpu.read_temperature()),floor(gyro["x"]),floor(gyro["y"]),floor(gyro["z"]),mpu.read_angle(),mpu.read_accel_abs())
  #sleep(0.1)
  #response = web_page("x: " + str(accel["x"]) + " y: " + str(accel["y"]) + " z: " + str(accel["z"]) + " temp: " + str(mpu.read_temperature()))
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
  
uart1 = UART(1, baudrate=9600, tx=33, rx=32)
  
def read_distance():
    # Send the trigger command
    uart1.write(b"\xff")
    sleep(0.1)
    
    # Read 4 bytes from the UART
    data = uart1.read(4)
    # print(list(data))
    if data and len(data) == 4:
        # Parse the received data
        header, high_byte, low_byte, checksum = data
        
        # Validate the header
        if header == 0xFF:
            # Calculate the checksum
            calculated_checksum = (header + high_byte + low_byte) & 0xFF
            
            # Validate the checksum
            # print(header,(high_byte << 8) + low_byte,checksum,calculated_checksum)
            if calculated_checksum == checksum:
                # Calculate the distance in cm
                distance = (high_byte << 8) + low_byte
                return distance/10
    
    return None
    
    
print(read_distance())
#while(True):
#  print(read_distance())
#accel = mpu.read_accel_data()
#gyro = mpu.read_gyro_data()
#print((accel["x"]),(accel["y"]),(accel["z"]),(mpu.read_temperature()),(gyro["x"]),(gyro["y"]),(gyro["z"]))#,mpu.read_angle(),mpu.read_accel_abs())
#sleep(0.1)
