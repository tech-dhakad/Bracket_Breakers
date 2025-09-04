import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# ---------------- Config ----------------
st.set_page_config(page_title="Weather App", layout="wide")

API_KEY = "YOUR_OPENWEATHER_API_KEY"  # 🔑 Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/"

# ---------------- Helper functions ----------------
def get_weather(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    r = requests.get(url).json()
    return r

def get_forecast(city):
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
    r = requests.get(url).json()
    return r

# ---------------- UI ----------------
st.title("🌦️ Weather App with Maps")

city = st.text_input("Enter city name", "Bhopal")

if st.button("Get Weather"):
    data = get_weather(city)

    if data.get("cod") != 200:
        st.error("City not found!")
    else:
        st.subheader(f"📍 {data['name']}, {data['sys']['country']}")
        st.write(f"**Temperature:** {data['main']['temp']}°C")
        st.write(f"**Weather:** {data['weather'][0]['description'].title()}")
        st.write(f"**Humidity:** {data['main']['humidity']}%")
        st.write(f"**Wind:** {data['wind']['speed']} m/s")

        # Show location on map
        lat, lon = data["coord"]["lat"], data["coord"]["lon"]
        m = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker(
            [lat, lon],
            tooltip=f"{data['name']}: {data['main']['temp']}°C",
            popup=f"Weather: {data['weather'][0]['description']}",
        ).add_to(m)
        st_folium(m, width=700, height=500)

        # Forecast
        forecast = get_forecast(city)
        st.subheader("📅 5-Day Forecast (Every 3 hours)")
        for item in forecast["list"][:10]:  # show first 10 entries
            st.write(
                f"{item['dt_txt']} - {item['main']['temp']}°C, {item['weather'][0]['description']}"
            )
