
from flask import Flask, render_template,request
import config
app = Flask(__name__)

@app.route('/')
def index():
    config.cfg_read()
    zhiyun_ip= config.zhiyun_ip
    zhiyun_port= config.zhiyun_port
    zhiyun_uid= config.zhiyun_uid
    zhiyun_password= config.zhiyun_password
    cdz_uart = config.cdz_uart
    print(zhiyun_ip,zhiyun_port,zhiyun_uid,zhiyun_password,cdz_uart)
    return render_template('config_page.html', zhiyun_ip=zhiyun_ip, zhiyun_port=zhiyun_port,zhiyun_uid = zhiyun_uid,zhiyun_password=zhiyun_password,cdz_uart=cdz_uart)

@app.route('/ok',  methods=['POST'])
def success():
   if request.method == 'POST':
       IP = request.form['IP']
       PORT = request.form['PORT']
       UID = request.form['UID']
       PASSWORD = request.form['PASSWORD']
       UART = request.form['UART']
       if IP!='':
           config.zhiyun_ip=IP
           config.cfg_write()
           if PORT!='':
               config.zhiyun_port=PORT
               config.cfg_write()
               if UID != '':
                   config.zhiyun_uid = UID
                   config.cfg_write()
                   if PASSWORD!='':
                       config.zhiyun_password=PASSWORD
                       config.cfg_write()
                       if UART != '':
                           config.cdz_uart = UART
                           config.cfg_write()
                           return render_template('success.html', ok="修改成功", ip=IP, port=PORT,uid=UID, password=PASSWORD, uart=UART)
       return render_template('success.html', ok="内容有空值，请返回重新填写")
   else:
       pass

def main():
    app.run(host='0.0.0.0', port=9527, debug=False)


if __name__ == "__main__":
    main()
