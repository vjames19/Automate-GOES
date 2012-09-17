'''
Created on Sep 16, 2012

@author: TheZen
'''
import time
import os
import logging
import glob

logger = logging.getLogger(__name__)

def waitToAppear(tries, seconds, conditionalFunc, *conditionalArgs):
  '''
  Waits for something to appear, that something is specified by the method supplied in the conditionalFunc
  tries- number of tries
  seconds - seconds to wait after each try
  conditionalFunc - hook method to determine if the something is there or not
  
  Returns whatever the conditionalFunc returns when its true, false if the number of tries >= tries 
  '''
  i =0
  while i <=tries:
    result = conditionalFunc(*conditionalArgs)
    if result:
      logger.info("exists")
      return result
    else:
      time.sleep(seconds)
      i+=1
  return False



def getLogMessage(logFilePath):
  """
  Gets the specified logs message and returns as a string
  """
  if os.path.exists(logFilePath) and os.path.isfile(logFilePath):
    handle = open(logFilePath, 'r')
    message =''
    for line in handle:
      message += line
    return message
  else:
    error ="log path: %s is not a valid file" % logFilePath
    logger.error(error)
    return error
  
def findFiles(pattern, directory):
    """
    Search the specified directory for the the pattern
    returns -> A list of tuples containing (filename, filepath)
    filepath: the whole path
    filename: the name of the filepath
    """ 
    path = os.path.join(directory,pattern)
    ls = glob.glob(path)
    logging.info("Found files: "+ str(ls))
    return ls
  
    
    

    

    
  