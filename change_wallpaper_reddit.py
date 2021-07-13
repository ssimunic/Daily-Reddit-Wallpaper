#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import ctypes
import json
import os
import platform
import re
import sys
import random
from collections import defaultdict
from configparser import ConfigParser
from io import StringIO

import praw
import requests

if sys.version_info <= (2, 6):
    import commands as subprocess
else:
    import subprocess


def load_config():
    default = defaultdict(str)
    default["subreddit"] = "wallpaper"
    default["nsfw"] = False
    default["time"] = "day"
    default["display"] = "0"
    default["output"] = "Pictures/Wallpapers"
    default["sort"] = "hot"
    default["limit"] = 20
    default["random"] = False

    config_path = os.path.expanduser("~/.config/change_wallpaper_reddit.rc")
    section_name = "root"
    try:
        conf = ConfigParser(default)
        with open(config_path, "r") as stream:
            stream = StringIO("[{section_name}]\n{stream_read}".format(section_name=section_name,
                                                                       stream_read=stream.read()))
            if sys.version_info >= (3, 0):
                conf.read_file(stream)
            else:
                conf.read_file(stream)

            ret = {}

            # Add a value to ret, printing an error message if there is an error
            def add_to_ret(fun, name):
                try:
                    ret[name] = fun(section_name, name)
                except ValueError as e_code:
                    err_str = "Error in config file.  Variable '{}': {}. The default '{}' will be used."

                    # print sys.stderr >> err_str.format(name, str(e_code), default[name])
                    ret[name] = default[name]

            add_to_ret(conf.get, "subreddit")
            add_to_ret(conf.getboolean, "nsfw")
            add_to_ret(conf.getint, "display")
            add_to_ret(conf.get, "time")
            add_to_ret(conf.get, "output")
            add_to_ret(conf.get, "sort")
            add_to_ret(conf.get, "limit")
            add_to_ret(conf.get, "random")

            return ret

    except IOError as e:
        return default


config = load_config()


def parse_args():
    """parse args with argparse
    :returns: arguments
    """
    parser = argparse.ArgumentParser(description="Daily Reddit Wallpaper")
    parser.add_argument("-s", "--subreddit", type=str, default=config["subreddit"],
                        help="Example: art, getmotivated, wallpapers, ...")
    parser.add_argument("-t", "--time", type=str, default=config["time"],
                        help="Example: hour, day, week, month, year")
    parser.add_argument("-n", "--nsfw", action='store_true', default=config["nsfw"], help="Enables NSFW tagged posts.")
    parser.add_argument("-d", "--display", type=int, default=config["display"],
                        help="Desktop display number on OS X (0: all displays, 1: main display, etc")
    parser.add_argument("-o", "--output", type=str, default=config["output"],
                        help="Set the outputfolder in the home directory to save the Wallpapers to.")
    parser.add_argument("--sort", type=str, default=config["sort"],
                        help="Can be one of: hot, top, new.")
    parser.add_argument("-l","--limit", type=str, default=config["limit"],
                        help="Set a limit to pull posts")
    parser.add_argument("-r","--random", action='store_true', default=config["random"],
                        help="Randomize witin sort")

    arguments = parser.parse_args()
    return arguments


def get_top_image(sub_reddit):
    """Get image link of most upvoted wallpaper of the day
    :sub_reddit: name of the sub reddit
    :return: the image link
    """
    if args.sort == "top":
        submissions = sub_reddit.top(params={"t": args.time}, limit=int(args.limit))
    elif args.sort == "new":
        submissions = sub_reddit.new(params={"t": args.time}, limit=int(args.limit))
    else:
        submissions = sub_reddit.hot(params={"t": args.time}, limit=int(args.limit))

    if args.random:
        submissions= sorted(submissions, key=lambda k: random.random())
    else:
        submissions = submissions

    for submission in submissions:
        ret = {"id": submission.id}
        if not args.nsfw and submission.over_18:
            continue
        url = submission.url
        # Strip trailing arguments (after a '?')
        url = re.sub(R"\?.*", "", url)
        ret['type'] = url.split(".")[-1]

        if url.endswith(".jpg") or url.endswith(".png"):
            ret["url"] = url
        # Imgur support
        elif ("imgur.com" in url) and ("/a/" not in url) and ("/gallery/" not in url):
            if url.endswith("/new"):
                url = url.rsplit("/", 1)[0]
            id_toget = url.rsplit("/", 1)[1].rsplit(".", 1)[0]
            ret["url"] = "http://i.imgur.com/{id}.jpg".format(id=id_toget)
        else:
            continue

        return ret


def detect_desktop_environment():
    """Get current Desktop Environment
       http://stackoverflow.com
       /questions/2035657/what-is-my-current-desktop-environment
    :return: environment
    """
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
                            d.currentConfigGroup = Array("Wallpaper",
                                                   "org.kde.image",
                                                   "General");
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
    elif os.environ.get("DESKTOP_SESSION") == "i3":
        environment["name"] = "i3"
        environment["command"] = "feh --bg-scale {save_location}"
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

    args = parse_args()
    subreddit = args.subreddit
    save_dir = args.output

    supported_linux_desktop_envs = ["gnome", "mate", "kde", "lubuntu", "i3"]

    # Load credentials from credentials.json file
    with open(os.path.dirname(os.path.realpath(sys.argv[0])) + '/credentials.json') as f:
        params = json.load(f)

    # Python Reddit Api Wrapper
    r = praw.Reddit(client_id=params['client_id'],
                    client_secret=params['api_key'],
                    user_agent=f"Get top wallpaper from /r/{subreddit}")

    # Get top image link
    image = get_top_image(r.subreddit(subreddit))
    try:
        if "url" not in image:
            sys.exit("Error: No suitable images were found, the program is now exiting.")
    except TypeError:
        sys.exit("Error: No suitable images were found, the program is now exiting.")

    # Request image
    response = requests.get(image["url"], allow_redirects=False)

    # If image is available, proceed to save
    if response.status_code == requests.codes.ok:
        # Get home directory and location where image will be saved
        # (default location for Ubuntu is used)
        home_dir = os.path.expanduser("~")
        save_location = "{home_dir}/{save_dir}/{subreddit}-{id}.{image_type}".format(home_dir=home_dir,
                                                                                     save_dir=save_dir,
                                                                                     subreddit=subreddit,
                                                                                     id=image["id"],
                                                                                     image_type=image['type'])

        if not os.path.isfile(save_location):
            # Create folders if they don't exist
            directory = os.path.dirname(save_location)
            if not os.path.exists(directory):
                os.makedirs(directory)

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
            if args.display == 0:
                command = """
                        osascript -e 'tell application "System Events"
                            set desktopCount to count of desktops
                            repeat with desktopNumber from 1 to desktopCount
                                tell desktop desktopNumber
                                    set picture to "{save_location}"
                                end tell
                            end repeat
                        end tell'
                          """.format(save_location=save_location)
            else:
                command = """osascript -e 'tell application "System Events"
                                set desktopCount to count of desktops
                                tell desktop {display}
                                    set picture to "{save_location}"
                                end tell
                            end tell'""".format(display=args.display,
                                                save_location=save_location)
            os.system(command)
    else:
        sys.exit("Error: Image url is not available, the program is now exiting.")
