# gps = '103.893038&30.792931'
#从机地址列表
addr_list = ['01', '02']
#从机地址
ADDR01 = '01'
ADDR02 = '02'
#功能码类别
READ_REGISTERS = '04'             # 读表功能码
WRITE_REGISTERS = '10'            # 写表功能码
#各种只读寄存器地址
voltage ='0000'                   # 电压
current ='0008'                   # 电流
Active_power ='0012'              # 有功功率
Factor ='002A'                    # 功率因数
frequency ='0036'                 # 频率
always_active_power ='0100'       # 总有功电量
Power_status ='0064'              # 拉合闸状态
#只可写寄存器地址
Power_operation ='0010'           # 拉合闸操作

#各种可读写寄存器地址
bps='0000'                        # 电压
crc_type='0002'                   # crc校验类型
slave_addr='0008'                 # 修改从机地址
#读取长度
voltage_length='0002'
current_length='0002'
always_active_power_length='0002'
Active_power_length='0002'
Power_status_length='0001'


#写数据长度
write_length='000204'
write_length_power='000102'

#开关状态
power_on='5555'
power_off='AAAA'

#写入数据（四个字节）
write_data=''


