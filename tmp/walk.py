#!/usr/bin/python

import os

root = "/Users/chuy08/work/python/renamePics2/party"

ignore = [ '.thumbnails', 'thumbnails' ]

for root, subFolders, files in os.walk( root ):
   for one in ignore:
      if one in subFolders:
         subFolders.remove( one )

   print root, subFolders, files
