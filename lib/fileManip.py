#!/usr/bin/env python

import logging
import os
import shutil
import sys

sys.path.append( './lib' )

from exiftool     import ExifTool
from pprint       import pprint

class fileManipulation():

   def __init__( self, conf, logName ):
      ## Setup the logger for all subclasses.
      self.conf = conf 
      self.outdir = self.conf["outDir"]
      self.rootdir = self.conf["rootDir"] 
      self.unknown = self.conf["unknown"] 
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

      for root, subFolders, files in os.walk( self.rootdir ):
         for one in self.conf["ignoreDirs"]:
            if one in subFolders:
               subFolders.remove( one )
         for fileName in files:
            f.append( os.path.join( root, fileName ) )
#      pprint( f )

      meta = self.getMeta( f )
      self.identifyType( meta )
#      return meta 

   def createOutDirs( self, dir ):
      for one in dir:
         newdirs = ''
         if "unknown" in one:
            newdirs = self.rootdir + "/" + self.outdir + "/" + self.unknown 
         else:
            newdirs = self.rootdir + "/" + self.outdir + "/" + one["year"] + "/" + one["month"] + "/" + one["day"]

         try:
            os.makedirs( newdirs )
         except:
            pass 

   def copyFile( self, files ):
#      pprint( files)
      for one in files:
#         print type( one["sourcePath"] ), one["sourcePath"], type( one["origFileName"]), one["origFileName"]
         if "unknown" in one:
            newdir = self.rootdir + "/" + self.outdir + "/" + self.unknown
            try:
               shutil.copy2( one["unknown"], newdir )
            except:
               self.logger.info( "Copy failed for: %s" % ( one["unknown"] ))

         else:
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
#      pprint( meta )
      jpeg = []
      mp4 = []
      m2ts = []
      png = []
      for one in meta:
#         print one["File:FileType"]
         if one["File:FileType"] == "JPEG":
            jpeg.append( one )
         elif one["File:FileType"] == "MP4":
            mp4.append( one )
         elif one["File:FileType"] == "M2TS":
            m2ts.append( one )
         elif one["File:FileType"] == "PNG":
            png.append( one )
   
         else:
#            print one["File:FileType"]
            self.logger.info( "Don't know what to do with %s" % ( one["File:FileType"] ))

#      if len( jpeg ) > 0:
#         from fileManip_jpg      import fileManipulation_jpeg 
#         j = fileManipulation_jpeg( jpeg, self.conf, self.logName ) 

#      if len( mp4 ) > 0:
#         from fileManip_mp4      import fileManipulation_mp4
#         mp = fileManipulation_mp4( mp4, self.conf, self.logName ) 

#      if len( m2ts ) > 0:
#         from fileManip_m2ts      import fileManipulation_m2ts 
#         m2 = fileManipulation_m2ts( m2ts, self.conf, self.logName ) 
      
      if len( png ) > 0:
         from fileManip_png      import fileManipulation_png
         p = fileManipulation_png( png, self.conf, self.logName ) 

