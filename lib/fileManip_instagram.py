#!/usr/bin/env python

import logging
import sys

from pprint       import pprint

sys.path.append( './lib' )
from fileManip    import fileManipulation

class fileManipulation_instagram( fileManipulation ):

   extension = ".mkv"

   def __init__( self, meta, conf, logName ):
      fileManipulation.__init__( self, conf, logName )
      self.logger = logging.getLogger(logName+".fileManipulation_instagram")
      self.logger.info("fileManipulation_instagram")
      self.main( meta )

   def retPart( self, date, num ):
      # YYYY:MM:DD:HH:MM:SS where num = it's position
      return date.replace( " ", ":" ).split( ":" )[num]

   def buildNewFileName( self, fileName ):
      t = self.trimFileName( fileName )
      return t[1] + "_" + t[2] + self.extension

   def trimFileName( self, fileName ):
      fileName = fileName.split( "." )[0] 
      splitFile = fileName.split( "_" )
      return splitFile

   def buildNewFilePath( self, fileName ):
      t = self.trimFileName( fileName )
      d = self.conf["rootDir"] + "/" + self.conf["outDir"] + "/" + t[0][:4] + "/" + t[0][4:6] + "/" + t[0][6:8] 
      return d
      
     

   def main( self, meta ):
      a = []
      good = 0 
      un = 0
      for one in meta:
         if "File:Directory" in one:
            d = { "version" : 1
                 ,"sourcePath" : one["File:Directory"]
                 ,"origFileName" : unicode( one["File:FileName"] )
                 ,"newFilePath" : self.buildNewFilePath( one["File:FileName"] ) 
                 ,"newFileName" : self.buildNewFileName( one["File:FileName"] ) 
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

      self.logger.info( "Found %s valid Instagram videos" % ( good ))
      self.logger.info( "Found %s unknown Instagram videos" % ( un ))
      self.yahoo( a )

