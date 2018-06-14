#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# main.py
# (c) Oleg Plaxin 2018
# plaxoleg@gmail.com

from requests_html import HTMLSession
import sys
import time
import os


def check_user(ids):
    TAG = "user checker"
    vk_api_link = "https://api.vk.com/method/"
    access_token = "2cbc788c2cbc788c2cbc788c082cde2a0322cbc2cbc788c7670e35f9811d37cde017f2b"
    v = "5.78"
    user_ids = ",".join(str(e) for e in ids)
    get_link = vk_api_link + "users.get?user_ids=" + str(user_ids) + "&fields=sex,online,last_seen&access_token=" + access_token + "&v=" + v

    ms = int(round(time.time() * 1000))
    content = HTMLSession().get(get_link)
    json = content.json()
    countMillis = int(round(time.time() * 1000)) - ms

    sex = [["была в сети", "был в сети"], ["в сети", "в сети"]]
    device = ["", "с мобильного", "с iPhone", "", "с Android", "", "с Windows", "с ПК"]

    log("br", "")
    for i in range(num_of_user):
        userinfo = json["response"][i]
        userstat = userinfo["last_seen"]

        nameofuser = userinfo["first_name"] + " " + userinfo["last_name"]
        ms_time = time.gmtime(int(userstat["time"]) + 10800)

        log("online", nameofuser + " " + sex[int(userinfo["online"])][int(userinfo["sex"]) - 1] +
            " " + device[int(userstat["platform"])] + ", " + time.strftime("%d %b %Y %H:%M:%S", ms_time))
        title_ch(nameofuser + " " + sex[int(userinfo["online"])][int(userinfo["sex"]) - 1] +
                 " " + device[int(userstat["platform"])] + ", " + time.strftime("%H:%M:%S", ms_time))
    log("br", "")

    log(TAG, "Задержка " + str(countMillis) + " мс.")


def title_ch(title_string):
    from os import system
    system("title " + title_string)


def log(tag, message):
    now = time.localtime()
    log_to_file = open(path + str(now.tm_mday) + ".log", "a")

    nowtime = time.strftime("%d %b %Y %H:%M:%S", now)
    if str(tag) == "i":
        text_return = "\n" + str(nowtime) + ": " + str(message) + "\n"
    elif str(tag) == "br":
        text_return = ""
    else:
        text_return = str(nowtime) + ": " + str(tag) + ": " + str(message)
    print(text_return)

    log_to_file.write(text_return + "\n")
    log_to_file.close()


if __name__ == "__main__":
    TAG = "main"

    startup = time.time()
    runtimes = 0

    print("\tVK Online checker\t")

    num_of_user = int(input("Колличество отслеживаемых пользователей: "))
    users = []
    for i in range(num_of_user):
        users.append(input("ID пользователя " + str(i+1) + ": "))
    users.sort()

    tdelay = 1
    if len(sys.argv) == 2:
        tdelay = sys.argv[1]
    else:
        tdelay = input("Введите задержку таймера (мин): ")

    timer_delay = tdelay

    now = time.localtime()
    if now.tm_mon < 10:
        month = "0" + str(now.tm_mon)
    else:
        month = str(now.tm_mon)

        path = None
        if len(users) >= 2:
            users_s = "; ".join(str(e) for e in users)
            path = "logs\\" + "few users\\" + users_s + "\\" + str(now.tm_year) + month + "\\"
        else:
            path = "logs\\" + str(users) + "\\" + str(now.tm_year) + month + "\\"

        if not os.path.exists(path):
            os.makedirs(path)

    while True:
        runtimes += 1
        print()
        log(TAG, "### ###")
        log(TAG, "Программный цикл: " + str(runtimes))

        try:
            if users is None and users == "":
                break
            else:
                check_user(users)
            timer_delay = tdelay
        except Exception as e:
            log("error", "An error has occurred: " + str(e))
        finally:
            timer_delay = 1

        uptime = round(time.time() * 1000) - round(startup * 1000)

        log(TAG, "Повтор команды через " + str(timer_delay) + " минут.")
        log(TAG, "Uptime: " + str(uptime) + " ms")

        time.sleep(60 * float(timer_delay))
