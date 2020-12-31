
import logging
import os
import shutil

from .readExif import readExifData

class sort( readExifData ):

   def __init__(self, args, exif_date):
      readExifData.__init__(self, args)
      self.logger = logging.getLogger(__name__)
      self.args = args
      self.exif_date = exif_date

   def main(self):
      print("Hi chuy!!!")
      #file_name = (self.path.split("/")[-1])

      #splitDate = self.exif_date.split(" ")
      #date = splitDate[0]
      # time = splitDate[-1]

      #date_parts = date.split(":")
      #date_parts.insert(0, self.args.output)
      
      #dest_dir = ("/".join(date_parts))
      #self.logger.debug("Sorted destination: {}".format(dest_dir))

      #date_parts.insert(len(date_parts), file_name)
      #dest_file = ("/".join(date_parts))
      #self.logger.debug("Sorted destination file: {}".format(dest_file))

      #os.makedirs(dest_dir, exist_ok=True)
      #shutil.copyfile(self.path, dest_file)
      #self.logger.info("Copied File: {} into {}".format(self.path, dest_dir))
