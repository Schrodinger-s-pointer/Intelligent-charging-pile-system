from time import sleep
import threading
import modbus_rtu
import cd
import config
import define

from queue import Queue

import inspect
import ctypes

select_queue = Queue(2)

handshake_active = Queue(1)
handshake_passive = Queue(1)
charge_stop_01 = Queue(1)
charge_stop_02 = Queue(1)

thread_lock = threading.RLock()
recv_lock01 = threading.Event()
recv_lock02 = threading.Event()

pause = threading.Event()

D1 = -1
device = "00"
# recv_data = ''
recv_data_ahead = ''
recv_data_rear = ''


def recharge(u_z, mac, Addr, charge_cycle):
    # 充电逻辑部分
    addr = Addr
    if Addr == "01":
        cycle = recv_lock01
        charge_stop = charge_stop_01

        cycle.set()
    if Addr == "02":
        cycle = recv_lock02
        charge_stop = charge_stop_02
        cycle.set()
    # print("充电周期开启")

    config.cfg_read()
    mac_name = addr + ':' + config.cdz_mac
    table_name = cd.date_select()
    num = cd.num_select_easy(table_name, mac_name)

    A1 = float("%.2f" % (modbus_rtu.read_current(addr)))  # ！！存在使用过程中可能会报错的问题
    A2 = float("%.2f" % (modbus_rtu.read_voltage(addr)))
    A3 = float("%.2f" % (modbus_rtu.read_Active_power(addr)))
    A4 = float("%.2f" % (modbus_rtu.read_always_active_power(addr)))
    # print("准备数据库中。")
    cd.insert_state_easy(Addr, table_name, num, A2, A1, A3, A4)
    print("充电循环开始")
    count_close=0
    while True:
        try:
            if charge_stop.get(timeout=10) == addr + "stop":
                print("准备关闭充电")
                # print("modbus_rtu.power_off(Addr)", modbus_rtu.power_off(Addr))
                while not modbus_rtu.power_off(Addr) == 'OFF':
                    sleep(0.1)
                print("设备关闭成功")
                cycle.clear()
                if cd.insert_power(Addr, 0):
                    print("数据登记关闭完成，关闭充电。")

                    msg1 = Addr + ":" + mac + "=" + "{D1=%d}" % 0
                    u_z.uart_send(msg1)
                    u_z.uart_send(msg1)
                    cycle.clear()

                    pause.clear()
                    print("关闭完成。")
                    break
        except:
            if cd.power_select_easy(num, table_name) == 1:
                power = cd.power_select_easy(num, table_name)
                try:
                    # thread_lock.acquire()
                    A1 = float("%.2f" % (modbus_rtu.read_current(addr)))  # ！！存在使用过程中可能会报错的问题
                    A2 = float("%.2f" % (modbus_rtu.read_voltage(addr)))
                    A3 = float("%.2f" % (modbus_rtu.read_Active_power(addr)))
                    A4 = float("%.2f" % (modbus_rtu.read_always_active_power(addr)))
                    # thread_lock.release()

                    if A1<0.0001:
                        count_close=count_close+1
                        if count_close>1:
                            print("空载自动断电")
                            # print("modbus_rtu.power_off(Addr)", modbus_rtu.power_off(Addr))
                            while not modbus_rtu.power_off(Addr) == 'OFF':
                                sleep(0.1)
                            print("设备关闭成功")
                            cycle.clear()
                            if cd.insert_power(Addr, 0):
                                print("数据登记关闭完成，关闭充电。")

                                msg1 = Addr + ":" + mac + "=" + "{D1=%d}" % 0
                                u_z.uart_send(msg1)
                                u_z.uart_send(msg1)
                                cycle.clear()

                                pause.clear()
                                print("关闭完成。")
                                break

                    print("准备更新数据库。")
                    cd.insert_state_easy(Addr, table_name, num, A2, A1, A3, A4)
                    report_to_web(Addr, u_z, A2, A1, A3, A4, power)
                    # print("本次登记数据库成功。")
                    print("本次更新智云数据库成功。")
                except(TypeError):
                    pass
                # if A1>=0.2:
                #     cd.insert_state(Addr,A2,A1,A3,A4)
                #     report_to_web(Addr, u_z, A2, A1, A3, A4, power)
                #     print("本次登记数据库成功。")
                #     print("本次更新智云数据库成功。")
                # if A1<0.001:
                #     if modbus_rtu.power_off(Addr) == 'OFF':
                #         if report_power_status(u_z,mac,Addr):
                #             print("未接入用电器，自动断电。")
                #             cd.insert_power(Addr,0)
                #             cd.install_stop_time(Addr,"16:55:33")
                #             return 0
            else:
                print("充电结束。")
                break
    return 0



