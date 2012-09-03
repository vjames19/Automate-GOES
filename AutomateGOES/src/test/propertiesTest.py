'''
Created on Sep 2, 2012

@author: TheZen
'''
import datetime
import logging
import logging.config
import unittest
import urllib2
from main.properties import *
from main.automategoes import GoesLinkParser

logconfig = LoggerProperties('log.cfg')
logging.config.dictConfig(logconfig)


class TestGoesProperties(unittest.TestCase):

    filename = 'automategoes.cfg'
    def setUp(self):
        self.properties = AutomateGoesProperties(self.filename)


    def tearDown(self):
        self.properties.clear()
        


    def test_getEmail(self):
      email = self.properties.getEmail()
      keys = ['from', 'to', 'password']      
      for key in keys:
        self.assertTrue(key in email)
        
    def test_getVariables(self):
      variables = self.properties.getVariables()
      print variables
      self.assertTrue(len(variables) == 25)
      
class TestLoggerProperties(unittest.TestCase):
  filename = 'log.cfg'

  def setUp(self):
    self.props = LoggerProperties(self.filename)

  def tearDown(self):
    self.props.clear()
    
  def testFileHandler(self):
    import json
    t = datetime.date.today()
    config = json.load(open(self.filename))
    test = config['handlers']['file']['filename']
    test = t.strftime(test)
    
    self.assertTrue(test == self.props['handlers']['file']['filename'])
    print test
    

class TestPropertiesJson(unittest.TestCase):
  
  filename = 'automategoes.cfg'
  def setUp(self):
    self.props = PropertiesJson(self.filename)
  
  def testIsDict(self):
    props = self.props
    self.assertTrue(props.isDict('email') == True)
    self.assertTrue(props.isDict('variables') == False)
  
  def testIsList(self):
    props = self.props
    self.assertTrue(props.isList('email') == False)
    self.assertTrue(props.isList('variables') == True)    
    
    
     
class TestGoesLinkParser(unittest.TestCase):   
   
  def construct(self,page,target):
    return GoesLinkParser(page,target)
  def setUp(self):
    unittest.TestCase.setUp(self)
     
  def testFind(self):
    url = 'http://academic.uprm.edu/hdc/GOES-PRWEB_RESULTS/actual_vapor_pressure/'
    page = urllib2.urlopen(url)
    target = r'.*201208\d\d'
    parser = self.construct(page,target)
    result = parser.find()
    test = 'actual_vapor_pressure20120801.jpg'
     
    self.assertEqual(result, test, result)
    print result
    

class TestPropertiesManager(unittest.TestCase):

  def setUp(self):
    self.props = AutomateGoesProperties('automategoes.cfg')
    self.man = PropertiesManager(self.props)
  
  def generalTest(self,original, test):
    join = lambda s: 'get_'+s
    call = lambda obj, attr: getattr(obj,attr)()
    
    for key in original.keys():
      print original[key],call(test,join(key)),key
      self.assertEqual(original[key],call(test,join(key)),key)
    
    
  def test_getFtp(self):
    original = self.props.getFtp()
    test = self.man.get_ftp()
    self.generalTest(original, test)
    
    

  def test_getEmail(self):
    original = self.props.getEmail()
    test = self.man.get_email()
    self.generalTest(original, test)
    
  def test_getDownload(self):
    original = self.props.getDownload()
    test = self.man.get_download()
    o = original.pop('downloads')
    t = test.get_downloads()
    self.generalTest(original, test)
    
    self.assertEqual(len(o), len(t))
    for i in xrange(0,len(t)):
      d = t[i].__dict__
      self.verifyDict(o[i], d)
    
      
  def verifyDict(self,o,t):
    for key in o:
      self.assertEqual(o[key],t[key])
       
  def test_getVariables(self):
    self.assertEqual(self.props.getVariables(), self.man.get_variables())
    
  def test_getDegrib(self):
    pass
  def test_getFinished(self):
    original = self.props.getFinished()
    test = self.man.get_finished()
    self.generalTest(original, test)
  def test_getGeneral(self):
    original = self.props.getGeneral()
    test = self.man.get_general()
    
    self.assertEqual(original['goesdir'], test['goesdir'])

    
    
    
  
    
    
     

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']

    print 'before'
    unittest.main()
    
