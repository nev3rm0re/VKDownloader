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
        except cookielib.LoadError:
            print "no cookies found"
            
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
            self.loginToVK()
            self.cj.save()
        
        print self.getAudio()
        
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
        self.opener.open('http://vkontakte.ru/audio')
        
        self.opener.addheaders = [('X-Requested-With', ('XMLHttpRequest')), ('Referer', ('http://vkontakte.ru/audio'))]
        
        post_data = urllib.urlencode({
          'act' : 'load_audios_silent',
          'al'  : '1',
          'edit': '0',
          'gid' : '0',
          'id'  : '5199746'})
        
        response = self.opener.open('http://vkontakte.ru/audio', post_data)
        
        response_html   = ''.join(response.readlines())
        
        response_html   = response_html.decode('windows-1251');
        
        response_splitted = response_html.split('<!>')
        
        response_html = response_splitted[-2]
        
        response_html = re.sub('([\[\],]?)\'(,?)', '\\1"\\2', response_html)
        
        f = codecs.open('/tmp/login_dump.txt', mode='w', encoding='utf-8')
        f.write(response_html)
        f.close()
        
        json_decoded    = json.loads(response_html)
        h = HTMLParser.HTMLParser()
        
        urls = []
        
        for a in json_decoded["all"]:
            filename = cleanUpForFilename(h.unescape(" - ".join(a[5:7])))

            if a[8] == "21065591":
                if len(filename) > 100:
                    filename = filename[:125]
                
                urls.append((a[2], filename + ".mp3"))
            
        downloader = Downloader(urls)
        downloader.startDownload()
        
        
config = ConfigParser.ConfigParser()
config.read("config.ini")
vk_username = config.get('login details', 'login')
vk_password = config.get('login details', 'password')

f = WebGamePlayer(vk_username,vk_password)