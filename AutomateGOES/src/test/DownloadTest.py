'''
Created on Sep 3, 2012

@author: TheZen
'''
import unittest
import os
import logging.config
from main.properties import *
from main.automategoes import GoesDownloader
import datetime

logconfig = LoggerProperties('log.cfg')
logging.config.dictConfig(logconfig)


class TestGoesDownloader(unittest.TestCase):
  filename = 'automategoes.cfg'
  props = PropertiesManager(AutomateGoesProperties(filename)).get_download()
  def setUp(self):
    self.downloader = GoesDownloader(self.props, datetime.date(2012,8,9), 'downloads')
    
  def testFindIterating(self):
    d = self.downloader
    name = d.findIterating('http://nomads.ncdc.noaa.gov/data/ndfd/201208/20120809/',
                            'YCAZ98_KWBN_2012080900',44)
    self.assertRegexpMatches(name,'YCAZ98_KWBN_2012080900\d\d' , name)
    
  def testFindIteratingWrong(self):
    d = self.downloader
    name = d.findIterating('http://nomads.ncdc.noaa.gov/data/ndfd/201208/',
                            'YCAZ98_KWBN_2012080900',44)
    self.assertEqual(name, None, name)
    
  def testDownload(self):
    d = self.downloader
    d.download()
    date = d.date
    join = os.path.join
    exists = os.path.exists
    props = self.props
    downloads = props.get_downloads()
    formatter = lambda s,d: d.strftime(s)
    
    for download in downloads:
      output = download.get_outputname()
      output = formatter(output,date)
      self.assertTrue(exists(join(d.todir,output)), download.get_name())
      

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()