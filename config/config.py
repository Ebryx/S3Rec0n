from config import *
from sys import argv

"""
------------------------------------------------------------------
						Argparse Variables
------------------------------------------------------------------
"""

version 	= "1.0"

_usage 		= f"\r{w}[{c}#{w}] Usage: python {g}{argv[0]}{w} --bucket myTestBucket --all"
_version 	= "{}[{}~{}] {}Version: {}{}".format(w,c,w,w,g,version)
