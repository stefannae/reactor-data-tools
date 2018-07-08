#!/bin/bash

outputFilePath="IAEA/"

# create IAEA folder if not present
if [ ! -d "$outputFilePath" ]; then
  mkdir $outputFilePath
fi
cd $outputFilePath

# 2017 DATA - 2018 Edition
YEAR="2017"
ARCHIVE="P1828_OPEX_CD_web"
URL="https://www-pub.iaea.org/MTCD/Publications/PDF/"$ARCHIVE".zip"

# create 2017 folder if not present
if [ ! -d "$YEAR" ]; then
  mkdir $YEAR
fi
cd $YEAR

if [ -f $ARCHIVE".zip" ]
then
  echo $YEAR" data was already stored."
else
  # get 2017 data
  wget $URL
  # unpack
  unzip $ARCHIVE".zip" -d $ARCHIVE
  # convert to text
  filename="OPEX_2018_edition"
  input=$ARCHIVE"/PDF/"$filename".pdf"
  output=$ARCHIVE"/PDF/"$filename".txt"
  pdftotext $input $output
fi
cd ../..