def Analysis_command(u_z, Addr, command_text, command_value, mac, charge_cycle):
    # print("------(Analysis_command)------")
    # print("-----------指令解析ing-----------")
    # print(command_text + ":" + command_value)

    if command_text == 'A2' and command_value == '?':
        # print("A2 ing...")
        if Addr == "01":
            cycle = recv_lock01
        if Addr == "02":
            cycle = recv_lock02
        try:
            A2 = float("%.2f" % (modbus_rtu.read_voltage(Addr)))
            config.cfg_read()
            V3 = config.cdz_gps
            status = -1
            # print("开始查询开关！！！！")

            status_str = modbus_rtu.power_status(Addr)
            # print("开始查询开关:", status_str)
            if status_str == 'OFF':
                status = 0
                cycle.clear()
            if status_str == 'ON':
                status = 1
            if status != -1:
                global D1
                D1 = status
            # print("ing...")

            rep = []
            rep.append("A2=%.2f" % A2)
            rep.append("V3=%s" % V3)
            rep.append("D1=%d" % D1)
            if len(rep) > 0:
                dat = "{" + ",".join(rep) + "}"
                # thread_lock.acquire()
                msg = Addr + ":" + mac + "=" + dat
                u_z.uart_send(msg)  # zigbee透传
                # thread_lock.release()
            return
        except(TypeError):
            print("刷新失败，请重试")
            return

    if command_text == 'date':
        # print("存储日期完成。")
        cd.DATE = command_value  # 存储日期
        # print(cd.DATE)
    if command_text == 'time':
        # print("存储开始时间完成。")
        cd.START_TIME = command_value  # 存储开始时间
    if command_text == 'V1':
        # print("存储购买电量完成。")
        cd.KWH = int(command_value)  # 存储购买电量
        # print(cd.KWH)

    if command_text == 'OD1' and command_value == '1':
        print("充电开启中。")
        if Addr == "01":
            cycle = recv_lock01
        if Addr == "02":
            cycle = recv_lock02

        cd.MAC = Addr + ":" + mac
        if modbus_rtu.power_status(Addr) == 'OFF':
            print("握手开始")
            handshake_active.put(Addr + "ok")
            print("右边伸手")
            if handshake_passive.get() == Addr + "go":
                # print("右边握手")
                handshake_active.put(Addr + "fine")
                sleep(0.2)

                if cd.database_init():  # 判断数据库是否写入
                    if cd.insert_power(Addr, 1):
                        while not modbus_rtu.power_on(Addr) == 'ON':
                            sleep(0.1)

                        while not report_power_status(u_z, mac, Addr):
                            sleep(0.1)

                        # if report_power_status(u_z, mac, Addr) or report_power_status(u_z, mac, Addr):
                        print("数据初始化完成，开始充电。")
                        cycle.set()
                        # thread_lock.release()
                        pause.clear()
                        while not handshake_active.empty():
                            handshake_active.get()
                        while not handshake_passive.empty():
                            handshake_passive.get()
                        if Addr == "01":
                            while not charge_stop_01.empty():
                                charge_stop_01.get()
                        if Addr == "02":
                            while not charge_stop_02.empty():
                                charge_stop_02.get()
                        # thread_lock.release()
                        # 充电逻辑部分
                        # 完成零电量自动断电，写状态进入数据库，判断电量充多少
                        if recharge(u_z, mac, Addr, charge_cycle) == 0:
                            print("正常停止充电。")
                            # thread_list.remove(threading.get_ident())
                            return 0
        elif modbus_rtu.power_status(Addr) == 'ON':
            cycle.set()
            while not report_power_status(u_z, mac, Addr):
                sleep(0.1)
            # thread_lock.release()
            print(Addr + "号充电位之前已被开启，请停止后再试")
        else:
            print(Addr + "号充电位通信失败，请重新操作")

    if command_text == 'CD1' and command_value == '1':

        if modbus_rtu.power_status(Addr) == 'ON':
            # print('ON')
            if Addr == "01":
                cycle = recv_lock01
                charge_stop = charge_stop_01
            if Addr == "02":
                cycle = recv_lock02
                charge_stop = charge_stop_02
            print("关闭中。")
            while not charge_stop.empty():
                charge_stop.get()

            charge_stop.put(Addr + "stop")
            print("等待关闭中。")
            sleep(0.5)
            while cycle.wait(1):
                while not charge_stop.empty():
                    charge_stop.get()
                charge_stop.put(Addr + "stop")
                sleep(0.2)
            return

        elif modbus_rtu.power_status(Addr) == 'OFF':
            # thread_lock.release()
            cycle.clear()
            while not report_power_status(u_z, mac, Addr):
                sleep(0.1)
            print(Addr + "号充电位正处于关闭状态，请开启后再试")
        else:
            print(Addr + "号充电位通信失败，请重新操作")



