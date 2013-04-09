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
      logging.info("#### Start of rename job ####")
      logging.info("Found %s files to process", len(dir))
      files = []
      filesDir = os.listdir(dir)
      for file in filesDir:
         if re.match(r"\w+\.", file):
            files.append(dir + "/" + file)
            logging.info("File processed: %s", file)
         else:
            logging.warning("We omit this: %s", file)
      return files

   def get_metaData(self, dir):
      files = self.get_files(dir)
      et = exiftool.ExifTool()
      et.start()
      metadata = et.get_metadata_batch(files)
      et.terminate()
      return metadata

   def file_type(self, file):
      if ( file["File:MIMEType"] == "image/jpeg" ):
         if ( "EXIF:ModifyDate" in file ):
#            print "Yes"
            print file["File:FileName"]
            print file["EXIF:ModifyDate"]
            print "\n"
         else:
            logging.info("Doesn't have ModifyDate Tag : %s", file["SourceFile"])

#         print file["SourceFile"] 
#         print pformat(file)
#          print file["File:FileName"]
#          print file["EXIF:ModifyDate"]
#          print "\n"
      else:
         logging.info("I don't know what to do with this : %s", file["SourceFile"])

   def rename_files(self, dir):
      metadata = self.get_metaData(dir)
      for file in metadata:
#         print pformat(file)
#         logging.info("MIME Type : %s", file["File:MIMEType"])
         self.file_type(file)
      logging.info("#### End Job ####")
