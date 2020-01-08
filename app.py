from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for, flash, sessions, session, get_flashed_messages

from get_details import getLocations, safetyIndex, getData, getAddress, getAllLocations
from get_safe_locations import getSafeLocations
from encryption import storeDetails, matchDetails, checkEmail, getUserDetails
from recommendation import reco
import globals
import pandas as pd
# from update_news import updateNews

app = Flask(__name__)
app.secret_key = "abcdefgh"

@app.route('/')
def splash():
    # updateNews()
    return render_template('splash.html')

@app.route('/guest-login', methods=['GET', 'POST'])
def guestLogin():
    if request.method == 'POST':
        session['user_email'] = -1
        session['age'] = request.form['age']
        session['gender'] = request.form['gender']
        session['businessman'] = request.form['businessman']
        return redirect(url_for('decision'))
    return render_template('guest-login.html')


@app.route('/enter-details', methods=['GET', 'POST'])
def enterDetails():
    email = globals.signUpEmail
    password = globals.signUpPassword
    if request.method == 'POST':

        age = request.form['age']
        gender = request.form['gender']
        businessman = request.form['businessman']

        storeDetails(email, password, age, gender, businessman)

        return redirect(url_for('decision'))
    return render_template('enter-details.html')


@app.route('/sign-in', methods=['GET', 'POST'])
def signIn():
    error=None
    if request.method=='POST':
        username = request.form['username']
        password = request.form['pass']

        session['user_email'] = username

        flag = matchDetails(username, password)
        if flag==1:
            return redirect(url_for('decision'))
        else:
            error = 'Invalid email or password. Please try again!'
            flash('Wrong email or password')

    return render_template('login.html', error=error)

@app.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    error=None
    if request.method=='POST':
        email = request.form['email']
        password = request.form['pass']
        f = checkEmail(email)
        if f==1:
            globals.signUpEmail = email
            session['user_email'] = email
            globals.signUpPassword = password
            return redirect(url_for('enterDetails'))
        else:
            error = 'You are already registered.'
            flash('You are already registered.')
    return render_template('signup.html', error=error)


def rating(count):
    if count==60:
        r = 'A+'
    elif count>=50 and count<60:
        r = 'A'
    elif count>=40 and count<50:
        r = 'B'
    else:
        r = 'C'
    return r


@app.route('/location-details/<city_name>', methods=['GET', 'POST'])
def locationDetails(city_name):
    location = city_name
    df = pd.read_csv('area.csv')
    df = df[df['location']==location]

    school_count = df['#_schools'].iloc[0]
    park_count = df['#_parks'].iloc[0]
    hospital_count = df['#_hospitals'].iloc[0]
    restaurant_count = df['#_restaurants'].iloc[0]

    school_r = rating(school_count)
    park_r = rating(park_count)
    hospital_r = rating(hospital_count)
    restaurant_r = rating(restaurant_count)

    email = session['user_email']
    if str(email)!=str(-1):
        details = getUserDetails(email)
        age = int(details[0])
        gender = str(details[1])
        businessman = str(details[2])
    else:
        age = session['age']
        gender = session['gender']
        businessman = session['businessman']

    if request.method=="POST":
        if request.form['distance'] == '2.5km':
            session['distance'] = 2.5
        elif request.form['distance'] == '5km':
            session['distance'] = 5
        elif request.form['distance'] == '10km':
            session['distance'] = 10

        return redirect(url_for('safeAreas', city_name=city_name))

    news, crime_count, crime_ages, no_businessman, crimes, age_crimes, most_occ_crime, s = getData(location, int(age))
    si = safetyIndex(location)
    address = getAddress(location)
    return render_template('location-details.html', address=address, location=location, news=news,
                           crime_count=crime_count, crime_ages=crime_ages, no_businessman=no_businessman,
                           businessman=businessman, crimes=crimes, age_crimes=age_crimes,
                           most_occ_crime=most_occ_crime, s=s, si=si,
                           school_r=school_r, restaurant_r=restaurant_r, park_r=park_r, hospital_r=hospital_r)


@app.route('/crime-details/<city_name>', methods=['GET', 'POST'])
def crimeDetails(city_name):
    location = city_name
    df = pd.read_csv('area.csv')
    df = df[df['location']==location]

    school_count = df['#_schools'].iloc[0]
    park_count = df['#_parks'].iloc[0]
    hospital_count = df['#_hospitals'].iloc[0]
    restaurant_count = df['#_restaurants'].iloc[0]

    school_r = rating(school_count)
    park_r = rating(park_count)
    hospital_r = rating(hospital_count)
    restaurant_r = rating(restaurant_count)



    if int(df['safety_index'])!=(-1):

        email = session['user_email']
        print(email)
        if str(email)!=str(-1):
            details = getUserDetails(email)
            age = int(details[0])
            gender = str(details[1])
            businessman = str(details[2])
            print(age)
        else:
            age = session['age']
            gender = session['gender']
            businessman = session['businessman']

        if request.method=="POST":
            if request.form['distance'] == '2.5km':
                session['distance'] = 2.5
            elif request.form['distance'] == '5km':
                session['distance'] = 5
            elif request.form['distance'] == '10km':
                session['distance'] = 10

            return redirect(url_for('safeAreas', city_name=city_name))

        news, crime_count, crime_ages, no_businessman, crimes, age_crimes, most_occ_crime, s = getData(location, int(age))
        si = safetyIndex(location)
        address = getAddress(location)
        return render_template('crime-details.html', address=address, location=location, news=news,
                               crime_count=crime_count, crime_ages=crime_ages, no_businessman=no_businessman,
                               businessman=businessman, crimes=crimes, age_crimes=age_crimes,
                               most_occ_crime=most_occ_crime, s=s, si=si,
                               school_r=school_r, restaurant_r=restaurant_r, park_r=park_r, hospital_r=hospital_r)

    else:
        return render_template('location-details.html', school_r=school_r, restaurant_r=restaurant_r, park_r=park_r, hospital_r=hospital_r)


@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    if str(session['user_email'])!=str(-1):
        details = getUserDetails(session['user_email'])
        age = details[0]
        gender = details[1]
        bus = details[2]
    else:
        age = session['age']
        gender = session['gender']
        bus = session['businessman']

    rslts = reco(str(gender), age, bus)
    rated_rslt = rslts[0]
    school = rslts[3]
    hospital = rslts[1]
    park = rslts[2]
    restaurant = rslts[4]

    return render_template('recommendation.html', rated_rslt=rated_rslt, school=school, restaurant=restaurant, park=park, hospital=hospital)

@app.route('/analysis/<city_name>', methods=['GET', 'POST'])
def analysis(city_name):
    return redirect(url_for('crimeDetails', city_name=city_name))


@app.route('/decision', methods=['GET', 'POST'])
def decision():
    locations = getAllLocations()
    if request.method=="POST":
        if request.form['submit']=='Recommendation':
            return redirect(url_for('recommendation'))
        else:
            loc = request.form['location']
            return redirect(url_for('analysis', city_name=loc))

    return render_template('decision.html', locations = locations)


@app.route('/safe-areas/<city_name>', methods=['GET', 'POST'])
def safeAreas(city_name):
    src_loc = city_name
    dist = session['distance']
    safe_areas_lst, crime_area = getSafeLocations(src_loc, dist)

    return render_template('safe-areas.html', safe_areas_lst=safe_areas_lst, crime_area=crime_area, l=len(safe_areas_lst), src_loc=src_loc)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/flash')
def flash(message):
    message = request.args.get("msg")
    return render_template("flash.html", msg=message)


if __name__ == '__main__':
    app.run(debug=True)
