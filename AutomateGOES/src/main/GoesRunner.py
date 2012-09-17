'''
Created on Sep 3, 2012

@author: TheZen
'''
import logging.config
import datetime
from main.properties import AutomateGoesProperties, PropertiesManager, LoggerProperties
from main.automategoes import GoesDownloader, DirectoryManager, GoesWputUploader,\
  GoesDegribber
import os
from main import emailer, util

def wait_finished(directory,filename):
  path = os.path.join(directory,filename)
  logging.debug("Path "+ path)
  print path
  return os.path.exists(path)


if __name__ == '__main__':
  #yesterday = datetime.date.today() - datetime.timedelta(1)
  yesterday = datetime.date(2012,9,1)
  propsman = PropertiesManager(AutomateGoesProperties('automategoes.cfg'))
  #initialize directories
  directoryman = DirectoryManager(propsman.get_general(), yesterday)
  directory = directoryman.get_cwd()
  
  #logger
  logging.config.dictConfig(LoggerProperties('log.cfg'))
  
  #download part
#  downloader = GoesDownloader(propsman.get_download(), yesterday, directory)
#  downloader.download()

  #degrib part
#  degrib = GoesDegribber(propsman.get_degrib(), directory, yesterday)
#  degrib.degrib()
    
  #matlab part
  matlab = propsman.get_general().get_matlab() 
  os.system(matlab)
  
  #Wait for finished file
  finished = propsman.get_finished()
  util.waitToAppear(finished.get_tries(), finished.get_seconds(), wait_finished,directoryman.get_output(), finished.get_filename())
  
  #TODO: test this part
  #upload part
  uploader = GoesWputUploader(propsman.get_ftp())
  variables = propsman.get_variables()
  for variable in variables:
    pattern = variable + '*.jpg'
    uploader.upload(pattern, directory, variable)

  #email part
  emailprops = propsman.get_email()
  emailer.sendEmail(emailprops.get_from( ), emailprops.get_password(), emailprops.get_from(), emailprops.get_to())