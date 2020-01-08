import pandas as pd
import operator
import requests, json
import time

# Google Maps API
api_keys = ['AIzaSyAux3YK6j7_D6467O5yfV0pwMSr_kILXUQ','AIzaSyAsm2BPtan-wa3lMYxfB5OiOMIFfMdT85I',
            'AIzaSyBHvJ9v9mUsH8dQ_jNKEgnrr-LGrv2yLfk', 'AIzaSyBu884h3TqS0usWbDasAe-Jfek9YauaMg0']
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

def getLocations():
    df = pd.read_csv('news_data.csv', index_col=False)
    locations = list(df['location'])
    locations = sorted(locations)
    return locations

def getAllLocations():
    df = pd.read_csv('location_cordinates.csv', index_col=False)
    locations = list(df['location'])
    locations = sorted(locations)
    return locations

def getData(loc_name, age):
    df = pd.read_csv('news_data.csv', index_col=False)
    df_new = df[df['location']==loc_name]
    headlines = list(df_new['headline'])[0].split('\t')
    dates = list(df_new['date'])[0].split('\t')
    crime_types = list(df_new['crime_type'])[0].split('\t')
    sources = list(df_new['source'])[0].split('\t')
    urls = list(df_new['url'])[0].split('\t')
    ages = list(df_new['age'])[0].split('\t')
    businessmans = list(df_new['businessman'])[0].split('\t')

    crime_count = len(headlines)
    no_businessman = businessmans.count('1')

    age_groups = [0, 22, 51, 101]

    min_age = 0
    max_age = 100
    for i in range(1):
        if age>=age_groups[i] and age<age_groups[i+1]:
            min_age = age_groups[i]
            max_age = age_groups[i+1]

    crimes_age = 0
    lst = []
    for i in range(len(ages)):
        a = int(ages[i].replace("'", "").replace('"', ''))
        if int(a)>=min_age and int(a)<=max_age:
            crimes_age+=1
            lst.append(crime_types[i])

    if len(lst)!=0:
        s = str(max(set(lst), key = lst.count))
        s = s[0].upper() + s[1:]
    else:
        s = -1


    crimes = {'burglary':crime_types.count('burglary'),
              'robbery':crime_types.count('robbery'),
              'murder':crime_types.count('murder'),
              'kidnapping':crime_types.count('kidnapping'),
              'rape':crime_types.count('rape')}
    age_crimes = {'0-21':0,
                  '22-50':0,
                  '50+':0,
                  'NA':0}

    for k in ages:
        i = int(k.replace("'", "").replace('"', ''))

        if i>=0 and i<=21:
            age_crimes['0-21']+=1
        elif i>21 and i<=50:
            age_crimes['22-50']+=1
        elif i>50:
            age_crimes['50+']+=1
        else:
            age_crimes['NA']+=1

    x = str(sorted(crimes.items(), key=operator.itemgetter(1))[::-1][0][0])
    most_occ_crime = x[0].upper() + x[1:]
    return [dates, headlines, crime_types, sources, urls], crime_count, crimes_age, no_businessman, crimes, age_crimes, most_occ_crime, s

def safetyIndex(loc):
    si = 0
    df = pd.read_csv('news_data.csv', index_col=False)
    for i in range(len(df)):
        if df['location'].iloc[i]==loc:
            si = df['percentile'].iloc[i]
            break

    return si


def getAddress(loc):
    df = pd.read_csv('location_cordinates.csv')
    for i in range(len(df)):
        if df['location'].iloc[i]==loc:
            address = df['address'].iloc[i]
            break
    return address


def getRestaurants(loc):
    query = 'schools in ' + loc + ' rajasthan'

    lst = []
    ind = 0
    api_key = api_keys[ind]

    r = requests.get(url + 'query=' + query + '&key=' + api_key)
    x = r.json()

    ct = 0

    while x['status'] != 'OK':
        print('Loading', x['status'])

        if x['status']=='OVER_QUERY_LIMIT':
            ct+=1
            if ct==3:
                print('---')
                ind+=1
                if ind==len(api_keys):
                    ind = 0
                api_key = api_keys[ind]
                ct = 0

        time.sleep(2)

        r = requests.get(url + 'query=' + query + '&key=' + api_key)
        x = r.json()

    y = x['results']
    for i in range(len(y)):
        lst.append(y[i]['name'])

    while True:
        print('...')
        if 'next_page_token' not in x:
            break
        try:
            r = requests.get(url + 'key=' + api_key + '&pagetoken=' + x['next_page_token'])
            a = r.json()

            ct = 0

            while a['status'] != 'OK':
                print('trying', a['status'])

                if a['status'] == 'OVER_QUERY_LIMIT':
                    ct+=1
                    if ct==3:
                        print('---')
                        ind += 1
                        if ind == len(api_keys):
                            ind = 0
                        api_key = api_keys[ind]
                        ct = 0

                time.sleep(2)

                r = requests.get(url + 'key=' + api_key + '&pagetoken=' + x['next_page_token'])
                a = r.json()

            x = a
            y = x['results']
            for i in range(len(y)):
                lst.append(y[i]['name'])
        except Exception as e:
            pass

    return lst

# lst = sorted(getRestaurants('sikar'))
# [print(i) for i in lst]
#
# print(len(lst))
# print(len(list(set(lst))))