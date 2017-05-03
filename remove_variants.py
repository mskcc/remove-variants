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
   parser = argparse.ArgumentParser(prog='remove_variants.py', description='Remove snps/indels from the output maf where a complex variant is called', usage='%(prog)s [options]')
   parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="make lots of noise")
   parser.add_argument("-imaf", "--input-maf", action="store", dest="inputMaf", required=True, type=str, metavar='SomeID.maf', help="Input maf file which needs to be fixed")
   parser.add_argument("-omaf","--output-maf",action="store", dest="outputMaf", required=True, type=str, metavar='SomeID.maf', help="Output maf file name")
   parser.add_argument("-o", "--outDir", action="store", dest="outdir", required=False, type=str, metavar='/somepath/output', help="Full Path to the output dir.")
   
   args = parser.parse_args()
   if(args.verbose):
       logger.info("remove_variants: Started the run for removing simple variants.")
   (cvDF,mafDF) =read_maf(args)
   (posToCheck) = make_coordinate_for_complex_variants(cvDF)
   (cleanDF) = remove_variants(posToCheck,mafDF)
   write_output(args,cleanDF)
   if(args.verbose):
       logger.info("remove_variants: Finished the run for removing simple variants.")

def read_maf(args):
    dataDF = pd.read_table(args.inputMaf, comment="#", low_memory=False)
    complex_variant_dataDF = dataDF.loc[dataDF['TYPE'] == "Complex"]
    return(complex_variant_dataDF,dataDF)

def make_coordinate_for_complex_variants(cvDF):
    positions_to_check = pd.DataFrame(columns=["Chromosome","Start"])
    count = 0
    for index, row in cvDF.iterrows():
        chr = row.loc['Chromosome']
        start = row.loc['Start_Position']
        end = row.loc['End_Position']
        for i in range(start,end+1):
            positions_to_check.loc[count,["Chromosome","Start"]]=[chr,i]
            count = count + 1
    return(positions_to_check)

def remove_variants(positions_to_check,all_variants_df):
    all_variants_df_copy = all_variants_df.copy()
    drop_index = list()
    for i_index, i_row in all_variants_df.iterrows():
        m_chr = i_row.loc['Chromosome']
        m_start = i_row.loc['Start_Position']
        m_end = i_row.loc['End_Position']
        m_type = i_row.loc['TYPE']
        flag = False
        if(m_type != "Complex"):
            specific_chr_df = positions_to_check.loc[positions_to_check['Chromosome'] == m_chr]
            if((specific_chr_df["Start"] == m_start).any()):
                flag = True
                drop_index.append(i_index)
    all_variants_df_copy2 = all_variants_df_copy.drop(all_variants_df_copy.index[drop_index])
    return(all_variants_df_copy2)

def write_output(args,output_DF):
    if(args.outdir):
        outFile = os.path.join(args.outdir,args.outputMaf)
    else:
        outFile = os.path.join(os.getcwd(),args.outputMaf)
    output_DF.to_csv(outFile, sep='\t', index=False)
    
if __name__ == "__main__":
    start_time = time.time()  
    main()
    end_time = time.time()
    totaltime = end_time - start_time
    logging.info("remove_variants: Elapsed time was %g seconds", totaltime)
    sys.exit(0)
