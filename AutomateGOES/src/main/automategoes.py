'''
Created on Sep 1, 2012

@author: TheZen
'''
import datetime
import logging
import remote
import urlparse
import time
import re
import urllib2
from main.remote import FtpMeta
log= logging.getLogger("main.automategoes")

class PropertiesJson(dict):
  def __init__(self,filename):
    import json
    self.update( json.load(open(filename,'r')))
    
  def isDict(self, key):
    r = self.get(key)
    if r:
      return type(r) == dict
    return False
  
  def isList(self, key):
    r = self.get(key)
    if r:
      return type(r) == list
    return False

class LoggerProperties(PropertiesJson):
  def __init__(self,filename):
    PropertiesJson.__init__(self, filename)
    handlers = self['handlers']
    filehandler = handlers.get('file')
    if filehandler:
      filename = filehandler.get('filename')
      if filename:
        today = datetime.date.today()
        underbar = filename.index('_')
        dot = filename.index('.')
        fileformat = filename[underbar:dot]
        filename = filename[:underbar]+today.strftime(fileformat)+filename[dot:]
        filehandler['filename'] = filename
        
class AutomateGoesProperties(PropertiesJson):
  '''
  AutomateGoesProperties has methods for getting the 
  different properties pertinent to the project, once it loads
  the configuration file
  '''
  def __init__(self,filename):
    PropertiesJson.__init__(self, filename)
  
  def getFtp(self):
    return self['ftp']
  
  def getGeneral(self):
    return self['general']
  
  def getDownload(self):
    return self['download']
  
  def getEmail(self):
    return self['email']
  
  def getFinished(self):
    return self['finished']
  
  def getDegrib(self):
    return self['degrib']
  
  def getVariables(self):
    return self['variables']

    
class GoesDownloader:
  '''
  GoesDownloader is in charge of downloading all the files specified in the downloadConfig dictionary
  
  Each download should have the following properties:
    name - A name for the download 
    remotename - name of the file in the web
    outputname - name for the downloaded file
    dirurl - parent dir of the file
    finditerating - true or false if the file must be found changing the last two digits
    dateoffset - offset from the date specified when constructing this object
  '''
  DIR_URL = 'dirurl'
  REGEX = 'regex'
  NAME = 'name'
  REMOTE_NAME = 'remotename'
  DATE_OFFSET = 'dateoffset'
  TRIES ='tries'
  SECONDS ='seconds'
  DOWNLOADS = 'downloads'
  OUTPUT_NAME='outputname'
  FIND_ITERATING ='finditerating'
  def __init__(self, props, date, todir=''):
    self.wget = remote.WebDownload()
    self.__initializeProps(props)
    self.date = date
    self.todir = todir
    
  def __processRegex(self, remotedir, regex):
    '''
    Used for processing the remotedir(web directory) looking for the supplied regex
    '''
    page = urllib2.urlopen(remotedir)
    parser = GoesLinkParser(page, regex)
    return parser.find()

  def download(self):
    '''
    Processes all the downloads specified in the downloadConfig
    '''
    for download in self.downloads:
      log.info("Starting download process for: "+ download[self.NAME])
      tempDate = self.date + datetime.timedelta(download[self.DATE_OFFSET])
      log.info("Date: "+str(tempDate))
      
      #Format the strings using the corresponding date
      remotedir = self.__formatString(download[self.DIR_URL], tempDate)
      log.info("Remotedir: "+remotedir)
      
      remoteName = self.__formatString(download[self.REMOTE_NAME], tempDate)
      
      #Process regex looking in the web directory for the remote name
