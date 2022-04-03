from pythonosc.udp_client import SimpleUDPClient
import PySimpleGUI as sg
import time
import threading
import sys
import datetime
import math

msg = """
//////////////////////////////////////////
VRChat Open Sound Control 
                  時刻表示プログラム

Analog Clock System Stable Version 2.1 for GUI

//////////////////////////////////////////
"""

#作成 : 風庭ゆい
#最終更新 : 2022/04/03

AC_hh = "AC_hh"
AC_mh = "AC_mh"
AC_sc = "AC_sc"

layout = [
    [
        sg.Text("IP"), sg.InputText("127", key="ip1", size=(3,1)),
        sg.Text("."), sg.InputText("0", key="ip2", size=(3,1)),
        sg.Text("."), sg.InputText("0", key="ip3", size=(3,1)),
        sg.Text("."), sg.InputText("1", key="ip4", size=(3,1))
    ],

    [
        sg.Text("Port"), sg.InputText("9000", key="port", size=(4,1))
    ],

    [],

    [sg.Text("Advanced Settings")],

    [sg.Text("時", size=(2,1)), sg.Text("/avatar/parameters/"), sg.InputText("AC_hh", key="hh")],

    [sg.Text("分", size=(2,1)), sg.Text("/avatar/parameters/"), sg.InputText("AC_mh", key="mh")],

    [sg.Text("秒", size=(2,1)), sg.Text("/avatar/parameters/"), sg.InputText("AC_sc", key="sc")],

    [
        sg.Submit(button_text="設定を反映する", key="settings"),
        sg.Text("", size=(20,1), key="paramtext")
    ],

    [],

    [
        sg.Button("送信開始", key="startbutton"),
        sg.Button("送信停止", key="stopbutton"),
        sg.Text("", size=(20,1), key="sstext")
    ]

]

window = sg.Window("Analog Clock System Beta 2.1 for GUI", layout)

class Receive():
    def __init__(self):
        self.ROOP = False


    def target(self):

        client = SimpleUDPClient(ip, port)

        param_hh = "/avatar/parameters/" + AC_hh
        param_mh = "/avatar/parameters/" + AC_mh
        param_sc = "/avatar/parameters/" + AC_sc

        print(param_hh)
        print(param_mh)
        print(param_sc)

        while (self.ROOP):

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
            client.send_message(param_hh, hours_hand)
            client.send_message(param_mh, minutes_hand)
            client.send_message(param_sc, seconds_hand)

            time.sleep(1)


    def start(self):
        self.thread = threading.Thread(target = self.target)
        self.thread.start()


if __name__ == "__main__":
    r = Receive()

    def startEvent(event):
        r.ROOP = True
        r.start()

    def changeEvent(event):
        pass

    def finishEvent(event):
        r.ROOP = False
        window.close()
        sys.exit()

    def is_integer(n):
        return n.isascii() and n.isdecimal()

    def ip_check(values):

        ip_list = [
            values["ip1"],
            values["ip2"],
            values["ip3"],
            values["ip4"]
        ]

        for i in ip_list:
            if is_integer(i) and int(i) <= 255:
                ip_set = ip_list[0] + "." + ip_list[1] + "." + ip_list[2] + "." + ip_list[3]

                ip = str(ip_set)
                return ip

            else:
                sg.popup("エラーが発生しました！\n【IPに使用できない値が含まれています】")

                window["ip1"].update("127")
                window["ip2"].update("0")
                window["ip3"].update("0")
                window["ip4"].update("1")

                ip = "127.0.0.1"
                return ip

    def port_check(values):
        valid_flag = False
        if is_integer(values["port"]):
            #数値の場合
            port = int(values["port"])
            #ポート範囲のチェック
            if 1 <= port <= 65535:
                valid_flag = True
        
        if not valid_flag:
            #失敗
            sg.popup("エラーが発生しました！\n【PORTに使用できない値が含まれています】")

            window["port"].update("9000")
            port = 9000
        
        return port

    def str_check(values):

        param_list = [
            values["hh"],
            values["mh"],
            values["sc"]
        ]

        for i in param_list:
            if i.isascii():
                hh = param_list[0]
                mh = param_list[1]
                sc = param_list[2]

                return hh, mh, sc

            else:
                sg.popup("エラーが発生しました！\n【parametersに使用できない文字列が含まれています】")

                window["hh"].update("AC_hh")
                window["mh"].update("AC_mh")
                window["sc"].update("AC_sc")

                hh = "AC_hh"
                mh = "AC_mh"
                sc = "AC_sc"

                return hh, mh, sc


while True:

    event, values = window.read()
    print(event, values)

    if event is None:
        break

    if event == sg.WINDOW_CLOSED:
        break

    if event == "settings":

        ip = ip_check(values)
        port = port_check(values)
        window["paramtext"].update(ip + ":" + str(port))

        print(ip, ":", end="")
        print(port)

        strcheck = str_check(values)

        AC_hh = strcheck[0]
        AC_mh = strcheck[1]
        AC_sc = strcheck[2]


    if event == "startbutton":

        ip = ip_check(values)
        port = port_check(values)
        window["paramtext"].update(ip + ":" + str(port))

        print("start")

        startEvent(event)

        window["sstext"].update("送信を開始しました")

    if event == "stopbutton":
        r.ROOP = False

        window["sstext"].update("送信を停止しました")

finishEvent(event)