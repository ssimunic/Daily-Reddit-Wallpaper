#!/usr/bin/env python
import praw
import os
import subprocess
import requests
import argparse
import ctypes
import platform
import time

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--subreddit", type=str, default="wallpapers")
parser.add_argument("-t", "--time", type=str, default="day")
parser.add_argument("--kde", action="store_true")
args = parser.parse_args()

# Get image link of most upvoted wallpaper of the day
def get_top_image(subreddit):
    for submission in subreddit.get_top(params={'t': args.time}, limit=10):
        url = submission.url
        if url.endswith(".jpg"):
            return url
        # Imgur support
        if ("imgur.com" in url) and ("/a/" not in url):
            if url.endswith("/new"):
                url = url.rsplit("/", 1)[0]
            id = url.rsplit("/", 1)[1].rsplit(".", 1)[0]
            return "http://imgur.com/" + id + ".jpg"

# Get current Desktop Environment
# http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
def detect_desktop_environment():
    desktop_environment = 'generic'
    if os.environ.get('KDE_FULL_SESSION') == 'true':
        desktop_environment = 'kde'
    elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
        desktop_environment = 'gnome'
    elif os.environ.get('DESKTOP_SESSION') == 'mate':
        desktop_environment = 'mate'
    else:
        try:
            info = getoutput('xprop -root _DT_SAVE_MODE')
            if ' = "xfce4"' in info:
                desktop_environment = 'xfce'
        except (OSError, RuntimeError):
            pass
    return desktop_environment

# Python Reddit Api Wrapper
r = praw.Reddit(user_agent="Get top wallpaper from /r/" + args.subreddit + " by /u/ssimunic")

# Get top image path
imageUrl = get_top_image(r.get_subreddit(args.subreddit))

# Request image
response = requests.get(imageUrl)

# If image is available, proceed to save
if response.status_code == 200:
    # Get home directory and location where image will be saved (default location for Ubuntu is used)
    homedir = os.path.expanduser('~')
    saveLocation = homedir + "/Pictures/Wallpapers/" + args.subreddit + "-" + time.strftime("%d-%m-%Y") + ".jpg"

    # Create folders if they don't exist
    dir = os.path.dirname(saveLocation)
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Write to disk
    with open(saveLocation, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)

    # Check OS and environments
    platformName = platform.system()
    if platformName.startswith("Lin"):

        # Check desktop environments for linux
        desktopEnvironment = detect_desktop_environment();
        if desktopEnvironment == 'gnome':
            os.system("gsettings set org.gnome.desktop.background picture-uri file://" + saveLocation)
        elif desktopEnvironment == 'mate':
            os.system("gsettings set org.mate.background picture-filename " + saveLocation)
        elif desktopEnvironment == 'kde':
            kde_console_string = """
                qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
                    var allDesktops = desktops();
                    print (allDesktops);
                    for (i=0;i<allDesktops.length;i++) {{
                        d = allDesktops[i];
                        d.wallpaperPlugin = "org.kde.image";
                        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                        d.writeConfig("Image", "file:///{}")
                    }}
                '
            """
            os.system(kde_console_string.format(saveLocation))
        else:
            print "Unsupported desktop environment"

    # Windows
    if platformName.startswith("Win"):
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, saveLocation, 3)
