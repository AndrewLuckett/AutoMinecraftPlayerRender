import json
import urllib.request as requests
import base64

_UsernameURL = "https://api.mojang.com/users/profiles/minecraft/"
_UuidURL = "https://sessionserver.mojang.com/session/minecraft/profile/"

def getSkinFromUN(name):
    url = _UsernameURL + name
    r = requests.urlopen(url).read()
    dat = json.loads(r)

    return getSkinFromUUID(dat["id"])


def getSkinFromUUID(uuid):
    url = _UuidURL + uuid
    r = requests.urlopen(url).read()
    dat = json.loads(r)

    dat = decodeTextureValue(dat["properties"][0]["value"])
    return dat


def decodeTextureValue(value):
    dat = base64.b64decode(value)
    dat = json.loads(dat)
    return dat["textures"]["SKIN"]["url"]


def downloadTexture(url, path):
    requests.urlretrieve(url, path)

