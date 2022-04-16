from pythonosc.udp_client import SimpleUDPClient
import time
import sys
import datetime
import math

msg = """
//////////////////////////////////////////
VRChat Open Sound Control 
                  時刻表示プログラム

Analog Clock System Stable Version 2.1

//////////////////////////////////////////
"""

#作成 : 風庭ゆい
#最終更新 : 2022/04/17

#ipとポートをセット
ip = "127.0.0.1"
port = 9000

client = SimpleUDPClient(ip, port)

print(msg)

print('初期化します', end="")

#初期化を実行
client.send_message("/avatar/parameters/AC_hh", float(0.0))
client.send_message("/avatar/parameters/AC_mh", float(0.0))
client.send_message("/avatar/parameters/AC_sc", float(0.0))

print('\rOSC送信を開始します')

print("set_IP:", ip, ":", port, "\n")

print('Ctrl+Cで終了できます\n')

try:

    while True:

        #PCのローカル時間を取得
        dt_now = datetime.datetime.now()

        hours = dt_now.hour % 12
        minutes = dt_now.minute
        seconds = dt_now.second
        meridian = dt_now.strftime('%p')

        minutes_hand = minutes / 100
        seconds_hand = seconds / 100

        print("\r現在時刻:", hours, ":", minutes, ":", seconds,".", meridian,".", end="")

        #hourを60に分割
        min_hours = math.floor(minutes / 12)

        if hours != 12:
            hours_hh = hours / 20

        else:
            hours_hh = 0

        hh = hours_hh + (min_hours / 100)
        hours_hand = round(hh, 2)

        #とんでけーー！！
        client.send_message("/avatar/parameters/AC_hh", hours_hand)
        client.send_message("/avatar/parameters/AC_mh", minutes_hand)
        client.send_message("/avatar/parameters/AC_sc", seconds_hand)

        time.sleep(1)

except KeyboardInterrupt:

    #終了時初期化
    client.send_message("/avatar/parameters/AC_hh", float(0.0))
    client.send_message("/avatar/parameters/AC_mh", float(0.0))
    client.send_message("/avatar/parameters/AC_sc", float(0.0))

    print("\n\n初期化しました\n終了します")

    time.sleep(1)

    #メモリを開放するよ、またねー
    sys.exit()



