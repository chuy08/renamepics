
import logging
import os
import shutil
import sys

from exif import Image
from pprint import pprint

IGNORE_DIRS = [ ".thumbnails", "thumbnails" ]

class readExifData(object):

   def __init__(self, args):
      self.logger = logging.getLogger(__name__)
      self.args = args 

   def _removeErrors( self, meta ):
      r = [] 
      for each in meta:
         if "ExifTool:Error" not in each:
            r.append( each )
         else:
            self.logger.info( "Not a valid file: %s" % ( each["SourceFile"] ))
      self.logger.info( "Found %s files with vaild meta information" % ( len( r ) ))
      return r

   # General methods, can be overloaded
   def buildUnknownFilePath( self ):
      d = self.args["rootDir"] + "/" + self.args["outDir"] + "/" + self.args["unknown"]
      return d

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
#         print( type( one["sourcePath"] ), one["sourcePath"], type( one["origFileName"]), one["origFileName"])
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
            if self.args["rename"]:
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

   def readFiles( self ):
      if not os.path.exists( self.args.source ):
         self.logger.error("Root dir doesn't seem to be vaild")
         sys.exit( 1 )

      for root, subFolders, files in os.walk( self.args.source ):
         for one in IGNORE_DIRS:
            if one in subFolders:
               subFolders.remove( one )
         
         for fileName in files:
            absolute_path = "{}/{}".format(root, fileName)
            self.logger.debug(absolute_path)
            
            with open(absolute_path, 'rb') as image_file:
               current_image = Image(image_file)
               if current_image.has_exif:
                  file_extension = fileName.split('.')[-1].upper()
                  self.logger.debug("Absolute Path: {}, Extension: {}, Date: {}, Digitized Date: {}".format(absolute_path,
                                                                                                            file_extension,
                                                                                                            current_image.datetime_original,
                                                                                                            current_image.datetime_digitized))

                  self.identifyType( absolute_path, file_extension, current_image.datetime_original)
               else:
                  self.logger.error("No EXIF data available for: {}".format(absolute_path))

   def identifyType(self, path, extension, exif_date):
      if extension == "JPG" or extension == "JPEG":
         from .sort_jpg import sort_jpg
         s = sort_jpg(self.args, path, extension, exif_date)
         s.main()
