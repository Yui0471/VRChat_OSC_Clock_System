from pythonosc.udp_client import SimpleUDPClient
import PySimpleGUI as sg
import time
import threading
import sys
import datetime
import math
import ipaddress

#////////////////////////////////////////////////////
#VRChat Open Sound Control 
#                  時刻表示プログラム
#
#Analog Clock System Stable Version 2.1 for GUI
#
#////////////////////////////////////////////////////

#作成 : 風庭ゆい
#最終更新 : 2022/04/17

AC_hh = "AC_hh"
AC_mh = "AC_mh"
AC_sc = "AC_sc"

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
        sg.Text("時", size=(2,1)), sg.Text("/avatar/parameters/"), sg.InputText("AC_hh", key="hh", size=(20,1)),
        sg.Text("AC_hh", key="text_hh", size=(20,1))
    ],

    [
        sg.Text("分", size=(2,1)), sg.Text("/avatar/parameters/"), sg.InputText("AC_mh", key="mh", size=(20,1)),
        sg.Text("AC_mh", key="text_mh", size=(20,1))
    ],

    [
        sg.Text("秒", size=(2,1)), sg.Text("/avatar/parameters/"), sg.InputText("AC_sc", key="sc", size=(20,1)),
        sg.Text("AC_sc", key="text_sc", size=(20,1))
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

        param_hh = "/avatar/parameters/" + AC_hh
        param_mh = "/avatar/parameters/" + AC_mh
        param_sc = "/avatar/parameters/" + AC_sc

        print(param_hh)
        print(param_mh)
        print(param_sc)

        while (self.roop):

            dt_now = datetime.datetime.now()

            hours = dt_now.hour % 12
            minutes = dt_now.minute
            seconds = dt_now.second
            meridian = dt_now.strftime('%p')

            minutes_hand = minutes / 100
            seconds_hand = seconds / 100

            time_hh = str(hours)
            time_mh = str(minutes)
            time_sc = str(seconds)

            time_notify = time_hh + ":" + time_mh + ":" + time_sc + "." + meridian + "."

            print("\r現在時刻:", time_notify, end="")

            window["time"].update("送信中の現在時刻 :" + str(time_notify))

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

        else: #_だったら
            pass

    return True


def is_integer(n):
    return n.isascii() and n.isdecimal()


def ip_check(values): #IPv4が有効かどうか
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


    #リスト形式に戻すかもしれない
    #ip_list = [
    #    values["ip1"],
    #    values["ip2"],
    #    values["ip3"],
    #    values["ip4"]
    #]

    #for i in ip_list:
    #    if not is_integer(i) or int(i) > 255:
            #エラー処理
    #        return ip
    #成功
    #ip = ".".join(ip_list)
    #return ip


def port_check(values): #ポート番号が有効かどうか
    valid_flag = False
    if is_integer(values["port"]):
        #数値の場合
        port = int(values["port"])
        #ポート範囲のチェック
        if 1 <= port <= 65535:
            valid_flag = True

    if not valid_flag:
        if values["port"] == "small is beautiful":
            sg.popup(title="Image", image="./image.png")

        #失敗
        sg.popup("エラーが発生しました！\n【Portに使用できない値が含まれています】", title="Port Error!")

        window["port"].update("9000")
        port = 9000
        return None

    return port


def interval_check(values):
    valid_flag = False
    if is_integer(values["interval"]):
        #数値の場合
        interval = int(values["interval"])
        #有効範囲のチェック(1秒から最大1時間)
        if 1 <= interval <= 3600:
            valid_flag = True

    if not valid_flag:
        #失敗
        sg.popup("エラーが発生しました！\n【送信間隔に使用できない値が含まれています】", title="Interval Error!")
        window["interval"].update("1")
        interval = 1
        return None

    return interval


def str_check(values): #パラメータが有効かどうか
    if parameter_check(values):
        hh = values["hh"]
        mh = values["mh"]
        sc = values["sc"]

        param_list = [hh, mh, sc]

        if len(param_list) != len(set(param_list)):
            sg.popup("エラーが発生しました！\n【Parametersの文字列が重複しています】", title="Parameter Error!")

            window["hh"].update("AC_hh")
            window["mh"].update("AC_mh")
            window["sc"].update("AC_sc")

            hh = "AC_hh"
            mh = "AC_mh"
            sc = "AC_sc"

            return hh, mh, sc

        return hh, mh, sc

    else:
        sg.popup("エラーが発生しました！\n【Parametersに使用できない文字列が含まれています】", title="Parameter Error!")

        window["hh"].update("AC_hh")
        window["mh"].update("AC_mh")
        window["sc"].update("AC_sc")

        hh = "AC_hh"
        mh = "AC_mh"
        sc = "AC_sc"

        return hh, mh, sc
            

def parameter_check(values):
    param_list = [
        values["hh"],
        values["mh"],
        values["sc"]
    ]

    for i in param_list:
        if not isalnum_ascii(i):
            return False
                
        if " " in i:
            return False

    return True


window = sg.Window("Analog Clock System V2.1 for GUI", layout)

if __name__ == "__main__":
    r = Receive()

    while True:

        event, values = window.read()
        print(event, values)

        if event is None:
            break

        elif event == sg.WINDOW_CLOSED: #ウインドウの×ボタン
            break

        elif event == "settings": #設定反映ボタン
            ip = ip_check(values)
            port = port_check(values)
            interval = interval_check(values)

            if all([ip, port, interval]):
                window["paramtext"].update(ip + ":" + str(port))

                print(ip, ":", end="")
                print(port)
                print(interval, "秒")

                strcheck = str_check(values)

                AC_hh = strcheck[0]
                AC_mh = strcheck[1]
                AC_sc = strcheck[2]

                window["text_hh"].update(AC_hh)
                window["text_mh"].update(AC_mh)
                window["text_sc"].update(AC_sc)


        elif event == "startbutton": #送信ボタン
            if not buttonflag: #送信ボタンがFalseのとき
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

                    #入力部ロック
                    window["ip"].update(disabled=True)
                    window["port"].update(disabled=True)
                    window["interval"].update(disabled=True)
                    window["settings"].update(disabled=True)
                    window["hh"].update(disabled=True)
                    window["mh"].update(disabled=True)
                    window["sc"].update(disabled=True)

            else: #送信ボタンがTrueのとき
                r.roop = False
                window["startbutton"].update("送信開始")
                window["sstext"].update("送信を停止しました")
                buttonflag = False

                #入力部ロック解除
                window["ip"].update(disabled=False)
                window["port"].update(disabled=False)
                window["interval"].update(disabled=False)
                window["settings"].update(disabled=False)
                window["hh"].update(disabled=False)
                window["mh"].update(disabled=False)
                window["sc"].update(disabled=False)

    finishEvent(event)