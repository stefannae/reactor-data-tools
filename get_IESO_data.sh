#!/bin/bash

outputFilePath="IESO/"

# create IESO folder if not present
if [ ! -d "$outputFilePath" ]; then
  mkdir $outputFilePath
fi
cd $outputFilePath

# '-m' OR '--mirror' are equivalent to ‘-r -N -l inf --no-remove-listing’
# meaning (recursive, new, depth, with .listing)
# '--no-parent' means do not ascend to parent directory (if recursive)
wget --mirror --no-parent reports.ieso.ca/public/GenOutputCapability/
cd ..
