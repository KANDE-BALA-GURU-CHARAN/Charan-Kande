"""Weather App mini project using the Open-Meteo API."""

import json
import threading
import tkinter as tk
from tkinter import messagebox
from urllib.parse import quote
from urllib.request import urlopen


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    95: "Thunderstorm",
}


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("520x380")
        self.resizable(False, False)
        self.configure(bg="#f8fafc")

        tk.Label(self, text="Weather App", font=("Segoe UI", 22, "bold"), bg="#f8fafc").pack(pady=(24, 8))

        form = tk.Frame(self, bg="#f8fafc")
        form.pack(pady=10)
        self.city_entry = tk.Entry(form, width=30, font=("Segoe UI", 12))
        self.city_entry.insert(0, "Mumbai")
        self.city_entry.pack(side="left", padx=6)
        tk.Button(form, text="Get Weather", command=self.start_fetch).pack(side="left", padx=6)

        self.result = tk.Label(
            self,
            text="Enter a city and click Get Weather.",
            font=("Segoe UI", 12),
            bg="#ffffff",
            fg="#111827",
            justify="left",
            anchor="nw",
            relief="solid",
            bd=1,
            padx=14,
            pady=14,
            width=46,
            height=10,
        )
        self.result.pack(pady=18)

    def start_fetch(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Missing City", "Please enter a city name.")
            return
        self.result.config(text="Loading weather data...")
        threading.Thread(target=self.fetch_weather, args=(city,), daemon=True).start()

    def fetch_json(self, url):
        with urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    def fetch_weather(self, city):
        try:
            location_url = f"https://geocoding-api.open-meteo.com/v1/search?name={quote(city)}&count=1"
            location_data = self.fetch_json(location_url)
            if not location_data.get("results"):
                raise ValueError("City not found.")

            place = location_data["results"][0]
            latitude = place["latitude"]
            longitude = place["longitude"]
            weather_url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={latitude}&longitude={longitude}"
                "&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
            )
            weather_data = self.fetch_json(weather_url)
            current = weather_data["current"]
            condition = WEATHER_CODES.get(current["weather_code"], "Unknown")
            text = (
                f"City: {place['name']}, {place.get('country', '')}\n"
                f"Temperature: {current['temperature_2m']} C\n"
                f"Humidity: {current['relative_humidity_2m']}%\n"
                f"Wind Speed: {current['wind_speed_10m']} km/h\n"
                f"Condition: {condition}\n\n"
                "Source: Open-Meteo API"
            )
            self.after(0, lambda: self.result.config(text=text))
        except Exception as error:
            self.after(0, lambda: self.result.config(text=f"Could not load weather data.\n\n{error}"))


if __name__ == "__main__":
    WeatherApp().mainloop()
