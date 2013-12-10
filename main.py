#!/usr/bin/env python

import json
import logging
import logging.config
import sys

from pprint           import pprint

sys.path.append( './lib' )

from fileManip    import fileManipulation
from minify_json  import json_minify

CONFFILE = 'params.conf'
LOGNAME = 'manip'

def main():

   # Loading config file
   json_data = open( CONFFILE )
   data = json.loads( json_minify( json_data.read()))
   json_data.close()

   conf = data["config"]

   ## Logger configuration.
   try:
      logging.config.dictConfig(data["loggerConf"])
   except ValueError:
      print >> sys.stderr, "logger configuration not excepted"
      print >> sys.stderr, data["loggerConf"]
      sys.exit()

   logger = logging.getLogger(LOGNAME)
   logger.info( "Config file used: %s" % ( CONFFILE ))

   fm = fileManipulation( conf, LOGNAME )
   fm.files()
   




if __name__ == "__main__":
   main()
