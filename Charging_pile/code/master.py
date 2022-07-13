from time import sleep
import threading
import modbus_rtu
import cd
import config
import define
import time

thread_lock = threading.RLock()
recv_lock = threading.Event()

stop = threading.Event()

pause = threading.Event()

lock = 1
D1 = -1
device = "00"

def recharge(u_z, mac, Addr):
    # 充电逻辑部分
    addr = Addr
    A1 = 0;A2 = 0;A3 = 0;A4 = 0
    config.cfg_read()
    mac_name = addr + ':' + config.cdz_mac
    table_name = cd.date_select()
    num = cd.num_select_easy(table_name, mac_name)
    while True:

        if stop.wait(15):
            stop.clear()
            if cd.power_select_easy(num, table_name) == 0:
                report_power_status(u_z,mac,Addr)
                break

            break
        if cd.power_select_easy(num, table_name) == 1:

            power = cd.power_select_easy(num, table_name)
            try:

                thread_lock.acquire()
                A1 = float("%.2f" % (modbus_rtu.read_current(addr)))
                A2 = float("%.2f" % (modbus_rtu.read_voltage(addr)))
                A3 = float("%.2f" % (modbus_rtu.read_Active_power(addr)))
                A4 = float("%.2f" % (modbus_rtu.read_always_active_power(addr)))
                thread_lock.release()

                cd.insert_state_easy(Addr, table_name, num, A2, A1, A3, A4)
                report_to_web(Addr, u_z, A2, A1, A3, A4, power)
                print("本次更新智云数据库成功。")
                if A1<0.001:
                    if modbus_rtu.power_off(Addr) == 'OFF':
                        if report_power_status(u_z,mac,Addr):
                            print("未接入用电器，自动断电。")
                            cd.insert_power(Addr,0)
            except(TypeError):
                pass
        else:
            print("充电结束。")
            break


def Analysis_command(u_z, Addr, command_text, command_value, mac):

    if command_text == 'A2' and command_value == '?':
        A2 = float("%.2f" % (modbus_rtu.read_voltage(Addr)))
        rep = []
        rep.append("A2=%.2f" % A2)
        if len(rep) > 0:
            dat = "{" + ",".join(rep) + "}"
            msg = Addr + ":" + mac + "=" + dat
            u_z.uart_send(msg)  # zigbee透传
        return

    if command_text == 'V3' and command_value == '?':
        config.cfg_read()
        V3 = config.cdz_gps
        rep = []
        rep.append("V3=%s" % V3)
        if len(rep) > 0:
            dat = "{" + ",".join(rep) + "}"
            msg = Addr + ":" + mac + "=" + dat
            u_z.uart_send(msg)  # zigbee透传
        return

    if command_text == 'date':
        cd.DATE = command_value  # 存储日期
    if command_text == 'time':
        cd.START_TIME=command_value# 存储开始时间
    if command_text == 'V1':
        cd.KWH = int(command_value)  # 存储购买电量
        print(cd.KWH)

    if command_text == 'OD1' and command_value == '1':
        print("充电开启中。")
        thread_lock.acquire()
        cd.MAC = Addr + ":" + mac
        if (cd.database_init()):  # 判断数据库是否写入
            if modbus_rtu.power_status(Addr) == 'OFF':
                if modbus_rtu.power_on(Addr) == 'ON':
                    if cd.insert_power(Addr, 1):
                        report_power_status(u_z, mac, Addr)
                        if report_power_status(u_z, mac, Addr):
                            print("数据初始化完成，开始充电。")
                            thread_lock.release()
                            pause.clear()

                            # 充电逻辑部分
                            # 完成零电量自动断电，写状态进入数据库，判断电量充多少
                            recharge(u_z, mac, Addr)
            else:
                report_power_status(u_z,mac,Addr)
                thread_lock.release()
                print(Addr+"号充电位之前已被开启，请停止后再试")


    if command_text == 'CD1' and command_value == '1':
        thread_lock.acquire()
        modbus_rtu.power_off(Addr)
        if modbus_rtu.power_status(Addr) == 'ON':
            if modbus_rtu.power_off(Addr) == 'OFF':
                cd.insert_power(Addr, 0)
                if cd.insert_power(Addr, 0):
                    stop.set()
                    print("数据登记关闭完成，关闭充电。")
                    msg1 = Addr + ":" + mac + "=" + "{D1=%d}" % 0
                    u_z.uart_send(msg1)
                    u_z.uart_send(msg1)

                pause.clear()
                thread_lock.release()
                print("关闭完成。")
        else:
            thread_lock.release()
            report_power_status(u_z, mac, Addr)
            print(Addr + "号充电位正处于关闭状态，请开启后再试")

def charge_select(mac, u_z,device_lock):
    global device, recv_data
    while True:
        if device_lock.wait():
            device_lock.clear()
            try:
                # 判断MAC地址
                if recv_data[17] == '=' and recv_data[3:17] == mac:
                    # 获取数据内容
                    Addr=recv_data[0:2]
                    recv_data = recv_data[18:]
                    if recv_data[0] == '{' and recv_data[-1] == '}':
                        order = recv_data[1:-1].split(",")
                        for i in order:
                            command = i.split("=")  # 拆指令
                            if len(command) == 2:
                                command_text = command[0]
                                command_value = command[1]
                                Analysis_command(u_z, Addr, command_text, command_value, mac)

                # lock = 1
            except(IndexError):
                print("发现异常！跳过本次循环。")
                pass
        recv_lock.clear()

