#!/usr/bin/env python

import logging
import os
import shutil
import argparse

from os.path import isfile, join
from pprint import pprint

import exiftool

logging.basicConfig(filename='testtest.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s')

### Global Variables
__directory = None 
__outDir = 'output'

parser = argparse.ArgumentParser( description='Sort pictures by EXIF created date' )
parser.add_argument( '-d', '--directory', default=__directory, help="Directory of pictures to parse" )
parser.add_argument( '-o', '--output', default=__outDir, help="Folder where sorted pictures go" )
parser.add_argument( '-c', '--create', action='store_true', help="By default we only log things, set this flag to actually do things." )
parser.add_argument( '-v', '--verbose', action='store_true', help="Print helpful debugging things" )

args = parser.parse_args()
directory = args.directory
outDir = args.output

if directory is None:
   print "I need a directory of pictures for this to work"
   exit(1)

def get_files(dir):
   return [ f for f in os.listdir(directory) if isfile(join(directory, f)) ]

def absFileName(names):
   absFiles = []
   for file in names:
      afile = directory + "/" + file
      absFiles.append(afile)
   return absFiles

def getMetaData(files):
   et = exiftool.ExifTool()
   et.start()
   metadata = et.get_metadata_batch(files)
   et.terminate()
   return metadata

def newDirName(date):
   date = date.replace(' ', ':')
   split = date.split(":")
   yyyy = split[0]
   subdir = split[0] + "_" + split[1] + "_" + split[2]
   newdir = directory + "/" + outDir + "/" + yyyy + "/" + subdir
   return newdir 

def createDir(newdir, args):
   if os.path.exists(newdir):
      pass
#      logging.info("Directory exists, moving on to next one %s", newdir)

   else:
      logging.info("Creating directory %s", newdir)
      if args.create:
         os.makedirs(newdir)
      
def copyFile(newdir, each, args):
   orig = each["File:Directory"] + "/" + each["File:FileName"] 
   backup = newdir + "/" + each["File:FileName"]
   logging.info("%s Copying file %s", i, each["File:FileName"])
   if args.create:
      shutil.copy2(orig, backup)

logging.info("### START ###")

if not args.create:
   logging.info("DRY RUN ONLY, we won't actually move anything")

onlyfiles = get_files(dir)
logging.info("Found %s files to process", len(onlyfiles))

afile = absFileName(onlyfiles)

metadata = getMetaData(afile)

i = 1 
for each in metadata:
   if 'ExifTool:Error' in each:
      logging.info("%s Skipping this %s - %s", i, each["File:FileName"], each["ExifTool:Error"])
      error = directory + "/" + outDir + "/error"
      createDir(error, args)
      backup = error + "/" + each["File:FileName"]

      if args.create:
         shutil.copy(each["SourceFile"], backup)
      i += 1

   elif 'EXIF:DateTimeOriginal' in each:
#   elif 'EXIF:CreateDate' in each:
      newdir = newDirName(each["EXIF:DateTimeOriginal"])
      createDir(newdir, args)
      copyFile(newdir, each, args)
      i += 1

   elif 'QuickTime:MediaCreateDate' in each:
      newdir = newDirName( each["QuickTime:MediaCreateDate"] )
      createDir(newdir, args)
      copyFile(newdir, each, args)
      i += 1

   else:
      if args.verbose:
         pprint(each)
      logging.info("### HOUSTWEHAVEAPROBLEM ###") 
      logging.info("%s %s", i, each["SourceFile"]) 
      unknown = directory + "/" + outDir + "/unknown" 
      createDir(unknown, args)
      backup = unknown + "/" + each["File:FileName"]
     
      if args.create:
         shutil.copy(each["SourceFile"], backup)
      i += 1


logging.info("### END ###")
