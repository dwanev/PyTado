import json
import glob
# from datetime import date, timedelta
import datetime
import time


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


if __name__ =="__main__":

    with open ("./data_files/data.json", "r") as f:
        data = json.load(f)


    print("")
    # Keys
    # "hotWaterProduction"
    #   "settings": {
    #     "timeSeriesType": "dataIntervals",
    #     "dataIntervals": [
    #       {
    #         "from": "2024-04-05T22:45:00.000Z",
    #         "to": "2024-04-06T06:30:00.000Z",
    #         "value": {
    #           "type": "HEATING",
    #           "power": "OFF",
    #           "temperature": null
    #         }
    #       }, ....
    #
    #     "dataIntervals": [
    #       {
    #         "from": "2024-04-05T22:45:00.000Z",
    #         "to": "2024-04-05T23:00:00.000Z",
    #         "value": true
    #       },
    #
    #   "callForHeat": {
    #     "timeSeriesType": "dataIntervals",
    #     "dataIntervals": [
    #       {
    #         "from": "2024-04-05T22:45:00.000Z",
    #         "to": "2024-04-06T06:31:34.276Z",
    #         "value": "NONE"
    #       },

    start_date = datetime.date(2024, 3, 8)
    end_date = datetime.date(2024, 4, 7)
    interval_in_minutes = 15
    intervals_per_day = int(24 * (60/interval_in_minutes))
    sorted_zones = list(data.keys())
    sorted_zones.sort()
    for single_date in daterange(start_date, end_date):
        date_str = single_date.strftime("%Y-%m-%d")
        point_in_time = datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.strptime(date_str, "%Y-%m-%d").timetuple()))
        for i in range(intervals_per_day):
            point_in_time = point_in_time + datetime.timedelta( minutes = interval_in_minutes )

            print(point_in_time)
            # Build a record for this point in time
            record = {
                "PointInTime":point_in_time
            }

            for zone in sorted_zones:
                days_data = data[zone]["zone_historic_data"][date_str]

                # keys: stripes, callForHeat,
                # hotWaterProduction (duplicated?)
                # weather (duplicated?)