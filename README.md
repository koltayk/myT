# myT
Az utazások (trips) lekérése a Toyotától

mytgettrips.py: python3 script az autó útjainak lekérdezésére a Toyotától. Zátonyi László powershell scriptjének átírása python3-ra: https://www.facebook.com/groups/253426685820690/permalink/942858226877529/
A paraméterek többsége egyértelmű. 
Egy CSV fájlt hoz létre a myt_dir könyvtárban csv_file_name néven, ahol minden sorban egy út  tulajdonságai vannak.
Ha write_trip = True, akkor külön alkönyvtárakan kiírja az utakat JSON és GPX formában.
A colon paraméter akkor érdekes, ha a kettőspont a fájlnevekben nem megengedett, akkor erre lehet cserélni, ugyanis a JSON és GPX fájlnevekben az idő is szerepel, benne kettőspontokkal
