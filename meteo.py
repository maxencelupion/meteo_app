import os
import requests
from dotenv import load_dotenv


class Meteo:
    def __init__(self):
        self.name = ""
        self.country = ""
        self.localtime = ""
        self.temp_c = 0
        self.wind_kph = 0
        self.is_day = 0
        self.condition = ""
        self.humidity = 0

    def fill_meteo(self, liste):
        self.name, self.country, self.localtime, self.temp_c, self.wind_kph, self.is_day, self.condition, self.humidity = liste

    def __str__(self):
        day_night = "jour" if self.is_day == 1 else "nuit"
        formats_temps = {
            "Ensoleillé": "Le temps est ensoleillé",
            "Pluvieux": "Le temps est pluvieux",
            "Neigeux": "Le temps est neigeux",
            "Clair": "Le temps est clair",
            "Pluie légère": "Il y a une pluie légère",
            "Pluie modérée": "Il y a une pluie modérée"
        }
        temps_actual = formats_temps.get(self.condition, "Le temps est inconnu")
        date, time = self.localtime.split(" ")
        return f"Il fait actuellement {self.temp_c} degrés celsius dans la ville de {self.name}, {self.country}. On est le {date} et l'heure est {time}. {temps_actual} et il fait actuellement {day_night}. Le vent est de {self.wind_kph} km/h et l'humidité est de {self.humidity}%."

    def get_img_src(self):
        formats_temps = {
            "Ensoleillé": "static/images/sun.png",
            "Pluvieux": "static/images/rain.png",
            "Peigeux": "static/images/snow.png",
            "Clair": "static/images/clear.png",
            "Pluie légère": "static/images/light_rain.png",
            "Pluie modérée": "static/images/light_rain.png"
        }
        img_src = formats_temps.get(self.condition)
        return img_src


def valid_ville(city):
    if city is None:
        return False
    load_dotenv()
    key = os.getenv("api_key")
    api_response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={key}&q={city}&aqi=no&lang=fr")
    if api_response.status_code != 200:
        return False
    return True


def get_weather_data(city):
    load_dotenv()
    key = os.getenv("api_key")
    response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={key}&q={city}&aqi=no&lang=fr")
    json_data = response.json()
    meteo_actual = Meteo()
    current = json_data["current"]
    location = json_data["location"]
    data_list = [
        location["name"],
        location["country"],
        location["localtime"],
        current["temp_c"],
        current["wind_kph"],
        current["is_day"],
        current["condition"]["text"],
        current["humidity"]
    ]
    meteo_actual.fill_meteo(data_list)
    return str(meteo_actual)


def get_img_src(city_name):
    load_dotenv()
    key = os.getenv("api_key")
    response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={key}&q={city_name}&aqi=no&lang=fr")
    json_data = response.json()
    meteo_actual = Meteo()
    current = json_data["current"]
    location = json_data["location"]
    data_list = [
        location["name"],
        location["country"],
        location["localtime"],
        current["temp_c"],
        current["wind_kph"],
        current["is_day"],
        current["condition"]["text"],
        current["humidity"]
    ]
    meteo_actual.fill_meteo(data_list)
    return meteo_actual.get_img_src()
