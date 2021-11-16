# DJango-Vuejs - Meteorite logging application

Simple Django + Vue application that store from a csv, the meteorite sightings.

Put the csv (see [example_reg.csv](example_reg.csv) for more information) inside the "sightings" folder and run the application.

|date      |time      |observatory_code|device_code|device_resolution|device_matrix           |
|:--------:|:--------:|:--------------:|:---------:|:---------------:|:----------------------:|
|2019-02-22| 12:01:57 |    ob_35634    | de_10354  |       5x4       | 1000010000110011000000 |
|2019-02-25| 03:24:21 |   ob_3482734   | de_00234  |       4x6       |000000000100010001100110|

It will parse the csv, store all of them into the database and then move it to "registered" folder (inside).



##Setup
1. Create the database :
```shell
python manage.py migrate  
```
2. Build vue application (read the [README.md](frontend/README.md) for more information)
3. Copy the static files :
```shell
python manage.py collectstatic
```
4. Start the server
```shell
python manage.py runserver
```
