
import logging
import os
import sys
import shutil

from .readExif import readExifData

class sort(readExifData):

   def __init__(self, args, exif_data):
      readExifData.__init__( self, args )
      self.logger = logging.getLogger(__name__)
      self.args = args
      self.exif_data = exif_data

   def main(self):
      print("From GIF chuy")
