
import logging
import sys

from pprint       import pprint

from .fileManip    import fileManipulation

class fileManipulation_jpeg( fileManipulation ):

   extension = ".jpg"

   def __init__( self, meta, conf, logName ):
      fileManipulation.__init__( self, conf, logName )
      self.logger = logging.getLogger(logName+".fileManipulation_jpeg")
      self.logger.info("fileManipulation_jpeg")
      self.main( meta )

   def retPart( self, date, num ):
      # YYYY:MM:DD:HH:MM:SS where num = it's position
      return date.replace( " ", ":" ).split( ":" )[num]

   def buildNewFileName( self, date ):
      f = date.replace( " ", "_" ).replace( ":", "")
      return f + self.extension 

   def buildNewFilePath( self, date ):
      d = self.conf["rootDir"] + "/" + self.conf["outDir"] + "/" + self.retPart( date, 0 ) + "/" + self.retPart( date, 1 ) + "/" + self.retPart( date, 2 )
      return d

   def main( self, meta ):
      a = []
      good = 0 
      un = 0
      for one in meta:
         if "EXIF:CreateDate" in one:
            d = { "version" : 1
                 ,"sourcePath" : one["File:Directory"]
                 ,"origFileName" : unicode( one["File:FileName"] )
                 ,"newFilePath" : self.buildNewFilePath( one["EXIF:CreateDate"] ) 
                 ,"newFileName" : self.buildNewFileName( one["EXIF:CreateDate"] ) 
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

      self.logger.info( "Found %s valid JPEG's" % ( good ))
      self.logger.info( "Found %s unknown JPEG's" % ( un ))
      self.yahoo( a )

