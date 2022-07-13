import binascii
import threading
import time
import serial


# 端口：CNU； Linux上的/dev /ttyUSB0等； windows上的COM3等
portx = "/dev/ttyS1"
# portx = "COM3"
# 波特率，标准值有：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
bps = 9600
# 超时设置，None：永远等待操作；
#         0：立即返回请求结果；.02
#        其他：等待超时时间（单位为秒）
timex = 5
# 打开串口，并得到串口对象
ser = serial.Serial(portx, bps, timeout=timex)
# 写数据

def uart_send(rtu_all):
    try:
        d = bytes.fromhex(rtu_all)
        result = ser.write(d)
        print("写总字节数：", result)
    except Exception as e:
        print("error!", e)

def uart_recv():
    while True:
        time.sleep(0.02)
        count = ser.inWaiting()
        if count > 0:
            data = ser.read(count)
            if data != b'':
                recv_data=str(binascii.b2a_hex(data))[2:-1]
                return recv_data

