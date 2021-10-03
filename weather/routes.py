from weather import app
from flask import render_template, request, abort,url_for, redirect, flash
from weather.forms import loginForm
from weather.models import User
from flask_login import login_user, logout_user, login_required
import json
import urllib.request

def tofahrenheit(temp):
    return str(round((float(temp) - 273.16) * 9/5 + 32))
    
@app.route('/weather',methods=['POST','GET'])
@app.route('/',methods=['POST','GET'])
def weather():
    api_key = 'e0e42510dbbc3629acc6497a7071fb13'
    
    if request.method == 'POST':
        rawZipcode = request.form['zipcode']
        if rawZipcode.isdecimal() and len(rawZipcode) == 5:
            zipcode = rawZipcode
        else:
            zipcode = '19107'
            flash('Wrong zipcode', category='danger')
    else:
        #default zipcode
        zipcode = '19107'
    
    # source contain json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?zip=' + zipcode + ',us&appid=' + api_key).read()
    except:
        return abort(404)
    # converting json data to dictionary

    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "weather" : str(list_of_data['weather'][0]['main']),
        "temp": str(list_of_data['main']['temp']) + 'k',
        "temp_far": tofahrenheit(list_of_data['main']['temp']) + 'F',
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']) + '%',
        "cityname": str(list_of_data['name']),

    }
    return render_template('index.html',data=data)

@app.route('/settings')
@login_required
def settings_page():
    return render_template('settings.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():

    form = loginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success, logged in as: {attempted_user.username} ', category='success')
            return redirect(url_for('settings_page'))
        else:
            flash('Wrong username or password', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():

    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('weather'))