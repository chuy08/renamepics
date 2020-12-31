
import argparse
import json
import logging
import sys

from .__init__ import __version__
from .readExif import readExifData

def main():
   parser = argparse.ArgumentParser(description='Picture Sorter')

   parser.add_argument('--debug',
                        help="Enable Debug",
                        action='store_true',
                        default=False)

   parser.add_argument('--output',
                        help="Output Directory (debugging only)",
                        type=str,
                        default='/output')

   parser.add_argument('--source',
                        help="Source Directory (debugging only)",
                        type=str,
                        default='/work')

   parser.add_argument('--version',
                       action='version',
                       version='%(prog)s {}'.format(__version__))

   args = parser.parse_args()

   # Instantiate logger stream to stdout
   if args.debug:
      logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                          stream=sys.stdout,
                          level=logging.DEBUG)
   else:
      logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                          stream=sys.stdout,
                          level=logging.INFO)

   logging.info("Start picture sorting")

   fm = readExifData(args)
   fm.readFiles()
   
   logging.info( "Finished..." )


if __name__ == "__main__":
   main()
