'''
Created on Aug 25, 2012

@author: vjames19
'''

import urllib
import urllib2
import os

def check_url(url):
    try:
        urllib2.urlopen(url)
        return True
    except:
        return False

def wget(url, todir, outputFileName):
    pass

def wput(ftpurl, filename):
    pass



