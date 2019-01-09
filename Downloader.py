import wx.adv
import wx
import praw
import subprocess
import os
import datetime
import random
import ctypes
import xml.etree.ElementTree as ET
import time
import threading
import sys
import urllib.request
from PIL import Image

TRAY_TOOLTIP = 'Reddit Wallpaper Crawler'
TRAY_ICON = 'Data/icon.png'
CURRENT_PIC = ""
DURATION = 0
STILLALIVE = False
WALLPAPERCHANGED = False


# Starting the API
reddit = praw.Reddit(client_id='EEPkNhcUV4y8gg',
                     client_secret='OZN1DEPwlM_xConxa3S9dwkpj-c',
                     user_agent='Wallpaper Dowloader',
                     username='VegetableBike8',
                     password='\OY42=h2zk$Zl[!>;gUxc=U}~N+SSUqM')


def WallpaperDownloader(number, Subs, AllWallpaper):
    global CURRENT_PIC
    todaysSub = Subs[random.randint(0, len(Subs)-1)]
    subreddit = reddit.subreddit(todaysSub).hot(limit=10*number)
    for submission in subreddit:
        if(submission.url not in AllWallpaper and "comment" not in submission.url):
            selectedlink = submission.url
            now = datetime.datetime.now()
            timeRightNow = now.strftime("%Y-%m-%d-%H%M")+str(random.randint(1, 1024))
            CURRENT_PIC = timeRightNow+".jpg"
            with open("Normal/Wallpaper.log", "a") as WallpaperLog:
                WallpaperLog.write(str(selectedlink)+", " + now.strftime("%Y-%m-%d %H:%M")+","+todaysSub+"\n")
            try:
                urllib.request.urlretrieve(selectedlink, "Normal\\"+CURRENT_PIC)
            except:
                return
            resolution = Image.open("Normal\\"+CURRENT_PIC)
            if(resolution.size[0]/resolution.size[1] < 1 and resolution.size[0] < 3000):
                return False
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.getcwd()+"\\Normal\\"+timeRightNow+".jpg", 0)
            return True
    return False


def InitWallpaper():
    global DURATION
    # Downloading the image and setting Background
    # Extracting data from Configs.xml
    # Subs
    tree = ET.parse("Data/config.xml")
    root = tree.getroot()
    Subs = []
    for lines in root.find("Subs"):
        Subs.append(lines.text)
    if(len(Subs) == 0):
        Subs = ["wallpapers"]
    # Duration
    try:
        DURATION = int(root.find("Interval").text)
    except:
        DURATION = 30
    # Collecting All Previous Images downloaded
    try:
        WallpaperLog = open("Normal/Wallpaper.log")
        AllWallpaper = []
        for lines in WallpaperLog:
            plink = lines.split(",")[0]
            AllWallpaper.append(plink)
        WallpaperLog.close()
        AllWallpaper = set(AllWallpaper)
    except:
        AllWallpaper = set()
    # Downloading a new Random Picture
    Status = False
    Number = 2
    while not Status:
        Status = WallpaperDownloader(Number, Subs, AllWallpaper)
        Number *= 2


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.ShowBalloon(title="Welcome to RWC", text="Your timely wallpaper changer", msec=100)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'New Image', self.requestImage)
        create_menu_item(menu, 'Add To Favorite', self.MoveToFavorite)
        create_menu_item(menu, 'Remove this image and add new', self.DeleteCurrent)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        subprocess.call("cd Data & notepad.exe config.xml", shell=True)

    def MoveToFavorite(self, event):
        global CURRENT_PIC
        str1 = "move /y Normal\\" + CURRENT_PIC+" Favorite\\" + CURRENT_PIC
        subprocess.call(str1, shell=True)
        self.ShowBalloon(title="Reddit Wallpaper Crawler", text="Image Moved to Favorite Folder", msec=50)

    def requestImage(self, event):
        global WALLPAPERCHANGED
        InitWallpaper()
        self.ShowBalloon(title="Reddit Wallpaper Crawler", text="Image Changed", msec=50)
        WALLPAPERCHANGED = True

    def DeleteCurrent(self, event):
        global CURRENT_PIC
        global WALLPAPERCHANGED
        command = "del /f "+os.getcwd()+"\\Normal\\"+CURRENT_PIC
        subprocess.call(command, shell=True)
        command = "del /f "+os.getcwd()+"\\Favorite\\"+CURRENT_PIC
        subprocess.call(command, shell=True)
        InitWallpaper()
        self.ShowBalloon(title="Reddit Wallpaper Crawler", text="Image Changed", msec=50)
        WALLPAPERCHANGED = True

    def on_exit(self, event):
        global STILLALIVE
        STILLALIVE = True
        wx.CallAfter(self.Destroy)
        self.frame.Close()


def IntervalChange():
    global DURATION
    global STILLALIVE
    global WALLPAPERCHANGED
    while(True):
        InitWallpaper()
        i = 0
        while(i < DURATION*6):
            time.sleep(10)
            i += 1
            if(STILLALIVE):
                return
            if(WALLPAPERCHANGED):
                i = 0
                WALLPAPERCHANGED = False


class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True


def main():
    ImageChangerAfterInterval = threading.Thread(target=IntervalChange)
    ImageChangerAfterInterval.start()
    app = App(False)
    app.MainLoop()
    ImageChangerAfterInterval.join()


if __name__ == '__main__':
    PATH = sys.argv[1]
    # Making Directory if not present
    if(not os.path.isdir(PATH)):
        os.mkdir(PATH)
    os.chdir(PATH)
    if(not os.path.isdir(PATH+"\\Favorite")):
        os.mkdir(PATH+"\\Favorite")
    if(not os.path.isdir(PATH+"\\Normal")):
        os.mkdir(PATH+"\\Normal")
    main()
