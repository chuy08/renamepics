#!/usr/bin/env python

import logging
import sys

from pprint       import pprint

sys.path.append( './lib' )
from fileManip    import fileManipulation

class fileManipulation_mov( fileManipulation ):
   
   extension = ".mov"

   def __init__( self, meta, conf, logName ):
      fileManipulation.__init__( self, conf, logName )
      self.logger = logging.getLogger(logName+".fileManipulation_mov")
      self.logger.info("fileManipulation_mov")
      self.main( meta )

   def retPart( self, date, num ):
      # YYYY:MM:DD:HH:MM:SS where num = it's position
      d = self.removeUTC( date )
      return d.replace( " ", ":" ).split( ":" )[num]

   def removeUTC( self, date ):
      splitDate = date.split( "-" )
      return splitDate[0]

   def buildNewFileName( self, date ):
      d = self.removeUTC( date )
      f = d.replace( " ", "_" ).replace( ":", "")
      return f + self.extension

   def buildNewFilePath( self, meta ):
      d = self.conf["rootDir"] + "/" + self.conf["outDir"] + "/" + self.retPart( meta["QuickTime:CreateDate"], 0 ) + "/" + self.retPart( meta["QuickTime:CreateDate"], 1 ) + "/" + self.retPart( meta["QuickTime:CreateDate"], 2 )
#      print d
      return d

   def main( self, meta ):
      pprint( meta )
      a = []
      good = 0 
      un = 0
      for one in meta:
         if "QuickTime:CreateDate" in one:
            d = { "sourcePath" : one["File:Directory"]
                 ,"origFileName" : unicode( one["File:FileName"] )
                 ,"year" : self.retPart( one["QuickTime:CreateDate"], 0 ) 
                 ,"month" : self.retPart( one["QuickTime:CreateDate"], 1 ) 
                 ,"day" : self.retPart( one["QuickTime:CreateDate"], 2 )
                 ,"newFilePath" : self.buildNewFilePath( one ) 
                 ,"newFileName" : self.buildNewFileName( one["QuickTime:CreateDate"] ) 
                }
            a.append( d )
            good += 1
         else:
            d = { "unknown" : one["SourceFile"] } 
            a.append( d )
            un += 1

      self.logger.info( "Found %s valid MOV's" % ( good ))
      self.logger.info( "Found %s unknown MOV's" % ( un ))
      self.yahoo( a )

