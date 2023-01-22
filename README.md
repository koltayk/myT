# myT
Az utazások (trips) lekérése a Toyotától

[mytgettrips.py](https://github.com/koltayk/myT/blob/main/mytgettrips.py): python3 script az autó útjainak lekérdezésére a Toyotától. 
<br>**Zátonyi László** powershell scriptjének átírása python3-ra: https://www.facebook.com/groups/253426685820690/permalink/942858226877529/
<br>A paraméterek többsége egyértelmű. 
<br>Egy CSV fájlt hoz létre a **myt_dir** könyvtárban **csv_file_name** néven, ahol minden sorban egy út tulajdonságai vannak.
<br>Ha **write_trip = True**, akkor külön alkönyvtárakban kiírja az utakat JSON és GPX formában.
<br>A **colon** paraméter akkor érdekes, ha a kettőspont a fájlnevekben nem megengedett, akkor azt erre lehet cserélni, ugyanis a JSON és GPX fájlnevekben az idő is szerepel, benne kettőspontokkal.
