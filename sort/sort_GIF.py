
import logging
import sys

import pprint

from .readExif import readExifData

pp = pprint.PrettyPrinter(indent=4)

class sort(readExifData):

   def __init__(self, args, exif_data):
      readExifData.__init__( self, args )
      self.logger = logging.getLogger(__name__)
      self.args = args
      self.exif_data = exif_data

   def main(self):
      pp.pprint(self.exif_data)
      create_date = self.get_create_date(self.exif_data)
      print("Chuy Create Date: {}".format(create_date))
