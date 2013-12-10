#!/usr/bin/env python

import logging
import sys

from pprint       import pprint

sys.path.append( './lib' )
from fileManip        import fileManipulation

class fileManipulation_m2ts( fileManipulation ):

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
      return date.replace( " ", "_" ).replace( ":", "" )

   def buildNewFilePath( self, meta ):
      d = self.conf["rootDir"] + "/" + self.conf["outDir"] + "/" + self.retPart( meta["File:FileModifyDate"], 0 ) + "/" + self.retPart( meta["File:FileModifyDate"], 1 ) + "/" + self.retPart( meta["File:FileModifyDate"], 2 )
#      print d
      return d

   def main( self, meta ):
#      pprint( meta )
      a = []
      for one in meta:
         if "File:FileModifyDate" in one:
            d = { "sourcePath" : one["File:Directory"]
                 ,"origFileName" : unicode( one["File:FileName"] )
                 ,"year" : self.retPart( one["File:FileModifyDate"], 0 ) 
                 ,"month" : self.retPart( one["File:FileModifyDate"], 1 ) 
                 ,"day" : self.retPart( one["File:FileModifyDate"], 2 )
                 ,"newFilePath" : self.buildNewFilePath( one ) 
                 ,"newFileName" : self.buildNewFileName( one["File:FileModifyDate"] ) 
                }
            a.append( d )
         else:
            self.logger.info( "No CreateDate: %s" % ( one["SourceFile"] )) 

#      print a
      self.yahoo( a )
