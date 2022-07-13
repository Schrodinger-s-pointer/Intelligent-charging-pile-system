import threading
import uart
import config

import web
thread_lock = threading.RLock()

to_web_lock = threading.Event()
to_uart_lock = threading.Event()

bps = 115200

part_1 = "{\"method\":\""
part_2 = "\",\"addr\":\""
part_3 = "\",\"data\":\""
part_4 = "\"}"
method = "sensor"

def to_uart(uart, ZY):
    while True:
        if ZY.if_to_uart:
            get_data = ZY.slave_get
            print("下发控制中")
            uart.uart_send(get_data)
            ZY.if_to_uart = False


def to_web(ZY,to_web_lock):
    while True:
        if to_web_lock.wait():
            thread_lock.acquire()
            addr = uar.addr_str
            data = uar.data_str
            msg = part_1 + method + part_2 + addr + part_3 + data + part_4
            ZY.tcp_send(msg)
            to_web_lock.clear()
            thread_lock.release()


if __name__ == '__main__':
    config.cfg_read()
    ip = config.zhiyun_ip
    com= config.cdz_uart
    port = int(config.zhiyun_port)
    ZY = web.Zhiyun(ip, port)
    ZY.tcp_con()
    uar = uart.UART(com, bps)
    # 打开来自网关的串口接收线程
    uart_recv = threading.Thread(target=uar.uart_recv, args=(to_web_lock,thread_lock))
    uart_recv.setDaemon(True)  # 设置守护线程
    uart_recv.start()
    # 打开来自网关的心跳线程
    heart_beat = threading.Thread(target=ZY.heart_beat, args=(to_web_lock,))
    heart_beat.setDaemon(True)  # 设置守护线程
    heart_beat.start()
    # 打开来自接收智云的线程
    recv_tcp = threading.Thread(target=ZY.recv_msg, args=(uar,to_uart_lock))
    recv_tcp.setDaemon(True)  # 设置守护线程
    recv_tcp.start()
    # 上报智云状态
    to_uart_thread = threading.Thread(target=to_web, args=(ZY,to_web_lock))
    to_uart_thread.setDaemon(True)  # 设置守护线程
    to_uart_thread.start()

    uart_recv.join()
    heart_beat.join()
    recv_tcp.join()
    to_uart_thread.join()

