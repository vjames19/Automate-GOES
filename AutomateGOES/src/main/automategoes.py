'''
Created on Sep 1, 2012

@author: TheZen

Module contains the high level classes needed to automate the process
'''
from main.properties import LoggerProperties, PropertiesJson
from main.remote import FtpMeta, FtpUpload, WputFtpUpload
import datetime
import logging
import os
import re
import remote
import urllib2
import urlparse
import util
logger = logging.getLogger(__name__)


class GoesDownloader(object):
  '''
  GoesDownloader is in charge of downloading all the files specified in the DownloadProps
  object

  Each download should have the following properties using a get_<propertyname>() method:
    name - A name for the download
    remotename - name of the file in the web
    outputname - name for the downloaded file
    dirurl - parent dir of the file
    finditerating - true or false if the file must be found changing the last two digits
    dateoffset - offset from the date specified when constructing this object
  '''

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
    Processes all the downloads specified in the DownloadProps
    '''
    for download in self.downloads:
      logger.info("Starting download process for: " + download.get_name())
      tempDate = self.date + datetime.timedelta(download.get_dateoffset())
      logger.info("Date: " + str(tempDate))

      #Format the strings using the corresponding date
      remotedir = self.__formatString(download.get_remotedir(), tempDate)
      logger.debug("Remotedir: " + remotedir)


      remoteName = self.__formatString(download.get_remotename(), tempDate)

      #Process regex looking in the web directory for the remote name
#      if download[self.REGEX]:
#        
#        if self.wget.check_url(remotedir):
#          
#          remoteName = waitToAppear(self.tries, self.seconds, self.__processRegex,remotedir, remoteName)
#          if remoteName:
#            logger.info("Found the target: "+remoteName)
#          else:
#            logger.error("Couldn't find a link for: "+download[self.NAME])
#            continue
#        else:
#          logger.error("Remote Directory doesn't exists: "+remotedir)
      if download.get_finditerating():
        remoteName = util.waitToAppear(self.tries, self.seconds, self.findIterating, remotedir, remoteName)

      #Create the absolute url      
      absoluteUrl = urlparse.urljoin(remotedir, remoteName)
      logger.debug("Absolute Url: " + absoluteUrl)

      #Wait for the file to be there, then download it.
      if util.waitToAppear(self.tries, self.seconds, self.wget.check_url, absoluteUrl):
        logger.info("Downloading...")
        outputname = self.__formatString(download.get_outputname(), self.date)
        result = self.wget.wget(absoluteUrl, self.todir, outputname)
        logger.info("Downloaded: %s" % str(result))
      else:
        logger.error("Download error the url:%s doesn't exists" % absoluteUrl)
        continue

  def __initializeProps(self, props):
    """
    Initializes this object with the specified properties.
    """
    self.downloads = props.get_downloads()
    self.tries = props.get_tries()
    self.seconds = props.get_seconds()

  def __formatString(self, string, date):
    '''
    Formats the given string with the specified date
    '''
    return date.strftime(string)
  def findIterating(self, remotedir, remoteName, starting_number=0):
    """
    Finds the file by trying a different number of combinations.
    Since the last 2 numbers change and until now are in the range from 0 to 60,
    it will iterate until it finds the correct one

    returns: the complete path path
    """

    absoluteUrl = urlparse.urljoin(remotedir, remoteName)
    number = starting_number
    logger.info("Absolute url: %s" % absoluteUrl)

    while number <= 60:
      tempUrl = absoluteUrl + '%.2d' % number
      logger.debug('Trying: ' + tempUrl)
      if self.wget.check_url(tempUrl):
        slash = tempUrl.rindex('/')
        return tempUrl[slash + 1:]
      else:
        number += 1
    logger.warning("Coudn't find a link")
    return None


class GoesUploader(object):
  """
  Uploads all the files specified in the ftpProps.
  It must have the following properties:
    user
    password
    host - hydroclimate.ece.uprm.edu
    port
    rootdir - GOES-PRWEB_RESULTS/
  """
  def __init__(self, ftpProps):
    f = ftpProps
    self.ftpmeta = FtpMeta(f.get_host(), f.get_user(), f.get_password(), f.get_port())
    self.ftp = FtpUpload(self.ftpmeta)
    self.rootdir = f.get_rootdir()

  #TODO: verify ftp server, verify the findfiles part to see if changes need to be made to FtpUpload in remote
#  def upload(self,pattern, directory, variable):
#    """ 
#    pattern: if you want to upload more than one file use wildcards
#                else just give the file name
#    
#    directory: location of the file to be uploaded
#    
#    variable: variable to upload to. Ex: 'WIND', 'SOLAR' and 'PRECIPITATION'
#    """
#    
#    uploads = self.findFiles(pattern, directory)
#    logging.debug("Uploads: "+str(uploads))
#    
#    if self.ftp.isClosed():
#      self.ftp = FtpUpload(self.ftpmeta)
#    
#    remotedir = urlparse.urljoin(self.rootdir, variable)
#    self.ftp.wput(remotedir, uploads)

  def close(self):
    """
    Closes the connection
    """
    if not self.ftp.isClosed():
      self.ftp.close()



class GoesWputUploader(object):
  """
  Uploads all the files specified in the ftpProps.
  It must have the following properties:
    user
    password
    host - hydroclimate.ece.uprm.edu
    port
    rootdir - GOES-PRWEB_RESULTS/
  """
  def __init__(self, ftpProps):
    f = ftpProps
    self.ftpmeta = FtpMeta(f.get_host(), f.get_user(), f.get_password(), f.get_port())
    self.ftp = WputFtpUpload(self.ftpmeta)
    self.rootdir = f.get_rootdir()

  def upload(self, pattern, directory, variable):
    """
    Uploads the files found with specified pattern.

    pattern - If in need to upload more than one file, using wildcards. Else just use the filename to upload the file
    directory - directory to look for the files.
    variable - which variable to upload the found files

    """
    uploads = util.findFiles(pattern, directory)
    uploads = map(os.path.basename, uploads)
    remotedir = urlparse.urljoin(self.rootdir, variable)
    #If '/' is missing, it needs to append one to comply with wput
    if remotedir[-1] != '/':
      remotedir += '/'
    logger.debug("Remotedir:" + remotedir)
    self.ftp.wput(directory, remotedir, uploads)



class GoesLinkParser(object):
  '''
  Class used to parse the links out of html pages and look for a specific target using regular expressions
  '''
  pattern = r'<a.*href\s*="(.*)".*>(.*)<\s*/a\s*>'
  def __init__(self, page, target):
    self.page = page
    self.target = target

  def find(self):
    '''
    Searches for the target in the given page
    Returns filename if found, None if not found
    '''
    logging.info("Starting to look for the link")
    for line in self.page:
      match = re.search(self.pattern, line)
      if match:
        link = match.group(1)
        logger.debug("Found a link: " + link)
        if re.search(self.target, link):
          logger.info("Found the target")
          return link

    logger.warning("Couldn't find a match")
    return None



class GoesDegribber(object):

  COMMAND = 'degrib %(infile)s -out %(output)s -C -msg %(messagenumber)s -Csv -Unit m -Decimal 2'

  def __init__(self, degripProps, directory, date):
    self.variablesDicts = degripProps.get_variables()
    self.directory = directory
    self.date = date

  def degrib(self):
    """
    degribs the file
    gribName: file with whole directory specified. Ex. C:\my_data\gribFile

    output : with whole directory specified
    cformat: format to convert the file. Csv, Shp.

    msg: Which message to convert if 0 it will convert the whole file.
    """
    for variable in self.variablesDicts:
      degribFiles = util.findFiles(variable.get_name(), self.directory)
      logger.debug("Got files: %s" % degribFiles)
      for degribFile in degribFiles:
        self.__degribFile(degribFile, variable)


  def __degribFile(self, degribFile, degribVariable):
    for message in degribVariable.get_messages():
      outputname = self.date.strftime(degribVariable.get_output()) + '_message' + str(message)
      outputname = os.path.join(os.path.dirname(degribFile), outputname)
      cmd = GoesDegribber.COMMAND % {"infile": degribFile, "output":outputname, "messagenumber": message}
      logger.debug("Degrib command: " + cmd)
      degribOutput = os.popen(cmd)
      self.__getError(degribOutput)
      degribOutput.close()

  def __getError(self, f):
    for line in f:
      if 'Error' in line or 'error' in line:
        logger.error(line)
      else:
        logger.debug(line)


class DirectoryManager(object):
  """
  Manages the directory needed by the project. It also has methods for getting, the following dirs:
    root,LOGS,INPUT and OUTPUT.
  Inside the rootdir it will make
  ${rootdir}/ Root directory of the project
              LOGS/ all the logs go here
              %Y/%m/%d/  tree for the date specified. All the raw data goes here.
                        INPUT/ All the input files go here, .mat files for matlab to use
                        OUTPUT/ All of the output files goes here

  When instantiated it will create the above directories for you.
  """
  def __init__(self, generalProps, date):
    self.__rootdir = generalProps.get_goesdir()
    self.__logdir = generalProps.get_logdir()
    self.__date = date
    self.__init_dirs()

  def __init_dirs(self):
    join = os.path.join
    strftime = self.date.strftime
    self.__cwddir = strftime(join(self.__rootdir, '%Y', '%m', '%d'))
    self.__inputdir = strftime(join(self.__rootdir, '%Y', '%m', '%d', 'INPUT'))
    self.__outputdir = strftime(join(self.__rootdir, '%Y', '%m', '%d', 'OUTPUT'))
    self.__logdir = strftime(join(self.__logdir))


    dirs = [self.__cwddir, self.__inputdir, self.__outputdir, self.__logdir]
    logger.debug("Going to make the following dirs: %s" % dirs)
    for directory in dirs:
      self.mk_dir(directory)

  def mk_dirs(self, directory):
    try:
      os.makedirs(directory)
      logger.info("Made directory: %s" % directory)
    except Exception, e:
      logger.error("Exception making dirs: " + str(e))


  def get_rootdir(self):
    return self.__rootdir


  def get_logdir(self):
    return self.__logdir


  def get_cwddir(self):
    return os.getcwd()


  def get_inputdir(self):
    return self.__inputdir


  def get_outputdir(self):
    return self.__outputdir


  def set_rootdir(self, value):
    self.__rootdir = value


  def set_logdir(self, value):
    self.__logdir = value


  def set_cwddir(self, path):
    """
    Tries to change the current working directory, if successful returns True
    else returns False
    """
    try:
      os.chdir(path)
      return True
    except Exception , e:
      logger.debug("Exception trying to change dir: " + str(e))


  def set_inputdir(self, value):
    self.__inputdir = value


  def set_outputdir(self, value):
    self.__outputdir = value


if __name__ == '__main__':
  import json
  logprops = LoggerProperties('logger.cfg')
  print json.dumps(logprops, indent=4)
  import logging.config as lc
  lc.dictConfig(logprops)
  logger.info('configured the logger')

  goesprops = PropertiesJson('automategoes.cfg')
  print json.dumps(goesprops, indent=4)

  download = goesprops['download']
  downloads = download['downloads']
  d = downloads[0]
  pattern = d['remotename']
  date = datetime.date.today()

  pattern = date.strftime(pattern)
  target = 'YCAZ98_KWBN_2012090049'








