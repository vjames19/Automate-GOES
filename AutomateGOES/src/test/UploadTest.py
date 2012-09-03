'''
Created on Sep 3, 2012

@author: TheZen
'''
import unittest
from main.automategoes import GoesUploader
from main.properties import PropertiesManager,AutomateGoesProperties,LoggerProperties
import logging.config
logconfig = LoggerProperties('log.cfg')
logging.config.dictConfig(logconfig)

class TestGoesUploader(unittest.TestCase):

  ftpprops = PropertiesManager(AutomateGoesProperties('automategoes.cfg')).get_ftp()
  def setUp(self):
    self.uploader = GoesUploader(self.ftpprops)
  
  def test_upload(self):
    u = self.uploader
    u.upload('*','','actual_ET')
    
    


  def tearDown(self):
    self.uploader.close()
    self.uploader = None
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()