import pandas as pd

def reco(gender, age, bus):
    gender = str(gender).lower()[0]
    age = int(age)
    bus = str(bus).lower()
    bus = bus.lower()
    df = pd.read_csv('area.csv')
    if gender == 'f':
        rslt_df = df[df['rape'] == 0]
        if (age > 0) & (age <= 21):
            rslt_df = rslt_df[rslt_df['0-21'] == 0]
            if bus == 'yes':
                rslt_df = rslt_df[rslt_df['businessman'] == 0]


        elif (age > 21) & (age <= 50):
            rslt_df = rslt_df[rslt_df['22-50'] == 0]
            if bus == 'yes':
                rslt_df = rslt_df[rslt_df['businessman'] == 0]
        elif (age > 50) & (age <= 100):
            rslt_df = rslt_df[rslt_df['50+'] == 0]
            if bus == 'yes':
                rslt_df = rslt_df[rslt_df['businessman'] == 0]
    else:
        rslt_df = df
        if (age > 0) & (age <= 21):
            rslt_df = rslt_df[rslt_df['0-21'] == 0]
            if bus == 'yes':
                rslt_df = rslt_df[rslt_df['businessman'] == 0]
        elif (age > 21) & (age <= 50):
            rslt_df = rslt_df[rslt_df['22-50'] == 0]
            if bus == 'yes':
                rslt_df = rslt_df[rslt_df['businessman'] == 0]
        elif (age > 50) & (age <= 100):
            rslt_df = rslt_df[rslt_df['50+'] == 0]
            if bus == 'yes':
                rslt_df = rslt_df[rslt_df['businessman'] == 0]

    rslt1 = rslt_df[rslt_df['safety_index'] == -1]
    rslt_schools = list(rslt1.sort_values(by='#_schools', ascending=False).iloc[:3].location)
    rslt_hospitals = list(rslt1.sort_values(by='#_hospitals', ascending=False).iloc[:3].location)
    rslt_parks = list(rslt1.sort_values(by='#_parks', ascending=False).iloc[:3].location)
    rslt_restaurants = list(rslt1.sort_values(by='#_restaurants', ascending=False).iloc[:3].location)

    rslt2 = rslt_df[rslt_df['safety_index'] != -1]
    rslt2 = rslt2.sort_values(by='safety_index', ascending=False).iloc[:5][['location', 'safety_index']]

    rated_rslt = []
    for i in range(len(rslt2)):
        rated_rslt.append([rslt2['location'].iloc[i], rslt2['safety_index'].iloc[i]])

    return [rated_rslt, rslt_hospitals, rslt_parks, rslt_schools, rslt_restaurants]
