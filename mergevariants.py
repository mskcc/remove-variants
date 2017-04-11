#!/usr/bin/python
'''
@Description : This tool helps to filter muTect v1.14 txt and vcf through command line. 
@Created :  07/17/2016
@Updated : 03/17/2017
@author : Ronak H Shah

'''
from __future__ import division
import argparse
import sys
import os
import time
import logging

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.DEBUG)
logger = logging.getLogger('filter_mutect')
try:
    import coloredlogs
    coloredlogs.install(level='DEBUG')
except ImportError:
    logger.warning("filter_mutect: coloredlogs is not installed, please install it if you wish to see color in logs on standard out.")
    pass
try:
    import vcf
except ImportError:
    logger.fatal("filter_mutect: pyvcf is not installed, please install pyvcf as it is required to run the mapping.")
    sys.exit(1)
try:
    import pandas as pd
except ImportError:
    logger.fatal("filter_mutect: pandas is not installed, please install pandas as it is required to run the mapping.")
    sys.exit(1)

def main():
   parser = argparse.ArgumentParser(prog='filter_mutect.py', description='Filter snps from the output of muTect v1.14', usage='%(prog)s [options]')
   parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="make lots of noise")
   parser.add_argument("-ivcf", "--inputVcf", action="store", dest="inputVcf", required=True, type=str, metavar='SomeID.vcf', help="Input vcf muTect file which needs to be filtered")
   parser.add_argument("-itxt", "--inputTxt", action="store", dest="inputTxt", required=True, type=str, metavar='SomeID.txt', help="Input txt muTect file which needs to be filtered")
   parser.add_argument("-tsn", "--tsampleName", action="store", dest="tsampleName", required=True, type=str,metavar='SomeName', help="Name of the tumor Sample")
   parser.add_argument("-dp", "--totaldepth", action="store", dest="dp", required=False, type=int, default=0, metavar='0', help="Tumor total depth threshold")
   parser.add_argument("-ad", "--alleledepth", action="store", dest="ad", required=False, type=int, default=5, metavar='5', help="Tumor allele depth threshold")
   parser.add_argument("-tnr", "--tnRatio", action="store", dest="tnr", required=False, type=int, default=5, metavar='5', help="Tumor-Normal variant frequency ratio threshold ")
   parser.add_argument("-vf", "--variantfrequency", action="store", dest="vf", required=False, type=float, default=0.01, metavar='0.01', help="Tumor variant frequency threshold ")
   parser.add_argument("-hvcf", "--hotspotVcf", action="store", dest="hotspotVcf", required=False, type=str, metavar='hostpot.vcf', help="Input bgzip / tabix indexed hotspot vcf file to used for filtering")
   parser.add_argument("-o", "--outDir", action="store", dest="outdir", required=False, type=str, metavar='/somepath/output', help="Full Path to the output dir.")
   
   args = parser.parse_args()
   if(args.verbose):
       logger.info("Started the run for doing standard filter.")
   (stdfilterVCF) = RunStdFilter(args)
   if(args.verbose):
       logger.info("Finished the run for doing standard filter.")