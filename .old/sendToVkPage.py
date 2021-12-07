import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import time
import random
from SETTINGS import *


elems = []
f = open('links.txt', 'r')
lines = f.readlines()

session = vk_api.VkApi(token=VK_token)
vk = session.get_api()



def getUserId(owner_link):
    data = session.method("users.get", {"user_ids": owner_link})
    return data[0]["id"] 


def postToWall(owner_id, attachments):
    post = session.method("wall.post", {"owner_id" : owner_id, "attachments": attachments})


def sendMessage(owner_id, attachments):
    send = session.method("messages.send", {"user_id" : owner_id, "message": attachments,"random_id": 0})
    

for i in range(30):
    time.sleep(1)
#    postToWall(getUserId(VK_reciever), random.choice(lines))
    sendMessage(getUserId(VK_reciever), random.choice(lines))


f.close()
