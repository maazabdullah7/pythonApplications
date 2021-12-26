import requests
import json

lst = list()

api_key = 42
serviceurl = 'http://py4e-data.dr-chuck.net/json'
fh = open("address.txt")
c = 0
for line in fh:
    c += 1
    print(c)
    address = line.rstrip()
    if len(address) < 1: continue

    payload = dict()
    payload['address'] = address
    if api_key is not False: payload['key'] = api_key

    r = requests.get(serviceurl, params=payload)
    data = r.text

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(data)
        continue

    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']
    location = js['results'][0]['formatted_address']
    parts = location.split(",")
    try: 
        cd = parts[len(parts)-2][-6:]
        st = parts[len(parts)-2][1: len(parts[len(parts)-2])-6]
        ct = parts[len(parts)-3][1:]
        lt = parts[len(parts)-4][1:]
    except:
        continue

    try:
        ad = address.split(",")
        if ad[0].startswith("#"):
            ad1 = (ad[0])[1:]
        else:
            ad1 = ad[0]

        ad2 = ad[1]

    except:
        ad = address.split(" ")

        ad1 = ""
        c2 = 0
        for i in ad[0:5]:
            ad1 += i+" "
            c2 += 1

        ad2 = ""
        for i in ad[5:10]:
            ad2 += i+" "
            c2 += 1

    geo = str(lat)+", "+str(lng)

    ddd = {"addressline1": ad1,"addressline2": ad2,"locality": lt,"city": ct,"state": st,"pincode": cd,"geocodes": geo}
    lst.append(ddd)

ddd2 = {"addresses": lst}
jsonString = json.dumps(ddd2, indent=4)

jsonF = open("addresses_data.json", "w")
jsonF.write(jsonString)
jsonF.close()



