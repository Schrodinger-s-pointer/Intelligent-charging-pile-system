import binascii
import threading
from asyncio import sleep
import serial
import threading




class UART:
    def __init__(self,com,bps):
        # 端口：CNU； Linux上的/dev /ttyUSB0等； windows上的COM3等
        self.portx = com
        # 波特率，标准值有：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
        self.bps = bps
        # 超时设置，None：永远等待操作；
        #         0：立即返回请求结果；.02
        #        其他：等待超时时间（单位为秒）
        self.timex = 5
        # 打开串口，并得到串口对象
        self.ser = serial.Serial(self.portx, self.bps, timeout=self.timex)
        # 写数据
        self.recv_slave = ""
        self.if_to_web = False

    def uart_send(self,getway_data):
        try:
            result = self.ser.write(getway_data.encode())
            print("写总字节数：", result)
            print("下发数据：", getway_data)
        except Exception as e:
            print("发送数据失败：!", e)

    def uart_recv(self,to_web_lock,thread_lock):

        while True:
            if to_web_lock.wait(0.2):
                continue
            else:

                count = self.ser.inWaiting()
                if count > 5:
                    thread_lock.acquire()
                    self.recv_slave = (self.ser.read(count)).decode()
                    data = self.recv_slave.split("=",1)
                    self.addr_str=data[0]
                    self.data_str=data[1]
                    self.ser.flushInput()

                    to_web_lock.set()
                    thread_lock.release()
