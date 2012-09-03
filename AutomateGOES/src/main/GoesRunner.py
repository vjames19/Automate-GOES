'''
Created on Sep 3, 2012

@author: TheZen
'''
import logging.config
import datetime
from main.properties import AutomateGoesProperties, PropertiesManager, LoggerProperties
logconfig = LoggerProperties('log.cfg')
logging.config.dictConfig(logconfig)


if __name__ == '__main__':
  yesterday = datetime.date.today() - datetime.timedelta(1)
  propsman = PropertiesManager(AutomateGoesProperties('automategoes.cfg'))
  