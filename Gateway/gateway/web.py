from socket import *
import http.client
import time
import config
import threading

thread_lock = threading.RLock()

date_now=''
time_now=''
def get_webservertime(host):
    conn=http.client.HTTPConnection(host)
    conn.request("GET", "/")
    r=conn.getresponse()
    ts=  r.getheader('date') #获取http头date部分
    #将GMT时间转换成北京时间
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    ttime=time.localtime(time.mktime(ltime)+8*60*60)
    global date_now,time_now
    date_now="%u%02u%02u"%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
    time_now="%02u:%02u:%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)

class Zhiyun:
    def __init__(self,ip,port):
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        self.server_ip = ip
        self.server_port = port
        self.send_data = ''
        self.recv_data = ''
        self.slave_get = ''
        self.if_to_uart = False

    def tcp_con(self):
        self.tcp_client_socket.connect((self.server_ip, self.server_port))
        uid= config.zhiyun_uid
        password= config.zhiyun_password
        self.send_data = "{\"method\":\"authenticate\",\"uid\":\""+uid+"\",\"key\":\""+password+"\",\"version\":\"0.1.0\",\"autodb\":true}"
        self.tcp_client_socket.send(self.send_data.encode("gbk"))

    def recv_msg(self,u_z,to_uart_lock):
        self.U_Z = u_z
        while True:
            self.recv_data = self.tcp_client_socket.recv(1024)
            thread_lock.acquire()
            print('智云发来的数据为:', self.recv_data.decode('gbk'))
            get_data=self.recv_data.decode()
            method_str = get_data.split('"')[3]
            if (method_str == 'echo'):
                print("心跳中。。。")
                continue
            if (method_str == 'authenticate_rsp'):
                print("登录智云成功")
                continue
            if (method_str == 'control'):

                data_str = get_data.split('"')[7]
                #加入日期和时间
                get_webservertime('www.baidu.com')
                data_str="{date="+date_now+",time="+time_now+","+data_str[1:]

                addr_str = get_data.split('"')[11]
                if addr_str[0:4]=="WIFI":
                    print("wifi mode")
                    self.slave_get = addr_str[5:] + "=" + data_str
                else:self.slave_get=addr_str + "=" + data_str
                self.U_Z.uart_send(self.slave_get)
            thread_lock.release()



    def heart_beat(self,to_web_lock):
        while True:
            if to_web_lock.wait(20):
                continue
            else:
                thread_lock.acquire()
                self.send_data = "{\"method\":\"echo\",\"timestamp\":1605141585800,\"seq\":5}"
                self.tcp_client_socket.send(self.send_data.encode("gbk"))
                thread_lock.release()


    def tcp_stop(self):
        self.tcp_client_socket.close()


    def tcp_send(self,data):
        print("上报智云中:"+data)
        self.tcp_client_socket.send(data.encode("gbk"))
