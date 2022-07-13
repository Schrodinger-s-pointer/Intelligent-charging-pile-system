
import sqlite3
import config

NUM=0                       #序号（主键）
DATE="20220701"               #日期
MAC="01:01:20:22:55:4F"     #设备号
START_TIME="01:16:03"       #开始时间
KWH=0                      #电量
POWER=0                     #开关位
STOP_TIME=""       #开始时间

#数据库初始化
def database_init():
    # 1.硬盘上创建连接
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    table_name="C"+DATE

    sql = 'create table '+table_name+'(num INTEGER PRIMARY KEY  AUTOINCREMENT ,' \
                                     'date text ,' \
                                     'mac text NOT NULL ,' \
                                     'start_time text,' \
                                     'kwh int ,' \
                                     'power int ,' \
                                     'voltage real ,' \
                                     'current real ,' \
                                     'watt real ,' \
                                     'quantity real ,' \
                                     'stop_time text)'


    try:
        cur.execute(sql)
    except Exception as e:
        print(e)


    sql = 'select * from '+table_name+' order by num desc limit 1'
    try:
        global NUM
        cur.execute(sql)
        # 获取一条数据
        num_now = cur.fetchone()

        if (num_now == None):
            print("今天第一张表")
            NUM = 1
        if (num_now != None):
            NUM = num_now[0]+1
    except Exception as e:
        print(e)
        print('查询序号失败')

    sql = 'insert into '+table_name+'(num,date,mac,start_time,kwh) values(?,?,?,?,?)'
    try:
        cur.execute(sql, (NUM,DATE,MAC,START_TIME,KWH))
        # 提交事务
        con.commit()
        print('加入新表成功')
        # 关闭游标
        cur.close()
        # 关闭连接
        con.close()
        return True
    except Exception as e:
        print(e)
        print('插入失败')
        con.rollback()

    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False
#登记电源开关状态 参数0关或者1开
def insert_power(addr,power):
    # 1.硬盘上创建连接
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    table_name=date_select()
    num_now=num_select(addr)
    config.cfg_read()
    mac_name=addr+':'+config.cdz_mac

    sql = 'update '+table_name+' set power=? where num=? and mac=?'
    try:
        cur.execute(sql, (power,num_now,mac_name))
        # 提交事务
        con.commit()
        print('更新电源状态',power,'成功')
        # 关闭游标
        cur.close()
        # 关闭连接
        con.close()
        return True
    except Exception as e:
        print(e)
        print('更新电源状态失败')
        con.rollback()

    # 关闭游标
    print("操作失败，数据库关闭!")
    cur.close()
    # 关闭连接
    con.close()
    return False
#查询最新表名日期
def date_select():
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    table_name="sqlite_master"

    sql = 'select count(*) from '+table_name
    try:

        cur.execute(sql)
        row=cur.fetchone()[0]

        sql = 'select * from ' + table_name
        cur.execute(sql)
        # 获取一条数据
        if row==2:
            row=1
        date_now = cur.fetchmany(row)[row-1][1]
        if date_now == None:
            print("没有最新表名")
            return 0
        if date_now != None:
            return date_now

    except Exception as e:
        print(e)
        print('查询最新表名失败')
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False
#查询最新表中最新数据的num序号
def num_select(addr):
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    table_name=date_select()
    config.cfg_read()

    mac_name = addr +':'+ config.cdz_mac
    sql = 'select * from '+table_name+' where mac=? order by num desc limit 1'
    try:
        cur.execute(sql,[mac_name])
        # 获取一条数据
        num_now = cur.fetchone()
        if (num_now == None):
            print("未查到"+addr+"设备的表记录序号")
            return 0
        if (num_now != None):
            return num_now[0]
    except Exception as e:
        print(e)
        print('表记录序号失败')
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False

def num_select_easy(table_name,mac_name):
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    sql = 'select * from '+table_name+' where mac=? order by num desc limit 1'
    try:
        cur.execute(sql,[mac_name])#里面不宜用括号查字符串
        # 获取一条数据
        num_now = cur.fetchone()
        if (num_now == None):
            print("快捷查询未查到"+mac_name+"设备的表记录序号")
            return 0
        if (num_now != None):
            return num_now[0]
    except Exception as e:
        print(e)
        print('快捷查询表记录序号失败')
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False
#登记充电状态，电压，电流，功率，已用电量
def insert_state(addr,voltage,current,watt,quantity):
    #传入电压，电流，功率，已用电量
    # 1.硬盘上创建连接
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象

    cur = con.cursor()
    table_name=date_select()
    num_now=num_select(addr)
    sql = 'update '+table_name+' set voltage=?,current=?,watt=?,quantity=? where num=?'
    try:
        cur.execute(sql, (voltage,current,watt,quantity,num_now))
        # 提交事务
        con.commit()
        print('插入成功')
        # 关闭游标
        cur.close()
        # 关闭连接
        con.close()
        return True
    except Exception as e:
        print(e)
        print('插入失败')
        con.rollback()

    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False

