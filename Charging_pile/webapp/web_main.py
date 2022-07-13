

from flask import Flask, render_template,request
import config

app = Flask(__name__)

@app.route('/')
def index():
    config.cfg_read()
    cdz_mac=config.cdz_mac
    cdz_uart=config.cdz_uart
    cdz_time=config.cdz_time
    cdz_gps=config.cdz_gps
    print(cdz_gps,cdz_uart,cdz_time,cdz_gps)
    return render_template('config_page.html', cdz_mac=cdz_mac, cdz_uart=cdz_uart,cdz_time = cdz_time,cdz_gps=cdz_gps)

@app.route('/ok',  methods=['POST'])
def success():
   if request.method == 'POST':
       MAC = request.form['MAC']
       UART = request.form['UART']
       TIME = request.form['TIME']
       GPS = request.form['GPS']
       if MAC!='':
           config.cdz_mac=MAC
           config.cfg_write()
           if UART!='':
               config.cdz_uart=UART
               config.cfg_write()
               if TIME != '':
                   config.cdz_time = TIME
                   config.cfg_write()
                   if GPS!='':
                       config.cdz_gps=GPS
                       config.cfg_write()
                       return render_template('success.html', ok="修改成功", mac=MAC, uart=UART,time=TIME, gps=GPS)
       return render_template('success.html', ok="内容有空值，请返回重新填写")
   else:
       pass

def main():
    app.run(host='0.0.0.0', port=9527, debug=False)


if __name__ == "__main__":
    main()
