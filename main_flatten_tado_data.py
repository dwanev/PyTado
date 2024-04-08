import json
import glob
# from datetime import date, timedelta
import datetime
import time
import pandas as pd



def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def _get_surrounding_record(list_of_dicts:list, point_in_time:datetime, key1:str, key2:str=None):

    search_str = point_in_time.isoformat()+".000Z"
    if key2 is not None:
        matches = [r for r in list_of_dicts if r[key1] <= search_str and r[key2] > search_str]
        return matches
    else:
        matches = [r for r in list_of_dicts if r[key1] == search_str]
        return matches





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

    start_date = datetime.date(2024, 3, 16)
    end_date = datetime.date(2024, 4, 6)
    interval_in_minutes = 15
    temperature_unit = "celsius"
    intervals_per_day = int(24 * (60/interval_in_minutes))
    sorted_zones = list(data.keys())
    sorted_zones.sort()
    results = []
    for single_date in daterange(start_date, end_date):
        date_str = single_date.strftime("%Y-%m-%d")
        point_in_time = datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.strptime(date_str, "%Y-%m-%d").timetuple()))
        for i in range(intervals_per_day):
            point_in_time = point_in_time + datetime.timedelta( minutes = interval_in_minutes )

            print(point_in_time)
            # Build a record for this point in time
            record = {
                "PointInTime":point_in_time.isoformat()
            }

            for zone in sorted_zones:
                days_data = data[zone]["zone_historic_data"][date_str]

                # keys: stripes, callForHeat,
                # hotWaterProduction (duplicated?)
                # weather (duplicated?)



                key_prefix= "zone"+str(zone)
                if "stripes" in days_data:
                    match = _get_surrounding_record(days_data["stripes"]["dataIntervals"],point_in_time, key1="from", key2="to")
                    if len(match) > 0:
                        record[key_prefix+"StripeType"] = match[0]["value"]["stripeType"]
                        if "setting" in match[0]["value"]:
                            record[key_prefix + "SettingType"] = match[0]["value"]["setting"]["type"]
                            record[key_prefix + "SettingPower"] = match[0]["value"]["setting"]["power"]

                            temperature = match[0]["value"]["setting"]["temperature"]
                            if temperature is not None and temperature_unit in temperature:
                                record[key_prefix + "SettingTemperature"] = temperature[temperature_unit]

                if "callForHeat" in days_data:
                    match = _get_surrounding_record(days_data["callForHeat"]["dataIntervals"],point_in_time, key1="from", key2="to")
                    if len(match) > 0:
                        # print("here")
                        record[key_prefix + "CallForHeat"] = match[0]["value"]

                if "insideTemperature" in  days_data:
                    match = _get_surrounding_record(days_data["insideTemperature"]["dataPoints"],point_in_time, key1="timestamp", key2=None)
                    if len(match) > 0:
                        # print("here")
                        record[key_prefix + "InsideTemperature"] = match[0]["value"][temperature_unit]

                if "hotWaterProduction" in days_data:
                    pass
                    match = _get_surrounding_record(days_data["hotWaterProduction"]["dataIntervals"], point_in_time,
                                                    key1="from", key2="to")
                    if len(match) > 0:
                        # print("here")
                        record[key_prefix + "HotWaterProduction"] = match[0]["value"]

                if "weather" in days_data:
                    # Temperature
                    match = _get_surrounding_record(days_data["weather"]["condition"]["dataIntervals"], point_in_time,
                                                    key1="from", key2="to")
                    if len(match) > 0:
                        # print("here")
                        record[key_prefix + "WeatherConditionTemperature"] = match[0]["value"]["temperature"][temperature_unit]
                    # Sunny
                    match = _get_surrounding_record(days_data["weather"]["sunny"]["dataIntervals"], point_in_time,
                                                    key1="from", key2="to")
                    if len(match) > 0:
                        # print("here")
                        record[key_prefix + "WeatherConditionSunny"] = match[0]["value"]

                    # Cloudy, Rain , Drizzle etc
                    # TODO needs to pick by time, and to know the time zone....
                    # match = _get_surrounding_record(days_data["weather"]["slots"]["slots"], point_in_time,
                    #                                 key1="from", key2="to")
                    # if len(match) > 0:
                    #     # print("here")
                    #     record[key_prefix + "WeatherConditionDescript"] = match[0]["value"]

            results.append(record)

    with open("./data_files/flattened.json", "w") as f:
        json.dump(results, f, indent=2)

    df = pd.DataFrame.from_dict(results)

    print(df.head())

    df.to_csv("./data_files/data_frame.csv")

    # print(df.to_latex())