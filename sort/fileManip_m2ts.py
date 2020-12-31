#!/usr/bin/env python

import logging
import sys

from pprint       import pprint

sys.path.append( './lib' )
from fileManip        import fileManipulation

class fileManipulation_m2ts( fileManipulation ):

   extension = '.mts'

   def __init__( self, meta, conf, logName ):
      fileManipulation.__init__( self, conf, logName )
      self.logger = logging.getLogger(logName+".fileManipulation_m2ts")
      self.logger.info("fileManipulation_m2ts")
      self.main( meta )

   def retPart( self, date, num ):
      # [ 'YYYY', 'MM', 'DD', 'HH', 'MM', 'SEC' ] - send in which is needed
      date = self.removeTZOffset( date ) 
      d = date.replace( " ", ":" )
      splitD = d.split( ":" )
#      print type( num )
      return splitD[num]

   def removeTZOffset( self, date ):
      return date.split( "-" )[0]
   
   def buildNewFileName( self, date ):
      date = self.removeTZOffset( date ) 
      return date.replace( " ", "_" ).replace( ":", "" ) + self.extension 

   def buildNewFilePath( self, date ):
      d = self.conf["rootDir"] + "/" + self.conf["outDir"] + "/" + self.retPart( date, 0 ) + "/" + self.retPart( date, 1 ) + "/" + self.retPart( date, 2 )
#      print d
      return d

   def main( self, meta ):
      a = []
      good = 0
      un = 0 
      for one in meta:
         if "File:FileModifyDate" in one:
            d = { "version" : 1
                 ,"sourcePath" : one["File:Directory"]
                 ,"origFileName" : unicode( one["File:FileName"] )
                 ,"newFilePath" : self.buildNewFilePath( one["File:FileModifyDate"] ) 
                 ,"newFileName" : self.buildNewFileName( one["File:FileModifyDate"] ) 
                }
            a.append( d )
            good += 1
         else:
            d = { "unknown" : 0 
                 ,"sourcePath" : one["File:Directory"]
                 ,"origFileName" : unicode( one["File:FileName"] )
                 ,"newFilePath" : self.buildUnknownFilePath()
                 ,"newFileName" : unicode( one["File:FileName"] ) 
                }
            a.append( d )
            un += 1

      self.logger.info( "Found %s valid M2TS's" % ( good ))
      self.logger.info( "Found %s unknown MT2S's" % ( un ))
      self.yahoo( a )
