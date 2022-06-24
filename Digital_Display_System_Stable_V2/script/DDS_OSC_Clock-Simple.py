from pythonosc.udp_client import SimpleUDPClient
import time
import sys
import datetime
import ipaddress

msg = """
//////////////////////////////////////////
VRChat Open Sound Control 
                  時刻表示プログラム

Digital Display System Beta Version 2.1.1

//////////////////////////////////////////
"""

#作成 : 風庭ゆい
#最終更新 : 2022/06/24

def is_integer(n):
    return n.isascii() and n.isdecimal()

def ip_check(values):
    try:
        ip_set = ipaddress.ip_address(values)

        if type(ip_set) is ipaddress.IPv4Address:
            ip = str(ip_set)
            return ip

        else:
            return None
    
    except ValueError:
        return None

def port_check(values):
    valid_flag = False

    if is_integer(values):
        port=int(values)

        if 1 <= port <= 65535:
            valid_flag = True

    if not valid_flag:
        return None

    return port

#ipとポートをセット
if not (len(sys.argv) <= 2):
    ip = ip_check(sys.argv[1])
    port = port_check(sys.argv[2])

    if not all([ip, port]):
        print("ERROR!【引数が間違っているためデフォルトの数値を使用します】")
        ip = "127.0.0.1"
        port = 9000

else:
    ip = "127.0.0.1"
    port = 9000


client = SimpleUDPClient(ip, port)

print(msg)

print('初期化します', end="")

#初期化を実行
client.send_message("/avatar/parameters/DD_thp", 0)
client.send_message("/avatar/parameters/DD_hp", 0)
client.send_message("/avatar/parameters/DD_tp", 0)
client.send_message("/avatar/parameters/DD_op", 0)

print('\rOSC送信を開始します')

print("set_IP:", ip, ":", port, "\n")

print('Ctrl+Cで終了できます\n')

try:

    while True:

        #PCのローカル時間を取得
        dt_now = datetime.datetime.now()

        #時、分、秒で分けてゼロ埋め
        hours = dt_now.strftime('%H')
        minutes = dt_now.strftime('%M')
        seconds = dt_now.strftime('%S')

        num_h = hours.zfill(2)
        num_m = minutes.zfill(2)
        num_s = seconds.zfill(2)

        #それぞれの桁を変数に
        htp = num_h[-2]
        hop = num_h[-1]

        mtp = num_m[-2]
        mop = num_m[-1]

        stp = num_s[-2]
        sop = num_s[-1]

        print("\r現在時刻:", htp,hop,":",mtp,mop,":",stp,sop, end="")

        #とんでけーー！！
        client.send_message("/avatar/parameters/DD_thp", int(htp))
        client.send_message("/avatar/parameters/DD_hp", int(hop))
        client.send_message("/avatar/parameters/DD_tp", int(mtp))
        client.send_message("/avatar/parameters/DD_op", int(mop))

        #一秒待機
        time.sleep(1)

except KeyboardInterrupt:

    #終了時初期化
    client.send_message("/avatar/parameters/DD_thp", 0)
    client.send_message("/avatar/parameters/DD_hp", 0)
    client.send_message("/avatar/parameters/DD_tp", 0)
    client.send_message("/avatar/parameters/DD_op", 0)

    print("\n\n初期化しました\n終了します")

    time.sleep(1)

    #メモリを開放するよ、またねー
    sys.exit()



