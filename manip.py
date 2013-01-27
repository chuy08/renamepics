#!/usr/bin/env python

import os
import re
import logging

import exiftool

from pprint import pformat

class Manipulate():

   def __init__(self):
      self.logger = self.set_logging() 

   def echo(self):
      print self.username

   def set_logging(self):
      logger = logging.getLogger('myapp')
      hdlr = logging.FileHandler('/tmp/testtest.log')
      logger.setLevel(logging.WARNING)
      logger.info("Works?")

   def get_files(self, dir):
      files = []
      filesDir = os.listdir(dir)
      for file in filesDir:
         if re.match(r"\w+\.", file):
            files.append(dir + "/" + file)
      return files

   def get_metaData(self, dir):
      files = self.get_files(dir)
      et = exiftool.ExifTool()
      et.start()
      metadata = et.get_metadata_batch(files)
      et.terminate()
      return metadata

   def rename_files(self, dir):
      metadata = self.get_metaData(dir)
      for k in metadata:
#         self.logger.info(k["File:MIMEType"])
         print k["File:MIMEType"]