def charge_select(mac, u_z, recv_data, charge_cycle):
    print("--------进入控制--------")
    # print('进入控制的线程 id : %d' % threading.get_ident())
    thread_list.append(threading.get_ident())
    # print('开始前现有线程 id : ', thread_list)
    try:
        receive_data = recv_data
        # print("receive_data",receive_data)
        # 判断MAC地址
        if receive_data[17] == '=' and receive_data[3:17] == mac:
            # 获取数据内容
            Addr = receive_data[0:2]
            receive_data = receive_data[18:]
            # print("recv_data"+recv_data)
            if receive_data[0] == '{' and receive_data[-1] == '}':
                order = receive_data[1:-1].split(",")
                # print(order)
                for i in order:
                    command = i.split("=")  # 拆指令
                    if len(command) == 2:
                        command_text = command[0]
                        command_value = command[1]
                        # print("command_text" + command_text)
                        # print("command_value" + command_value)
                        Analysis_command(u_z, Addr, command_text, command_value, mac, charge_cycle)
                print("-----------指令解析完成-----------")

        # print('结束控制线程 id : %d' % threading.get_ident())
        thread_list.remove(threading.get_ident())
        # print('现有线程 id : ', thread_list)

        print("-----------指令完成-----------\n")
        # continue
        return
    except(IndexError):
        print("发现异常！跳过本次循环。")
        # pass
        return


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    if not thread.is_alive():
        return
    _async_raise(thread.ident, SystemExit)


def task_timer(mac, u_z, recv_data, charge_cycle):
    try:
        # print('初始化生命线程 id : %d' % threading.get_ident())
        if select_queue.get() == "ok":
            charge_select(mac, u_z, recv_data, charge_cycle)

    finally:
        if threading.get_ident() in thread_list:
            thread_list.remove(threading.get_ident())
        # print('回收超时线程id : %d' % threading.get_ident())
        print('现有线程 id : ', thread_list)
        return


def thread_manage(U_Z, mac, recv_data):
    # t.submit(task_timer, mac, U_Z, )
    print("生命周期开始")
    # print('生命周期 id : ', threading.get_ident())
    charge_cycle = threading.Event()
    charge_cycle.clear()

    addr = recv_data[0:2]

    task = threading.Thread(target=task_timer, args=(mac, U_Z, recv_data, charge_cycle))
    # task.setDaemon(True)
    task.start()

    sleep(0.05)
    if addr == "01":
        cycle = recv_lock01
    if addr == "02":
        cycle = recv_lock02
    # print("被动握手等待")
    # if handshake_active.empty() is False:
    try:
        if handshake_active.get(timeout=2) == addr + "ok":
            print("左边伸手")
            handshake_passive.put(addr + "go")
            if handshake_active.get(timeout=1) == addr + "fine":
                # print("左边握手")
                print("握手完成")
                count = 0
                # sleep(0.5)
                while not handshake_active.empty():
                    handshake_active.get()
                while not handshake_passive.empty():
                    handshake_passive.get()
                print("充电周期等待")
                if cycle.wait(2):
                    while cycle.is_set():
                        sleep(0.5)
                        count = count + 0.5
                        if count % 2 == 0:
                            print(addr + " charge:", cycle.is_set(), count)
                            if count == 10:
                                count = 0
    except:
        pass
    task.join(4)
    # sleep(0.5)
    try:

        stop_thread(task)
        print("清理超时线程 id", task.ident)

        # terminate_thread(task)
    except(ValueError):
        print("ValueError")
    sleep(0.5)
    # print("电表结束", addr)
    # for thread in threading.enumerate():
    #     print('现有线程 id : ', thread)
    print('现有线程 id : ', thread_list)
    # print('线程管理结束', threading.get_ident())
    print("生命周期结束")
    return


thread_list = []


