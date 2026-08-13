import machine

from machine import Pin, SoftI2C
from machine_i2c_lcd import I2cLcd

from machine import I2C

import network
import urequests
import socket

import ntptime
import time
from time import sleep

import asyncio
import gc


delay = 60

pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

domains = [["google", "https://google.com"], ["duckduckgo", "https://duckduckgo.com/"], ["solarpoweredstuff", "https://solarpoweredstuff.net"]]

#old_minute = 0

ssid = "camp horsey ducky"
password = "nomoreshawwifi"

import os
print(os.listdir('/html'))
print(os.stat('/html/index.html'))   # index 6 in the tuple is size in bytes
print(os.stat('/html/style.css'))


# Define the LCD I2C address and dimensions
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C and LCD objects
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400000)

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)


#cycles through list of domains/IPs, checks HTTP/HTTPS status codes
async def check_connectivity():
#def check_connectivity():
    print("checking connectivity")
    
    for entry in domains:
        
        #gets a status code for each domain/IP
        try:
            status = urequests.get(entry[1])
            
            #200 is good
            if status.status_code == 200:
                lcd.clear()
                lcd.move_to(0, 0)
                
                lcd.putstr(f"{entry[0]}: online")
                print(f"{entry[0]}: online")
           
            else:
                #assumes that the site is offline                
                lcd.clear()
                lcd.move_to(0, 0)
                
                lcd.putstr(f"{entry[0]}: offline")
                print(f"{entry[0]}: offline")
                
            lcd.move_to(0, 1)
            lcd.putstr(f"Status Code: {status.status_code}")
            
            status.close()
            gc.collect()
        
        #if it gets no response...
        except:
            lcd.clear()
            lcd.move_to(0, 0)

            lcd.putstr(f"error: {entry[0]}")
            print("error")
            
            
        #gc.collect()
        await asyncio.sleep(delay//len(domains))


                
            
def connect_wifi(ssid, password):
    #print("Free memory:", gc.mem_free())
    print("trying to connect to wifi")
    lcd.clear()
    lcd.putstr("connecting...")
    
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    gc.collect()

    # Connect to your network
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    # Wait for connection
    timeout = 10
    while not station.isconnected() and timeout > 0:
        sleep(1)
        timeout -= 1
        print(f"timout: {timeout}")
        lcd.clear()
        lcd.putstr(f"timeout: {timeout}")
        #gc.collect()

    if station.isconnected():
        print("Connection successful")
        lcd.clear()
        lcd.putstr("successful")
        lcd.move_to(0, 1)
        lcd.putstr(station.ifconfig()[0])
        print(station.ifconfig())
        sleep(3)
        #gc.collect()
        return True
    else:
        print("Connection failed. Timeout reached")
        lcd.clear()
        lcd.putstr("failed :(")
        #gc.collect()
        return False
    gc.collect()
    

def sync_time():
    #gets the current time
    current_minute = time.localtime()[4]
    current_hour = time.localtime()[3]

    #syncs time every 24 hrs at midnight
    if current_hour == 0 and current_minute == 0:
        try:
            ntptime.settime()
            print("time synced")
    
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("time synced")
        except Exception as e:
            print("time not synced", e)
    
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("time not synced")
    
    gc.collect()
 


async def webserver():
    while True:
        try:
            cl, addr = s.accept()
            print('client connected from', addr)
            
            cl_file = cl.makefile('rwb', 0)
            request = cl_file.readline()
            
            # Discard headers
            while True:
                line = cl_file.readline()
                if not line or line == b'\r\n':
                    break
            
            if not request:
                cl.close()
                continue
                
            request = request.decode('utf-8')
            request_parts = request.split()
            path = request_parts[1] if len(request_parts) > 1 else '/'
            
            if path == '/style.css':
                response = b'HTTP/1.0 200 OK\r\nContent-Type: text/css\r\nConnection: close\r\n\r\n' + css
            else:
                response = b'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n' + html
            
            cl.sendall(response)
            cl.close()
            
        except Exception as e:
            print("error: ", e)
            await asyncio.sleep(0.1)
            
        
        
async def main():
    while True:
        await check_connectivity()

        await asyncio.sleep(1)


#main logic
#startup
print("hello")
lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("hello")
lcd.move_to(0, 1)
lcd.putstr("starting... :)")
sleep(1)

#connects to wifi
if not connect_wifi(ssid, password):
    lcd.clear()
    lcd.putstr("Check WiFi!")
    while True:
        sleep(5)

sync_time()

with open('/html/index.html', 'rb') as f:
    html = f.read()
    
with open('/html/style.css', 'rb') as f:
    css = f.read()

# html = b'<html><body><h1>ESP32 Online</h1></body></html>'
# css = b'body { font-family: sans-serif; }'
    

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]


s = socket.socket()
s.settimeout(2)
s.bind(addr)
s.listen(1)



loop = asyncio.get_event_loop()
loop.create_task(main())
loop.create_task(webserver())
loop.run_forever()


   
        

    
        
    
    

    