#      if download[self.REGEX]:
#        
#        if self.wget.check_url(remotedir):
#          
#          remoteName = waitToAppear(self.tries, self.seconds, self.__processRegex,remotedir, remoteName)
#          if remoteName:
#            log.info("Found the target: "+remoteName)
#          else:
#            log.error("Couldn't find a link for: "+download[self.NAME])
#            continue
#        else:
#          log.error("Remote Directory doesn't exists: "+remotedir)
      if download[self.FIND_ITERATING]:
        remoteName = waitToAppear(self.tries,self.seconds, self.findIterating,remotedir,remoteName )
          
      #Create the absolute url      
      absoluteUrl = urlparse.urljoin(remotedir,remoteName)
      log.info("Absolute Url: "+absoluteUrl)
      
      #Wait for the file to be there, then download it.
      if waitToAppear(self.tries, self.seconds, self.wget.check_url, absoluteUrl):
        log.info("Downloading...")
        outputname = self.__formatString(download[self.OUTPUT_NAME], self.date)
        result = self.wget.wget(absoluteUrl, self.todir,outputname)
        log.info("Downloaded: "+ str(result))
      else:
        log.error("Download error the url doesn't exists")
        continue
        
  def __initializeProps(self, downloadConfig):
    #initializes the downloads list
    self.downloads =  downloadConfig[self.DOWNLOADS]
    self.tries = downloadConfig[self.TRIES]
    self.seconds = downloadConfig[self.SECONDS]
    
  def __formatString(self,string, date):
    '''
    Formats the given string with the specified date
    '''
    return date.strftime(string)
  def findIterating(self,remotedir,remoteName, starting_number=49):
    """
    Finds the file by trying a different number of combinations.
    Since the last 2 numbers change and until now are in the range from 0 to 60, 
    it will iterate until it finds the correct one
    
    returns: the complete path path
    """

    absoluteUrl = urlparse.urljoin(remotedir,remoteName)
    number = starting_number
    
    while number <= 60:        
      tempUrl =absoluteUrl +'%.2d'%number
      log.debug('Trying: '+tempUrl)
      if self.wget.check_url(tempUrl):
        slash = tempUrl.rindex('/')
        return tempUrl[slash+1:]
      else:
        number+=1
    log.warning("Coudn't find a link")
    return None
  

class GoesUploader:
  def __init__(self, ftpConfig):
    pass

  
class GoesLinkParser:
  '''
  Class used to parse the links out of html pages and look for a specific target using regular expressions
  '''
  pattern = r'<a.*href\s*="(.*)".*>(.*)<\s*/a\s*>'
  def __init__(self, page,target):
    self.page = page
    self.target = target
  
  def find(self):
    '''
    Searches for the target in the given page 
    Returns filename if found, None if not found
    '''
    logging.info("Starting to look for the link")
    for line in self.page:
      match = re.search(self.pattern,line)
      if match:
        link = match.group(1)
        log.debug("Found a link: "+link)
        if re.search(self.target,link):
          log.info("Found the target")
          return link
    
    log.warning("Couldn't find a match")
    return None

def waitToAppear(tries, seconds, conditional, *conditionalArgs):
  '''
  Waits for something to appear, that something is specified by the method supplied in the conditional
  tries- number of tries
  seconds - seconds to wait after each try
  conditional - hook method to determine if the something is there or not
  
  Returns whatever the conditional returns when its true, false if the number of tries >= tries 
  '''
  i =0
  while i <=tries:
    result = conditional(*conditionalArgs)
    if result:
      return result
    else:
      time.sleep(seconds)
      i+=1
  return False
    

if __name__ == '__main__':
  import json
  logprops = LoggerProperties('log.cfg')
  print json.dumps(logprops, indent = 4)
  import logging.config as lc
  lc.dictConfig(logprops)
  log.info('configured the logger')

  goesprops = PropertiesJson('automategoes.cfg')
  print json.dumps(goesprops, indent = 4)
  
  download = goesprops['download']
  downloads= download['downloads']
  d = downloads[0]
  pattern = d['remotename']
  date = datetime.date.today()
  
  pattern = date.strftime(pattern)
  target = 'YCAZ98_KWBN_2012090049'

  
  
  
  
  
    

  