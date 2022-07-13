import gi
from threading import Timer
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import cd

class TableWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="用户界面")
        self.set_default_size(1024, 750)

        a1 = cd.current_select("01")
        v1 = cd.voltage_select("01")
        w1 = cd.watt_select("01")
        t1 = "00:00:00"
        q1 = cd.quantity_select("01")

        a2 = cd.current_select("02")
        v2 = cd.voltage_select("02")
        w2 = cd.watt_select("02")
        t2 = "0:0:0"
        q2 = cd.quantity_select("02")

        # 一号cdz
        self.label_A = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电电流:</span>\n"
        self.label_A.set_markup(p)
        self.label_A_Value = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{a1}</span>\n"
        self.label_A_Value.set_markup(p)

        self.label_V = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电电压:</span>\n"
        self.label_V.set_markup(p)
        self.label_V_Value = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e'  >{v1}</span>\n"
        self.label_V_Value.set_markup(p)

        self.label_W = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电功率:</span>\n"
        self.label_W.set_markup(p)

        self.label_W_Value = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{w1}</span>\n"
        self.label_W_Value.set_markup(p)

        self.label_T = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电时间:</span>\n"
        self.label_T.set_markup(p)

        self.label_T_Value = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{t1}</span>\n"
        self.label_T_Value.set_markup(p)

        self.label_Q = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >已充电量:</span>\n"
        self.label_Q.set_markup(p)

        self.label_Q_Value = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{t1}</span>\n"
        self.label_Q_Value.set_markup(p)

        self.label_A = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电电流:</span>\n"
        self.label_A.set_markup(p)
        self.label_A_Value = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{a1}</span>\n"
        self.label_A_Value.set_markup(p)

        self.label_V = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电电压:</span>\n"
        self.label_V.set_markup(p)
        self.label_V_Value = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e'  >{v1}</span>\n"
        self.label_V_Value.set_markup(p)

        self.label_W = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电功率:</span>\n"
        self.label_W.set_markup(p)

        self.label_W_Value = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{w1}</span>\n"
        self.label_W_Value.set_markup(p)

        self.label_T = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电时间:</span>\n"
        self.label_T.set_markup(p)

        self.label_T_Value = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{t1}</span>\n"
        self.label_T_Value.set_markup(p)

        self.label_Q = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >已充电量:</span>\n"
        self.label_Q.set_markup(p)

        self.label_Q_Value = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{q1}</span>\n"
        self.label_Q_Value.set_markup(p)



        # 二号cdz
        self.label_A_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电电流:</span>\n"
        self.label_A_2.set_markup(p)
        self.label_A_Value_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{a2}</span>\n"
        self.label_A_Value_2.set_markup(p)

        self.label_V_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电电压:</span>\n"
        self.label_V_2.set_markup(p)
        self.label_V_Value_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e'  >{v2}</span>\n"
        self.label_V_Value_2.set_markup(p)

        self.label_W_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电功率:</span>\n"
        self.label_W_2.set_markup(p)

        self.label_W_Value_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{w2}</span>\n"
        self.label_W_Value_2.set_markup(p)

        self.label_T_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电时间:</span>\n"
        self.label_T_2.set_markup(p)

        self.label_T_Value_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{t2}</span>\n"
        self.label_T_Value_2.set_markup(p)

        self.label_Q_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >已充电量:</span>\n"
        self.label_Q_2.set_markup(p)

        self.label_Q_Value_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{t2}</span>\n"
        self.label_Q_Value_2.set_markup(p)

        self.label_A_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电电流:</span>\n"
        self.label_A_2.set_markup(p)
        self.label_A_Value_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{a2}</span>\n"
        self.label_A_Value_2.set_markup(p)

        self.label_V_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电电压:</span>\n"
        self.label_V_2.set_markup(p)
        self.label_V_Value_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e'  >{v2}</span>\n"
        self.label_V_Value_2.set_markup(p)

        self.label_W_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电功率:</span>\n"
        self.label_W_2.set_markup(p)

        self.label_W_Value_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{w2}</span>\n"
        self.label_W_Value_2.set_markup(p)

        self.label_T_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >充电时间:</span>\n"
        self.label_T_2.set_markup(p)

        self.label_T_Value_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{t2}</span>\n"
        self.label_T_Value_2.set_markup(p)

        self.label_Q_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fcff38' >已充电量:</span>\n"
        self.label_Q_2.set_markup(p)

        self.label_Q_Value_2 = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >{q2}</span>\n"
        self.label_Q_Value_2.set_markup(p)

        self.label_reminder = Gtk.Label()
        p = f"<span font_desc='18' foreground='#fb0e0e' >请扫码开启充电之旅</span>\n"
        self.label_reminder.set_markup(p)

        self.image_code = Gtk.Image()
        # 二维码 300X300
        self.image_code.set_from_file("./image/code.png")

        self.image_back = Gtk.Image()
        # 背景图片
        self.image_back.set_from_file("./image/bjtp.png")


        table = Gtk.Table(n_rows=11, n_columns=11, homogeneous=False)
        self.add(table)

        table.attach(self.label_A, 1, 2, 2, 3)
        table.attach(self.label_A_Value, 1, 2, 3, 4)
        table.attach(self.label_V, 2, 3, 2, 3)
        table.attach(self.label_V_Value, 2, 3, 3, 4)
        table.attach(self.label_W, 1, 2, 5, 6)
        table.attach(self.label_W_Value, 1, 2, 6, 7)
        table.attach(self.label_T, 2, 3, 5, 6)
        table.attach(self.label_T_Value, 2, 3, 6, 7)
        table.attach(self.label_Q, 1, 2, 7, 8)
        table.attach(self.label_Q_Value, 1, 2, 8, 9)

        table.attach(self.label_A_2, 6, 7, 2, 3)
        table.attach(self.label_A_Value_2, 6, 7, 3, 4)
        table.attach(self.label_V_2, 7, 8, 2, 3)
        table.attach(self.label_V_Value_2, 7, 8, 3, 4)
        table.attach(self.label_W_2, 6, 7, 5, 6)
        table.attach(self.label_W_Value_2, 6, 7, 6, 7)
        table.attach(self.label_T_2, 7, 8, 5, 6)
        table.attach(self.label_T_Value_2, 7, 8, 6, 7)
        table.attach(self.label_Q_2, 7, 8, 7, 8)
        table.attach(self.label_Q_Value_2, 7, 8, 8, 9)

        table.attach(self.label_reminder, 4, 6, 9, 10)
        table.attach(self.image_code, 4, 5, 2, 9)
        # table.attach(self.image_code, 4, 5, 2, 8)
        table.attach(self.image_back, 0, 11, 0, 11)

