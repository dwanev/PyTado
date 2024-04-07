import json
from PyTado.interface import Tado
from datetime import date, timedelta


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


if __name__ =="__main__":
    t = Tado('dwanev@gmail.com', 'HettyCat123!')
    temp_zone_info = t.get_zones()

    zone_info = {}
    for r in temp_zone_info:
        zone_info[r["id"]] = r

    start_date = date(2024, 3, 8)
    end_date = date(2024, 4, 7)

    # results = {
    #     "zone_info":zone_info,
    #     "zone_historic_data":{}
    # }

    for single_date in daterange(start_date, end_date):
        date_str = single_date.strftime("%Y-%m-%d")

        for zone in zone_info.keys():
            r = t.get_historic(zone,date_str)
            print(date_str)
            if "zone_historic_data" not in zone_info[zone]:
                zone_info[zone]["zone_historic_data"]={}
            if date_str not in zone_info[zone]["zone_historic_data"]:
                zone_info[zone]["zone_historic_data"][date_str] = r

    with open ("./data_files/data.json", "w") as f:
        json.dump(zone_info, f, indent=2)