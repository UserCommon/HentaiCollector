import os


class SETTINGS:
    def __init__(self):
        self.query = ''
        self.download_path = "default"
        self.basic_url_path = "https://yande.re"
        self.basic_url_page_path = "https://yande.re/post?page="
        self.page = 0
        # change it
        self.cores = 32

    def initialize(self):
        self.request()
        self.get_page()

    def create_directory(self, dir_name: str):
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        self.download_path = dir_name

    def request(self):
        print("What do you want to find?")
        self.query = input()
        self.create_directory(self.query)

    def get_page(self):
        print("Do you want start finding something from certain page?\n (Number/Enter(NO))")
        tmp = input()
        if tmp != (' ' or '') and tmp.isdigit():
            self.page = int(tmp)



