#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# main.py
# (c) Oleg Plaxin 2018
# plaxoleg@gmail.com

from requests_html import HTMLSession
import sys
import time


def check_user(id):
    TAG = "user checker"
    vk_api_link = "https://api.vk.com/method/"
    access_token = "2cbc788c2cbc788c2cbc788c082cde2a0322cbc2cbc788c7670e35f9811d37cde017f2b"
    v = "5.74"
    get_link = vk_api_link + "users.get?user_ids=" + str(
        id) + "&fields=sex,online,last_seen&access_token=" + access_token + "&v=" + v

    ms = int(round(time.time() * 1000))
    content = HTMLSession().get(get_link)
    json = content.json()
    countMillis = int(round(time.time() * 1000)) - ms

    userinfo = json["response"][0]
    userstat = userinfo["last_seen"]

    nameofuser = userinfo["first_name"] + " " + userinfo["last_name"]
    sex = [["была в сети", "был в сети"], ["в сети", "в сети"]]
    device = ["", "с мобильного", "с iPhone", "", "с Android", "", "с Windows", "с ПК"]
    ms_time = int(userstat["time"]) + 10800

    log("i", nameofuser + " " + sex[int(userinfo["online"])][int(userinfo["sex"]) - 1] +
        " " + device[int(userstat["platform"])] + ", " + time.strftime("%d %b %Y %H:%M:%S", time.gmtime(ms_time)))
    log(TAG, "Задержка " + str(countMillis) + " мс.")


def log(tag, message):
    nowtime = time.strftime("%d %b %Y %H:%M:%S", time.localtime())
    if str(tag) == "i":
        text_return = "\n" + str(nowtime) + ": " + str(message) + "\n"
    else:
        text_return = str(nowtime) + ": " + str(tag) + ": " + str(message)
    print(text_return)


if __name__ == "__main__":
    TAG = "main"

    startup = time.time()
    runtimes = 0

    log("i", "\tVK Online checker\t")

    user = None
    timer_delay = 1
    if len(sys.argv) == 2:
        user = sys.argv[1]
    elif len(sys.argv) == 3:
        timer_delay = int(sys.argv[2])
    else:
        user = input("Введите ID пользователя: ")
        timer_delay = float(input("Введите задержку таймера (мин): "))

    while True:
        runtimes += 1
        print()
        log(TAG, "Программный цикл: " + str(runtimes))

        if user is None and user == "":
            break
        else:
            check_user(user)

        uptime = round(time.time() * 1000) - round(startup * 1000)

        log(TAG, "Повтор команды через " + str(timer_delay) + " минут.")
        log(TAG, "Uptime: " + str(uptime) + " ms")

        time.sleep(60 * timer_delay)
