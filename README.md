# myT
Az utazások (trips) lekérése a Toyotától

[mytgettrips.py](https://github.com/koltayk/myT/blob/main/mytgettrips.py): python3 script az autó útjainak lekérdezésére a Toyotától. 
<br>A paraméterek többsége egyértelmű. 
<br>Egy CSV fájlt hoz létre a **myt_dir** könyvtárban, a fájl nevében az első és utolsó út idejével <br>(pl. **trips 2023-01-25T15:00:07Z - 2023-02-22T18:24:15Z.csv**), ahol minden sorban egy út tulajdonságai vannak. 
Egy statisztika sorral zárul a CSV fájl.
<br>Ha **write_trip = True**, akkor külön alkönyvtárakban kiírja az utakat JSON és GPX formában.
<br>A **colon** paraméter akkor érdekes, ha a kettőspont a fájlnevekben nem megengedett, akkor azt erre lehet cserélni, ugyanis a létrehozott fájlok neveiben az idő is szerepel, benne kettőspontokkal.
<br>A **myt_dir** könyvtárban az összes így keletkezett **trips ...** CSV fájl útjait összefésüli időben növekvő sorrendbe rendezve, egy statisztika sorral kiegészítve a **trips.csv** fájlba.
