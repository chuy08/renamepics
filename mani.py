#!/usr/bin/env python

import datetime
import json
import logging
import logging.config
import os
import pytz
import shutil
import sys
import time

from exiftool     import ExifTool
from minify_json  import json_minify
from pprint       import pprint

CONFFILE = 'params.conf'
LOGNAME = 'manip'

class fileManipulation():

   def __init__( self, conf, logName ):
      ## Setup the logger for all subclasses.
      self.conf = conf 
      self.outdir = self.conf["outDir"]
      self.rootdir = self.conf["rootDir"] 
      self.logName = logName
      self.logger = logging.getLogger(logName+".fileManipulation")
      self.logger.info("fileManipulation")

   def _removeErrors( self, meta ):
      r = [] 
      for each in meta:
         if "ExifTool:Error" not in each:
            r.append( each )
         else:
            self.logger.info( "Not a valid file: %s" % ( each["SourceFile"] ))
      self.logger.info( "Found %s files with vaild meta information" % ( len( r ) ))
      return r

   def getMeta( self, files ):
      et = ExifTool()
      et.start()
      a = et.get_metadata_batch( files )
      et.terminate()
      meta = self._removeErrors( a )
      return meta

   def files( self ):
      f = []
      if not os.path.exists( self.rootdir ):
         print "Root dir doesn't seem to be vaild"
         sys.exit( 1 )

      for dir in os.walk( self.rootdir ):
         for fileName in dir[2]:
            f.append( os.path.join( dir[0], fileName ) )

      meta = self.getMeta( f )
      self.identifyType( meta )
      return meta 

   def createOutDirs( self, dir ):
      for one in dir:
         newdirs = self.rootdir + "/" + self.outdir + "/" + one["year"] + "/" + one["month"] + "/" + one["day"]
         try:
            os.makedirs( newdirs )
         except:
            pass 

   def copyFile( self, files ):
      for one in files:
#         print type( one["sourcePath"] ), one["sourcePath"], type( one["origFileName"]), one["origFileName"]
         origfile = os.path.join( one["sourcePath"], one["origFileName"] )
         # Checking if were gonna do a rename or just copy
         if self.conf["rename"]:
            newfile = ( os.path.join( one["newFilePath"], one["newFileName"] )) 
            try:
               shutil.copy2( origfile, newfile )
            except:
               self.logger.info( "Copy failed for: %s" % ( origfile ))
         else:
            try:
               shutil.copy2( origfile, one["newFilePath"] )
            except:
               self.logger.info( "Copy failed for: %s" % ( origfile ))

   def yahoo( self, data ):
      self.createOutDirs( data )
      self.copyFile( data )

   def identifyType( self, meta ):
      jpeg = []
      mp4 = []
      m2ts = []
      for one in meta:
#         print one["File:FileType"]
         if one["File:FileType"] == "JPEG":
            jpeg.append( one )
         elif one["File:FileType"] == "MP4":
            mp4.append( one )
         elif one["File:FileType"] == "M2TS":
            m2ts.append( one )
   
         else:
#            print one["File:FileType"]
            self.logger.info( "Don't know what to do with %s" % ( one["File:FileType"] ))

      if len( jpeg ) > 0:
         j = fileManipulation_jpeg( jpeg, self.conf, self.logName ) 
      if len( mp4 ) > 0:
         mp = fileManipulation_mp4( mp4, self.conf, self.logName ) 
      if len( m2ts ) > 0:
         m2 = fileManipulation_m2ts( m2ts, self.conf, self.logName ) 
      

class fileManipulation_m2ts( fileManipulation ):

   def __init__( self, meta, conf, logName ):
      fileManipulation.__init__( self, conf, logName )
      self.logger = logging.getLogger(logName+".fileManipulation_m2ts")
      self.logger.info("fileManipulation_m2ts")
      self.main( meta )

   def retPart( self, date, num ):
      # [ 'YYYY', 'MM', 'DD', 'HH', 'MM', 'SEC' ] - send in which is needed
      date = self.removeTZOffset( date ) 
      d = date.replace( " ", ":" )
      splitD = d.split( ":" )
#      print type( num )
      return splitD[num]

   def removeTZOffset( self, date ):
      return date.split( "-" )[0]
   
   def buildNewFileName( self, date ):
      date = self.removeTZOffset( date ) 
      return date.replace( " ", "_" ).replace( ":", "" )

   def buildNewFilePath( self, meta ):
      d = self.conf["rootDir"] + "/" + self.conf["outDir"] + "/" + self.retPart( meta["File:FileModifyDate"], 0 ) + "/" + self.retPart( meta["File:FileModifyDate"], 1 ) + "/" + self.retPart( meta["File:FileModifyDate"], 2 )
#      print d
      return d

   def main( self, meta ):
#      pprint( meta )
      a = []
      for one in meta:
         if "File:FileModifyDate" in one:
            d = { "sourcePath" : one["File:Directory"]
                 ,"origFileName" : unicode( one["File:FileName"] )
                 ,"year" : self.retPart( one["File:FileModifyDate"], 0 ) 
                 ,"month" : self.retPart( one["File:FileModifyDate"], 1 ) 
                 ,"day" : self.retPart( one["File:FileModifyDate"], 2 )
                 ,"newFilePath" : self.buildNewFilePath( one ) 
                 ,"newFileName" : self.buildNewFileName( one["File:FileModifyDate"] ) 
                }
            a.append( d )
         else:
            self.logger.info( "No CreateDate: %s" % ( one["SourceFile"] )) 

#      print a
      self.yahoo( a )


class fileManipulation_mp4( fileManipulation ):

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
      return t.strftime( "%Y%m%d_%H%M%S" ) + ".mp4"

   def buildNewFilePath( self, meta ):
      d = self.conf["rootDir"] + "/" + self.conf["outDir"] + "/" + self.retPart( meta["QuickTime:CreateDate"], '%Y' ) + "/" + self.retPart( meta["QuickTime:CreateDate"], '%m' ) + "/" + self.retPart( meta["QuickTime:CreateDate"], '%d' )      
#      print d
      return d

   def main( self, meta ):
#      pprint( meta )
      a = []
      for one in meta:
         if "QuickTime:CreateDate" in one:
            d = { "sourcePath" : one["File:Directory"]
                 ,"origFileName" : unicode( one["File:FileName"] )
                 ,"year" : self.retPart( one["QuickTime:CreateDate"], '%Y' ) 
                 ,"month" : self.retPart( one["QuickTime:CreateDate"], '%m' ) 
                 ,"day" : self.retPart( one["QuickTime:CreateDate"], '%d' )
                 ,"newFilePath" : self.buildNewFilePath( one ) 
                 ,"newFileName" : self.buildNewFileName( one["QuickTime:CreateDate"] ) 
                }
            a.append( d )
         else:
            self.logger.info( "No CreateDate: %s" % ( one["SourceFile"] )) 

#      print a
      self.yahoo( a )


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
