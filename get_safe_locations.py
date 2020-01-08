import pandas as pd

def getSafeLocations(src_loc, dist):
    safe_area = []
    crime_area = []
    df = pd.read_csv('location_distance.csv', index_col=False)
    df = df[df['source']==src_loc]

    df1 = pd.read_csv('news_data.csv')
    src_crime_count = len(list(df1[df1['location']==src_loc].iloc[0])[1].split('\t'))


    for i in range(len(df)):
        dest_loc = df['destination'].iloc[i]
        dist_loc = df['distance'].iloc[i]
        if dest_loc in list(df1['location']) and dist_loc<dist:
            dest_crime_count = len(list(df1[df1['location']==dest_loc].iloc[0])[1].split('\t'))
            if dest_crime_count<src_crime_count:
                dest_percentile = df1[df1['location']==dest_loc]['percentile'].iloc[0]
                safe_area.append(dest_loc)
                crime_area.append(dest_percentile)

    return safe_area, crime_area
