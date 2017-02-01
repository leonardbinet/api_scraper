import os
import logging
from os import sys, path
import datetime

if __name__ == '__main__':
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    # Logging configuration
    from api_transilien_manager.utils_misc import set_logging_conf
    set_logging_conf(log_name="task_03_d_match.log")

from api_transilien_manager.mod_01_extract_api import get_station_ids
from api_transilien_manager.mod_03_match_collections import update_real_departures_mongo
from api_transilien_manager.utils_misc import get_paris_local_datetime_now

logger = logging.getLogger(__name__)

# This operation is done every week
logger.info("Task: daily update: adds trip_id, scheduled_departure_time, delay")

today_paris = get_paris_local_datetime_now()
today_paris_str = today_paris.strftime("%Y%m%d")
yesterday_paris = today_paris - datetime.timedelta(days=1)
yesterday_paris_str = yesterday_paris.strftime("%Y%m%d")
logger.info("Paris yesterday date is %s" % yesterday_paris_str)

# 8 digits stations
station_ids = get_station_ids(id_format="UIC")
for i, station in enumerate(station_ids):
    logger.info("Processing station %s, number %d out of %d" %
                (station, i, len(station_ids)))
    update_real_departures_mongo(
        str(yesterday_paris_str), threads=5, one_station=station)
