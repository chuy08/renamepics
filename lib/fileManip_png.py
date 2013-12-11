#!/usr/bin/env python

import logging
import sys

from pprint       import pprint

sys.path.append( './lib' )
from fileManip    import fileManipulation

class fileManipulation_png( fileManipulation ):

   extension = ".png"

   def __init__( self, meta, conf, logName ):
      fileManipulation.__init__( self, conf, logName )
      self.logger = logging.getLogger(logName+".fileManipulation_png")
      self.logger.info("fileManipulation_png")
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
         if "File:FileModifyDate" in one:
            d = { "version" : 1
                 ,"sourcePath" : one["File:Directory"]
                 ,"origFileName" : unicode( one["File:FileName"] )
                 ,"newFilePath" : self.buildNewFilePath( one["File:FileModifyDate"] ) 
                 ,"newFileName" : self.buildNewFileName( one["File:FileModifyDate"] ) 
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

      self.logger.info( "Found %s valid PNG's" % ( good ))
      self.logger.info( "Found %s unknown PNG's" % ( un ))
      self.yahoo( a )

