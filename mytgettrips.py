
vid="ALVÁZSZÁM"
username="felhasználóneved a toyota.hu-n"
pwd="jelszavad"
param ="1" # 0- ma, 1- elmúlt hét, 2- elmúlt hónap, 3- elmúlt év
myt_dir = "könyvtár elérési útja ahova a CSV és esetleg a JSON és GPX fájlok íródnak"
write_trip = True   # az utazások kiírása JSON és GPX formában, ha nem kell, akkor: False
colon = ":" # ha a kettőspont a fájlnevekben nem megengedett, akkor erre lehet cserélni


sum_attrs = ['totalDurationInSec', 'idleDurationInSec', 'highwayDurationInSec', 'overspeedDurationInSec', 'totalDistanceInKm', 'highwayDistanceInKm', 'overspeedDistanceInKm', 'fuelConsumptionInL', 'hardAccelerationCount', 'hardBrakingCount', 'hardaccs', 'hardbrakes', 'totalDistanceInMiles']
STATISTICS = 'statistics'

import datetime
import requests
import csv 
import os
import json
import glob


def write_csv(recentTrips, csv_file_path):    
    csv_headers = recentTrips[0].keys()
    stat(recentTrips, csv_headers)
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(recentTrips)


def sum_attr(recentTrips, attr_name):  
    sum_value = 0
    maxSpeedInKmph = 0
    for trip in recentTrips :
        if attr_name in sum_attrs :
            curr_value = float(trip[attr_name])
            sum_value += curr_value  
            trip[attr_name] = float_format(curr_value)
            if sum_value.is_integer(): 
                sum_value = int(sum_value) 
        elif attr_name == 'maxSpeedInKmph' :
            maxSpeedInKmph = max(maxSpeedInKmph, float(trip[attr_name]))
        elif 'average' in attr_name :
            trip[attr_name] = float_format(float(trip[attr_name]))
    if attr_name in sum_attrs :
        if 'InSec' in attr_name :
            sum_value /= 3600  
        return sum_value
    if attr_name == 'maxSpeedInKmph' :
        return maxSpeedInKmph
    return ''
   
        
def float_format(value): 
    return f"{value:.2f}"
   
        
def stat(recentTrips, csv_headers):  
    stat_row = {}
    stat_row['maxSpeedInKmph'] = 0
    for attr_name in csv_headers:
        stat_row[attr_name] = sum_attr(recentTrips, attr_name)
    stat_row['tripId'] = STATISTICS
    stat_row['averageFuelConsumptionInL'] = float_format(stat_row['fuelConsumptionInL'] / stat_row['totalDistanceInKm'] * 100)
    stat_row['averageSpeedInKmph'] = float_format(stat_row['totalDistanceInKm'] / stat_row['totalDurationInSec'])
    for attr_name in sum_attrs:
        stat_row[attr_name] = float_format(stat_row[attr_name])
    recentTrips.append(stat_row)


def write_json_gpx(recent_trip, trip_json):
    trip = {}
    trip.update(recent_trip)
    trip['tripEvents'] = trip_json['tripEvents']
    json_dir = f"{myt_dir}/json/"
    desc = f"{trip['startTimeGmt']} {trip['startAddress']} - {trip['endTimeGmt']} {trip['endAddress']}".replace(':', colon)
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    json_object = json.dumps(trip, indent=4)
    with open(f"{json_dir}{desc}.json", "w", encoding='utf-8') as outfile:
        outfile.write(json_object)

    gpx_dir = f"{myt_dir}/gpx/"
    if not os.path.exists(gpx_dir):
        os.makedirs(gpx_dir)
    gpx = f'<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.0" creator="kk" xmlns="http://www.topografix.com/GPX/1/0">\n  <time>{trip["startTimeGmt"]}</time>\n  <trk>\n    <name>{trip["tripId"]}</name>\n    <desc>{desc}</desc>\n    <trkseg>'
    for point in trip_json['tripEvents']:
        gpx += f'\n      <trkpt lat="{point["lat"]}" lon="{point["lon"]}" />'
    gpx += '\n    </trkseg>\n  </trk>\n</gpx>'
    with open(f"{gpx_dir}{desc}.gpx", "w", encoding='utf-8') as outfile:
        outfile.write(gpx)


def merge_trip_csv():
    trips = {}
    files = glob.glob(myt_dir+'/**/trips *.csv', recursive=True)       
    all_line_count = 0
    for file in files :        
        line_count = 0
        with open(file, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if  row['tripId'] == STATISTICS :
                    continue                
                line_count += 1
                #print(f'\t{row["startTimeGmt"]} tripId {row["tripId"]}')
                trips[row["startTimeGmt"]] = row
        print(f'{file} processed {line_count} lines.')
        all_line_count += line_count
    sorted_trips = list(dict(sorted(trips.items())).values())
    print(f'all files processed {all_line_count} lines.')
    csv_file_path = f"{myt_dir}/trips.csv"
    write_csv(sorted_trips, csv_file_path)
    print(f'merged {len(sorted_trips)} lines to {csv_file_path}.')
    

start = datetime.datetime.now()

startTimeGmt = '3'
endTimeGmt = ''
total_consumption = 0
total_distance = 0

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
for recent_trip in recentTrips :
    tripId = recent_trip['tripId']
    recent_startTimeGmt = recent_trip['startTimeGmt']
    recent_endTimeGmt = recent_trip['endTimeGmt']
    print(f"tripId: {tripId} {recent_startTimeGmt} - {recent_endTimeGmt}")
    url_gettrip = f'https://cpb2cs.toyota-europe.com/api/user/{uuid}/cms/trips/v2/{tripId}/events/vin/{vid}'
    response = requests.get(url = url_gettrip, headers = headers)
    trip_json = response.json()
    statistics = trip_json['statistics']
    recent_trip.update(statistics) 
    total_consumption += float(statistics['fuelConsumptionInL'])
    total_distance += float(statistics['totalDistanceInKm'])
    if startTimeGmt > recent_startTimeGmt:
        startTimeGmt = recent_startTimeGmt
    if endTimeGmt < recent_endTimeGmt:
        endTimeGmt = recent_endTimeGmt
        
    if write_trip :
        write_json_gpx(recent_trip, trip_json)
    
print(f'össztávolság: {total_distance:2.2f} km')
print(f'összfogyasztás: {total_consumption:2.2f} l')
print(f'átlagfogyasztás: {total_consumption * 100 / total_distance:2.2f} l/100km')

csv_file_path = myt_dir + f"/trips {startTimeGmt} - {endTimeGmt}.csv".replace(':', colon)
write_csv(recentTrips, csv_file_path)

merge_trip_csv()

dur = datetime.datetime.now()
total_seconds = (dur - start).total_seconds()
hours, remainder = divmod(total_seconds, 3600)
minutes, seconds = divmod(remainder, 60)
print(f'{len(recentTrips)} utazás letöltve a következő helyre: {csv_file_path}')
print(f'futási idő: {total_seconds:2.2f} sec:   {hours:.0f}h {minutes:.0f}m {seconds:2.2f}s')
