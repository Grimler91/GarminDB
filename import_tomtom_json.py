"""A script for importing CSV formatted TomTom export data."""

__author__ = "Henrik Grimler"
__copyright__ = "Copyright Henrik Grimler"
__license__ = "GPL"

import sys
import logging
from tqdm import tqdm

from utilities import CsvImporter
import TomTomDB
from utilities import FileProcessor


logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


class TomTomData(object):
    """A object for importing JSON formatted TomTom export data."""

    cols_map = {
        'aggregates.active_time_daily': ('active_hours', CsvImporter.map_integer),
        'aggregates.distance_daily': ('distance', CsvImporter.map_float),
        'aggregates.steps_daily': ('steps', CsvImporter.map_integer),
        'aggregates.metabolic_energy_daily': ('calories', CsvImporter.map_kilojoule),
        sleep_unknown_daily
        sleep_asleep_daily
        sleep_restless_daily
        'aggregates.hr_avg_daily': ('hr_avg', CsvImporter.map_integer),
        'aggregates.hr_min_daily': ('hr_min', CsvImporter.map_integer),
        'aggregates.hr_max_daily': ('hr_max', CsvImporter.map_integer),
        hr_zones_daily
        resting_hr_weekly
        resting_hr_daily
        muscle_daily
        'aggregates.fat_daily': ('body_fat', CsvImporter.map_float),
        'aggregates.weight_daily': ('weight', CsvImporter.map_kgs),
        vo2_max_daily
        vo2_max_min_daily
        activity_score_daily
        'activities-activityCalories': ('activities_calories', CsvImporter.map_integer),
        'sleep-minutesAfterWakeup': ('after_wakeup_mins', CsvImporter.map_integer),
        'activities-minutesFairlyActive': ('fairly_active_mins', CsvImporter.map_integer),
        'sleep-efficiency': ('sleep_efficiency', CsvImporter.map_integer),
        'sleep-timeInBed': ('in_bed_mins', CsvImporter.map_integer),
        'activities-minutesVeryActive': ('very_active_mins', CsvImporter.map_integer),
        'activities-minutesSedentary': ('sedentary_mins', CsvImporter.map_integer),
        'activities-elevation': ('elevation', CsvImporter.map_meters),
        'activities-minutesLightlyActive': ('lightly_active_mins', CsvImporter.map_integer),
        'sleep-startTime': ('sleep_start', CsvImporter.map_time),
        'activities-calories': ('calories', CsvImporter.map_integer),
        'foods-log-water': ('log_water', CsvImporter.map_float),
        'sleep-minutesAsleep': ('asleep_mins', CsvImporter.map_integer),
        'body-bmi': ('bmi', CsvImporter.map_float),
        'dateTime': ('day', CsvImporter.map_ymd_date),
        'sleep-awakeningsCount': ('awakenings_count', CsvImporter.map_integer),
    }

    def __init__(self, input_file, input_dir, db_params, metric, debug):
        """Return a new instance of TomTomData given the location of the data files, paramters for accessing the database, and if the data should be stored in metric units."""
        self.metric = metric
        self.tomtomdb = TomTomDB.TomTomDB(db_params, debug)
        if input_file:
            self.file_names = FileProcessor.match_file(input_file, r'.*\.json_2')
        if input_dir:
            self.file_names = FileProcessor.dir_to_files(input_dir, r'.*\.json_2')

    def file_count(self):
        """Return the number of files that will be propcessed."""
        return len(self.file_names)

    def __write_entry(self, db_entry):
        TomTomDB.DaysSummary.insert_or_update(self.tomtomdb, TomTomDB.DaysSummary.intersection(db_entry))

    def process_files(self):
        """Import files into a database."""
        for file_name in tqdm(self.file_names, unit='files'):
            logger.info("Processing file: " + file_name)
            self.csvimporter = CsvImporter(file_name, self.cols_map, self.__write_entry)
            self.csvimporter.process_file(not self.metric)
