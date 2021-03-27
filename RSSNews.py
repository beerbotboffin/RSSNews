'''
    RSS News Reader 2.0
    Get the news that's (hopefully) worth reading!
    Version 2.0 presents the links in a (hopefully) better way
    Go on, Google - leave the Australian news market. I dare you!

    Shane Frost
    20210218 From the original Aug 2020 version

    CHANGELOG
    -----------
    20210219 v2.0
        Changed the method for organising / sorting stories.
        Changed some div tags for the css.
        Added news organisation as suffix to story
    20210220
        Added page icon
    
    
    TODO
    -----------
    download the content and display it in my own format so that we don't have cookies everywhere.

'''

import feedparser
import json
import datetime
import csv
import dominate
from dominate.tags import *

def cls(): # Used only for development
    print("\n" * 100)

def CleanJSONText(jsonString):
    unwantedText = ["[{'rss': '","'}","'}]"," {'rss': '","]","[{'url': '","{'keyword': '","[","'}]","{'rss': '"]
    for i in unwantedText:
        jsonString = jsonString.replace(i,"").strip()
    return jsonString

def GetRSSDataFromJSONfile():
    # Get the RSS data from the JSON file
    with open('News RSS Feeds.json', 'r') as myfile:
        data=myfile.read()
        obj = json.loads(data)
    return obj

def ConvertDateTime(inputDateTimeString):
    returnDateTimeString = inputDateTimeString[12:16] + '-' # YEAR
    for monthAbbreviation in monthNameAbbreviations: # MONTH
        if(inputDateTimeString[8:11].lower() == monthAbbreviation):
            returnDateTimeString += ('00' + str(monthNameAbbreviations.index(monthAbbreviation)+1))[-2:] + '-'
    returnDateTimeString += ('00' + inputDateTimeString[5:7])[-2:] + ' ' # DAY
    returnDateTimeString += inputDateTimeString[17:25] # hh:mm:ss
    return returnDateTimeString

def DatetimeDifferenceInHours(publishedDate):
    format = "%Y-%m-%d %H:%M:%S"
    dt_object = datetime.datetime.strptime(publishedDate, format) # Convert string to datetime
    DateTimeDifference = str(datetime.datetime.now() - dt_object) # get the difference between the two

    try:
        if str(DateTimeDifference).find('day') != -1: # Current day, nothing to find.
            if str(DateTimeDifference).find('day,') == -1:
                try:
                    DateTimeDifferenceHours = int(DateTimeDifference[:DateTimeDifference.find(',')].replace(' days',''))*24 #Days difference in hours
                except:
                    print('Error with ' + publishedDate + ' | DateTimeDifference is ' + DateTimeDifference)
            else:
                if str(DateTimeDifference).find('-1 day,') == 0:
                    DateTimeDifferenceHours = 0
                else:
                    DateTimeDifferenceHours = int(DateTimeDifference[:DateTimeDifference.find(',')].replace(' days','').replace(' day',''))*24 #Days difference in hours
                    DateTimeDifferenceHours += int(DateTimeDifference[DateTimeDifference.find(', ')+2:DateTimeDifference.find(':')]) # add the balance of the hours
        else:
            DateTimeDifferenceHours = int(DateTimeDifference[:DateTimeDifference.find(':')]) # add the hours
        return DateTimeDifferenceHours
    except:
        print('Def Error with ' + publishedDate)
    
    

monthNameAbbreviations = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
NewsStories = []
FeaturedNewsStories = []

#cls() # Clear the IDLE screen (mainly for debugging you know)
RSSData = GetRSSDataFromJSONfile()

