#!/usr/bin/env python

import os
import re

import exiftool

from pprint import pformat

class Manipulate():

   def __init__(self):
      self.username = "chuy"
      self.dir = None
      self.file = None

   def echo(self):
      print self.username
      print self.dir
      print self.file 

   def rename_files(self, dir):
      self.get_files(dir)

   def get_files(self, dir):
      files = []
      filesDir = os.listdir(dir)
      for file in filesDir:
         if re.match(r"\w+\.", file):
            files.append(dir + "/" + file)
      self.get_metaData(files)

   def get_metaData(self, files):
      et = exiftool.ExifTool()
      et.start()
      metadata = et.get_metadata_batch(files)
      et.terminate()
      print pformat(metadata)

