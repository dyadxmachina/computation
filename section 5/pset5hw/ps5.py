# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import os
#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):

    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

    def constructor(self):
        '''
            Stores guid, title, description, link and pubdate of a feed into a dictionary for the later use
            Returns: feed dictionary 
                - type: dict
        '''
        feed_dict = {}
        feed_dict['guid'] = self.get_guid
        feed_dict['title'] = self.get_title
        feed_dict['description'] = self.get_description
        feed_dict['link'] = self.get_link
        feed_dict['pubdate'] = self.get_pubdate

        return feed_dict


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhaseTrigger(Trigger):
    def __init__(self, phase):
        self.phase = phase
    def is_phase_in(self, input_string):
        '''
            Takes in one string argument text, returns True if the whole phrase is presented in text, False other wise
            Return: True or False
                - type: Boolean val

            Requirement: 
                - A pharse is one or more works sperated by a single space between words
                - The trigger will fire only when each word in the phrase is present in its 
                entirety and appears consecutively in the text, sperated by spaces or punction
                - the trigger should not be case sensitive 
                - split/replace/join methods will be certainly helpful
        '''
        lower_phase = self.phase.lower()
        phase_list = lower_phase.split(' ')
        print('CLEAN PHASE: ', phase_list)
        join_phase =  ''.join(phase_list)
        lower_string = input_string.lower()
        exclude = list(string.punctuation)
        # nopunc_string = lower_string.replace(str([i for i in exclude]), ' ')
        # print('NO PUNC STRING: ', nopunc_string)
        clean_string = ''.join(charac if charac not in exclude else ' ' for charac in lower_string)
        string_list = clean_string.split(' ')
        print('CLEAN TEXT: ', string_list)
        join_text = ''.join(string_list)
        if set(phase_list).issubset(set(string_list)) and join_phase in join_text: 
            print('True')
            return True
        else: 
            print('False')
            return False 
   


            


# Problem 3
class TitleTrigger(PhaseTrigger):
    def __init__(self, phase):
        self.phase = phase

    def check_title(self, story):
        text = story.get_title()
        print('INPUT TEXT: ', text)
        return self.is_phase_in(text)
    def evaluate(self, story):
        return self.check_title(story)


# Problem 4
class DescriptionTrigger(PhaseTrigger):
    def __init__(self, phase):
        self.phase = phase
    def check_description(self, story):
        descrip = story.get_description()
        return self.is_phase_in(descrip)
    def evaluate(self, story):
        return self.check_description(story)

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

    def __init__(self,time):
        self.time = datetime.strptime(time, '%d %b %Y %H:%M:%S') 

    def convert_time(self, story_time):
        # conv_time = story_time.replace(tzinfo=pytz.timezone("EST"))
        conv_time = story_time.replace(tzinfo=None)
        return conv_time
        # if self.time == conv_time: 
        #     return True
        # else: 
        #     return False


# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, trigger_time):
        self.time = datetime.strptime(trigger_time, '%d %b %Y %H:%M:%S') 
    def beforetrigger(self, story):
        story_time = self.convert_time(story.get_pubdate())
        print('STORY TIME: ', story_time)
        print('TRIGGER TIME: ', self.time)
        return story_time < self.time
        #     return True
        # else: 
        #     return False
    def evaluate(self, story):
        return self.beforetrigger(story)


class AfterTrigger(TimeTrigger):
    def __init__(self, trigger_time):
        self.time = datetime.strptime(trigger_time, '%d %b %Y %H:%M:%S') 
    def aftertrigger(self, story):
        story_time = self.convert_time(story.get_pubdate())
        return story_time > self.time 
        #     return True
        # else: 
        #     return False
    def evaluate(self, story):
        return self.aftertrigger(story)


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    def invert_trigger(self, story):
        return not self.trigger.evaluate(story)
    def evaluate(self, story):
        return self.invert_trigger(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def trigger_both(self, story):
        trig_1 = self.trigger1.evaluate(story)
        trig_2 = self.trigger2.evaluate(story)
        return trig_1 & trig_2
    def evaluate(self, story):
        return self.trigger_both(story)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def trigger_both(self, story):
        trig_1 = self.trigger1.evaluate(story)
        trig_2 = self.trigger2.evaluate(story)
        return trig_1 | trig_2
    def evaluate(self, story):
        return self.trigger_both(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    fire_stories = []
    for story in stories: 
        for trigger in triggerlist:
            if trigger.evaluate(story):
                fire_stories.append(story)
    return fire_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    trig_map = {'DESCRIPTION':DescriptionTrigger,
                'TITLE': TitleTrigger,
                'AFTER': AfterTrigger,
                'BEFORE': BeforeTrigger,
                'NOT': NotTrigger,
                'AND': AndTrigger,
                'OR': OrTrigger}
    config_trigs = {}
    triggers = []
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    for line in lines: 
        eles = line.split(',')
        trig_name = eles[0]
        
        if trig_name != 'ADD':
            args = eles[2:]
            if trig_name[1] in trig_map.keys():
                config_trigs[trig_name] = trig_map[trig_name[1]](str(arg) for arg in args)
            else:
                raise ValueError
        else: 
            triggers.append(config_trigs[tg] for tg in eles[1:])

    print(lines) # for now, print it so you see what it contains!
    return triggers


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    cwd = os.getcwd()
    path = os.path.join(cwd, 'section 5/pset5hw/hw.txt')
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config(path)
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            # print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

