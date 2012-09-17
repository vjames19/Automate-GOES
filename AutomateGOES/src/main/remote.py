'''
Created on Aug 25, 2012

@author: vjames19
'''

import urllib
import urllib2
import urlparse
import os
import logging
from ftplib import FTP

#setup handler
logger = logging.getLogger('main.remote')
logger.addHandler(logging.NullHandler())

class WebDownload:
  """
  Represents a download through HTTP
  """

  def check_url(self, url):
    """
    Verifies if the url exists

    check_url -> True if exists, false otherwise.
    """
    try:
      urllib2.urlopen(url)
      return True
    except:
      return False

  def wget(self, url, todir, outputFileName=''):
    """
    Downloads a remote object to a local directory

    if outputFilename is None it will get the filename from the url
    using the string after the last '/'

    wget -> (filename, headers)
    """
    if outputFileName == '':
      outputFileName = url.split('/')[-1]
      logger.debug("Stripped outputfilename: %s" % outputFileName)
    path = os.path.join(todir, outputFileName)
    logger.info("url:%s targetDir:%s" % (url, path))
    return urllib.urlretrieve(url, path)

  def urlopen(self, url):
    """
    Returns a file like object to read from
    """
    return urllib2.urlopen(url)


class FtpMeta:
  """
  Meta information for the FTP connection
  """
  def __init__(self, host, user, password, port=21):
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

  def setPassword(self, password):
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
    self.ftp.connect(m.getHost(), m.getPort())
    self.ftp.login(m.getUser(), m.getPassword())



  def close(self):
    """
    Closes the connection
    """
    self.ftp.close()

  def wput(self, remoteDir, filenamesTuple):
    """
    Uploads the files to the server
    remoteDir - dir to store the files

    filenamesTuple - List of tuples of the form
                    [(remotefilename,localfilename),...]
    """
    if remoteDir != '':
      try:
        self.ftp.cwd(remoteDir)
        logger.debug("CWD:" + remoteDir)
      except Exception, e:
        logger.error("Error trying to cwd: %s\nNot going to upload anything" % e)
        return

    for remotefilename, localfilename in filenamesTuple:
      try:
        logger.info('Going to upload %s...' % remotefilename)
        self.__connectIfNeeded()
        self.ftp.storbinary("STOR " + remotefilename, open(localfilename, 'rb'))
        logger.info("Stored " + remotefilename)
      except Exception, e:
        logger.error("Failed to store:" + remotefilename)
        logger.error("Exception: %s" % str(e))


  def __connectIfNeeded(self):
    """
    Sometimes the connection closes and needs to be reopened.
    """
    if self.isClosed():
      self.__constructFtp()
      logger.info("Connecting again to the ftp server...")

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
    """
    Verifies if the connection is closed
    """
    try:
      self.ftp.pwd()
      return False
    except:
      return True

  def currentDir(self):
    return self.pwd()
  def changeDir(self, dirname):
    self.ftp.cwd(dirname)
    
class WputFtpUpload:
  """
  Uploads files using wput command
  
  Uses FtpMeta to initialize the ftp url
  """
  def __init__(self, ftpMeta):
    self.ftpMeta = ftpMeta
    self.initialWorkingDir = os.getcwd()
    self.__constructFtp()
  
  def __constructFtp(self):
    f = self.ftpMeta
    #TODO add port
    d = {"host":f.getHost(),"user":f.getUser(),"passwd":f.getPassword()}
    self.ftpUrl = "ftp://%(user)s:%(passwd)s@%(host)s" % d
    logging.debug("ftp url: %s" % self.ftpUrl)
  
  def wput(self,filedir, remotedir, filenames):
    """
    uploads the specified files to ftp server
    
    filenames - should only be the name of the file, also all filenames should be in the specified filedir
    filedir - parent dir of the files
    remotedir - path in the server, where files are going to be stored. Ex. ftp:user:pass@host/remotedir
    
    When the method is finished the working dir will change to the initial working directory, that was when the class was instantiated
 
    """
    absoluteUrl = urlparse.urljoin(self.ftpUrl, remotedir)
    logger.info("absolote url: %s" %absoluteUrl)
    os.chdir(filedir)
    cmds = ["wput"]
    cmds.extend(filenames)
    cmds.append(absoluteUrl)
    logger.debug("cmds: %s" %cmds)
    strcmd = " ".join(cmds)
    logger.debug(strcmd)
    logger.debug("cwd:%s"%os.getcwd())
    output = os.popen(strcmd)
    self.__getErrors(output)
    os.chdir(self.initialWorkingDir)

  def __getErrors(self, outputFile):
    for line in outputFile:
      if 'Error' in line or 'error' in line:
        logger.error(line)
      else:
        logger.debug(line)
    outputFile.close()
    
    
  
      


if __name__ == "__main__":
  import json, logging.config as lc
  print os.getcwd()


  config = json.load(open('logger.cfg', 'r'))
  print config
  lc.dictConfig(config)

  logger = logging.getLogger()
  logger.info('loaded the configuration')
  print logger.handlers

  os.chdir("C:\\Users\\TheZen\\Documents\\academic.uprm.edu\\hdc")
  logger.error(os.listdir(os.getcwd()))
  ftpMeta = FtpMeta("hydroclimate.ece.uprm.edu", "victorj", "eiqu9O")
  upload = FtpUpload(ftpMeta)
  file = "logo.jpg"
  files = [(file, open(file, 'rb'))]
  upload.wput("", files)
  logger.debug("debugging message")

  upload.close()




  print 'done'













