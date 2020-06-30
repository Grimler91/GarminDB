#!/usr/bin/env python3

"""Script for importing into a DB and summarizing CSV formatted TomTom export data."""

__author__ = "Henrik Grimler"
__copyright__ = "Copyright Henrik Grimler"
__license__ = "GPL"

import sys
import argparse
import logging


import TomTomDB
from import_tomtom_csv import TomTomData
from analyze_tomtom import Analyze
import garmin_db_config_manager as GarminDBConfigManager
from version import format_version


logging.basicConfig(filename='tomtom.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))
root_logger = logging.getLogger()


def usage(program):
    """Print the usage info for the script."""
    print('%s -i <inputfile> ...' % program)
    sys.exit()


def main(argv):
    """Import into a DB and summarize CSV formatted TomTom export data."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="print the program's version", action='version', version=format_version(sys.argv[0]))
    parser.add_argument("-t", "--trace", help="Turn on debug tracing", type=int, default=0)
    modes_group = parser.add_argument_group('Modes')
    modes_group.add_argument("-i", "--input_file", help="Specifiy the CSV file to import into the database")
    modes_group.add_argument("--delete_db", help="Delete TomTom db file.", action="store_true", default=False)
    args = parser.parse_args()

    root_logger = logging.getLogger()
    if args.trace > 0:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    db_params = GarminDBConfigManager.get_db_params()

    if args.delete_db:
        TomTomDB.TomTomDB.delete_db(db_params)
        sys.exit()

    tomtom_dir = GarminDBConfigManager.get_or_create_tomtom_dir()
    metric = GarminDBConfigManager.get_metric()
    fd = TomTomData(args.input_file, tomtom_dir, db_params, metric, args.trace)
    if fd.file_count() > 0:
        fd.process_files()

    analyze = Analyze(db_params)
    analyze.get_years()
    analyze.summary()


if __name__ == "__main__":
    main(sys.argv[1:])
