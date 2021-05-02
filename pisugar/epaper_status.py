#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13b_V3
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import datetime

import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


import subprocess
import re
def get_ssid():
    # r = re.compile('ESSID:"([^"]+)"')
    output = subprocess.check_output(['sudo', 'iwgetid']).decode("UTF-8").strip()
    # print(output)
    # m = r.match(output)
    # if m:
    #     return m.group(1)
    return output

logging.basicConfig(level=logging.DEBUG)

try:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = get_ip()
    ssid = get_ssid()

    logging.info("e-paper status script: {0}".format(timestamp))
    logging.info(ssid)

    epd = epd2in13b_V3.EPD()
    epd.init()
    epd.Clear()
    time.sleep(1)

    # Drawing on the image
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)

    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red or yellow image

    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)

    drawblack.text((10, 0), ssid, font = font20, fill = 0)   
    drawblack.text((10, 20), "IP Address: {0}".format(ip_address), font = font16, fill = 0)
    drawblack.text((10, 90), "Last Updated: {0}".format(timestamp), font = font12, fill = 0)

    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(2)

    epd.sleep()
    time.sleep(3)
    epd.Dev_exit()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13b_V3.epdconfig.module_exit()
    exit()
