#!/usr/bin/env python

import exiftool
import json
import os
import re

from pprint import pprint
from pprint import pformat

dir = "/Users/jorosco/Downloads/DCIM/GS2/Camera"
#dir = "/Users/jorosco/Downloads/DCIM/Camera"

#files = os.listdir("/Users/jorosco")
#files = ["P1010679.JPG", "P1010680.JPG"]

def get_files(dir):
   files = []
   filesDir = os.listdir(dir)
   for file in filesDir:
      if re.match(r"\w+\.", file):
         files.append(dir + "/" + file)
   return files

def get_mimeType(files):
   et = exiftool.ExifTool()
   et.start()
   metadata = et.get_metadata_batch(files)
   print pformat(metadata)
   et.terminate()

files = get_files(dir)
get_mimeType(files)


#et = exiftool.ExifTool()
#et.start()
#metadata = et.get_metadata_batch(files)
#print pformat(metadata)
#et.terminate()


#with exiftool.ExifTool() as et:
#    metadata = et.get_metadata_batch(files)
#    print pformat(metadata)
#    for d in metadata:
#       print d["File:MIMEType"]
#        print("{:20.20} {:20.20}".format(d["SourceFile"],
#                                         d["EXIF:DateTimeOriginal"]))
