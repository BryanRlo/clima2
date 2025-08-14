from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Tu API Key de OpenWeatherMap
API_KEY = "733f0520abceba771846c6094cdc3374"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        if city:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric",
                "lang": "es"
            }
            try:
                response = requests.get(BASE_URL, params=params)
                data = response.json()

                if data.get("cod") == 200:
                    weather_data = {
                        "city": data["name"],
                        "temp": data["main"]["temp"],
                        "description": data["weather"][0]["description"].capitalize(),
                        "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
                    }
                else:
                    error = f"No se encontró la ciudad: {city}"
            except Exception as e:
                error = f"Error al obtener el clima: {e}"
        else:
            error = "Por favor ingresa una ciudad."

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
