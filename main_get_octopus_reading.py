import copy
import os
import json
import requests

def convert_kWh_to_m3(kWh):
    # the following was copied from the octopus bill. Constants will change from time to time.
    # 6.5 × 1.02264 × 39.0†   ÷ 3.6 = 71.9
    # m3 × Volume Correction (for temperature & pressure) × Calorific Value (energy in each m3
    #  of gas) ÷ conversion to joules == kWh
    m3 = ( kWh * 3.6 ) / 39.0 / 1.02264
    return m3


def get_octopus_readings():
    api_key = os.environ["API_KEY"]
    print("api_key:", api_key)
    gas_meter_serial_number = "E6S13402372462"
    gas_mprn = "3400689906"

    url = ("https://api.octopus.energy/v1/gas-meter-points/"+gas_mprn+"/meters/"+gas_meter_serial_number+
           "/consumption/?group_by=day"+
           "&period_from=2024-12-14T00:00Z")
    #  "https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/E-1R-AGILE-18-02-21-C/standard-unit-rates/?period_from=2020-03-29T00:00Z&period_to=2020-03-29T02:29Z"


    headers = {
        "X-Octopus-ApiKey": api_key
    }
    response = requests.get(url, auth=(api_key, ''))
    output_dict = response.json()
    # print(json.dumps(output_dict, indent=2))

    results = copy.deepcopy(output_dict["results"])
    results = reversed(results)
    running_total = 0.0
    print("Date, kWk, m3, Cumulative m3")
    for r in results:
        r["kWh"] = r["consumption"]
        m3 = convert_kWh_to_m3(r["kWh"])
        r["m3"] = m3
        running_total += m3
        r["total_m3"] = running_total
        del r["consumption"]
        print(r )

    print("Appears to be in kWh, as of midnight the day before, i.e. 14/jan on the bill, is units up until midnight on the 13th in the api download.")
    print("Dates appear correct, i.e. we use less gas Mon&Tues and this seems to reflect in the data.")

    return output_dict


if __name__ == "__main__":
    get_octopus_readings()

