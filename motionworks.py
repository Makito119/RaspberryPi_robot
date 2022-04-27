import serial
import time


# 手を振る動作
def motion1(con):
    puton(con)
    vsrc_send_1byte(con, '09c0', 12)
    time.sleep(0.8)
    putoff(con)
    vsrc_send_1byte(con, '0048', 0)

def motion2(con):
    puton(con)
    vsrc_send_1byte(con, '09c0', 13)
    time.sleep(0.8)
    putoff(con)
    time.sleep(0.5)
    vsrc_send_1byte(con, '0048', 0)

# 指定アドレスに1バイト書き込むコマンドを送信する関数
def vsrc_send_1byte(con, addr, data):
    data_str = format(data, '02x')
    str_send = 'w ' + addr + ' ' + data_str + '\r'
    con.write(str_send.encode())
    print(str_send)
    time.sleep(0.012)
    str_read = con.read(con.inWaiting())


# 指定アドレスから1バイト読み込むコマンドを送信し、返答を取得する関数
def vsrc_read_1byte(con, addr):
    str_send = 'r ' + addr + ' 1\r'
    con.write(str_send.encode())
    time.sleep(0.012)
    str_read = con.read(con.inWaiting()).decode()
    start_pos = str_read.find('#0000'+addr)+10
    return str_read[start_pos]+str_read[start_pos+1]


# 指定アドレスから2バイト読み込むコマンドを送信し、返答を取得する関数
def vsrc_read_2byte(con, addr):
    str_send = 'r ' + addr + ' 2\r'
    con.write(str_send.encode())
    # print(str_send)
    time.sleep(0.012)
    str_read = con.read(con.inWaiting()).decode()
    start_pos = str_read.find('#0000'+addr)+10
    if start_pos+3 < len(str_read):
      return str_read[start_pos+3]+str_read[start_pos+4]+str_read[start_pos]+str_read[start_pos+1]
    else:
      return ''

def puton(con):
    #con = serial.Serial('/dev/ttyAMA0', 115200)
    time.sleep(0.1)
    # サーボ電源ON
    vsrc_send_1byte(con, '0048', 1)
    time.sleep(1)
    print('サーボ電源オン')

def putoff(con):
    #con = serial.Serial('/dev/ttyAMA0', 115200)
    vsrc_send_1byte(con, '09c0', 0)

    # モーション終了待ち
    while True:
        ret = vsrc_read_2byte(con, '0ff8')
        # print(ret)
        if ret == "0000":
            time.sleep(1)
            break

    # サーボ電源OFF
    # time.sleep(0.1)
    # vsrc_send_1byte(con, '0048', 0)
    # time.sleep(1)

if __name__ == "__main__":
    con = serial.Serial('/dev/ttyAMA0', 115200)
    motion2(con)