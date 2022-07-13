# -* - coding: UTF-8 -* -
import os
import configparser


CONFIG_FILE = "../webapp/config.cfg"
#zhiyun_config
zhiyun_ip = "47.99.214.175"
zhiyun_port = "28082"
zhiyun_uid = "729774038670"
zhiyun_password = "BwIJBgUEAgIIBAcFW11WWVBHX10Z"

#cdz_config
cdz_host = "127.0.0.1"
cdz_port = "9527"
cdz_mac = "mac"
cdz_uart = "COM6"
cdz_time = "10"
cdz_gps = "112.342774&16.84041"

def cfg_write():
    conf = configparser.ConfigParser()
    cfgfile = open(CONFIG_FILE, 'w')
    conf.add_section("cdz_config")  # 在配置文件中增加一个段

    # 第一个参数是段名，第二个参数是选项名，第三个参数是选项对应的值
    conf.set("cdz_config", "cdz_host", cdz_host)
    conf.set("cdz_config", "cdz_port", cdz_port)
    conf.set("cdz_config", "cdz_mac", cdz_mac)
    conf.set("cdz_config", "cdz_uart", cdz_uart)
    conf.set("cdz_config", "cdz_time", cdz_time)
    conf.set("cdz_config", "cdz_gps", cdz_gps)

    conf.add_section("zhiyun_config")
    conf.set("zhiyun_config", "zhiyun_ip", zhiyun_ip)
    conf.set("zhiyun_config", "zhiyun_port", zhiyun_port)
    conf.set("zhiyun_config", "zhiyun_uid", zhiyun_uid)
    conf.set("zhiyun_config", "zhiyun_password", zhiyun_password)

    # 将conf对象中的数据写入到文件中
    conf.write(cfgfile)
    cfgfile.close()

def cfg_read():
    if os.path.exists(os.path.join(os.getcwd(), CONFIG_FILE)):
        config = configparser.ConfigParser()

        config.read(CONFIG_FILE)

        # 第一个参数指定要读取的段名，第二个是要读取的选项名
        global cdz_host,cdz_port,cdz_mac,cdz_uart,cdz_time,cdz_gps
        cdz_host = config.get("cdz_config", "cdz_host")
        cdz_port = config.get("cdz_config", "cdz_port")
        cdz_mac = config.get("cdz_config", "cdz_mac")
        cdz_uart = config.get("cdz_config", "cdz_uart")
        cdz_time = config.get("cdz_config", "cdz_time")
        cdz_gps = config.get("cdz_config", "cdz_gps")
        print(cdz_host, cdz_port, cdz_mac,cdz_uart,cdz_time,cdz_gps)
        global zhiyun_ip,zhiyun_port,zhiyun_uid,zhiyun_password
        zhiyun_ip = config.get("zhiyun_config", "zhiyun_ip")
        zhiyun_port = config.get("zhiyun_config", "zhiyun_port")
        zhiyun_uid = config.get("zhiyun_config", "zhiyun_uid")
        zhiyun_password = config.get("zhiyun_config", "zhiyun_password")
        print(zhiyun_ip, zhiyun_port, zhiyun_uid, zhiyun_password)

