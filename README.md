# Daily Reddit Wallpaper
[![Build Status](https://travis-ci.org/federicotorrielli/Daily-Reddit-Wallpaper.svg?branch=master)](https://travis-ci.org/federicotorrielli/Daily-Reddit-Wallpaper)

This script changes your wallpaper to most upvoted image of the day on [/r/wallpaper](https://www.reddit.com/r/wallpaper/) or from any other subreddit.


**Run it on startup for new wallpaper on every session.**

*Supported: Linux (gnome, kde, mate, lxde), Windows and OS X*

Dependencies
=======
Make sure you have [Python3](https://www.python.org/downloads/) installed and PATH variable set.

Ubuntu
------
If you don't have ```pip ``` for Python:
```
sudo apt-get install python-pip
```

You will need modules ```requests``` and ```praw``` installed, which are in requirements.txt:

```
pip install -r requirements.txt
```

Arch
------
If you don't have ```pip``` for Python:
```
pacman -S python-pip
```
or, with yay:
```
yay -S python-pip
```
Then just install the requirements.txt with:
```
pip install -r requirements.txt
```

Windows
------
Follow [this guide](https://pip.pypa.io/en/stable/installing/) to install  ```pip```  and configure PATH variable.
The rest is the same.

Using script
=======
First, you'll need to configure the _credentials.json_ file with your personal Reddit API.
Your api_key will be the Reddit API secret and your client_id the first and smaller code:

![Reddit API](https://camo.githubusercontent.com/d53f92cd85d1279a239444acee25179e8e6d8bb5/687474703a2f2f692e696d6775722e636f6d2f65326b4f5231612e706e67)

Then, in the current project folder, run:
```
python change_wallpaper_reddit.py
```

If you wanna use other subreddit, include argument with the subreddit name:
```
python change_wallpaper_reddit.py --subreddit art
```

If you don't want to change your wallpaper daily, you can use hourly, weekly, monthly or yearly wallpaper too by adding one of the following arguments: ```hour```, ```week```, ```month```, ```year``` to the script.

Example:
```
python change_wallpaper_reddit.py --time week
```

If you want to choose which wallpaper appears, you can sort posts by adding the arguments: ```hot```, ```top```, ```new``` to the script.

Example:
```
python change_wallpaper_reddit.py --sort top
```

NSFW images are disabled by default, to enable them add ```--nsfw```.

On OS X, you can specify display number with option ```--display```. Use 0 for all display (default), 1 for main display and so on.

To change default location where image will be saved, use ```--output folder/subfolder```.

Running on startup
=======
Ubuntu
------
To make managment of the script simple, we can accomplish this using built-in Startup Applications.

![Startup Applications](http://i.imgur.com/NDFmFd9.png)


Click on Add.

![Add new startup command](http://i.imgur.com/uFqQ8ky.png)

Note: you can use ```--subreddit``` and ```--time``` arguments here aswell.


Windows
------
We will be using Task Scheduler for this. You can find it in Windows search.
Once you open it, click on ```Create Basic Task```
Follow the procedure.

![Procedure](http://i.imgur.com/1uZMpyc.png)

![Procedure](http://i.imgur.com/3ApvF6W.png)

![Procedure](http://i.imgur.com/fPdwcyg.png)

![Procedure](http://i.imgur.com/zOCCfQI.png)

In ```Add arguments``` field type the location of the script. Example

```
"D:\change_wallpaper_reddit.py"
```

or

```
"D:\change_wallpaper_reddit.py" --subreddit art --time week
```

Running every minute or hour
=======

Look into using cronjobs on Linux or Task Scheduler on Windows for performing this.

Configuration file
=======

Instead of writing arguments every time you run the script, you can also use configuration file which should be located at ```~/.config/change_wallpaper_reddit.rc```.

Example of configuration file:

```
subreddit=art
time=day
sort=top
```
