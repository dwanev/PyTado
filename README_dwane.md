

Code in progress

see
main_download_tado_data.py
main_get_octopus_reading.py


It is possible to write a reading to Tado, in m3.
It is possible to download octupus usage in kWh cumulative for any particular day.

In my octopus code, there is code to convert from kWh to m3.

There is an offset 17847 than needs to be added when updating tado as our meeter
went back to zero on the switch to octopus, but tado does not allow this.


    # - needs units converted from kWh to m3 (octopus download does do this)
    # - needs cumulative values, that match tados cumulative values