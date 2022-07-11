#!/usr/bin/python3

import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import quote
from datetime import datetime

# Define some usefull URL
url_mail = 'https://correo.uv.es/cgi-bin/ppostman/cclient/mb_change/noop/ca/'
url_header = 'https://portal.uv.es'

# Load the contents of the .env file with credentials
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Store the UV credentials into a dict to use it with the requests session later
data = {
    'username': os.environ.get("UV_USER"),
    'password': os.environ.get("UV_PASS")
}

# Store telegram token and chat id
token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("CHAT_ID")

def getCurrentDate():
    now = datetime.now()
    return now.strftime("%d/%m/%y %H:%M:%S")

def getNotSeen(soup):
    messages = soup.find("table", {"class": "imap_index_table"}).findAll("tr")
    not_seen = []
    if messages:
        for message in messages:
            flags = message.findAll("img", {"class": "img_flags"})
            if flags:
                for flag in flags:
                    if flag.get('title') == 'Nou':
                        not_seen.append(message)
    return not_seen

def getHref(soup):
    a_tags = soup.findAll("a")
    if a_tags:
        for item in a_tags:
            try:
                # Dirty fix to be sure we are in the correct path
                if 'prevpage.gif' == item.find("img", {"class": "buttons_img"}).get('src').split('/')[-1]:
                    return item.get('href')
            except:
                pass
    return ''

def sendMessage(item):
    text = item.find("td", {"class": "i_subject"}).find("a").text
    if any(x in text for x in ["[PREGON", "[OFERTA"]):
        return
    date = item.find("td", {"class": "i_date"}).text
    sender = item.find("td", {"class": "i_from"}).text
    bars = '----------------------------------------------------------------'
    message = quote(f'{bars}\n\n<b>NUEVO MENSAJE</b>❕ <i>{date}</i>\n\n\n🗣 {sender}\n\n\n{text}\n\n{bars}')
    url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Html&text=' + message
    requests.post(url)

def monitor_msgs(s, saved):
    try:
        request = s.get(url_header)
    except:
        return saved
    soup = BeautifulSoup(request.text, "html.parser")

    test = soup.find("span", {"class": "itemdesc"})

    if not test:
        print(f'\n{getCurrentDate()} $-> Sesión caducada, volviendo a iniciar')
        try:
            s.post(requests.get('https://correo.uv.es').url, data=data)
        except:
            pass
        return saved

    num = soup.find("div", {"class": "itemmailu"})
    not_seen = []

    if num:
        num = int(num.text)

        try:
            request = s.get(url_mail)
        except:
            return saved
        soup = BeautifulSoup(request.text, "html.parser")
        not_seen.extend(getNotSeen(soup))

        while num > len(not_seen):
            href = getHref(soup)
            if href:
                try:
                    request = s.get(url_header + href)
                except:
                    return saved
                soup = BeautifulSoup(request.text, "html.parser")
                not_seen.extend(getNotSeen(soup))
        cont = 0
        if abs(len(saved)-num) > 0:
            print(f'\n{getCurrentDate()} $-> Hay {abs(len(saved)-num)} nuevo/s mensaje/s')
            print(f'{getCurrentDate()} $-> Enviando mensaje/s')
        for i in not_seen:
            send = True
            for j in saved:
                i_num = i.find("td", {"class": "i_num"}).text
                j_num = j.find("td", {"class": "i_num"}).text
                if i_num == j_num:
                    send = False
            if send:
                cont += 1
                sendMessage(i)
        if cont > 0:
            print(f'{getCurrentDate()} $-> Se ha enviado {cont} mensajes')
    saved = not_seen
    return saved

def main():
    saved = []
    with requests.Session() as s:
        while True:
            print(f'{getCurrentDate()} $-> Esperando nuevo mensaje...', end='\r')
            saved = monitor_msgs(s, saved)

if __name__ == "__main__":
    main()