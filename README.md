# ESP32_netwatch
simple script to check internet and site connectivity, running on a ESP32 + I2C 16x2 LCD

i have a lot of raspberry pi servers making up a homelab. i created this project as a way to see if my servers are online and working, you can also use it to check if you can connect to other websites, like google etc, to make sure that you are connected, when running custom DNS servers or whatever. 

in my case, i am running pi-hole on my network and the pi board is really old (OG pi 1 256mb ram) and it goes offline every few weeks. so this way, i can see when the pi-hole server goes offline and can reboot it. 


i have it set to check uptime every 5 minutes, thats very easy to change. 

i plan on patching some small issues in the next few weeks/months:
  
