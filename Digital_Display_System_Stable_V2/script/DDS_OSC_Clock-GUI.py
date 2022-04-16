from pythonosc.udp_client import SimpleUDPClient
import PySimpleGUI as sg
import time
import threading
import sys
import datetime
import ipaddress

#////////////////////////////////////////////////////
#VRChat Open Sound Control 
#                  時刻表示プログラム
#
#Digital Display System Stable Version 2.1 for GUI
#
#////////////////////////////////////////////////////

#作成 : 風庭ゆい
#最終更新 : 2022/04/17

DD_thp = "DD_thp"
DD_hp = "DD_hp"
DD_tp = "DD_tp"
DD_op = "DD_op"

buttonflag = False

sg.theme("Default")

layout = [
    [
        sg.Text("IP", size=(8,1)), sg.InputText("127.0.0.1", key="ip", size=(15,1))
    ],

    [
        sg.Text("Port", size=(8,1)), sg.InputText("9000", key="port", size=(15,1))
    ],

    [
        sg.Text("送信間隔", size=(8,1)), sg.InputText("1", key="interval", size=(5,1)),
        sg.Text("秒")
    ],

    [
        sg.Submit(button_text="設定を反映", key="settings"),
        sg.Text("設定中のIPアドレス:ポート番号 ▷"),
        sg.Text("127.0.0.1:9000", size=(15,1), key="paramtext")
    ],

    [
        sg.Text("Advanced Settings---"),
        sg.Text(" 【送信するパラメータを変更します】")
    ],

    [
        sg.Text("時1", size=(3,1)), sg.Text("/avatar/parameters/"), sg.InputText("DD_thp", key="thp", size=(20,1)),
        sg.Text("DD_thp", key="text_thp", size=(20,1))
    ],

    [
        sg.Text("時2", size=(3,1)), sg.Text("/avatar/parameters/"), sg.InputText("DD_hp", key="hp", size=(20,1)),
        sg.Text("DD_hp", key="text_hp", size=(20,1))
    ],

    [
        sg.Text("分1", size=(3,1)), sg.Text("/avatar/parameters/"), sg.InputText("DD_tp", key="tp", size=(20,1)),
        sg.Text("DD_tp", key="text_tp", size=(20,1))
    ],

    [
        sg.Text("分2", size=(3,1)), sg.Text("/avatar/parameters/"), sg.InputText("DD_op", key="op", size=(20,1)),
        sg.Text("DD_op", key="text_op", size=(20,1))
    ],

    [
        sg.Button("送信開始", key="startbutton"),
        sg.Text("送信停止中", size=(20,1), key="sstext")
    ],

    [
        sg.Text("", key="time")
    ]

]


class Receive():
    def __init__(self):
        self.roop = False

    
    def target(self):

        client = SimpleUDPClient(ip, port)

        param_thp = "/avatar/parameters/" + DD_thp
        param_hp = "/avatar/parameters/" + DD_hp
        param_tp = "/avatar/parameters/" + DD_tp
        param_op = "/avatar/parameters/" + DD_op

        print(param_thp)
        print(param_hp)
        print(param_tp)
        print(param_op)

        while (self.roop):

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

            time_notify = htp + hop + ":" + mtp + mop + ":" + stp + sop

            print("\r現在時刻:", time_notify, end="")

            window["time"].update("送信中の現在時刻 :" + str(time_notify))

            #とんでけーー！！
            client.send_message(param_tp, int(htp))
            client.send_message(param_op, int(hop))
            client.send_message(param_tp, int(mtp))
            client.send_message(param_op, int(mop))

            #待機
            time.sleep(interval)


    def start(self):
        self.thread = threading.Thread(target = self.target)
        self.thread.start()


def startEvent(event):
    r.roop = True
    r.start()


def finishEvent(event):
    r.roop = False
    window.close()
    sys.exit()


def isalnum_ascii(s):
    str_list = list(s)

    for i in str_list:
        if not i == "_":
            if i.isalnum() and i.isascii():
                pass

            else:
                return False

        else:
            pass
    
    return True


def is_integer(n):
    return n.isascii() and n.isdecimal()


def ip_check(values):
    try:
        ip_set = ipaddress.ip_address(values["ip"])

        if type(ip_set) is ipaddress.IPv4Address:
            ip = str(ip_set)

            return ip

        else:
            sg.popup("エラーが発生しました！\n【このIPは使用できません】", title="IP Error!")
            window["ip"].update("127.0.0.1")
            ip = "127.0.0.1"

            return None
    
    except ValueError:
        sg.popup("エラーが発生しました！\n【IPに使用できない値が含まれています】", title="IP Error!")
        window["ip"].update("127.0.0.1")
        ip = "127.0.0.1"

        return None


