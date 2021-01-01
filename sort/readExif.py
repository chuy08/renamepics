
import importlib
import logging
import os
import shutil
import sys

from .exiftool import ExifTool

IGNORE_DIRS = [ ".thumbnails", "thumbnails" ]

class readExifData(object):

   def __init__(self, args):
      self.logger = logging.getLogger(__name__)
      self.args = args 

   def _get_exif(self, file):
      et = ExifTool()
      et.start()
      exif_data = et.get_metadata(file)
      et.terminate()
      self.logger.debug("Exif information: {}".format(exif_data))
      return exif_data

   # General methods, can be overloaded
   def get_create_date(self, exif_data):
      create_date = None
      if 'EXIF:DateTimeOriginal' in exif_data:
         create_date = exif_data['EXIF:DateTimeOriginal']
      elif 'File:FileModifyDate' in exif_data:
         self.logger.info("No create date found for {}, using file modify date".format(exif_data['SourceFile']))
         create_date = exif_data['File:FileModifyDate']
      else:
         self.logger.error("Something is wrong, no time stamp found")
      
      return create_date

   def parse_date(self, date, filename):
      splitDate = date.split(" ")
      date = splitDate[0]
      # time = splitDate[-1]

      date_parts = date.split(":")
      date_parts.insert(0, self.args.output)
      
      dest_dir = ("/".join(date_parts))
      self.logger.debug("Sorted destination: {}".format(dest_dir))

      date_parts.insert(len(date_parts), filename)
      dest_file = ("/".join(date_parts))
      self.logger.debug("Sorted destination file: {}".format(dest_file))

      return dest_dir, dest_file

   # Entrypoint
   def readFiles(self):
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
            exif_data = self._get_exif(absolute_path)
            
            module_name = "sort.sort_{}".format(exif_data['File:FileType'])
            self.logger.debug("Importing module: {}".format(module_name))
            
            i = None
            try:
               i = importlib.import_module(module_name)
            except ImportError as err:
               self.logger.error('File Name: {} of FileType: {} caused error: {}'.format(fileName, exif_data['File:FileType'], err))
            
            if i:
               s = i.sort(self.args, exif_data)
               s.main()