def auto_control_zigbee(U_Z, mac):
    # print("------(auto_control_zigbee)------")
    print('初始化接收网关指令的线程 id : %d' % threading.get_ident())

    while True:

        global device, pause, recv_data_ahead, recv_data_rear
        recv_data = U_Z.uart_recv()
        # print('从Zigbee接收到内容:' + recv_data)
        print("\n------(收到网络控制)------")
        # print('接收网关指令的线程 id : %d' % threading.get_ident())
        thread_list.append(threading.get_ident())
        # print('现有线程 id : ', thread_list)

        # print("接收数据：", recv_data)
        head = recv_data[0:2]
        tail = recv_data[-2:]
        # print("接收数据head：", head)
        # print("接收数据tail：", tail)
        if head == "AA" and tail != "ZZ":
            recv_data_ahead = recv_data[2:]

        if head != "AA" and tail == "ZZ":
            recv_data_rear = recv_data[:-2]
            recv_data = recv_data_ahead + recv_data_rear

        if head == "AA" and tail == "ZZ":
            # recv_data_ahead = recv_data[2:]
            # recv_data_rear = recv_data[:-2]
            # print("去掉头数据：", recv_data_ahead+"---"+recv_data_rear)
            recv_data = recv_data[2:-2]

        print("去掉头尾数据：", recv_data)
        device = recv_data[0:2]
        while not select_queue.empty():
            select_queue.get()

        if recv_data[17] == '=' and recv_data[-1] == '}':

            if device == "01":
                print("1号充电位指令")
                print("**************************")
                pause.set()
                select_queue.put("ok")
                # device01_lock.set()
                # stop_power_lock.set()
                thread_list.remove(threading.get_ident())
                task = threading.Thread(target=thread_manage, args=(U_Z, mac, recv_data,))
                task.start()
                task.join(0.1)
                continue

            if device == "02":
                print("2号充电位指令")
                print("**************************")
                pause.set()
                select_queue.put("ok")
                # device02_lock.set()
                # stop_power_lock.set()
                thread_list.remove(threading.get_ident())
                task = threading.Thread(target=thread_manage, args=(U_Z, mac, recv_data,))
                task.start()
                task.join(0.1)

                continue
        else:
            print("recive data error")
            thread_list.remove(threading.get_ident())
            continue


def report_power_status(U_Z, mac, addr):
    # thread_lock.acquire()

    # print("------(report_power_status)------")
    status = -1
    # print("开始查询开关！！！！")
    status_str = modbus_rtu.power_status(addr)
    # print("开始查询开关:::::" + status_str)
    if status_str == 'OFF':
        status = 0
    if status_str == 'ON':
        status = 1
    if status != -1:
        global D1
        D1 = status
        msg1 = addr + ":" + mac + "=" + "{D1=%d}" % status
        U_Z.uart_send(msg1)  # zigbee透传
        # time.sleep(0.5)
        U_Z.uart_send(msg1)  # zigbee再次透传

        # thread_lock.release()
        return True

    else:
        print("report power error")

        # thread_lock.release()
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
    STATUS_DEVICE_OFFLINE = 'OFF'
    STATUS_IDLE = 0
    STATUS_CHARGING = 1

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

        self.V0 = int(config.cdz_time)  # 主动上报时间间隔
        self.V1 = 0  # 储值电量

        self.V3 = config.cdz_gps  # gps 经度 纬度
        self.INIT = 0

    def auto_init(self):
        # thread_lock.acquire()

        for iter in define.addr_list:
            self.INIT = 1
            self.addr = iter
            modbus_rtu.power_on(str(iter))
            modbus_rtu.power_off(iter)
            # report_power_status(self.U_Z, self.mac, iter)
            self.get_status_report(iter)
            # self.report()

        # thread_lock.release()

    def set_addr(self, addr):
        self.addr = addr

    def sendmsg(self, U_Z, dat):

        # thread_lock.acquire()
        msg = self.addr + ":" + self.mac + "=" + dat
        U_Z.uart_send(msg)  # zigbee透传
        # thread_lock.release()

    def get_status_report(self, addr):
        # if self.STATUS_DEVICE_OFFLINE == modbus_rtu.power_status(self.addr):
        #     print("----电表设备不在线，不上报----" ) # !!!!!!!!!! 可能需要向上报问题
        #     return
        try:
            # self.A1 = float("%.2f" % (modbus_rtu.read_current(addr)))  # ！！存在使用过程中可能会报错的问题
            self.A2 = float("%.2f" % (modbus_rtu.read_voltage(addr)))
            # self.A3 = float("%.2f" % (modbus_rtu.read_Active_power(addr)))
            # self.A4 = float("%.2f" % (modbus_rtu.read_always_active_power(addr)))

            status_str = modbus_rtu.power_status(addr)
            # print("开始查询开关:::::" + status_str)
            if status_str == 'OFF':
                self.D1 = 0
            if status_str == 'ON':
                self.D1 = 1
            rep = []
            # rep.append("A0=%.2f" % self.A0)
            # rep.append("A1=%.2f" % self.A1)
            rep.append("A2=%.2f" % self.A2)
            # rep.append("A3=%.2f" % self.A3)
            # rep.append("A4=%.2f" % self.A4)
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
                # sleep(10)
                if pause.wait(10):
                    pause.clear()
                    continue
                else:
                    # print("22",pause.is_set())
                    # thread_lock.acquire()
                    print("\n轮询状态中\n")
                    for iter in define.addr_list:
                        self.addr = iter
                        self.get_status_report(iter)
                    # thread_lock.release()

            except(TypeError):
                # thread_lock.release()
                print("本轮上报错误")
                pass
