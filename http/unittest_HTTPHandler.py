# -*- coding: utf-8 -*-
'''
Created on Dec 29, 2010

@author: iRoot
'''
import unittest
from HTTPHandler import HTTPHandler 

class HTTPHandlerTest(unittest.TestCase):

    def setUp(self):
        self.http = HTTPHandler("UnittestCookie")


    def tearDown(self):
        pass


    def testSimpleRequest(self):
        resp = self.http.sendRequest("http://i/Python/Unittest%20Equipment/XHTML.html", False, True, False, False, self.http.__browserHeaders)
        self.checkXHTMLHash(resp['content'])
    
    def testGetContent(self):
        resp = self.http.getContent("http://i/Python/Unittest%20Equipment/XHTML.html")
        self.checkXHTMLHash(resp)
        
    def checkXHTMLHash(self, resp):
        import hashlib
        resp_hash = hashlib.md5(resp).hexdigest()
        self.failUnlessEqual(resp_hash, "a328fa0c14f6c8c01ddd6f1aa67dd192", msg="Fail processing simple request.")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    