#使用表名字和序号快捷登记充电状态，电压，电流，功率，已用电量
def insert_state_easy(addr,table_name,num_now,voltage,current,watt,quantity):
    #传入电压，电流，功率，已用电量
    # 1.硬盘上创建连接
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    sql = 'update '+table_name+' set voltage=?,current=?,watt=?,quantity=? where num=?'
    try:
        cur.execute(sql, (voltage,current,watt,quantity,num_now))
        # 提交事务
        con.commit()
        print('快捷更新四值状态成功')
        # 关闭游标
        cur.close()
        # 关闭连接
        con.close()
        return True
    except Exception as e:
        print(e)
        print('快捷更新四值状态失败')
        con.rollback()

    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False


#登记充电停止时间
def install_stop_time(addr,stop_time):
    # 1.硬盘上创建连接
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    table_name = date_select()
    num_now=num_select(addr)

    sql = 'update ' + table_name + ' set stop_time=? where num=?'
    try:
        cur.execute(sql, (stop_time, num_now))
        # 提交事务
        con.commit()
        print('插入成功')
        # 关闭游标
        cur.close()
        # 关闭连接
        con.close()
        return True
    except Exception as e:
        print(e)
        print('插入失败')
        con.rollback()

    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False
#查询电压
def voltage_select(addr):
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    table_name=date_select()
    num_now = num_select(addr)
    sql = 'select voltage from '+table_name+' where num=? '
    try:
        cur.execute(sql,[num_now])
        # 获取一条数据
        voltage = cur.fetchone()
        if (voltage == None):
            print("null")
            return 0
        if (voltage != None):
            return voltage[0]
            # print(NUM)
    except Exception as e:
        print(e)
        print('查询失败')
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False
#查询电流
def current_select(addr):
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    table_name=date_select()
    num_now = num_select(addr)
    sql = 'select current from '+table_name+' where num=?'
    try:
        cur.execute(sql,[num_now])
        # 获取一条数据
        current = cur.fetchone()
        if (current == None):
            print("null")
            return 0
        if (current != None):
            return current[0]
    except Exception as e:
        print(e)
        print('查询失败')
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False
#查询功率
def watt_select(addr):
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    table_name=date_select()
    num_now = num_select(addr)
    sql = 'select watt from '+table_name+' where num=?'
    try:
        cur.execute(sql,[num_now])
        # 获取一条数据
        watt = cur.fetchone()
        if (watt == None):
            print("null")
            return 0
        if (watt != None):
            return watt[0]
    except Exception as e:
        print(e)
        print('查询失败')
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False
#查询已用电量
def quantity_select(addr):
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    table_name=date_select()
    num_now = num_select(addr)
    sql = 'select quantity from '+table_name+' where num=?'
    try:
        cur.execute(sql,[num_now])
        # 获取一条数据
        quantity = cur.fetchone()
        if (quantity == None):
            print("null")
            return 0
        if (quantity != None):
            return quantity[0]
    except Exception as e:
        print(e)
        print('查询失败')
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False


#查询开关状态
def power_select(addr):
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    table_name=date_select()
    num_now = num_select(addr)
    sql = 'select power from '+table_name+' where num=?'
    try:
        cur.execute(sql,[num_now])
        # 获取一条数据
        power = cur.fetchone()
        if (power == None):
            print("null")
            return 0
        if (power != None):
            return power[0]
    except Exception as e:
        print(e)
        print('查询失败')
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False

def power_select_easy(num_now,table_name):
    con = sqlite3.connect('./cd.db')
    # 获取cursor对象
    cur = con.cursor()
    sql = 'select power from '+table_name+' where num=?'
    try:
        cur.execute(sql,[num_now])
        # 获取一条数据
        power = cur.fetchone()
        if (power == None):
            print("null")
            return 0
        if (power != None):
            return power[0]
    except Exception as e:
        print(e)
        print('快捷电源读取失败')
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return False

