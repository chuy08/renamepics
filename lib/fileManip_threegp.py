#!/usr/bin/env python

import logging
import sys

from pprint       import pprint

sys.path.append( './lib' )
from fileManip    import fileManipulation

class fileManipulation_threegp( fileManipulation ):

   extension = ".3gp"

   def __init__( self, meta, conf, logName ):
      fileManipulation.__init__( self, conf, logName )
      self.logger = logging.getLogger(logName+".fileManipulation_3gp")
      self.logger.info("fileManipulation_3gp")
      self.main( meta )

   def retPart( self, date, num ):
      # YYYY:MM:DD:HH:MM:SS where num = it's position
      return date.replace( " ", ":" ).split( ":" )[num]

   def buildNewFileName( self, date ):
      f = date.replace( " ", "_" ).replace( ":", "")
      return f + self.extension 

   def buildNewFilePath( self, date ):
      d = self.conf["rootDir"] + "/" + self.conf["outDir"] + "/" + self.retPart( date, 0 ) + "/" + self.retPart( date, 1 ) + "/" + self.retPart( date, 2 )
      return d

   def main( self, meta ):
      a = []
      good = 0 
      un = 0
      for one in meta:
         if "QuickTime:CreateDate" in one:
            d = { "version" : 1
                 ,"sourcePath" : one["File:Directory"]
                 ,"origFileName" : unicode( one["File:FileName"] )
                 ,"newFilePath" : self.buildNewFilePath( one["QuickTime:CreateDate"] ) 
                 ,"newFileName" : self.buildNewFileName( one["QuickTime:CreateDate"] ) 
                }
            a.append( d )
            good += 1
         else:
            d = { "unknown" : 0
                 ,"sourcePath" : one["File:Directory"]
                 ,"origFileName" : unicode( one["File:FileName"] )
                 ,"newFilePath" : self.buildUnknownFilePath()
                 ,"newFileName" : unicode( one["File:FileName"] )
                }
            a.append( d )
            un += 1

      self.logger.info( "Found %s valid 3GP's" % ( good ))
      self.logger.info( "Found %s unknown 3GP's" % ( un ))
      self.yahoo( a )

