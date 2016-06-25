# Daily Reddit Wallpaper (on startup)
This script changes your wallpaper to most upvoted image of the day on /r/wallpapers or from any other subreddit.


**Run it on startup for new wallpaper on every session.**

*Supported: Linux (GNOME, KDE, MATE), Windows and OS X*

Dependencies
=======
Make sure you have Python installed and PATH variable set.

Ubuntu
------
If you don't have ```pip ``` for Python:
```
sudo apt-get install python-pip
```

You will need modules ```requests``` and ```praw``` installed, which can be done running following commands:

```
pip install requests
pip install praw
```

Windows
------
Follow [this guide](https://pip.pypa.io/en/stable/installing/) to install  ```pip```  and configure PATH variable.
The rest is the same.

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

If you don't want to change your wallpaper daily, you can use newest, hourly, weekly, monthly or yearly wallpaper too by adding one of the following arguments: ```new```, ```hour```, ```week```, ```month```, ```year``` to the script.

Example:
```
python /home/silvio/Scripts/change_wallpaper_reddit.py --time week 
```

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

Look into using cronjobs on Linux for performing this.
