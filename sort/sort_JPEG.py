
import logging
import os
import shutil
import pprint

from .readExif import readExifData

pp = pprint.PrettyPrinter(indent=4)

class sort( readExifData ):

   def __init__(self, args, exif_data):
      readExifData.__init__(self, args)
      self.logger = logging.getLogger(__name__)
      self.args = args
      self.exif_data = exif_data

   def main(self):
      create_date = None
      if 'EXIF:DateTimeOriginal' in self.exif_data:
         create_date = self.exif_data['EXIF:DateTimeOriginal']
      elif 'File:FileModifyDate' in self.exif_data:
         self.logger.info("No create date found, using file modify date")
         create_date = self.exif_data['File:FileModifyDate']
      else:
         self.logger.error("Something is wrong no time stamp found")
      
      splitDate = create_date.split(" ")
      date = splitDate[0]
      # time = splitDate[-1]

      date_parts = date.split(":")
      date_parts.insert(0, self.args.output)
      
      dest_dir = ("/".join(date_parts))
      self.logger.debug("Sorted destination: {}".format(dest_dir))

      date_parts.insert(len(date_parts), self.exif_data['File:FileName'])
      dest_file = ("/".join(date_parts))
      self.logger.debug("Sorted destination file: {}".format(dest_file))

      os.makedirs(dest_dir, exist_ok=True)
      shutil.copyfile(self.exif_data['SourceFile'], dest_file)
      self.logger.info("Copied File: {} into {}".format(self.exif_data['SourceFile'], dest_dir))
