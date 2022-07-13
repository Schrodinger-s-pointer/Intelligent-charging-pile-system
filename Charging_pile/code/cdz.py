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

from MyQR import myqr


device01_lock = threading.Event()
device02_lock = threading.Event()
stop_power_lock = threading.Event()


#初始化上报
def init(Master):
    Master.auto_init()
    return 0



from PIL import Image
def image_change():
    image = Image.open('./qr_code/code.png')
    imagechange = image.resize((250,250))
    imagechange.save('./qr_code/code.png')

if __name__ == '__main__':

    config.cfg_read()
    id=config.zhiyun_uid
    key=config.zhiyun_password
    MAC="01:"+config.cdz_mac

    url = 'http://119.3.2.36/cdz_phone2.4/src/main/webapp/index.html?id=' + id + '&key=' + key + '&MAC=' + MAC + ''
    # 二维码制作
    myqr.run(
        words=url,  # 包含信息
        version=1,
        save_name='./image/code.png'  # 输出文件名
    )
    image_change()

    com = config.cdz_uart
    mac = config.cdz_mac
    bps = 115200
    U_Z = uart_zigbee.UART(com, bps)
    Master=master.Master(U_Z)

    #开机初始化上报登录
    init(Master)

    # 初始化完成后开始接收建立消息连接
    recv_zigbee = threading.Thread(target=master.auto_control_zigbee, args=(U_Z, mac,device01_lock,device02_lock,stop_power_lock))  # 打开来自ZIGBEE的接收线程
    recv_zigbee.setDaemon(True)  # 设置守护线程
    recv_zigbee.start()

    # 打开设备一控制线程
    charge01 = threading.Thread(target=master.charge_select, args=(mac, U_Z,device01_lock))
    charge01.setDaemon(True)  # 设置守护线程
    charge01.start()

    # 打开设备二控制线程
    charge02 = threading.Thread(target=master.charge_select, args=(mac, U_Z,device02_lock))
    charge02.setDaemon(True)  # 设置守护线程
    charge02.start()

    # 打开控制设备开关进程
    charge_off = threading.Thread(target=master.charge_select, args=(mac, U_Z,stop_power_lock))
    charge_off.setDaemon(True)  # 设置守护线程
    charge_off.start()

    # 打开自动上报状态
    auto_report = threading.Thread(target=Master.run, args=())
    auto_report.setDaemon(True)  # 设置守护线程
    auto_report.start()

    recv_zigbee.join()
    charge01.join()
    charge02.join()
    charge_off.join()



