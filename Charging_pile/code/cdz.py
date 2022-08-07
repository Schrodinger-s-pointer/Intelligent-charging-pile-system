import os
from time import sleep
import master
import modbus_rtu
import uart_zigbee
import threading
import time
import config
import cd
import define
# import webapp.web_main
from MyQR import myqr
from multiprocessing import Process

# from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor

# device01_lock = threading.Event()
# device02_lock = threading.Event()
# stop_power_lock = threading.Event()

# 初始化上报
def init(Master):
    Master.auto_init()
    return 0


from PIL import Image


def image_change():
    image = Image.open('./image/code.png')
    imagechange = image.resize((250, 250))
    imagechange.save('./image/code.png')


def qr_creat():
    config.cfg_read()
    id = config.zhiyun_uid
    key = config.zhiyun_password
    MAC = "01:" + config.cdz_mac
    url = 'http://119.3.2.36/cdz_phone3.3/src/main/webapp/index.html?id=' + id + '&key=' + key + '&MAC=' + MAC + ''

    myqr.run(
        words=url,  # 包含信息
        # words='http',  # 包含信息
        version=1,
        # picture='./image/logo.png',  # 背景图片
        # colorized=True,  # 是否有颜色，如果为False则为黑白
        save_name='./image/code.png'  # 输出文件名
    )
    image_change()


if __name__ == '__main__':
    qr_creat()

    config.cfg_read()
    com = config.cdz_uart
    mac = config.cdz_mac
    bps = 115200
    U_Z = uart_zigbee.UART(com, bps)
    Master = master.Master(U_Z)

    # 开机初始化上报登录
    init(Master)
    task = threading.Thread(target=master.auto_control_zigbee, args=(U_Z, mac,))
    task.start()
    task.join()

