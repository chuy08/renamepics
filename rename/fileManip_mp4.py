#!/usr/bin/env python

import datetime
import logging
import pytz
import sys
import time

from pprint       import pprint

sys.path.append( './lib' )
from fileManip        import fileManipulation

class fileManipulation_mp4( fileManipulation ):

   extension = ".mp4"

   def __init__( self, meta, conf, logName ):
      fileManipulation.__init__( self, conf, logName )
      self.logger = logging.getLogger(logName+".fileManipulation_mp4")
      self.logger.info("fileManipulation_mp4")
      self.main( meta )

   def retPart( self, date, fmt ):
      # fmt is the linux time format command 
      t = self.adjustUTC2Local( date )
      return t.strftime( fmt )

   def adjustUTC2Local( self, date ):
      # Quicktime encodes create date as UTC 
      splitDate = date.split( ":" )
#      print type( splitDate[0] )
      if int( splitDate[0] ) == 0000:
         date = ( "1970:01:01 00:00:00" )

      timeZone = pytz.timezone( self.conf["timeZone"] )
      dtformat = '%Y:%m:%d %H:%M:%S'
      t = datetime.datetime.strptime( date, dtformat).replace(tzinfo=pytz.utc)
      return timeZone.normalize( t )

   def buildNewFileName( self, date ):
      t = self.adjustUTC2Local( date )
      return t.strftime( "%Y%m%d_%H%M%S" ) + self.extension 

   def buildNewFilePath( self, date ):
      d = self.conf["rootDir"] + "/" + self.conf["outDir"] + "/" + self.retPart( date, '%Y' ) + "/" + self.retPart( date, '%m' ) + "/" + self.retPart( date, '%d' )      
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

      self.logger.info( "Found %s valid MP4's" % ( good ))
      self.logger.info( "Found %s unknown MP4's" % ( un ))
      self.yahoo( a )

