# -*- coding: utf-8 -*-
'''
Created on Dec 23, 2010

@author: iRoot
'''
import pickle
import os.path
from http.HTTPHandler import HTTPHandler
import sys

class Story(object):   
    
    def __init__(self, lastStoryHashStorage, author, title, url, hash, content):
        self.lastStoryHashStorage = lastStoryHashStorage
        self.getLastUploadedStoryHash()
        self.author = author
        self.title = title
        self.url = url
        self.hash = hash
        self.content = content
        
    def saveUploadedStoryHash(self):
        try:
            storage = file(self.lastStoryHashStorage, 'w')
            pickle.dump(self.hash, storage, protocol=pickle.HIGHEST_PROTOCOL)
            storage.close()
            del storage
        except:
            print 'WRITE ERR: Unable to write last uploaded story hash in file %s.' % (self.lastStoryHashStorage)
            
    def getLastUploadedStoryHash(self):
        if os.path.isfile(self.lastStoryHashStorage):
            try:
                storage = file(self.lastStoryHashStorage, 'r')
                lastUploadedStoryHash = pickle.load(storage)
                storage.close()
                del storage
                return lastUploadedStoryHash
            except:
                print 'READ ERR: Unable to read last uploaded story hash from file %s' % (self.lastStoryHashStorage)
        else:
            return ""

    def bookStoredOnBookmate(self):
        req = HTTPHandler("BookmateAPICookie")
        booksList = req.getBookmateBooks()
        for book in booksList:
            if book['document']['title'].encode('utf-8') == self.title and book['document']['authors'].encode('utf-8') == self.author:
                return True
        return False
    '''
    http://api.bookmate.com/a/3/u/speechkey/token.json
    loginData = { "password" : "mersedes", "key" : "I4jD4oZupzx9HIG0xpzeKEk4nZNZT2HfVbU3w7d38L5g9zpNyicJXw9pfeKTfm0S", "uuid" : "d8c21d6b7de61aec2411f2f9b6cedc5b196e18cb", "identity" : "iPhone" }
    token = handle.read()
    tokenDict = json.loads(token)
    realToken = tokenDict['token']
    >>> bookmateHeaders
{'Accept-Language': 'en-us', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'App-User-Agent': 'iPhone/1,1 iPhoneOS/3.1.3 Bookmate/2.0', 'Accept': '*/*', 'User-Agent': ' ', 'Host': 'api.bookmate.com'}
    req = urllib2.Request("http://api.bookmate.com/a/3/l/delta.json?updated_ge=0&auth_token=rFbZmNGXM39FsR1fGnP1qLL753FH6k0t", None, bookmateHeaders)
    handle = urllib2.urlopen(req)
    handle.headers['content-encoding'] << gzip
    compressedData = handle.read()
    compressedstream = StringIO.StringIO(compressedData)
    import gzip
    gzipper = gzip.GzipFile(fileobj=compressedstream)
    data = gzipper.read()
    import json
    parsedData = json.loads(data)
    lcs = parsedData['results']['lcs']
    lcs[0]['document']['title']
    lcs[0]['document']['authors']   '''     
