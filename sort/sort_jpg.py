
import logging
import sys

from .readExif import readExifData

class sort_jpg( readExifData ):
   def __init__(self, args, path, extension, exif_date):
      readExifData.__init__(self, args)
      self.logger = logging.getLogger(__name__)
      self.args = args
      self.path = path
      self.extension = extension
      self.exif_date = exif_date

   def main(self):
      splitDate = self.exif_date.split(" ")
      date = splitDate[0]
      # time = splitDate[-1]

      date_parts = date.split(":")
      date_parts.insert(0, self.args.output)

      print("/".join(date_parts))
