'''
Created on Aug 25, 2012

@author: vjames19
'''

import urllib
import urllib2
import os
import logging
from ftplib import FTP

#setup handler
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class HttpDownload:
  """
  Represents a download through HTTP
  """
  
  def check_url(self,url):
    """
    Verifies if the url exists
    
    check_url -> True if exists, false otherwise.
    """
    try:
      urllib2.urlopen(url)
      return True
    except:
      return False

  def wget(self,url, todir, outputFileName = ''):
    """
    Downloads a remote object to a local directory
    
    if outputFilename is None it will get the filename from the url
    using the string after the last '/'
    
    wget -> (filename, headers)
    """
    if outputFileName == '':
      outputFileName = url.split('/')[-1]
      
    path = os.path.join(todir,outputFileName)
    logger.info("url:%s targetDir:%s" % (url,path))
    return urllib.urlretrieve(url,path)
  

class FtpMeta:
  """
  Meta information for the FTP connection
  """
  def __init__(self, host, user,password, port =21):
    self.host = host
    self.user = user
    self.password = password
    self.port = port

  def getHost(self):
    return self.host
  
  def getUser(self):
    return self.user
  
  def getPassword(self):
    return self.password
  
  def getPort(self):
    return self.port
  
  def setPort(self, port):
    self.port = port
    
  def setHost(self, host):
    self.host = host
    
  def setUser(self, user):
    self.user = user
    
  def setPassword(self,password):
    self.password = password
    

  

class FtpUpload:
  """
  Class used to upload files into an ftpserver
  
  FtpUpload(ftpMeta) -> Creates an object of this class and creates the ftp connection
                        from the ftpMeta object
  """
  def __init__(self, ftpMeta):
    self.ftpMeta = ftpMeta
    self.__constructFtp()
    
    
  def __constructFtp(self):
    """
    Constructs the ftp connection from the FtpMeta
    """
    m = self.ftpMeta
    self.ftp = FTP()
    self.ftp.connect(m.getHost(),m.getPort())
    self.ftp.login(m.getUser(), m.getPassword())
    
    print self.ftp.pwd()
        
  def close(self):
    """
    Closes the connection
    """
    self.ftp.close()

  def wput(self,remoteDir, filenamesTuple):
    """
    Uploads the files to the server
    remoteDir - dir to store the files
    
    filenamesTuple - List of tuples of the form
                    [(remotefilename,localfilename),...]
    """
    if remoteDir != '':
      self.ftp.cwd(remoteDir)
    logger.info("CWD:"+remoteDir)
    
    for remotefilename, localfilename in filenamesTuple:
      self.ftp.storbinary("STOR "+remotefilename,localfilename)
      logger.info("Stored "+remotefilename)
      
  def dirExists(self, remoteDir):
    """
    Verifies if the remote dir exists
    """
    cwd = self.ftp.pwd()
    try:
      self.ftp.cwd(remoteDir)
      self.ftp.cwd(cwd)
      return True
    except:
      return False
    
  def isClosed(self):
    try:
      self.ftp.pwd()
      return False
    except:
      return True


if __name__ == "__main__":
  import os
  os.chdir("C:\\Users\\TheZen\\Documents\\academic.uprm.edu\\hdc")
  print os.listdir(os.getcwd())
  ftpMeta = FtpMeta("hydroclimate.ece.uprm.edu", "victorj", "eiqu9O")
  upload = FtpUpload(ftpMeta)
  file = "logo.jpg"
  files = [(file,open(file,'rb'))]
  upload.wput("", files)

  
  
  print 'done'
  
  
  
  

  
 
  

  
    