hour01=0;hour02=0
minute01=0;minute02=0
second01=0;second02=0

def printTime(addr,user):
    if cd.power_select(addr) == 1:
    # if 1 == 1:
        if addr=="01":
            global hour01, minute01, second01
            print()
            second01 += 1
            if second01 == 60:
                minute01 += 1
                second01 = 0
                if minute01 == 60:
                    hour01 += 1
                    minute01 = 0
                    if hour01 == 24:
                        hour01= 0
            t1=str(hour01).zfill(2)+":"+str(minute01).zfill(2)+ ":"+str(second01).zfill(2)
            p = f"<span font_desc='18' foreground='#26d3ef' >{t1}</span>\n"
            user.label_T_Value.set_markup(p)
            # user.label_T_Value.set_markup(p)
            print("addr",addr)
            a1 = cd.current_select(addr)
            v1 = cd.voltage_select(addr)
            w1 = cd.watt_select(addr)
            q1 = cd.quantity_select(addr)
            print(a1,v1,w1,q1)
            p_a = f"<span font_desc='18' foreground='#26d3ef' >{a1}</span>\n"
            p_v = f"<span font_desc='18' foreground='#26d3ef' >{v1}</span>\n"
            p_w = f"<span font_desc='18' foreground='#26d3ef' >{w1}</span>\n"
            p_q = f"<span font_desc='18' foreground='#26d3ef' >{q1}</span>\n"
            user.label_A_Value.set_markup(p_a)
            user.label_V_Value.set_markup(p_v)
            user.label_W_Value.set_markup(p_w)
            user.label_Q_Value.set_markup(p_q)


        if addr == "02":
            global hour02, minute02, second02
            print()
            second02 += 1
            if second02==60:
                minute02 += 1
                second02 = 0
                if minute02==60:
                    hour02 += 1
                    minute02 = 0
                    if hour02==24:
                        hour02 = 0

            t2=str(hour02).zfill(2)+":"+str(minute02).zfill(2)+ ":"+str(second02).zfill(2)
            p = f"<span font_desc='18' foreground='#26d3ef' >{t2}</span>\n"
            user.label_T_Value_2.set_markup(p)
            print("addr",addr)


            a2 = cd.current_select(addr)
            v2 = cd.voltage_select(addr)
            w2 = cd.watt_select(addr)
            q2 = cd.quantity_select(addr)
            print(a2, v2, w2, q2)
            p_a = f"<span font_desc='18' foreground='#26d3ef' >{a2}</span>\n"
            p_v = f"<span font_desc='18' foreground='#26d3ef' >{v2}</span>\n"
            p_w = f"<span font_desc='18' foreground='#26d3ef' >{w2}</span>\n"
            p_q = f"<span font_desc='18' foreground='#26d3ef' >{q2}</span>\n"
            user.label_A_Value_2.set_markup(p_a)
            user.label_V_Value_2.set_markup(p_v)
            user.label_W_Value_2.set_markup(p_w)
            user.label_Q_Value_2.set_markup(p_q)
    t = Timer(1, printTime, (addr,user))
    t.start()

if __name__ == '__main__':
    user=TableWindow()
    user.show_all()
    printTime("01",user)
    printTime("02",user)


    Gtk.main()