import json
import codecs
import json
from os.path import expanduser

def is_admin(user):
    with open(expanduser("~/credentials/discordConfig.json"), 'r',encoding='utf8') as f:
        data=json.load(f)
    if user in data["owners"]:
        return True
    else:
        return False

def getState(lysliste):
    state = {}
    for light in lysliste:
        state[light] = b.get_light(light,'xy')
    return state

def returnState(lysliste,state):
     for light in lysliste:
        b.set_light(light,'xy',state[light])

def log(time,user,message,channel,file):
    f= open(expanduser("~/credentials/") + file + ".log","a+")
    f.write(str(time) + " " + str(user) + " " + str(message) + " " + str(channel)+"\n")
    f.close()
