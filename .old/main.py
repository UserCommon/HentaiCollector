from multiprocessing import Pool
from bs4 import BeautifulSoup, SoupStrainer
from SETTINGS import *
import requests

import time
import uuid
from os.path import basename
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os

f = open('links.txt', 'a+')


def parsePage(x):
    response = requests.get(url_to_parse + str(x) + "&tags=" + what_to_search)
    strainer = SoupStrainer('div', attrs={'class': 'content'})
    soup = BeautifulSoup(response.text, "lxml", parse_only=strainer)
    mydivs = soup.find_all('div', {"class": "inner"})
    posts = []
    for divs in mydivs:
        post = divs.find('a', href=True)
        link = post["href"]
        posts.append("https://yande.re" + link)
    return posts


def getPicturesSrc(post_src):
    response = requests.get(post_src.rstrip())
    strainer = SoupStrainer('img', attrs={'id': 'image'})
    soup = BeautifulSoup(response.text, "lxml", parse_only=strainer)
    img = soup.find('img', id="image")
    src = img["src"]
    return src


def downloadPictures(src):
    unique_name = src[63:].replace("%20", "_")
    img_data = requests.get(src).content
    if what_to_search != "" or " ":
        image = open(what_to_search + "/" + unique_name, 'wb')
    else:
        image = open("imgs/" + unique_name, 'wb')
    image.write(img_data)


def get_input():
    print("Maybe you want parse from a certain page? (press enter if no)")
    return input()


def main(inp):

    if inp == '\n' or ' ' or '':
        x = 0
    else:
        x = int(inp)

    print("Parsing started...\n")

    last_line = 0

    while True:
        to_download = []
        print("Page " + str(x) + " parsed.")
        srcs = parsePage(x)

        for src in srcs:
            print(src)
            to_download.append(getPicturesSrc(src))  # <----

        thing = (str(srcs)[1:-1]).replace(",", "\n").replace("'", "").replace(" ", "") + '\n'
        print(*thing)
        print("Parsed: \n" + thing)

        if thing != '\n':
            # f.writelines(thing)
            pass
        else:
            print("END.")
            break

        print("Downloading... \n")
        print(to_download)
        for downloads in to_download:
            print(downloads)
            if 'http' in downloads:
                try:
                    downloadPictures(downloads)
                except Exception as e:
                    print(e)
        x += 1


if __name__ == '__main__':
    inp = get_input()
    with Pool(8) as p:
        p.map(main(inp))
