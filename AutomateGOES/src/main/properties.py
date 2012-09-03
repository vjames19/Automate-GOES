'''
Created on Sep 3, 2012

@author: TheZen
'''
import datetime
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
  
class PropertiesManager(object):
  def __init__(self,goesprops):
    p = goesprops
    self.ftp = FtpProps(p.getFtp())
    self.download = DownloadProps(p.getDownload())
    self.email = EmailProps(p.getEmail())
    self.finished = FinishedProps(p.getFinished())
    self.degrib = DegribProps(p.getDegrib())
    self.general = p.getGeneral()
    self.variables = p.getVariables()

  def get_ftp(self):
    return self.__ftp


  def get_download(self):
    return self.__download


  def get_email(self):
    return self.__email


  def get_finished(self):
    return self.__finished


  def get_degrib(self):
    return self.__degrib


  def get_general(self):
    return self.__general


  def get_variables(self):
    return self.__variables

class GoesDownloads(object):
  def __init__(self,downloadConfig):
    self.downloads = []
    self.decodeDownloads(downloadConfig['downloads'])
    self.tries = downloadConfig('tries')
    self.seconds = downloadConfig('seconds')

  def get_downloads(self):
    return self.__downloads


  def get_tries(self):
    return self.__tries


  def get_seconds(self):
    return self.__seconds


  def set_downloads(self, value):
    self.__downloads = value


  def set_tries(self, value):
    self.__tries = value


  def set_seconds(self, value):
    self.__seconds = value
  
  def decodeDownloads(self, downloads):
    for download in downloads:
      self.downloads.append(DownloadProps(download))

      
class FinishedProps(object):
  def __init__(self,props):
    self.filename = props['filename']
    self.tries = props['tries']
    self.seconds = props['seconds']

  def get_filename(self):
    return self.__filename


  def get_tries(self):
    return self.__tries


  def get_seconds(self):
    return self.__seconds


  def set_filename(self, value):
    self.__filename = value


  def set_tries(self, value):
    self.__tries = value


  def set_seconds(self, value):
    self.__seconds = value


class EmailProps(object):
  def __init__(self, props):
    self.fromaddress = props['from']
    self.to = props ['to']
    self.password = props['password']

  def get_fromaddress(self):
    return self.__fromaddress


  def get_to(self):
    return self.__to


  def get_password(self):
    return self.__password


  def set_fromaddress(self, value):
    self.__fromaddress = value


  def set_to(self, value):
    self.__to = value


  def set_password(self, value):
    self.__password = value

       
  
class DownloadProps(object):
  def __init__(self, props):
    self.name = props['name']
    self.remotename = props['remotename']
    self.outputname = props['outputname']
    self.remotdir = props['remotedir']
    self.finditerating = props['finditerating']

  def get_name(self):
    return self.__name


  def get_remotename(self):
    return self.__remotename


  def get_outputname(self):
    return self.__outputname


  def get_remotdir(self):
    return self.__remotdir


  def get_finditerating(self):
    return self.__finditerating


  def set_name(self, value):
    self.__name = value


  def set_remotename(self, value):
    self.__remotename = value


  def set_outputname(self, value):
    self.__outputname = value


  def set_remotdir(self, value):
    self.__remotdir = value


  def set_finditerating(self, value):
    self.__finditerating = value

class DegribVariable(object):
  def __init__(self, variable):
    self.name = variable['name']
    self.messages = variable['messages']

  def get_name(self):
    return self.__name


  def get_messages(self):
    return self.__messages


  def set_name(self, value):
    self.__name = value


  def set_messages(self, value):
    self.__messages = value


    

class DegribProps(object):
  def __init__(self, props):
    self.variables = []
    self.decodeVariables(props['variables'])

  def get_variables(self):
    return self.__variables


  def set_variables(self, value):
    self.__variables = value

  
  def decodeVariables(self, variables):
    for variable in variables:
      self.variables.append(DegribVariable(variable))
      

class FtpProps(object):
  def __init__(self, props):
    self.host = props['host']
    self.user= props['user']
    self.password = props['password']
    self.port = props['port']
    self.rootdir = props['rootdir']

  def get_host(self):
    return self.__host


  def get_user(self):
    return self.__user


  def get_password(self):
    return self.__password


  def get_port(self):
    return self.__port


  def get_rootdir(self):
    return self.__rootdir


  def set_host(self, value):
    self.__host = value


  def set_user(self, value):
    self.__user = value


  def set_password(self, value):
    self.__password = value


  def set_port(self, value):
    self.__port = value


  def set_rootdir(self, value):
    self.__rootdir = value

    




    
    
    
    
    
    
    
    
