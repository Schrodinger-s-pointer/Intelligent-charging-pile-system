import binascii
import threading
from time import sleep
import serial




class UART:
    def __init__(self,com,bps):
        # 端口：CNU； Linux上的/dev /ttyUSB0等； windows上的COM3等
        self.portx = com
        # 波特率，标准值有：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
        self.bps = 115200
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

                # 串口发送数据
                result = self.ser.write(getway_data.encode())
                print("写总字节数：", result)
                print("发送数据：", getway_data)
            except Exception as e:
                print("error!", e)
            sleep(0.15)

    def uart_recv(self):
        judge="="
        while True:

            sleep(0.1)
            self.if_to_web = False
            count = self.ser.inWaiting()
            if count > 0:
                self.recv_slave = (self.ser.read(count)).decode()
                if self.recv_slave.find(judge)!=-1:
                    data = self.recv_slave.split("=",1)
                    self.addr_str=data[0]
                    self.data_str=data[1]
                    self.if_to_web = True
                    print("接收数据：", self.recv_slave)
                    return  self.recv_slave

