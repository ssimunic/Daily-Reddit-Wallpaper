# Change Ubuntu Wallpaper (on startup)
This script changes your wallpaper to most upvoted image of the day on /r/wallpapers or from any other subreddit.


**Run it on startup for new wallpaper on every session.**

*Tested on Ubuntu 16.04.*

Dependencies
=======
Make sure you have Python installed.

If you don't have ```pip ``` for Python:
```
sudo apt-get install python-pip
```

You will need modules ```requests``` and ```praw``` installed, which can be done running following commands:

```
pip install requests
pip install praw
```

Using script
=======

Simply run:
```
python /home/silvio/Scripts/change_wallpaper_reddit.py 
```

If you wanna use other subreddit, include argument with the subreddit name:
```
python /home/silvio/Scripts/change_wallpaper_reddit.py --subreddit earthporn
```

If you don't want to change your wallpaper daily, you can use top weekly, monthly or yearly wallpaper too by adding argument ```week``` or ```month``` or ```year``` to the script.

Example:
```
python /home/silvio/Scripts/change_wallpaper_reddit.py --time week 
```

Running on startup
=======
To make managment of the script simple, we can accomplish this using built-in Startup Applications.

![Startup Applications](http://i.imgur.com/NDFmFd9.png)


Click on Add.

![Add new startup command](http://i.imgur.com/uFqQ8ky.png)

Note: you can use ```--subreddit``` and ```--time``` name arguments here aswell.

