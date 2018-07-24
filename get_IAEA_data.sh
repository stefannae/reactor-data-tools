#!/bin/bash

# . get_IAEA_data.sh 2016 P1792_OPEX_CD_web
# . get_IAEA_data.sh 2015 P1752_OPEX_CD_web

outputFilePath="IAEA/"

# create IAEA folder if not present
if [ ! -d "$outputFilePath" ]; then
  mkdir $outputFilePath
fi
cd $outputFilePath

if [ "$1" == "" ]
then
  # Default setting
  # 2017 DATA - 2018 Edition
  YEAR = "2017"
  ARCHIVE="P1828_OPEX_CD_web"
else
  YEAR="$1"
  ARCHIVE="$2"
fi

URL="https://www-pub.iaea.org/MTCD/Publications/PDF/"$ARCHIVE".zip"

# create a folder for the YEAR, if not present
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
  # should it be less than of equal to?
  if [ "$YEAR" == "2015" ]
  then
    filename="OPEX_"$(expr $YEAR + 1)""
    input=$ARCHIVE"/PDF/"$filename".pdf"
    output=$ARCHIVE"/PDF/"$filename"_edition.txt"
  else
    filename="OPEX_"$(expr $YEAR + 1)"_edition"
    input=$ARCHIVE"/PDF/"$filename".pdf"
    output=$ARCHIVE"/PDF/"$filename".txt"
  fi
  pdftotext $input $output
fi
cd ../..
