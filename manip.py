#!/usr/bin/env python

import os
import re
import logging

import exiftool

from pprint import pformat

logging.basicConfig(filename='/tmp/testtest.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s')

class Manipulate():

   def echo(self):
      print self.username

   def get_files(self, dir):
      logging.info("Found %s files to process", len(dir))
      files = []
      filesDir = os.listdir(dir)
      for file in filesDir:
         if re.match(r"\w+\.", file):
            files.append(dir + "/" + file)
            logging.info("File processed: %s", file)
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
         logging.info("MIME Type : %s", k["File:MIMEType"])
