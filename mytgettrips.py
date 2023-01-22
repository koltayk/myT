vid="ALVÁZSZÁM"
username="felhasználóneved a toyota.hu-n"
pwd="jelszavad"
param ="1" # 0- ma, 1- elmúlt hét, 2- elmúlt hónap, 3- elmúlt év
myt_dir = "könyvtár elérési útja ahova a CSV és esetleg a JSON és GPX fájlok íródnak"
csv_file_name = "trips.csv" # a CSV fájl neve a myt_dir könyvtárban
write_trip = True   # az utazások kiírása JSON és GPX formában, ha nem kell, akkor: False
colon = ':' # ha a kettőspont a fájlnevekben nem megengedett, akkor erre lehet cserélni


import datetime
import requests
import csv
import os
import json


def write_json_gpx(recent_trip, trip_json):
    trip = {}
    trip.update(recent_trip)
    trip['tripEvents'] = trip_json['tripEvents']
    json_dir = f"{myt_dir}/json/"
    desc = f"{trip['startTimeGmt']} {trip['startAddress']} - {trip['endTimeGmt']} {trip['endAddress']}"
    desc = desc.replace(':', colon)
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    json_object = json.dumps(trip, indent=4)
    with open(f"{json_dir}{desc}.json", "w") as outfile:
        outfile.write(json_object)

    gpx_dir = f"{myt_dir}/gpx/"
    if not os.path.exists(gpx_dir):
        os.makedirs(gpx_dir)
    gpx = f'<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.0" creator="kk" xmlns="http://www.topografix.com/GPX/1/0">\n  <time>{trip["startTimeGmt"]}</time>\n  <trk>\n    <name>{trip["tripId"]}</name>\n    <desc>{desc}</desc>\n    <trkseg>'
    for point in trip_json['tripEvents']:
        gpx += f'\n      <trkpt lat="{point["lat"]}" lon="{point["lon"]}" />'
    gpx += '\n    </trkseg>\n  </trk>\n</gpx>'
    with open(f"{gpx_dir}{desc}.gpx", "w") as outfile:
        outfile.write(gpx)


start = datetime.datetime.now()

headers = {
    'x-tme-lc' : 'hu-hu'
 }

body = {
    'username' : username,
    'password' : pwd
}

url_auth = 'https://ssoms.toyota-europe.com/authenticate'
response = requests.post(url = url_auth, data = body, headers = headers)

resp_json = response.json()
#print(resp_json)

token= resp_json['token']
#print(token)

uuid = resp_json['customerProfile']['uuid']
#print(uuid)

url_gettrips= f'https://cpb2cs.toyota-europe.com/api/user/{uuid}/cms/trips/v2/history/vin/{vid}/{param}'
headers ={
    'x-tme-token' : token
}
response = requests.get(url = url_gettrips, headers = headers)
resp_json = response.json()

recentTrips = resp_json['recentTrips']
total_consumption = 0
total_distance = 0
for recent_trip in recentTrips :
    tripId = recent_trip['tripId']
    print(f'tripId: {tripId}')
    url_gettrip = f'https://cpb2cs.toyota-europe.com/api/user/{uuid}/cms/trips/v2/{tripId}/events/vin/{vid}'
    response = requests.get(url = url_gettrip, headers = headers)
    trip_json = response.json()
    statistics = trip_json['statistics']
    recent_trip.update(statistics)
    total_consumption += float(statistics['fuelConsumptionInL'])
    total_distance += float(statistics['totalDistanceInKm'])

    if write_trip :
        write_json_gpx(recent_trip, trip_json)

print(f'össztávolság: {total_distance:2.2f} km')
print(f'összfogyasztás: {total_consumption:2.2f} l')
print(f'átlagfogyasztás: {total_consumption * 100 / total_distance:2.2f} l/100km')

csv_headers = recentTrips[0].keys()
csv_file_path = f"{myt_dir}/{csv_file_name}"
with open(csv_file_path, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerows(recentTrips)

dur = datetime.datetime.now()
total_seconds = (dur - start).total_seconds()
hours, remainder = divmod(total_seconds, 3600)
minutes, seconds = divmod(remainder, 60)
print(f'{len(recentTrips)} utazás letöltve a következő helyre: {csv_file_path}')
print(f'futási idő: {total_seconds:2.2f} sec:   {hours:.0f}h {minutes:.0f}m {seconds:2.2f}s')

