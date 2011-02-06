# -*- coding: utf-8 -*-
'''
Created on Dec 26, 2010

@author: iRoot
'''
from story.Story import Story 
from http.HTTPHandler import HTTPHandler
import hashlib
from story.BeautifulSoup import BeautifulSoup
import sys
import pickle
import os.path

class Smartfiction(Story):
    
    __feedsURL = "http://feeds.feedburner.com/smartfiction"
    __feedsHashStorage = "tmp/SmartfictionFeedsHash.tmp"
    
    def __init__(self, hashStorage='tmp/SmartfictionLastStoryHash.tmp'):
        story = self.fetchLastStory(hashStorage)
        if not story:
            sys.exit(0)
        else:
            Story.__init__(self, hashStorage, story['author'], story['title'], story['url'], story['hash'], "")
        
    def fetchLastStory(self, hashStorage):
        feed = HTTPHandler("tmp/SmartfictionCookie.tmp")
        feedXML = feed.getContent(self.__feedsURL)
        
        feedUpdated = self.feedsUpdateStatus(feedXML)
        if feedUpdated:
            soup = BeautifulSoup(feedXML)
            storyAttrs = soup.rss.channel.item.title.renderContents()
            storyAttrsList = storyAttrs.split(". ")
            
            title = storyAttrsList[0]
            author = storyAttrsList[1]
            storyHash = hashlib.new("ripemd160")
            storyHash.update(storyAttrs)
            hash = storyHash.hexdigest()
            url = soup.rss.channel.item.comments.renderContents()
            
            return {'author': author, 'title': title, 'url': url, 'hash': hash}
        else:
            return False
        
    def addStoryToBookmate(self):
        lastUploadedStoryHash = self.getLastUploadedStoryHash()

        if lastUploadedStoryHash == self.hash:
            return False
        else:
            bookmateRequest = HTTPHandler("tmp/SmartfictionCookie.tmp")
#            http://smartfiction.ru/prose/bride_and_tiger/#comments
            splitedUrl = self.url.split('#',1)
            
            uploadStatus = bookmateRequest.linkStoryToBookmate(splitedUrl[0])
            
            if uploadStatus:
                if self.bookStoredOnBookmate():
                    self.saveUploadedStoryHash()
                    self.saveFeedHash()
                    return True
                else:
                    return False
            else:
                return False
    
    def feedsUpdateStatus(self, feedXML):
        '''Compare stored feed hash with just obtained and return feeds update status.'''
        feedsHash = hashlib.new("ripemd160")
        feedsHash.update(feedXML)
        self.feedsHash = feedsHash.hexdigest()
        
        if self.getLastFeedHash() == self.feedsHash:
            return False
        else:
            return True
        
    def getLastFeedHash(self):
        '''Get last feeds hash from file and write it into class variable.'''    
        if os.path.isfile(self.__feedsHashStorage):
            try:
                storage = file(self.__feedsHashStorage, 'r')
                lastFeedsHash = pickle.load(storage)
                storage.close()
                del storage
                return lastFeedsHash
            except:
                sys.exit( 'READ ERR: Unable to read feeds hash from file %s' % (self.__feedsHashStorage) )
        else:
            return ''
    
    def saveFeedHash(self):
        '''Save last feed hash to file.'''
        try:
            storage = file(self.__feedsHashStorage, 'w')
            pickle.dump(self.feedsHash, storage, protocol=pickle.HIGHEST_PROTOCOL)
            storage.close()
            del storage
            return True
        except:
            print 'WRITE ERR: Unable to write feeds hash in file %s.' % (self.__feedsHashStorage)
            return False
