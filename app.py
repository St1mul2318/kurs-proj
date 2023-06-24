from flask import Flask, render_template, redirect, request, url_for
import requests, datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'supersecretkey'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime)
    updated_on = db.Column(db.DateTime(), default=datetime,  onupdate=datetime)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return render_template('register.html', message='User already exists')

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or user.password != password:
            return render_template('login.html', message='Invalid username or password')

        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    api_key = 'b41f842f9800a4d28dbe5d5bbea18a3e'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    weather_description = data['weather'][0]['description']
    temperature = round(data['main']['temp'] - 273.15, 1)
    wind_speed = data['wind']['speed']
    return render_template('get_weather.html', city=city, weather=weather_description, temperature=temperature, wind_speed=wind_speed)


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        return redirect(url_for('get_weather'))
    return render_template('weather.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/map')
def map():
    url = f'https://openweathermap.org/weathermap?basemap=map&cities=true&layer=temperature&lat=64.5340&lon=40.5631&zoom=5'
    return render_template('map.html', url=url)


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
