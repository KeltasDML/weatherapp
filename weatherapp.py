from flask import Flask,render_template,request,abort
from flask_sqlalchemy import SQLAlchemy
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_adress = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)


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
def settings_page():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)