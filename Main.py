import SkinGrabber as sg
import subprocess
import os
import cv2

Config = {}

def log(*lines):
    print(*lines)

def loadConfig(path):
    import csv
    badcommands = []
    with open(path) as f:
        r = csv.reader(f, delimiter=' ', skipinitialspace = True)
        for e in r:
            if len(e) == 0: continue # Empty lines
            if len(e) != 2: # Lines that arent 2 elements
                badcommands.append(f"\t{e}")
                continue
            try:
                e[1] = float(e[1])
            except:
                pass
            Config[e[0]] = e[1]
    if len(badcommands):
        log(f"Bad config command(s) in {path}", *badcommands)


def loadAndSanitize(name):
    texUrl = sg.getSkinFromUN(name)
    sg.downloadTexture(texUrl, Config["skinfilepath"])

    img = cv2.imread(Config["skinfilepath"], cv2.IMREAD_UNCHANGED)
    
    if img.shape[0] == 32:
        img = cv2.copyMakeBorder(img, 0, 32, 0, 0, cv2.BORDER_CONSTANT)
        cv2.imwrite(Config["skinfilepath"], img)


def main():
    loadConfig("Default.cfg")
    loadConfig("Settings.cfg")

    names = Config["username"].split(" ")
    for name in names:
        loadAndSanitize(name)

        args = f"{Config['blenderpath']} -b {Config['blendfilepath']}"
        args += f" -o {os.path.abspath(Config['outputpath'] + name + '-##' )}"
        args += " -a" if Config["allframes"] else f" -f {int(Config['frame'])}"
        print(args)
        proc = subprocess.run(args)

if __name__ == "__main__":
    t = main()