# Process each of the news sources
for RSSfeed in str(RSSData['news']).split(','):
    NewsFeed = feedparser.parse(CleanJSONText(RSSfeed))

    # Process all of the entries for the current RSS Feed
    for i in range(len(NewsFeed.entries)-1):
        NewsItem = []
        entry = NewsFeed.entries[i]
        keeper = True
        relevance = 0
        
        # Remove any article which contain keywords we don't want.
        for ignore in str(RSSData['ignore']).split(','): 
            if entry['title'].lower().find(CleanJSONText(ignore.lower())) != -1:
                keeper = False
                
        for topicRank in str(RSSData['topics']).split(','):
            if entry['title'].lower().find(CleanJSONText(topicRank)) != -1:
                if DatetimeDifferenceInHours(ConvertDateTime(entry['published'])) < 24:
                    NewsItem.append(entry['published'])
                    Agency = CleanJSONText(RSSfeed)
                    NewsItem.append(Agency[Agency.find('www.')+4:Agency.find('/',Agency.find('www.')+4)])
                    NewsItem.append(relevance)
                    NewsItem.append(DatetimeDifferenceInHours(ConvertDateTime(entry['published'])))
                    NewsItem.append(entry['title'])
                    NewsItem.append(entry['link'])                
                    FeaturedNewsStories.append(NewsItem)
                    keeper = False
        
        if keeper == True:
            if DatetimeDifferenceInHours(ConvertDateTime(entry['published'])) is None:
                DatetimeDifferenceInHours = 0
            else:
                if DatetimeDifferenceInHours(ConvertDateTime(entry['published'])) < 24:
                    NewsItem.append(entry['published'])
                    Agency = CleanJSONText(RSSfeed)
                    NewsItem.append(Agency[Agency.find('www.')+4:Agency.find('/',Agency.find('www.')+4)])
                    NewsItem.append(relevance)
                    NewsItem.append(DatetimeDifferenceInHours(ConvertDateTime(entry['published'])))
                    NewsItem.append(entry['title'])
                    NewsItem.append(entry['link'])
                    NewsStories.append(NewsItem)


# Sort the articles chronologically
SortedNewsStories = sorted(NewsStories, reverse=True)
SortedFeaturedNewsStories = sorted(FeaturedNewsStories, reverse=True)

######################################################
# Output to csv file
######################################################
##csvHeadings = ['publish date','News Agency','relevance','hours since published','title','url']
##wtr = csv.writer(open('news.csv', 'w'), delimiter=',', lineterminator='\n')
##wtr.writerow(csvHeadings)
##for NewsItem in SortedNewsStories:
##    wtr.writerow(NewsItem)


######################################################
# Create HTML
######################################################
doc = dominate.document(title='Gaggle News')

with doc.head:
    link(rel='stylesheet', href='https://www.w3schools.com/w3css/4/w3.css')
    link(rel='icon', href='icon.png')
    script(type='text/javascript', src='script.js')

with doc:
    # Add the logo
    with div():
        attr(cls='body')
        img(src='logo.png')
        attr(cls='w3-text-grey')
        a('Updated: ' + str(datetime.datetime.now())[:16])
        
    # Only create the 'Articles of Interest' section if there's something to show
    if len(FeaturedNewsStories) > 0: 
        with div(id='header').add(ul()):
            with div():
                attr(cls='w3-panel w3-round-large w3-red')
                p("Articles of Interest")
            for NewsItem in SortedFeaturedNewsStories: # Test for articles of interest.
                li(a(NewsItem[4], href=NewsItem[5]) ,  ' (' + str(NewsItem[1]) , ')' )

    # Now add the ordinary articles.
    with div(id='header').add(ul()): 
        with div():
            attr(cls='w3-panel w3-round-large w3-blue')
            p("Rest of the news")        
        for NewsItem in SortedNewsStories:
            #if NewsItem[1] == 0:
            li(a(NewsItem[4], href=NewsItem[5].replace('&amp;','').replace('#039;','\'')) ,  ' (' + str(NewsItem[1]) , ')' )
            
    with div():
        attr(cls='w3-text-blue')
        p("You don't need google for news.")

with open('gaggle news.html', 'w', encoding="utf-8") as f:
    for line in doc:
        try:
            f.write(str(line).replace('&amp;#039;',''''''))
        except:
            f.write('error' )
            continue



#.replace("&#039;","'")




















