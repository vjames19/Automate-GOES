'''
Created on Sep 3, 2012

@author: TheZen
'''
import unittest
from main.automategoes import GoesWputUploader
from main.properties import PropertiesManager,AutomateGoesProperties,LoggerProperties
import logging.config
logconfig = LoggerProperties('log.cfg')
logging.config.dictConfig(logconfig)

class TestGoesWputUploader(unittest.TestCase):

  ftpprops = PropertiesManager(AutomateGoesProperties('automategoes.cfg')).get_ftp()
  def setUp(self):
    self.uploader = GoesWputUploader(self.ftpprops)
  
#  def test_upload(self):
#    u = self.uploader
#    u.upload('*','','actual_ET')
    
  def test_multipleUploads(self):
    u = self.uploader
    #variables = ['actual_ET','actual_vapor_pressure']
    variables = ['actual_ET']
    for variable in variables:
      u.upload('*', 'logs',variable)
      
  def tearDown(self):
    self.uploader = None
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()