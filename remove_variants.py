#!/usr/bin/python
'''
@Description : This tool helps to remove simple snvs/indels called by muTect and SomaticIndelDetector in regions where VarDict calls ComplexVariants . 
@Created :  05/02/2017
@Updated : 05/02/2017
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
    logger.warning("remove_variants: coloredlogs is not installed, please install it if you wish to see color in logs on standard out.")
    pass
try:
    import pandas as pd
except ImportError:
    logger.fatal("remove_variants: pandas is not installed, please install pandas as it is required to run the removing process.")
    sys.exit(1)

def main():
   parser = argparse.ArgumentParser(prog='filter_mutect.py', description='Remove snps/indels from the output maf where a complex variant is called', usage='%(prog)s [options]')
   parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="make lots of noise")
   parser.add_argument("-imaf", "--inputMaf", action="store", dest="inputMaf", required=True, type=str, metavar='SomeID.maf', help="Input maf file which needs to be fixed")
   parser.add_argument("-omaf","--outputMaf",action="store", dest="inputMaf", required=True, type=str, metavar='SomeID.maf', help="Output maf file name"))
   parser.add_argument("-o", "--outDir", action="store", dest="outdir", required=False, type=str, metavar='/somepath/output', help="Full Path to the output dir.")
   
   args = parser.parse_args()
   if(args.verbose):
       logger.info("remove_variants: Started the run for removing simple variants.")
   (cvDF,mafDF) =read_maf(args)
   (posToCheck) = make_coordinate_for_complex_variants(cvDF);
   if(args.verbose):
       logger.info("remove_variants: Finished the run for removing simple variants.")

def read_maf(args):
    dataDF = pd.read_table(args.inputMaf, comment="#", low_memory=False)
    complex_variant_dataDF = dataDF.loc[dataDF['TYPE'] == "Complex"]
    return(complex_variant_dataDF,dataDF)

def make_coordinate_for_complex_variants(cvDF):
    posistions_to_check = pd.DataFrame(columns=["Chromosome","Start"])
    for index, row in cv.iterrows():
        chr = row.loc['Chromosome']
        start = row.loc['Start']
        end = row.loc['End']
        for i in range(start:end):
            print i
if __name__ == "__main__":
    start_time = time.time()  
    main()
    end_time = time.time()
    totaltime = end_time - start_time
    logging.info("remove_variants: Elapsed time was %g seconds", totaltime)
    sys.exit(0)
