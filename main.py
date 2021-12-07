from bs4 import BeautifulSoup, SoupStrainer
from multiprocessing import Pool, Manager
import requests
from time import sleep
from settings import SETTINGS
import os


class Parser:
    def __init__(self, lists):
        self.settings = SETTINGS()
        self.query = self.settings.query
        self.page = self.settings.page
        self.posts = []
        self.srcs = lists

    def main(self):
        self.settings.initialize()
        while True:
            print(f"Parsing page: {self.settings.page}")
            self.parse_pages()

            with Pool(self.settings.cores) as p:
                p.map(self.get_pictures_src, self.posts)

            with Pool(self.settings.cores) as p:
                p.map(self.download_pictures, self.srcs)
                print(f"DOWNLOADED PAGE {self.settings.page}")

            self.settings.page += 1

    def parse_pages(self):
        response = requests.get(self.settings.basic_url_page_path + str(self.settings.page) + "&tags=" + self.settings.query)
        strainer = SoupStrainer('div', attrs={'class': 'content'})
        soup = BeautifulSoup(response.text, "lxml", parse_only=strainer)
        divs = soup.find_all('div', {"class": "inner"})
        for div in divs:
            post = div.find('a', href=True)
            link = post["href"]
            self.posts.append(self.settings.basic_url_path + link)

    def get_pictures_src(self, i: str) -> str:
        try:
            response = requests.get(i.rstrip())
            strainer = SoupStrainer('img', attrs={'id': 'image'})
            soup = BeautifulSoup(response.text, "lxml", parse_only=strainer)
            img = soup.find('img', id="image")
            self.srcs.append(img["src"])
            print(self.srcs)
        except requests.exceptions.ConnectionError:
            print("Conn_err?")
            sleep(5)

    def download_pictures(self, src: str):
        try:
            unique_name = src[63:].replace("%20", "_")
            print(f"Downloading {unique_name}")
            img_data = requests.get(src).content

            if not os.path.isfile(self.settings.download_path + "/" + unique_name):
                with open(self.settings.download_path + "/" + unique_name, "wb") as image:
                    image.write(img_data)
        except requests.exceptions.ConnectionError:
            print("Conn_error?")
            sleep(5)


if __name__ == '__main__':
    lists = Manager().list()
    parser = Parser(lists)
    parser.main()
