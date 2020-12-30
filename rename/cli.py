
import argparse
import json
import logging
import logging.config
import sys

from pprint  import pprint

from .readExif import readExifData
from .minify_json  import json_minify

__CONFFILE = 'params.conf.json'

LOGNAME = 'manip'

def main():

   parser = argparse.ArgumentParser(description='File Manipulation')
   parser.add_argument( '-c', '--conf'
                       ,default=__CONFFILE
                       ,help='default config file is params.conf.json'
                      )

   parser.add_argument( '-d', '--directory'
                       ,default=None
                       ,help='The Absolute path of the pictures we are dealing with'
                      )

   args = parser.parse_args()
   rootdir = args.directory
   CONFFILE = args.conf

   # Loading config file
   json_data = open( CONFFILE )
   data = json.loads( json_minify( json_data.read()))
   json_data.close()

   conf = data["config"]
   # pprint(data["LOGGING_CONFIG"])

   # Overriding rootdir by command line if set
   if rootdir:
      conf["rootDir"] = rootdir

   ## Logger configuration.
   try:
      logging.config.dictConfig(data["LOGGING_CONFIG"])
   except ValueError:
      print >> sys.stderr, "logger configuration not excepted"
      print >> sys.stderr, data["LOGGING_CONFIG"]
      sys.exit()

   logger = logging.getLogger(__name__)
   logger.info( "Config file used: %s" % ( CONFFILE ))
   logger.info( "Rootdir used: %s" % ( conf["rootDir"] ))

   fm = readExifData( conf )
   fm.files()
   
   logger.info( "Finished..." )


if __name__ == "__main__":
   main()
