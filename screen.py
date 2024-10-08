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

epd.init_fast()
epd.Clear(0xFF)
#time.sleep(1)

dirname, filename = os.path.split(os.path.abspath(__file__))


# tmp_check = ""

#batt_icon = Image.open(dirname+"/icon.png").convert('1')

def get_ip_address(interface):
    try:
        result = subprocess.run(['ip', 'addr', 'show', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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

step_anime = 0
iface = "wlan0"
ip = get_ip_address(iface)
def fetch_screen(text, stat):
    print(os.environ.get("env_screen"))
    now = datetime.now()
    time_str = now.strftime('%H:%M:%S')
    date_str = now.strftime('%Y-%m-%d')

    
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: สีขาว
    #bg_black = Image.new('1', (epd.height-20, epd.width), 0)  
    #image.paste(bg_black, (0,20))

    # check = time_str+date_str+text+str(stat)
    draw = ImageDraw.Draw(image)
    #draw.text((120, 50), "ดีจ้าาาา", font=font15, fill=255)  
    #global tmp_check 
    #if check != tmp_check:
    
    # tmp_check = check
    # print(epd.height, epd.width)
 
    draw.text((2, 1), time_str, font=font, fill=0)  # แสดงเวลา
    draw.text((80, 1), date_str, font=font, fill=0)  # แสดงวันที่
    draw.text((220, 1), text, font=font, fill=0)  

    global step_anime
    global ip
    global iface
    if step_anime > 23:
        step_anime = 0
        ip = get_ip_address(iface)
    anime_img = Image.open(f"{dirname}/pic/enterprise-confused-{step_anime}.bmp")
    image.paste(anime_img, (0,20))
    step_anime += 1


    cpu_per = psutil.cpu_percent()
    draw.text((8, 25), f"{iface}: {ip}", font=font, fill=255)  
    draw.text((8, 40), f"CPU: {cpu_per}%", font=font, fill=255)  
    draw.text((8, 55), f"MEM: {psutil.virtual_memory().percent}%", font=font, fill=255)  
    draw.text((8, 70), f"DISK: {psutil.disk_usage('/').percent}%", font=font, fill=255)  
    draw.text((8, 85), f"TEM: {psutil.sensors_temperatures()['cpu_thermal'][0].current} c", font=font, fill=255)  

    epd.displayPartial(epd.getbuffer(image))

    #finally:
def readVoltage(bus):
        "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
        read = bus.read_word_data(CW2015_ADDRESS, CW2015_REG_VCELL)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 0.305 /1000
        return voltage


def readCapacity(bus):
        "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
        read = bus.read_word_data(CW2015_ADDRESS, CW2015_REG_SOC)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped/256
        return capacity


def QuickStart(bus):
        "This function wake up the CW2015 and make a quick-start fuel-gauge calculations "
        bus.write_word_data(CW2015_ADDRESS, CW2015_REG_MODE, 0x30)
      



       
#----------------------------------------------------------------------------------
        
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN)  # GPIO4 is used to detect whether an external power supply is inserted
  
bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)


QuickStart(bus)

print ("  ")
print ("Initialize the CW2015 ......")



while True:
    try:
        print ("++++++++++++++++++++")
        print ("Voltage:%5.2fV" % readVoltage(bus))
        batt_per = readCapacity(bus)
        is_plug = GPIO.input(4)
        fetch_screen("%i%%" % batt_per, is_plug == GPIO.HIGH)

        # if batt_per == 100:
        #     print ("Battery FULL")
        # if batt_per < 5:
        #     print ("Battery LOW")

        #GPIO is high when power is plugged in
        # if (is_plug== GPIO.HIGH):       
        #     print ("Power Adapter Plug In ") 
        # if (is_plug == GPIO.LOW):      
        #     print ("Power Adapter Unplug")

    except KeyboardInterrupt:
        print("กด Ctrl+C แล้วออกโปรแกรม")
        exit()
    except Exception as e:
        #print(f"เกิดข้อผิดพลาด: {e}")
        raise e
 
