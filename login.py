import cookielib
import urllib
import urllib2
import json
import codecs
import re
import ConfigParser

import string
import unicodedata
from  download import *

import HTMLParser

def cleanUpForFilename(string):
    filename = re.sub('[\/\\\:\*\?\"\<\>\|]', '', string);
    filename = re.sub(' +', ' ', filename)
    return filename

def fix_vk_json(string):
    return re.sub('([\[\],]?)\'(,?)', '\\1"\\2', string)

class WebGamePlayer(object):
    def __init__(self, login, password):
        """ Start up... """
        self.login = login
        self.password = password
        
        requires_login = True
        
        self.cj = cookielib.LWPCookieJar('vk-cookies.txt')
        try:
            self.cj.load()
            requires_login = False
        except IOError:
            pass
            
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]

        # need this twice - once to set cookies, once to log in...
        if requires_login:
            self.loginToVK()
            self.cj.save()
        
    def loginToVK(self):
        """
        Handle login. This should populate our cookie jar.
        """
        login_data = urllib.urlencode({
            'email' : self.login,
            'pass' : self.password,
        })
        response = self.opener.open("https://login.vk.com/?act=login", login_data)
        return ''.join(response.readlines())
    
    def getAudio(self):
        audio_url = "http://vkontakte.ru/audio"
        
        # extract user_id from response
        response = self.opener.open(audio_url)
        response = ''.join(response.readlines())
        
        matches = re.search('a name="(\d+)_', response)
        user_id = matches.group(1)
        
        self.opener.addheaders = [('X-Requested-With', 'XMLHttpRequest'), ('Referer', audio_url)]
        post_data = urllib.urlencode({
          'act' : 'load_audios_silent',
          'al'  : '1',
          'edit': '0',
          'gid' : '0',
          'id'  : user_id})
        
        
        response = self.opener.open(audio_url, post_data)
        
        response_html   = ''.join(response.readlines())
        response_html   = response_html.decode('windows-1251');
        response_splitted = response_html.split('<!>')
        response_html = response_splitted[-2]
        
        json_decoded = json.loads(fix_vk_json(response_splitted[-1]))
        albums = json_decoded["albums"].values()
            
        index = 0
        
        print "[%d] [%s]" % (1, "*all*")
        
        for index, data in enumerate(albums):
            print "[%d] [%s]" % (index + 2, data["title"])
        
        selected_album = raw_input("Select album from list [1-%d]: " % (int(index) + 2, ))
        
        if selected_album == 1:
            album_id = None
        else:
            album_id = albums[int(selected_album)-2]['id']
            
        response_html = fix_vk_json(response_html)
        
        json_decoded    = json.loads(response_html)
        h = HTMLParser.HTMLParser()
        
        urls = []
        
        for a in json_decoded["all"]:
            filename = cleanUpForFilename(h.unescape(" - ".join(a[5:7])))
            if (album_id == None or a[8] == album_id):
                if len(filename) > 100:
                    filename = filename[:125]
                urls.append((a[2], filename + ".mp3"))
            
        downloader = Downloader(urls)
        print urls
        downloader.startDownload()
        
        
config = ConfigParser.ConfigParser()
read_status = config.read("config.ini")
if len(read_status) == 0:
    from config import *
    (vk_username, vk_password) = ask_for_login()
else: 
    vk_username = config.get('login details', 'username')
    vk_password = config.get('login details', 'password')

f = WebGamePlayer(vk_username,vk_password)
f.getAudio()