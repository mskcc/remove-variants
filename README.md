# remove_variants
This repo helps to remove simple SNV's and INDEL's called by muTect and SomaticIndelDetector from MAF where Vardict called complex event.

## Requirements:
- pandas : [v0.16.2](http://pandas.pydata.org/)
- nose : [v1.3.7](http://nose.readthedocs.io/en/latest/)

[![Build Status](https://travis-ci.org/rhshah/remove_variants.svg?branch=master)](https://travis-ci.org/rhshah/remove_variants)
[![codecov](https://codecov.io/gh/rhshah/remove_variants/branch/master/graph/badge.svg)](https://codecov.io/gh/rhshah/remove_variants)

## remove_variants.py
#### Based on Mutation Annotation Format ([MAF](https://wiki.nci.nih.gov/display/TCGA/Mutation+Annotation+Format+%28MAF%29+Specification))
- Takes in a MAF and outputs a MAF (Note: You will loose the comments if any present in the MAF file)

```
python remove_variants.py --help
usage: remove_variants.py [options]

Remove snps/indels from the output maf where a complex variant is called

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         make lots of noise
  -imaf SomeID.maf, --input-maf SomeID.maf
                        Input maf file which needs to be fixed
  -omaf SomeID.maf, --output-maf SomeID.maf
                        Output maf file name
  -o /somepath/output, --outDir /somepath/output
                        Full Path to the output dir.
                        
```