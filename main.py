#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# main.py
# (c) Oleg Plaxin 2018
# plaxoleg@gmail.com

from requests_html import HTMLSession
import sys
import time
import os
import configparser

config_name = "Settings"
vkapiuri_tag = "VKAPIURI"
accesstoken_tag = "ACCESSTOKEN"
version_tag = "VKAPIVERSION"


def check_user(ids):
    TAG = "user checker"

    user_ids = ",".join(str(e) for e in ids)
    get_link = vk_api_link + "users.get?user_ids=" + str(user_ids) + "&fields=sex,online,last_seen&access_token=" + \
               access_token + "&v=" + v + "&lang=ru"

    ms = int(round(time.time() * 1000))
    content = HTMLSession().get(get_link)
    json = content.json()
    countMillis = int(round(time.time() * 1000)) - ms

    sex = [["была в сети", "был в сети"], ["в сети", "в сети"]]
    device = ["с мобильного", "с iPhone", "с iPad", "с Android", "с Windows Phone", "с Windows 10", "с ПК", "с VK Mobile"]

    log("br", "")

    title_mes = ""
    user_online = 0

    for i in range(num_of_user):
        userinfo = json["response"][i]
        userstat = userinfo["last_seen"]

        nameofuser = userinfo["first_name"] + " " + userinfo["last_name"]
        ms_time = time.gmtime(int(userstat["time"]) + 10800)

        log("online", nameofuser + " " + sex[int(userinfo["online"])][int(userinfo["sex"]) - 1] +
            " " + device[int(userstat["platform"])-1] + ", " + time.strftime("%d %b %Y %H:%M:%S", ms_time))

        if int(userinfo["online"]):
            user_online += 1

        if len(users) > 1:
            title_mes = str(num_of_user) + " наблюдаемых / " + str(user_online) + " в сети"
        else:
            title_mes = nameofuser + " " + sex[int(userinfo["online"])][int(userinfo["sex"]) - 1] + \
                        " " + device[int(userstat["platform"])-1] + ", " + time.strftime("%H:%M:%S", ms_time)
    log("br", "")

    title_ch(title_mes)

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


def createConfig(path):
    config = configparser.ConfigParser()
    config.add_section(config_name)
    config.set(config_name, vkapiuri_tag, "https://api.vk.com/method/")
    config.set(config_name, accesstoken_tag, "2cbc788c2cbc788c2cbc788c082cde2a0322cbc2cbc788c7670e35f9811d37cde017f2b")
    config.set(config_name, version_tag, "5.80")

    with open(path, "w") as config_file:
        config.write(config_file)


def readConfig(path, param):
    if not os.path.exists(path):
        createConfig(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config.get(config_name, param)


if __name__ == "__main__":
    TAG = "main"

    startup = time.time()
    runtimes = 0

    print("\n\tVKOC ver.1.1\t")

    vk_api_link = str(readConfig("./config.ini", vkapiuri_tag))
    access_token = str(readConfig("./config.ini", accesstoken_tag))
    v = str(readConfig("./config.ini", version_tag))

    print("\nИнициализация успешна.\nVK API URI = " + vk_api_link + "\nACCESS TOKEN = " + access_token +
          "\nVK API VERSION = " + v + "\n")

    num_of_user = 0
    users = []
    tdelay = 1

    if len(sys.argv) >= 2:
        users = str(sys.argv[1]).split(",")
        num_of_user = len(users)
        tdelay = sys.argv[2]
    else:
        num_of_user = int(input("Колличество отслеживаемых пользователей: "))
        users = []
        for i in range(num_of_user):
            users.append(input("ID пользователя " + str(i + 1) + ": "))
        tdelay = input("Введите задержку таймера (мин): ")

    users.sort()
    timer_delay = tdelay

    now = time.localtime()
    if now.tm_mon < 10:
        month = "0" + str(now.tm_mon)
    else:
        month = str(now.tm_mon)

    path = None
    if len(users) > 1:
        users_s = "; ".join(str(e) for e in users)
        path = "logs/" + "few users/" + users_s + "/" + str(now.tm_year) + month + "/"
    else:
        path = "logs/" + str(users[0]) + "/" + str(now.tm_year) + month + "/"

    if not os.path.exists(path):
        os.makedirs(path)

    while True:
        runtimes += 1
        log("br", "")
        log(TAG, "### ###")
        log(TAG, "Программный цикл: " + str(runtimes))

        try:
            if users is None and users == "":
                break
            else:
                check_user(users)
            timer_delay = tdelay
        except Exception as e:
            log("error", "Произошла ошибка: " + str(e))
            timer_delay = 1

        uptime = round(time.time() * 1000) - round(startup * 1000)

        log(TAG, "Повтор команды через " + str(timer_delay) + " минут.")
        log(TAG, "Uptime: " + str(uptime) + " ms")

        time.sleep(60 * float(timer_delay))
