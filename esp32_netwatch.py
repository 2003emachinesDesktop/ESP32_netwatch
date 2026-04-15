#designed to run on an ESP32 with a I2C 16x2 LCD, you may need to change things to run on your own hardware. 


from machine import Pin, SoftI2C
from machine_i2c_lcd import I2cLcd
from time import sleep

import time
import gc
import ntptime

import network
import urequests as requests

#input wifi network name and password
ssid = ""
password = ""

#put the domains or ip addresses that you want to check in a nested list (ip addresses must have 'http://' or 'https://'
#example: domains = [["google", "https://google.com"], ["yahoo", "https://yahoo.com"]

domains = 


# Define the LCD I2C address and dimensions
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C and LCD objects
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400000)

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)




# Connect to network
def connect_wifi(ssid, password):
    print("trying to connect to wifi")
    lcd.clear()
    lcd.putstr("connecting...")

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

    if station.isconnected():
        print("Connection successful")
        lcd.clear()
        lcd.putstr("successful")
        lcd.move_to(0, 1)
        lcd.putstr(station.ifconfig()[0])
        print(station.ifconfig())
        sleep(3)
        return True
    else:
        print("Connection failed. Timeout reached")
        lcd.clear()
        lcd.putstr("failed :(")
        return False




def check_connectivity():
    for entry in domains:
        
        try:
            status = requests.get(entry[1])
            
            if status.status_code == 200:
                lcd.clear()
                lcd.move_to(0, 0)
                
                lcd.putstr(f"{entry[0]}: online")
                print(f"{entry[0]}: online")
            
            else:
                lcd.clear()
                lcd.move_to(0, 0)
                
                lcd.putstr(f"{entry[0]}: offline")
                print(f"{entry[0]}: offline")
                
            lcd.move_to(0, 1)
            lcd.putstr(f"Status Code: {status.status_code}")
            
            status.close()
        
        except:
            lcd.clear()
            lcd.move_to(0, 0)

            lcd.putstr(f"error: {entry[0]}")
            print("error")
            
        gc.collect()
        sleep(5)
            

    
    
#main logic
    
lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("hello")
lcd.move_to(0, 1)
lcd.putstr("starting... :)")
sleep(3)

if not connect_wifi(ssid, password):
    lcd.clear()
    lcd.putstr("Check WiFi!")
    while True:
        sleep(5)


#syncs the device time to NTP time
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
    
    

while True:
    current_minute = time.localtime()[4]

    if current_minute % 5 == 0:
        print(f"current minute: {current_minute}")
        check_connectivity()
      
    #resets the time once an hr  
    if current_minute == 59:
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
