# -*- coding: utf-8 -*-
'''
Created on Dec 26, 2010

@author: iRoot
'''
import urllib2
import hashlib
from BeautifulSoup import BeautifulSoup

url = 'http://feeds.feedburner.com/smartfiction'
data = None
header = {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

Request = urllib2.Request
req = Request(url, data, header)
handle = urllib2.urlopen(req)

feedXML = handle.read()
print hashlib.md5(feedXML).hexdigest()
soup = BeautifulSoup(feedXML)
print soup.rss.channel.link.renderContents()
#print soup.find("img", {"alt" : "bookmate"}).parent
#e42340c847962ff7fefcf5efe3bbdec3