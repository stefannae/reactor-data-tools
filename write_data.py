#!/usr/bin/python

import argparse
import os.path                          # os.path.isfile
from collections import OrderedDict
import json

from parse_IAEA_data import read

def write_to_json():
    """
    Write data in csv format
    """

def write_to_csv():
    """
    Write data in csv format
    """

def write_to_ratdb(inData, year, month=''):
    """
    Write data with RATDB standard in JSON format
    """

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_index = None
    const_index = None

    # if month is not '':
    if month in months:
        const_index = months.index(month)
    else:
        print('Could not parse the month input.')
        return 0

    if isinstance(inData, dict):
        ratdbTypes = ["PHWR", "PWR", "BWR", "LWGR", "GCR", "FBR"]

        reactors = {}
        previous_reactor = ""

        for (reactor, data) in inData.items():

            if const_index is not None:
                month_index = const_index
                # month_index = const_index.copy()
                try:
                    if months[month_index] in data["month_operational"]:
                        if data['month_operational'].index(month) != month_index:
                            print('Month index correction for reactor {}.'.format(reactor))
                            month_index = data['month_operational'].index(month)

                            if len(data['month_operational']) != len(data["month_data"]):
                                print('Check inconsistent data! We need a correction for zero padding (when there are 0 loading factors, sometimes there are not associated month names). There is/are {} 0 value/s in data.'.format(data["month_data"].count(0)))
                    else:
                        print('Reactor {} was not operational during {}.'.format(reactor, month))
                        continue
                except:
                    print(months[month_index], data["month_operational"])
                    continue

            # print reactor, data
            # if previous_reactor in [reactor[:-2], reactor]:
            if previous_reactor == reactor[:-2] or previous_reactor == reactor:
                reactors[previous_reactor]["no_cores"] += 1
                if month_index is not None:
                    power = "{x:6.2f}".format(x=data["month_data"][month_index]*data["thermal_power"]/100.)
                else:
                    power = "{x:6.2f}".format(x=data["year"]*data["thermal_power"]/100.)
                # reactors[previous_reactor]["core_power"].append(data["year"]*data["thermal_power"]/100.)
                reactors[previous_reactor]["core_power"].append(float(power))
                # reactors[previous_reactor]["core_spectrum"].append(data["type"])
                foundSpectrum = False
                for spectrum in ratdbTypes:
                    if spectrum in data["type"]:
                        foundSpectrum = True
                        reactors[previous_reactor]["core_spectrum"].append(spectrum)
                        break

                if foundSpectrum is not True:
                    print "Could not find spectrum for " + data["type"] + "."

            else:
                separator = "-"
                if reactor[-2:-1] == separator:
                    try:
                        isinstance(int(reactor[-1:]),int)
                        name = reactor[:-2]
                    except:
                        name = reactor
                else:
                    name = reactor
                # name = reactor[:-2]

                reactors[name] = OrderedDict()
                reactors[name]["type"] = "REACTOR_STATUS"
                reactors[name]["version"] = 1
                reactors[name]["index"] = name
                reactors[name]["run_range"] = [0,0]
                reactors[name]["pass"] = 0
                reactors[name]["comment"] = ""
                reactors[name]["timestamp"] = ""
                reactors[name]["no_cores"] = 1
                if month_index is not None:
                    power = "{x:6.2f}".format(x=data["month_data"][month_index]*data["thermal_power"]/100.)
                else:
                    power = "{x:6.2f}".format(x=data["year"]*data["thermal_power"]/100.)
                # reactors[name]["core_power"] = [data["year"]*data["thermal_power"]/100.]
                reactors[name]["core_power"] = [float(power)]
                # reactors[name]["core_spectrum"] = [data["type"]]
                foundSpectrum = False
                for spectrum in ratdbTypes:
                    if spectrum in data["type"]:
                        foundSpectrum = True
                        reactors[name]["core_spectrum"] = [spectrum]
                        break

                if foundSpectrum is not True:
                    print "Counld not find spectrum for " + data["type"] + "."

                previous_reactor = name

        # print json.dumps(reactors, sort_keys=False, indent=2,
        #     separators=(',', ': '))

        debug = False # Pass it as an argument
        # debug = True # Pass it as an argument
        if debug:
            reactors = OrderedDict(sorted(reactors.items(), key=lambda t: t[0]))
            for reactor, data in reactors.items():
                # print reactor
                print "{"
                for key, value in data.items():
                    if isinstance(value, str):
                        print('{a}: "{b}",'.format(a=key,b=value))
                    else:
                        print('{a}: {b},'.format(a=key,b=value))
                print "}\n"

        if month_index is not None:
            f = "REACTORS_STATUS_{}_{}.ratdb".format(year, months[month_index])
        else:
            f = "REACTORS_STATUS_{}.ratdb".format(year)
        with open(f, 'w') as outF:
            reactors = OrderedDict(sorted(reactors.items(), key=lambda t: t[0]))
            for reactor, data in reactors.items():
                # print reactor
                outF.write("{\n")
                for key, value in data.items():
                    if isinstance(value, str):
                        outF.write('{a}: "{b}",\n'.format(a=key,b=value))
                    elif isinstance(value, list) and isinstance(value[0], str):
                        outF.write('{a}: '.format(a=key))
                        temp_string = "["
                        for item in value:
                            temp_string += '"{}", '.format(item)
                        outF.write(temp_string[:-2])
                        outF.write('],\n')
                    else:
                        outF.write('{a}: {b},\n'.format(a=key,b=value))

                outF.write("}\n\n")

        outF.close()
        # return 0
    else:
        print "Invalid input!"
        return 1

def main():
    """
    Main script for writing
    """

    # Define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', '-y', type=int, default=2017,
                        dest='year', required=False,
                        help='The year of the reactor data (e.g. 2017, for IAEA data published in 2018).')
    parser.add_argument('--month', '-m', type=str, default='',
                        dest='month', required=False,
                        help="The month as in ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec') for the requested data.")
    # parser.add_argument('--format', '-f', type=str, default="RATDB",
    #                     dest='format', required=True,
    #                     help='The standard of the data in the output file.')

    # Parse arguments
    args = parser.parse_args()
    print(args)

    # Write data
    write_to_ratdb(read(args.year), args.year, args.month)

if __name__ == '__main__':
    main()