def port_check(values):
    valid_flag = False
    if is_integer(values["port"]):
        port=int(values["port"])
        if 1 <= port <= 65535:
            valid_flag = True

    if not valid_flag:
        if values["port"] == "easter":
            sg.popup(title="Easter egg", image="pass")

        sg.popup("エラーが発生しました！\n【Portに使用できない値が含まれています】", title="Port Error!")

        window["port"].update("9000")
        port = 9000
        return None

    return port


def interval_check(values):
    valid_flag = False
    if is_integer(values["interval"]):
        interval = int(values["interval"])
        if 1 <= interval <= 3600:
            valid_flag = True

    if not valid_flag:
        sg.popup("エラーが発生しました！\n【送信間隔に使用できない値が含まれています】", title="Interval Error!")
        window["interval"].update("1")
        interval = 1
        return None

    return interval


def str_check(values):
    if parameter_check(values):
        thp = values["thp"]
        hp = values["hp"]
        tp = values["tp"]
        op = values["op"]

        param_list = [thp, hp, tp, op]

        if len(param_list) != len(set(param_list)):
            sg.popup("エラーが発生しました！\n【Parametersの文字列が重複しています】", title="Parameter Error!")

            window["thp"].update("DD_thp")
            window["hp"].update("DD_hp")
            window["tp"].update("DD_tp")
            window["op"].update("DD_op")

            thp = "DD_thp"
            hp = "DD_hp"
            tp = "DD_tp"
            op = "DD_op"

            return thp, hp, tp, op

        return thp, hp, tp, op

    else:
        sg.popup("エラーが発生しました！\n【Parametersに使用できない文字列が含まれています】", title="Parameter Error!")

        window["thp"].update("DD_thp")
        window["hp"].update("DD_hp")
        window["tp"].update("DD_tp")
        window["op"].update("DD_op")

        thp = "DD_thp"
        hp = "DD_hp"
        tp = "DD_tp"
        op = "DD_op"

        return thp, hp, tp, op


def parameter_check(values):
    param_list = [
        values["thp"],
        values["hp"],
        values["tp"],
        values["op"]
    ]

    for i in param_list:
        if not isalnum_ascii(i):
            return False

        if " " in i:
            return False

    return True


window = sg.Window("Digital Display System V2.1 for GUI", layout)

if __name__ == "__main__":
    r = Receive()

    while True:

        event, values = window.read()
        print(event, values)

        if event is None:
            break

        if event == sg.WINDOW_CLOSED:
            break

        elif event == "settings":
            ip = ip_check(values)
            port = port_check(values)
            interval = interval_check(values)

            if all([ip, port, interval]):
                window["paramtext"].update(ip + ":" + str(port))

                print(ip, ":", end="")
                print(port)
                print(interval, "秒")

                strcheck = str_check(values)

                DD_thp = strcheck[0]
                DD_hp = strcheck[1]
                DD_tp = strcheck[2]
                DD_op = strcheck[3]

                window["text_thp"].update(DD_thp)
                window["text_hp"].update(DD_hp)
                window["text_tp"].update(DD_tp)
                window["text_op"].update(DD_op)

        elif event == "startbutton":
            if not buttonflag:
                ip = ip_check(values)
                port = port_check(values)
                interval = interval_check(values)

                if all([ip, port, interval]):

                    window["paramtext"].update(ip + ":" + str(port))

                    print("start")

                    startEvent(event)

                    window["startbutton"].update("送信停止")
                    window["sstext"].update("送信を開始しました")
                    buttonflag = True

                    window["ip"].update(disabled=True)
                    window["port"].update(disabled=True)
                    window["interval"].update(disabled=True)
                    window["settings"].update(disabled=True)
                    window["thp"].update(disabled=True)
                    window["hp"].update(disabled=True)
                    window["tp"].update(disabled=True)
                    window["op"].update(disabled=True)

            else:
                r.roop = False
                window["startbutton"].update("送信開始")
                window["sstext"].update("送信を停止しました")
                buttonflag = False

                window["ip"].update(disabled=False)
                window["port"].update(disabled=False)
                window["interval"].update(disabled=False)
                window["settings"].update(disabled=False)
                window["thp"].update(disabled=False)
                window["hp"].update(disabled=False)
                window["tp"].update(disabled=False)
                window["op"].update(disabled=False)

    finishEvent(event)