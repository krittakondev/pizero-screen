from scapy.all import sniff
#from waveshare_epd import epd2in13_V4
import epaper
from PIL import Image, ImageDraw, ImageFont

packet_count = 0

def packet_handler(packet):
    global packet_count
    packet_count += 1

    epd = epaper.epaper("epd2in13_V4").EPD()
    epd.init_fast()

    # สร้างภาพใหม่
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    # วาดข้อมูลบนภาพ
    draw.text((10, 10), f'Packets: {packet_count}', font=ImageFont.load_default(), fill=0)

    # แสดงผลบน E-Paper
    #epd.displayPartial(epd.getbuffer(image))
    epd.display_fast(epd.getbuffer(image))
    epd.sleep()

# เริ่มดักจับแพ็กเก็ต
sniff(iface='wlan1', prn=packet_handler)

