import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import streamlit as st
import pandas as pd

# Configuration
CITY = "Sehore"  # Indian city
API_KEY = "2f5743af955e475586b93427252106"  # Your WeatherAPI key
EMAIL_SENDER = "dummy94377992@gmail.com"  # Your Gmail address
EMAIL_PASSWORD = "fzjw wqrx eiul ukak"  # Your Gmail App Password
EMAIL_RECEIVER = "bhabeshbk.7@gmail.com"  # Recipient email

# Fetch current weather data
def get_current_weather(city, api_key):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "temp_c": data["current"]["temp_c"],
            "feelslike_c": data["current"]["feelslike_c"],
            "humidity": data["current"]["humidity"],
            "condition": data["current"]["condition"]["text"],
            "wind_kph": data["current"]["wind_kph"],
            "wind_dir": data["current"]["wind_dir"],
            "pressure_mb": data["current"]["pressure_mb"],
            "visibility_km": data["current"]["vis_km"],
            "precip_mm": data["current"]["precip_mm"],
            "uv": data["current"]["uv"],
            "cloud": data["current"]["cloud"]
        }
        return weather_data, (
            f"**Current Weather**\n"
            f"Temperature: {weather_data['temp_c']}°C\n"
            f"Feels Like: {weather_data['feelslike_c']}°C\n"
            f"Humidity: {weather_data['humidity']}%\n"
            f"Condition: {weather_data['condition'].capitalize()}\n"
            f"Wind Speed: {weather_data['wind_kph']} km/h\n"
            f"Wind Direction: {weather_data['wind_dir']}\n"
            f"Pressure: {weather_data['pressure_mb']} mb\n"
            f"Visibility: {weather_data['visibility_km']} km\n"
            f"Precipitation: {weather_data['precip_mm']} mm\n"
            f"UV Index: {weather_data['uv']}\n"
            f"Cloud Cover: {weather_data['cloud']}%"
        )
    return None, f"Error fetching current weather: {response.status_code}"

# Fetch forecast data (tomorrow)
def get_forecast(city, api_key):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=2&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tomorrow = data["forecast"]["forecastday"][1]
        return (
            f"\n**Tomorrow's Forecast**\n"
            f"Max Temperature: {tomorrow['day']['maxtemp_c']}°C\n"
            f"Min Temperature: {tomorrow['day']['mintemp_c']}°C\n"
            f"Condition: {tomorrow['day']['condition']['text'].capitalize()}"
        )
    return f"Error fetching forecast: {response.status_code}"

# Fetch astronomy data
def get_astronomy(city, api_key):
    url = f"http://api.weatherapi.com/v1/astronomy.json?key={api_key}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        sunrise = data["astronomy"]["astro"]["sunrise"]
        sunset = data["astronomy"]["astro"]["sunset"]
        return (
            f"\n**Astronomy**\n"
            f"Sunrise: {sunrise}\n"
            f"Sunset: {sunset}"
        )
    return f"Error fetching astronomy data: {response.status_code}"

# Send email
def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print(f"Email sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Job to fetch weather and send email
def weather_job():
    weather_data, current_text = get_current_weather(CITY, API_KEY)
    forecast_text = get_forecast(CITY, API_KEY)
    astronomy_text = get_astronomy(CITY, API_KEY)
    email_body = f"{current_text}\n{forecast_text}\n{astronomy_text}"
    subject = f"Weather Update for {CITY} - {datetime.now().strftime('%Y-%m-%d')}"
    send_email(subject, email_body)
    return weather_data, current_text, forecast_text, astronomy_text

# Streamlit UI
def display_ui(weather_data, current_text, forecast_text, astronomy_text):
    # Force light mode
    st.config.set_option("theme.base", "light")
    st.set_page_config(page_title=f"Weather in {CITY}", page_icon="🌦️", layout="wide")
    st.title(f"Weather Update for {CITY}")
    st.markdown("### Current Weather, Forecast, and Astronomy")
    
    # Solid background and text styling
    st.markdown("""
        <style>
        .stApp { 
            background-color: #ffffff; 
            color: #000000;
        }
        .weather-box { 
            background-color: #e6f3ff; 
            padding: 15px; 
            border-radius: 10px; 
            color: #000000;
            font-family: Arial, sans-serif;
        }
        .stMarkdown, .stText, .stHeader, .stSubheader { 
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display text data
    st.subheader("Current Weather")
    st.markdown(f'<div class="weather-box">{current_text.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
    st.subheader("Tomorrow's Forecast")
    st.markdown(f'<div class="weather-box">{forecast_text.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
    st.subheader("Astronomy")
    st.markdown(f'<div class="weather-box">{astronomy_text.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
    
    # Bar chart for current weather metrics
    if weather_data:
        st.subheader("Weather Metrics Visualization")
        chart_data = {
            "Metric": ["Temperature (°C)", "Feels Like (°C)", "Humidity (%)", "Wind Speed (km/h)", "Pressure (mb)", "Visibility (km)"],
            "Value": [
                weather_data["temp_c"],
                weather_data["feelslike_c"],
                weather_data["humidity"],
                weather_data["wind_kph"],
                weather_data["pressure_mb"],
                weather_data["visibility_km"]
            ]
        }
        df = pd.DataFrame(chart_data)
        try:
            st.bar_chart(df.set_index("Metric"), color="#36A2EB")
            print("Bar chart rendered successfully.")
        except Exception as e:
            print(f"Error rendering chart: {e}")
            st.error(f"Failed to render chart: {e}")
    else:
        st.error("Failed to fetch weather data for charting.")
        print("No weather data for charting.")

# Run immediately
if __name__ == "__main__":
    print(f"Sending weather update for {CITY} now...")
    weather_data, current_text, forecast_text, astronomy_text = weather_job()
    display_ui(weather_data, current_text, forecast_text, astronomy_text)