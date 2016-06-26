#!/usr/bin/env python
import praw
import os
import requests
import argparse
import sys
import ctypes
import platform
import time

if sys.version_info <= (2, 6):
    import commands as subprocess
else:
    import subprocess

# Get image link of most upvoted wallpaper of the day
def get_top_image(sub_reddit):
    submissions = sub_reddit.get_new(limit=10) if args.time == "new" else sub_reddit.get_top(params={"t": args.time},
                                                                                             limit=10)
    for submission in submissions:
        if not args.nsfw and submission.over_18:
            continue
        url = submission.url
        if url.endswith(".jpg"):
            return url
        # Imgur support
        if ("imgur.com" in url) and ("/a/" not in url):
            if url.endswith("/new"):
                url = url.rsplit("/", 1)[0]
            id = url.rsplit("/", 1)[1].rsplit(".", 1)[0]
            return "http://imgur.com/{id}.jpg".format(id=id)


# Get current Desktop Environment
# http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
def detect_desktop_environment():
    environment = {}
    if os.environ.get("KDE_FULL_SESSION") == "true":
        environment["name"] = "kde"
        environment["command"] = """
                    qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
                        var allDesktops = desktops();
                        print (allDesktops);
                        for (i=0;i<allDesktops.length;i++) {{
                            d = allDesktops[i];
                            d.wallpaperPlugin = "org.kde.image";
                            d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                            d.writeConfig("Image", "file:///{save_location}")
                        }}
                    '
                """
    elif os.environ.get("GNOME_DESKTOP_SESSION_ID"):
        environment["name"] = "gnome"
        environment["command"] = "gsettings set org.gnome.desktop.background picture-uri file://{save_location}"
    elif os.environ.get("DESKTOP_SESSION") == "Lubuntu":
        environment["name"] = "lubuntu"
        environment["command"] = "pcmanfm -w {save_location} --wallpaper-mode=fit"
    elif os.environ.get("DESKTOP_SESSION") == "mate":
        environment["name"] = "mate"
        environment["command"] = "gsettings set org.mate.background picture-filename {save_location}"
    else:
        try:
            info = subprocess.getoutput("xprop -root _DT_SAVE_MODE")
            if ' = "xfce4"' in info:
                environment["name"] = "xfce"
        except (OSError, RuntimeError):
            environment = None
            pass
    return environment


if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subreddit", type=str, default="wallpapers",
                        help="Example: art, getmotivated, wallpapers, ...")
    parser.add_argument("-t", "--time", type=str, default="day", help="Example: new, hour, day, week, month, year")
    parser.add_argument("-n", "--nsfw", action='store_true', help="Enables NSFW tagged posts.")

    args = parser.parse_args()

    subreddit = args.subreddit

    supported_linux_desktop_envs = ["gnome", "mate", "kde", "lubuntu"]

    # Python Reddit Api Wrapper
    r = praw.Reddit(user_agent="Get top wallpaper from /r/ {subreddit} by /u/ssimunic".format(subreddit=subreddit))

    # Get top image path
    image_url = get_top_image(r.get_subreddit(subreddit))

    # Request image
    response = requests.get(image_url)

    # If image is available, proceed to save
    if response.status_code == requests.codes.ok:
        # Get home directory and location where image will be saved (default location for Ubuntu is used)
        home_dir = os.path.expanduser("~")
        save_location = "{home_dir}/Pictures/Wallpapers/{subreddit}-{time}.jpg".format(home_dir=home_dir,
                                                                                       subreddit=subreddit,
                                                                                       time=time.strftime("%d-%m-%Y"))

        # Create folders if they don't exist
        dir = os.path.dirname(save_location)
        if not os.path.exists(dir):
            os.makedirs(dir)

        # Write to disk
        with open(save_location, "wb") as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)

        # Check OS and environments
        platform_name = platform.system()
        if platform_name.startswith("Lin"):

            # Check desktop environments for linux
            desktop_environment = detect_desktop_environment()
            if desktop_environment and desktop_environment["name"] in supported_linux_desktop_envs:
                os.system(desktop_environment["command"].format(save_location=save_location))
            else:
                print("Unsupported desktop environment")

        # Windows
        if platform_name.startswith("Win"):
            # Python 3.x
            if sys.version_info >= (3, 0):
                ctypes.windll.user32.SystemParametersInfoW(20, 0, save_location, 3)
            # Python 2.x
            else:
                ctypes.windll.user32.SystemParametersInfoA(20, 0, save_location, 3)

        # OS X/macOS
        if platform_name.startswith("Darwin"):
            command = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX " \
                      "file \"{save_location}\"'".format(save_location=save_location)
            os.system(command)
