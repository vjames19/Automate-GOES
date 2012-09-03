'''
Created on Sep 3, 2012

@author: TheZen
'''
import unittest
import os
import main.automategoes as ag
import datetime


class TestGoesDownloader(unittest.TestCase):
  filename = 'automategoes.cfg'
  props = ag.AutomateGoesProperties(filename).getDownload()
  def setUp(self):
    self.downloader = ag.GoesDownloader(self.props, datetime.date(2012,8,9), '')
    
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
    exists = lambda path: os.path.exists(path)
    props = self.props
    downloads = props['downloads']
    formatter = lambda s,d: d.strftime(s)
    
    for download in downloads:
      output = download['outputname']
      output = formatter(output,date)
      self.assertTrue(exists(output), download['name'])
      

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()