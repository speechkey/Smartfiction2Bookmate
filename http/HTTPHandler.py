'''
Created on Dec 23, 2010

@author: iRoot
'''
import os.path
import urllib
import urllib2
import sys

class HTTPHandler(object):
    '''
    classdocs
    '''
    __bookmatePassword = "mersedes"
    __bookmateHeaders = {'Accept-Language': 'en-us',
                         'Accept-Encoding': 'gzip, deflate',
                         'Connection': 'keep-alive',
                         'App-User-Agent': 'iPhone/1,1 iPhoneOS/3.1.3 Bookmate/2.0',
                         'Accept': '*/*',
                         'User-Agent': ' ',
                         'Host': 'api.bookmate.com'}
    
    __browserHeaders = {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    def __init__(self, cookieFile):
        self.__cookieFile = cookieFile
        
    def sendRequest(self, url, useCookie, returnContent, uploadFile, data, headers):
        if useCookie:
            import cookielib
            cj = cookielib.LWPCookieJar()
            
            if cj != None:                                  # now we have to install our CookieJar so that it is used as the default CookieProcessor in the default opener handler
                if os.path.isfile(self.__cookieFile):
                    cj.load(self.__cookieFile)
                    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                    urllib2.install_opener(opener)   
        if data:
            txdata = urllib.urlencode(data)
        else:
            txdata = None
        try:
            req = urllib2.Request(url, txdata, headers)            # create a request object
            handle = urllib2.urlopen(req)
            if useCookie:
                cj.save(self.__cookieFile)
            if returnContent:
                return {'content' : handle.read(),
                        'redirectedTo' : handle.url }
            else:
                return {'redirectedTo' : handle.url}
        except IOError, e:
            print 'NETWORK ERR: We failed to open "%s".' % url
            if hasattr(e, 'code'):
                print '             Returned error code - %s.' % e.code
            else:
                print '             Here are the headers of the page :'
                print handle.info()                             # handle.read() returns the page, handle.geturl() returns the true url of the page fetched (in case urlopen has followed any redirects, which it sometimes does)

    #If login fails redirect to http://bookmate.ru/login, otherwise http://bookmate.ru      
    def bookmateLogin(self, login = "speechkey", password = "mersedes"):
        url = 'http://www.bookmate.ru/login'
        logindata = {'user_session[login]' : login, 
                     'user_session[password]' : password,
                     'user_session[remember_me]' : '0',
                     'user_session[remember_me]' : '1'}
        info = self.sendRequest(url, True, True, False, logindata, self.__browserHeaders)

        if info['redirectedTo'] == 'http://bookmate.ru/login':
            return False
        else:
            return True
    
    def __loginToBookmateAPI(self):
        import json
        url = 'http://api.bookmate.com/a/3/u/speechkey/token.json'
        loginData = { "password" : self.__bookmatePassword,
                     "key" : "I4jD4oZupzx9HIG0xpzeKEk4nZNZT2HfVbU3w7d38L5g9zpNyicJXw9pfeKTfm0S",
                      "uuid" : "d8c21d6b7de61aec2411f2f9b6cedc5b196e18cb", "identity" : "iPhone" }
    
        resp = self.sendRequest(url, False, True, False, loginData, self.__bookmateHeaders)
        
        respDict = json.loads(resp['content'])
        
        if respDict.has_key("token"):
            return respDict['token']
        else:
            if respDict.has_key('error'):
                sys.exit("ERROR" + respDict['error']['code'] +": Fail getting Bookmate API Token. " + unicode (respDict['error']['message']) + ".")
            else:
                sys.exit("ERROR. Fail getting Bookmate API Token. No error information found.")
    
    def getBookmateBooks(self):
        import StringIO
        import gzip
        import json
        token = self.__loginToBookmateAPI()
        url = "http://api.bookmate.com/a/3/l/delta.json?updated_ge=0&auth_token=" + token
        resp = self.sendRequest(url, False, True, False, False, self.__bookmateHeaders)
        compressedStream = StringIO.StringIO(resp['content'])
        gzipper = gzip.GzipFile(fileobj=compressedStream)
        data = gzipper.read()
        parsedData = json.loads(data)
        if parsedData.has_key('results'):
            return parsedData['results']['lcs']
        else:
            sys.exit("ERROR. Fail getting books information from Bookmate API.")
        
    def getContent(self, url):
        responce = self.sendRequest(url, False, True, False, False, self.__browserHeaders)
        return responce['content']
    
    def linkStoryToBookmate(self, link):
        if not self.checkLogin():
            loginstatus = self.bookmateLogin()
            
        url = 'http://www.bookmate.ru/upload'
        uploaddata = {'import[link]' : 'http://convert.smartfiction.ru/?uri=' + link +'&format=fb2',
              'import[ref]' : link,
              'since' : '1292979292'}

        info = self.sendRequest(url, True, False, False, uploaddata, self.__browserHeaders)
        if info['redirectedTo'] == 'http://bookmate.ru/login':
            return False
        else:
            return True
    
    #import[file], since
    def uploadStoryToBookmate(self):
        pass
    
    def getMyBooks(self):
        pass
    
    def checkLogin(self):
        return False

    
