import os
import json
import datetime
from datetime import date, timedelta


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def login():
    import webbrowser  # only needed for direct web browser access

    from PyTado.interface.interface import Tado

    tado = Tado(token_file_path=os.path.expanduser("~/tado/refresh_token"))

    status = tado.device_activation_status()

    if status == "PENDING":
        url = tado.device_verification_url()

        webbrowser.open_new_tab(url)

        tado.device_activation()

        status = tado.device_activation_status()

    if status == "COMPLETED":
        print("Login successful")
    else:
        print(f"Login status is {status}")

    return tado

# https://community.tado.com/en-gb/discussion/14426/efficient-multiroom-scheduling


def set_tado_reading(yyy_mm_dd_date, reading_in_m3):


    pass





if __name__ =="__main__":
    tado = login()
    temp_zone_info = tado.get_zones()

    readings = tado.get_eiq_meter_readings()
    print(readings)



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
            r = tado.get_historic(zone, date_str)
            print(date_str)
            if "zone_historic_data" not in zone_info[zone]:
                zone_info[zone]["zone_historic_data"]={}
            if date_str not in zone_info[zone]["zone_historic_data"]:
                zone_info[zone]["zone_historic_data"][date_str] = r

    with open ("./data_files/data.json", "w") as f:
        json.dump(zone_info, f, indent=2)



    # update tado with reading
    # - needs units converted from kWh to m3 (octopus download does do this)
    # - needs cumulative values, that match tados cumulative values

    # TODO

    # todo use python-tado rather than a forked repo.