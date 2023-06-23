from flask import Flask, render_template, redirect, request, url_for
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run(debug=True)