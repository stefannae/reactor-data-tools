#!/usr/bin/python

import argparse
import os.path                          # os.path.isfile()
from collections import OrderedDict
import json                             # json.dumps()

def read(year):
    """
    Parse the IAEA data
    """

    filepath = ""

    # Adapt this to search for the available data. Create a file for data sources. It will be used by both the get_IAEA_data.sh and this script.
    print "Checking available file paths for " + str(year) + " ...",
    if year == 2018:
        year_published = year + 1
        filepath += "IAEA/2018/OPEX-2019CD/PDF/"
        print "OK."
    elif year == 2017:
        year_published = year + 1
        filepath += "IAEA/2017/P1828_OPEX_CD_web/PDF/"
        print "OK."
    elif year == 2016:
        year_published = year + 1
        filepath += "IAEA/2016/P1792_OPEX_CD_web/PDF/"
        print "OK."
    elif year == 2015:
        year_published = year + 1
        filepath += "IAEA/2015/P1752_OPEX_CD_web/PDF/"
        print "OK."
    else:
        print "NO DATA."

        return 1

    filename = ""
    filename += "OPEX_"
    filename += str(year_published)
    filename += "_edition.txt"
    f = filepath + filename

    print "Searching for file at ..."
    print f
    fstat = os.path.isfile(f)

    count = 0
    previous_line = ""

    # all tags should be reset at the end of a reactor data cycle irespective of finding data or not
    yearDataTag = False
    yearLFTag = -1
    montlyLFTag = -1
    months_of_operation_tag = False
    months_parsing_space = -1
    rTypeTag = -1
    rPowerTag = -1

    rType = ""
    rPower = 0
    monthlyLF = []
    months_of_operation = []
    allLFData = False
    rYearlyData = OrderedDict()

    if fstat:
        print "Found searched file."
        with open(f, 'r') as inF:
            print "Parsing data for " + str(year) + "."
            for line in inF:
                # print line
                if "Status at end of year" in line:
                    count += 1
                    # print previous_line # reactor name
                    rNAME = previous_line.strip()
                    rYearlyData[rNAME] = {}

                if len(line) > 1:
                    previous_line = line

                if rTypeTag == 0:
                    if len(line) > 1 and ":" not in line:
                        rType = line.strip()
                        # print rType
                        rYearlyData[rNAME]["type"] = rType

                        rTypeTag = -1

                if "Reactor type and model" in line:
                    rTypeTag = 0

                if rPowerTag == 0:
                    if len(line) > 0 and ":" not in line and "MWth" in line:
                        try:
                            rPower = line[:-5].strip()
                            # print rType
                            rYearlyData[rNAME]["thermal_power"] = int(rPower)

                            rPowerTag = -1
                        except:
                            # Some grabbed values are not powers (e.g. "Gross electrical p"). Fix this!
                            pass

                if "Thermal power" in line:
                    rPowerTag = 0

                if "Annual Production Results (" + str(year) + ")" in line:
                    yearDataTag = True

                if "Annual Summary" in line:
                    months_of_operation_tag = True
                    months_parsing_space += 1

                if months_of_operation_tag:
                    if line.strip() in ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'):
                        months_of_operation.append(line.strip())
                        months_parsing_space -= 1
                    elif months_parsing_space == 3:
                        rYearlyData[rNAME]["month_operational"] = months_of_operation

                        months_of_operation = []
                        months_of_operation_tag = False
                        months_parsing_space = -1
                    else:
                        months_parsing_space += 1

                if yearDataTag:
                    if "Load Factor (LF)" in line:
                        yearLFTag = 0
                    elif "LF [%]" in line:
                        montlyLFTag = 0

                if yearLFTag == 0:
                    yearLFTag += 1
                elif yearLFTag == 1:
                    if len(line) > 1 and ":" not in line:
                        yearLF = line[:-2].strip()
                        # print yearLF
                        rYearlyData[rNAME]["year"] = float(yearLF)

                        yearLFTag = -1
                        # yearDataTag = False # this flag changes when all data for a reactor was gathered

                if montlyLFTag == 0:
                    montlyLFTag += 1
                elif montlyLFTag == 1:
                    if "OF [%]" in line:
                        print rNAME + " !!!CHECK DATA!!!"
                        allLFData = True
                    elif len(line) > 1:
                        monthlyLF.append(float(line.strip()))
                        # print monthlyLF
                    if len(monthlyLF) == 12 or allLFData:
                        rYearlyData[rNAME]["month_data"] = monthlyLF

                        montlyLFTag = -1
                        allLFData = False
                        monthlyLF = []
                        yearDataTag = False # this flag changes when all data for a reactor was gathered

        inF.close()

        debug = False # Pass it as an argument
        # debug = True # Pass it as an argument
        if debug:
            # print rYearlyData
            # for reactor in rYearlyData:
            # for reactor in rYearlyData.iteritems():
            # for (reactor, data) in rYearlyData.iteritems():
            for (reactor, data) in rYearlyData.items():
                # print reactor
                # print type(reactor), type(data)
                # print reactor, data

                print reactor, json.dumps(data, sort_keys=True, indent=4,
                    separators=(',', ': '))

                # if "CATAWBA" in reactor:
                #     print reactor, json.dumps(data, sort_keys=True, indent=4,
                #         separators=(',', ': '))


        print "Found " + str(count) + " statuses." # number of reactors in the data

        return rYearlyData

    else:
        print "Did not find the file."

        return 1

def main():
    """
    Main parser script
    """

    # Define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', '-y', type=int, default=2017,
                        dest='year', required=False,
                        help='The year of the reactor data (e.g. 2017, for IAEA data published in 2018).')

    # Parse arguments
    args = parser.parse_args()
    print(args)

    # Read data
    read(args.year)

    return 0

if __name__ == '__main__':
    main()
