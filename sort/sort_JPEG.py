
import logging
import os
import shutil

from .readExif import readExifData

class sort( readExifData ):

   def __init__(self, args, exif_data):
      readExifData.__init__(self, args)
      self.logger = logging.getLogger(__name__)
      self.args = args
      self.exif_data = exif_data

   def main(self):
      create_date = self.get_create_date(self.exif_data)
      
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

      if self.args.dry_run:
         os.makedirs(dest_dir, exist_ok=True)
         shutil.copyfile(self.exif_data['SourceFile'], dest_file)
      
      self.logger.info("Copied File: {} into {}".format(self.exif_data['SourceFile'], dest_dir))
