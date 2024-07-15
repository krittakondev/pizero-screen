#!/usr/bin/env python
import struct
import sys
import time
import subprocess
import RPi.GPIO as GPIO
#from waveshare_epd import epd2in13_V4
import epaper
import os
from PIL import ImageFont, ImageDraw, Image
from datetime import datetime  
import psutil
import smbus
import asyncio

epd = epaper.epaper('epd2in13_V4').EPD()
font_path = '/usr/share/fonts/truetype/tlwg/Sawasdee-Bold.ttf'  # แก้ไขตามตำแหน่งไฟล์ฟอนต์ของคุณ
font_eng = "/usr/share/fonts-hack/woff/hack-bold.woff"
font_size = 12
font = ImageFont.truetype(font_eng, font_size, encoding="utf-8")
font15 = ImageFont.truetype(font_path, 15, encoding="utf-8")

CW2015_ADDRESS   = 0X62
CW2015_REG_VCELL = 0X02
CW2015_REG_SOC   = 0X04
CW2015_REG_MODE  = 0X0A
#time.sleep(1)



tmp_check = ""

class Screen:

    step_anime = 0
    iface = "wlan0"
    anime_img = []


    """
    color
    0 = black
    255 = white
    """
    text_color_top_bar = 0 
    text_color = 255
    
    
    
    def __init__(self):

        epd.init_fast()
        epd.Clear(0xFF)

        self.image_screen = Image.new('1', (epd.height, epd.width), 255)  # 255: สีขาว

        self.draw = ImageDraw.Draw(self.image_screen)

        self.bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

        self.QuickStart()

        self.dirname, self.filename = os.path.split(os.path.abspath(__file__))

        self.ip = self.get_ip_address()

        for i in range(23):
             self.anime_img.append(Image.open(f"{self.dirname}/pic/enterprise-confused-{i}.bmp").convert('1'))

    def get_ip_address(self):
        try:
            result = subprocess.run(['ip', 'addr', 'show', self.iface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                #raise Exception(f"Error getting IP address: {result.stderr}")
                return ""

            lines = result.stdout.split('\n')
            for line in lines:
                if 'inet ' in line:
                    ip_address = line.strip().split()[1].split('/')[0]
                    return ip_address
            #raise Exception(f"No IP address found for interface {interface}")
            return ""

        except Exception as e:
            return ""       #epd2in13_V4.epdconfig.module_exit()

    def update_top_bar(self):
        now = datetime.now()
        time_str = now.strftime('%H:%M:%S')
        date_str = now.strftime('%Y-%m-%d')

    
        self.draw.text((2, 1), time_str, font=font, fill=self.text_color_top_bar) 
        self.draw.text((80, 1), date_str, font=font, fill=self.text_color_top_bar)
        self.draw.text((220, 1), "%i%%" % readCapacity(self.bus), font=font, fill=self.text_color_top_bar)  
        # if stat:
        #     icon_width, icon_height = icon.size
        #     #image.paste(icon, (epd.height - 1 - icon_width, 1))
        #     image.paste(icon, (185, -10))

            #epd.display_fast(epd.getbuffer(image))

    def refresh(self):
        epd.displayPartial(epd.getbuffer(self.image_screen))

    def loop_anime(self):
        count = 0
        max = len(self.anime_img)-1
        while True:
            if count > max:
                count = 0
            
            print(count)
            self.update_backgroud(self.anime_img[count])

            self.refresh()
            count += 1
        

    def update_backgroud(self, img):
        self.image_screen.paste(img, (0,20))

    def update_status(self):

        cpu_per = psutil.cpu_percent()
        self.draw.text((8, 25), f"{self.iface}: {self.ip}", font=font, fill=self.text_color)  
        self.draw.text((8, 40), f"CPU: {cpu_per}%", font=font, fill=self.text_color)
        self.draw.text((8, 55), f"MEM: {psutil.virtual_memory().percent}%", font=font, fill=self.text_color)  
        self.draw.text((8, 70), f"DISK: {psutil.disk_usage('/').percent}%", font=font, fill=self.text_color)  
        self.draw.text((8, 85), f"TEM: {psutil.sensors_temperatures()['cpu_thermal'][0].current} c", font=font, fill=self.text_color)  


    #finally:
    def readVoltage(self):
            "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
            read = self.bus.read_word_data(CW2015_ADDRESS, CW2015_REG_VCELL)
            swapped = struct.unpack("<H", struct.pack(">H", read))[0]
            voltage = swapped * 0.305 /1000
            return voltage


    def readCapacity(self):
            "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
            read = self.bus.read_word_data(CW2015_ADDRESS, CW2015_REG_SOC)
            swapped = struct.unpack("<H", struct.pack(">H", read))[0]
            capacity = swapped/256
            return capacity


    def QuickStart(self):
            "This function wake up the CW2015 and make a quick-start fuel-gauge calculations "
            self.bus.write_word_data(CW2015_ADDRESS, CW2015_REG_MODE, 0x30)
      



       
#----------------------------------------------------------------------------------
        
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)  # GPIO4 is used to detect whether an external power supply is inserted
  


if __name__ == "__main__":
    print("start screen")

    try:
        screen = Screen()
        screen.loop_anime()

    
    except KeyboardInterrupt:
        print("กด Ctrl+C แล้วออกโปรแกรม")
        exit()
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        raise e

# while True:
#
#  print ("++++++++++++++++++++")
#  print ("Voltage:%5.2fV" % readVoltage(bus))
#  fetch_screen("%i%%" % readCapacity(bus), GPIO.input(4) == GPIO.HIGH)
#  
#  if readCapacity(bus) == 100:
#         print ("Battery FULL")
#  if readCapacity(bus) < 5:
#         print ("Battery LOW")
#
#
#
#
# #GPIO is high when power is plugged in
#  if (GPIO.input(4) == GPIO.HIGH):       
#         print ("Power Adapter Plug In ") 
#  if (GPIO.input(4) == GPIO.LOW):      
#         print ("Power Adapter Unplug")

 #time.sleep(0.02)
 
