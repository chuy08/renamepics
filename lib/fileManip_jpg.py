#!/usr/bin/env python

import logging
import sys

from pprint       import pprint

sys.path.append( './lib' )
from fileManip    import fileManipulation

class fileManipulation_jpeg( fileManipulation ):

   def __init__( self, meta, conf, logName ):
      fileManipulation.__init__( self, conf, logName )
      self.logger = logging.getLogger(logName+".fileManipulation_jpeg")
      self.logger.info("fileManipulation_jpeg")
      self.main( meta )

   def retPart( self, date, num ):
      # YYYY:MM:DD:HH:MM:SS where num = it's position
      return date.replace( " ", ":" ).split( ":" )[num]

   def buildNewFileName( self, meta):
      f = ( meta["EXIF:CreateDate"] ).replace( " ", "_" ).replace( ":", "")
      return f + ".jpg"

   def buildNewFilePath( self, meta ):
      d = self.conf["rootDir"] + "/" + self.conf["outDir"] + "/" + self.retPart( meta["EXIF:CreateDate"], 0 ) + "/" + self.retPart( meta["EXIF:CreateDate"], 1 ) + "/" + self.retPart( meta["EXIF:CreateDate"], 2 )
#      print d
      return d

   def main( self, meta ):
      a = []
      for one in meta:
         if "EXIF:CreateDate" in one:
            d = { "sourcePath" : one["File:Directory"]
                 ,"origFileName" : unicode( one["File:FileName"] )
                 ,"year" : self.retPart( one["EXIF:CreateDate"], 0 ) 
                 ,"month" : self.retPart( one["EXIF:CreateDate"], 1 ) 
                 ,"day" : self.retPart( one["EXIF:CreateDate"], 2 )
                 ,"newFilePath" : self.buildNewFilePath( one ) 
                 ,"newFileName" : self.buildNewFileName( one ) 
                }
            a.append( d )
         else:
            self.logger.info( "No CreateDate: %s" % ( one["SourceFile"] )) 

      self.yahoo( a )