def auto_control_zigbee(U_Z, mac,device01_lock,device02_lock,stop_power_lock):

    while True:
        print("------(接收网络控制中)------\n")
        global recv_data, device,pause
        recv_data = U_Z.uart_recv()
        device = recv_data[0:2]
        if device == "01":
            print("1号充电位指令")
            pause.set()
            device01_lock.set()
            stop_power_lock.set()

        if device == "02":
            print("2号充电位指令")
            pause.set()
            device02_lock.set()
            stop_power_lock.set()

def report_power_status(U_Z, mac, addr):
    thread_lock.acquire()
    status = -1
    status_str = modbus_rtu.power_status(addr)
    if status_str == 'OFF':
        status = 0
    if status_str == 'ON':
        status = 1
    if status != -1:
        global D1
        D1 = status
        msg1 = addr + ":" + mac + "=" + "{D1=%d}" % status
        U_Z.uart_send(msg1)  # zigbee透传
        thread_lock.release()
        return True

    else:
        print("report power error")
        thread_lock.release()
        return False


def report_to_web(addr, u_z, A2, A1, A3, A4, D1):
    rep = []
    rep.append("A1=%.2f" % A1)
    rep.append("A2=%.2f" % A2)
    rep.append("A3=%.2f" % A3)
    rep.append("A4=%.2f" % A4)
    rep.append("D1=%d" % D1)

    if len(rep) > 0:
        config.cfg_read()
        dat = "{" + ",".join(rep) + "}"
        msg = addr + ":" + config.cdz_mac + "=" + dat
        u_z.uart_send(msg)


class Master:
    def __init__(self, u_z):
        print("==================")
        config.cfg_read()
        self.U_Z = u_z  # zigbee串口
        self.mac = config.cdz_mac
        self.addr = ''
        self.D0 = 0xff  # 主动上报使能
        self.D1 = 0  # 开关控制

        self.A0 = 0.00  # 历史用电量
        self.A1 = 0.00  # 电流
        self.A2 = 0.00  # 电压
        self.A3 = 0.00  # 功率
        self.A4 = 0.00  # 实时负载充电

        self.A5 = 0  #
        self.A6 = 0  # 充电开始时间
        self.A7 = 0  # 充电结束时间

        self.V0 = int(config.cdz_time) # 主动上报时间间隔
        self.V1 = 0  # 储值电量

        self.V3 = config.cdz_gps  # gps 经度 纬度
        self.INIT = 0


    def auto_init(self):
        thread_lock.acquire()
        for iter in define.addr_list:
            self.INIT = 1
            self.addr = iter
            modbus_rtu.power_on(str(iter))
            modbus_rtu.power_off(iter)
            report_power_status(self.U_Z, self.mac, iter)
            self.get_status_report(iter)
        thread_lock.release()

    def set_addr(self, addr):
        self.addr = addr

    def sendmsg(self, U_Z, dat):

        thread_lock.acquire()
        msg = self.addr + ":" + self.mac + "=" + dat
        U_Z.uart_send(msg)  # zigbee透传
        thread_lock.release()

    def get_status_report(self,addr):
        try:
            self.A1 = float("%.2f" % (modbus_rtu.read_current(addr)))
            self.A2 = float("%.2f" % (modbus_rtu.read_voltage(addr)))
            self.A3 = float("%.2f" % (modbus_rtu.read_Active_power(addr)))
            self.A4 = float("%.2f" % (modbus_rtu.read_always_active_power(addr)))

            status_str = modbus_rtu.power_status(addr)
            if status_str == 'OFF':
                self.D1 = 0
            if status_str == 'ON':
                self.D1= 1
            rep = []
            rep.append("A0=%.2f" % self.A0)
            rep.append("A1=%.2f" % self.A1)
            rep.append("A2=%.2f" % self.A2)
            rep.append("A3=%.2f" % self.A3)
            rep.append("A4=%.2f" % self.A4)
            if status_str == 'OFF' or status_str == 'ON':
                rep.append("D1=%d" % self.D1)
            if self.INIT == 1:
                rep.append("V3=%s" % self.V3)
                self.INIT = 0

            if len(rep) > 0:
                dat = "{" + ",".join(rep) + "}"
                self.sendmsg(self.U_Z, dat)

        except(TypeError):
            pass


    def run(self):
        print("\n+++++---开始自动上报----+++++\n")
        while True:
            global pause
            try:
                if pause.wait(10):
                    continue
                else:
                    thread_lock.acquire()
                    print("\n轮询状态中\n")
                    for iter in define.addr_list:
                        self.addr = iter
                        self.get_status_report(iter)
                    thread_lock.release()

            except(TypeError):
                thread_lock.release()
                print("本轮上报错误")
                pass


