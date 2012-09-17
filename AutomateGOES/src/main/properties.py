'''
Created on Sep 3, 2012

@author: TheZen
'''
import datetime
import logging
print __name__
logger = logging.getLogger(__name__)

class PropertiesJson(dict):
  def __init__(self,filename):
    import json
    try:
      self.update( json.load(open(filename,'r')))
    except Exception,e:
      logger.error("Error reading file %s. %s" %(filename, str(e)))
      raise e
    
    
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
    handlers = self.get('handlers')
    if handlers:
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
  def __init__(self,automateGoesProps):
    p = automateGoesProps
    self.ftp = FtpProps(p.getFtp())
    self.download = DownloadProps(p.getDownload())
    self.email = EmailProps(p.getEmail())
    self.finished = FinishedProps(p.getFinished())
    self.degrib = DegribProps(p.getDegrib())
    self.general = GeneralProps(p.getGeneral())
    self.variables = p.getVariables()

  def get_ftp(self):
    return self.ftp


  def get_download(self):
    return self.download


  def get_email(self):
    return self.email


  def get_finished(self):
    return self.finished


  def get_degrib(self):
    return self.degrib


  def get_general(self):
    return self.general


  def get_variables(self):
    return self.variables

class DownloadProps(object):
  def __init__(self,props):
    self.downloads = []
    self.__initDownloads(props['downloads'])
    self.tries = props['tries']
    self.seconds = props['seconds']

  def get_downloads(self):
    return self.downloads


  def get_tries(self):
    return self.tries


  def get_seconds(self):
    return self.seconds


  def set_downloads(self, value):
    self.downloads = value


  def set_tries(self, value):
    self.tries = value


  def set_seconds(self, value):
    self.seconds = value
  
  def __initDownloads(self, downloads):
    for download in downloads:
      self.downloads.append(DownloadMeta(download))

      
class FinishedProps(object):
  def __init__(self,props):
    self.filename = props['filename']
    self.tries = props['tries']
    self.seconds = props['seconds']

  def get_filename(self):
    return self.filename


  def get_tries(self):
    return self.tries


  def get_seconds(self):
    return self.seconds


  def set_filename(self, value):
    self.filename = value


  def set_tries(self, value):
    self.tries = value


  def set_seconds(self, value):
    self.seconds = value


class EmailProps(object):
  def __init__(self, props):
    self.fromaddress = props['from']
    self.to = props ['to']
    self.password = props['password']

  def get_from(self):
    return self.fromaddress


  def get_to(self):
    return self.to


  def get_password(self):
    return self.password


  def set_from(self, value):
    self.fromaddress = value


  def set_to(self, value):
    self.to = value


  def set_password(self, value):
    self.password = value

       
  
class DownloadMeta(object):
  def __init__(self, downloadprops):
    self.__name = downloadprops['name']
    self.remotename = downloadprops['remotename']
    self.outputname = downloadprops['outputname']
    self.remotedir = downloadprops['remotedir']
    self.finditerating = downloadprops['finditerating']
    self.dateoffset = downloadprops['dateoffset']

  def get_dateoffset(self):
    return self.dateoffset

  def set_dateoffset(self,value):
    self.dateoffset = value


  def get_name(self):
    return self.__name


  def get_remotename(self):
    return self.remotename


  def get_outputname(self):
    return self.outputname


  def get_remotedir(self):
    return self.remotedir


  def get_finditerating(self):
    return self.finditerating


  def set_name(self, value):
    self.__name = value


  def set_remotename(self, value):
    self.remotename = value


  def set_outputname(self, value):
    self.outputname = value


  def set_remotedir(self, value):
    self.remotedir = value


  def set_finditerating(self, value):
    self.finditerating = value


class DegribVariable(object):
  def __init__(self, variable):
    self.__name = variable['name']
    self.__messages = variable['messages']
    self.__output = variable['output']

  def get_output(self):
    return self.__output


  def set_output(self, value):
    self.__output = value


  def get_name(self):
    return self.__name


  def get_messages(self):
    return self.__messages


  def set_name(self, value):
    self.__name = value


  def set_messages(self, value):
    self.__messages = value



    

class DegribProps(object):
  def __init__(self, downloadprops):
    self.variables = []
    self.__initiDegribVariables(downloadprops['variables'])

  def get_variables(self):
    return self.variables


  def set_variables(self, value):
    self.variables = value

  
  def __initiDegribVariables(self, variables):
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
    return self.host


  def get_user(self):
    return self.user


  def get_password(self):
    return self.password


  def get_port(self):
    return self.port


  def get_rootdir(self):
    return self.rootdir


  def set_host(self, value):
    self.host = value


  def set_user(self, value):
    self.user = value


  def set_password(self, value):
    self.password = value


  def set_port(self, value):
    self.port = value


  def set_rootdir(self, value):
    self.rootdir = value


class GeneralProps(object):
  def __init__(self, props):
    self.__goesdir = props['goesdir']
    self.__logdir = props['logdir']
    self.__matlab = props['matlab']

  def get_goesdir(self):
    return self.__goesdir


  def get_logdir(self):
    return self.__logdir


  def get_matlab(self):
    return self.__matlab


  def set_goesdir(self, value):
    self.__goesdir = value


  def set_logdir(self, value):
    self.__logdir = value


  def set_matlab(self, value):
    self.__matlab = value

if __name__ == "__main__":
  props = AutomateGoesProperties('automategoes.cfg')
  print props.getFtp()



    
    
    
    
    
    
    
    
