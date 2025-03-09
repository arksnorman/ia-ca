from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

S3_BUCKET_URL = os.getenv("S3_BUCKET_URL", "")
BRANCH_NAME = os.getenv("BRANCH_NAME", "")

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'
            }
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                weather_data = response.json()
            else:
                weather_data = {'error': 'City not found!'}
    return render_template('index.html', weather_data=weather_data, s3_url=S3_BUCKET_URL, branch_name=BRANCH_NAME)

if __name__ == '__main__':
    app.run(debug=True)
