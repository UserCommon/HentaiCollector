import random
import string
import os

path = "default"
print("Type search querry")
what_to_search = input()

try:
    if not os.path.isdir(what_to_search):
        os.makedirs(what_to_search)

except OSError:
    if not os.path.isdir(path):
        raise


def generate_code(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def changeSpace(what_to_search):
    space = "%20"
    what_to_search = what_to_search.replace(' ', space)
    return what_to_search


def changePercTwent(word):
    space = " "
    word = word.replace("%20", space)
    return word


# what_to_search = changeSpace(what_to_search)

url_to_parse = "https://yande.re/post?page="
folder = "imgs/"
