#! /usr/bin/python
import praw
import os
import subprocess
import requests
import sys

# Get Imgur ID of most upvoted wallpaper
def get_top_image_id(subreddit):
    for submission in subreddit.get_top_from_day(limit=10):
        url = submission.url
        # Use only direct Imgur images
        if ("imgur.com" in url) and ("/a/" not in url):
            id = url.rsplit("/", 1)[1].rsplit(".", 1)[0]
            # Return ID for the first valid link
            return id

# Python Reddit Api Wrapper
r = praw.Reddit(user_agent="Get top wallpaper from /r/wallpers by /u/ssimunic")
subreddit = sys.argv[1] if len(sys.argv) > 1 else "wallpapers"

# Get Imgur ID and full path
topImageId = get_top_image_id(r.get_subreddit(subreddit))
imageUrl = "http://imgur.com/" + topImageId + ".jpg"

# Request image
response = requests.get(imageUrl)

# If image is available, proceed to save
if response.status_code == 200:
    # Get home directory and location where image will be saved (default location for Ubuntu is used)
    homedir = os.path.expanduser('~')
    saveLocation = homedir + "/Pictures/Wallpapers/"
    saveFileName = topImageId + ".jpg"

    # Write to disk
    with open(saveLocation + saveFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)

    # Execute command to change wallpaper
    os.system("gsettings set org.gnome.desktop.background picture-uri file:///home/" + homedir.rsplit("/",1)[1] + "/Pictures/Wallpapers/" + saveFileName)
