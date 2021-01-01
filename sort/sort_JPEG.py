
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
      dest_dir, dest_file = self.parse_date(create_date, self.exif_data['File:FileName'])

      if self.args.dry_run:
         os.makedirs(dest_dir, exist_ok=True)
         shutil.copyfile(self.exif_data['SourceFile'], dest_file)
      
      self.logger.info("Copied File: {} into {}".format(self.exif_data['SourceFile'], dest_dir))
