'''
Created on Sep 2, 2012

@author: TheZen
'''
import unittest
import main.automategoes as ag
import datetime
import urllib2


class TestGoesProperties(unittest.TestCase):

    filename = 'automategoes.cfg'
    def setUp(self):
        self.properties = ag.AutomateGoesProperties(self.filename)


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
    self.props = ag.LoggerProperties(self.filename)

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
    self.props = ag.PropertiesJson(self.filename)
  
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
    return ag.GoesLinkParser(page,target)
  def setUp(self):
    unittest.TestCase.setUp(self)
     
  def testFind(self):
    d = datetime.date(2012,8,9)
    url = 'http://academic.uprm.edu/hdc/GOES-PRWEB_RESULTS/actual_vapor_pressure/'
    page = urllib2.urlopen(url)
    target = r'.*201208\d\d'
    parser = self.construct(page,target)
    result = parser.find()
    test = 'actual_vapor_pressure20120801.jpg'
     
    self.assertEqual(result, test, result)
    print result
     

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
