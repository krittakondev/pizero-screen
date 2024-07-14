import asyncio
from pyrcrack.wrapper.airmon import AirmonNg
from pyrcrack.wrapper.airodump import AirodumpNg
from waveshare_epd import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont

async def capture_and_display():
    airmon = AirmonNg()
    airodump = AirodumpNg()

    # เริ่มต้น airmon-ng เพื่อเปิดโหมด monitor
    await airmon.start('wlan1')

    # เริ่มต้นการดักจับด้วย airodump-ng
    async for result in airodump(interface='wlan1'):
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)

        try:
            while True:
                # ดึงข้อมูลที่ต้องการแสดงผล
                packet_count = len(result['stations'])

                # สร้างภาพใหม่
                image = Image.new('1', (epd.height, epd.width), 255)
                draw = ImageDraw.Draw(image)

                # วาดข้อมูลบนภาพ
                draw.text((10, 10), f'Packets: {packet_count}', font=ImageFont.load_default(), fill=0)

                # แสดงผลบน E-Paper
                epd.display(epd.getbuffer(image))

                await asyncio.sleep(1)
        finally:
            epd.sleep()

asyncio.run(capture_and_display())

