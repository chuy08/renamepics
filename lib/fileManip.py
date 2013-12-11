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

   def buildUnknownFilePath( self ):
      d = self.conf["rootDir"] + "/" + self.conf["outDir"] + "/" + self.conf["unknown"]
      return d

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
         if "version" in one:
            try:
               os.makedirs( one["newFilePath"] )
            except:
               pass

         elif "unknown" in one:
            try:
               os.makedirs( one["newFilePath"] )
            except:
               pass 
         else:
            self.logger.warn( "I don't know what to do?" )

   def copyFile( self, files ):
#      pprint( files)
      for one in files:
#         print type( one["sourcePath"] ), one["sourcePath"], type( one["origFileName"]), one["origFileName"]
         orig = os.path.join( one["sourcePath"], one["origFileName"] )
         if "version" in one:
            try:
               shutil.copy2( orig, one["newFilePath"] ) 
            except:
               self.logger.info( "Copy failed for: %s" % ( orig ))

         elif "unknown" in one:
            #newdir = self.rootdir + "/" + self.outdir + "/" + self.unknown
            try:
               shutil.copy2( orig, one["newFilePath"] )
            except:
               self.logger.info( "Copy failed for: %s" % ( orig ))

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
      mov = []
      gif = []
      instagram = []
      music = []
      threegp = []
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
         elif one["File:FileType"] == "MOV":
            mov.append( one )
         elif one["File:FileType"] == "GIF":
            gif.append( one )
         elif one["File:FileType"] == "3GP":
            threegp.append( one )
         elif one["File:FileType"] == "WEBM" and 'instagram' in one["Matroska:WritingApp"]:
            instagram.append( one )
         elif one["File:FileType"] in self.conf["music"]:
            music.append( one ) 
   
         else:
#            print one["File:FileType"]
            self.logger.info( "Don't know what to do with %s" % ( one["File:FileType"] ))

      if len( jpeg ) > 0:
         from fileManip_jpg      import fileManipulation_jpeg 
         fileManipulation_jpeg( jpeg, self.conf, self.logName ) 

      if len( mp4 ) > 0:
         from fileManip_mp4      import fileManipulation_mp4
         fileManipulation_mp4( mp4, self.conf, self.logName ) 

      if len( m2ts ) > 0:
         from fileManip_m2ts      import fileManipulation_m2ts 
         fileManipulation_m2ts( m2ts, self.conf, self.logName ) 
      
      if len( png ) > 0:
         from fileManip_png      import fileManipulation_png
         fileManipulation_png( png, self.conf, self.logName ) 

      if len( mov ) > 0:
         from fileManip_mov      import fileManipulation_mov
         fileManipulation_mov( mov, self.conf, self.logName ) 

      if len( gif ) > 0:
         from fileManip_gif      import fileManipulation_gif
         fileManipulation_gif( gif, self.conf, self.logName ) 

      if len( music ) > 0:
         from fileManip_music      import fileManipulation_music
         fileManipulation_music( music, self.conf, self.logName ) 

      if len( instagram ) > 0:
         from fileManip_instagram      import fileManipulation_instagram
         fileManipulation_instagram( instagram, self.conf, self.logName ) 

      if len( threegp ) > 0:
         from fileManip_threegp      import fileManipulation_threegp
         fileManipulation_threegp( threegp, self.conf, self.logName ) 

