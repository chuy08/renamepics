#!/usr/bin/env python

import logging
import sys

from pprint       import pprint

sys.path.append( './lib' )
from fileManip    import fileManipulation

class fileManipulation_music( fileManipulation ):

   def __init__( self, meta, conf, logName ):
      fileManipulation.__init__( self, conf, logName )
      self.logger = logging.getLogger(logName+".fileManipulation_music")
      self.logger.info("fileManipulation_music")
      self.main( meta )

   def buildNewFilePath( self ):
      d = self.conf["rootDir"] + "/" + self.conf["outDir"] + "/" + self.conf["musicDir"]
#      print d
      return d

   def main( self, meta ):
      a = []
      good = 0 
      un = 0
      for one in meta:
         d = { "version" : 1
              ,"sourcePath" : one["File:Directory"]
              ,"origFileName" : unicode( one["File:FileName"] )
              ,"newFilePath" : self.buildNewFilePath() 
              ,"newFileName" : unicode( one["File:FileName"] ) 
             }
         a.append( d )
         good += 1

      self.logger.info( "Found %s Music files" % ( good ))
      self.yahoo( a )

