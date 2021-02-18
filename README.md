# RSSNews  
`RSSNews` is a personal Python RSS news aggregator.  
  
![Python version](https://img.shields.io/pypi/pyversions/dominate.svg?style=flat)  

## How To Use  
If not already installed, you'll need to add the following libraries:
> pip install feedparser  
> pip install json  
> pip install dominate  

The folder contains the file _News RSS Feeds.json_ which is used to select which RSS feeds you wish to monitor. It should be pretty obvious how it works.  
  
You can add or remove feeds under the _news_ section.  
The _topics_ section will highlight stories containing any keywords you add here.  
The _ignore_ section will ignore stories which contain matching keywords. This is useful for hiding story topics (sick of hearing about Trump? Well, here's where you block him (just like Twitter did!)) which will then not appear in your feed.  
  
Now, run the python script _RSS News Reader.py_ and then open _gaggle news.html_ in your favourite browser (you're not still using IE, are you?). News stories for the past 72 hours will be listed as links.  
  

## Why?  
Fed up with the drivel the drivel that certain online companies provide (and the tracking, let's not forget the tracking!), I decided to make my own news aggregator.

