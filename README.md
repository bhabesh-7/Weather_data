Weather Agent
A Python-based application that fetches real-time weather data for Sehore, India, sends email updates, and displays an interactive web interface with a bar chart using Streamlit. The project integrates with the WeatherAPI to retrieve current weather, forecast, and astronomy data, and is hosted on GitHub for version control.
Features

Weather Data Retrieval:
Current Weather (/current.json): Temperature (e.g., 30.2°C), feels-like (33.7°C), humidity (75%), wind speed (21.6 km/h), pressure (1003.0 mb), visibility (6.0 km), precipitation (0.91 mm), UV index (0.4), cloud cover (75%).
Tomorrow’s Forecast (/forecast.json): Max/min temperatures (28.7°C/24.8°C), condition (e.g., "Patchy rain nearby").
Astronomy (/astronomy.json): Sunrise (05:37 AM), sunset (07:11 PM).


Email Notifications:
Sends immediate weather updates via Gmail (dummy94377992@gmail.com to bhabeshbk.7@gmail.com) using a secure App Password.


Streamlit UI:
Displays weather data in styled boxes (light blue background, black text) at http://localhost:8501.
Includes a light-mode bar chart visualizing temperature, feels-like, humidity, wind speed, pressure, and visibility.


Security:
Stores WeatherAPI key and Gmail App Password in a .env file, excluded from Git via .gitignore.


GitHub Integration:
Version-controlled repository with weather_agent.py, .gitignore, and this README.



Prerequisites

Python 3.8+ (tested on Linux Mint).
Git for version control.
WeatherAPI Key: Obtain from weatherapi.com.
Gmail App Password: Generate from Google Account > Security > App Passwords (requires 2-Step Verification).

Setup Instructions

Clone the Repository:
git clone https://github.com/your-username/weather-agent.git
cd weather-agent


Set Up Virtual Environment:
python3 -m venv venv
source venv/bin/activate


Install Dependencies:
pip install requests streamlit pandas python-dotenv


Configure Credentials:Create ~/.env:
nano .env

Add:
API_KEY=your_weatherapi_key
EMAIL_PASSWORD=your_gmail_app_password

Save and exit.

Run the Application:
streamlit run weather_agent.py


Opens UI at http://localhost:8501.
Sends an email with weather data.



Usage

Immediate Run:

Run streamlit run weather_agent.py to fetch weather data, send an email, and display the UI.
Check bhabeshbk.7@gmail.com (inbox/spam) for the email.
View the UI in a browser with text data and a bar chart.


Sample Output:

Email:Subject: Weather Update for Sehore - 2025-06-21**Current Weather**
Temperature: 30.2°C
Feels Like: 33.7°C
Humidity: 75%
Condition: Partly cloudy
Wind Speed: 21.6 km/h
Wind Direction: WSW
Pressure: 1003.0 mb
Visibility: 6.0 km
Precipitation: 0.91 mm
UV Index: 0.4
Cloud Cover: 75%

**Tomorrow's Forecast**
Max Temperature: 28.7°C
Min Temperature: 24.8°C
Condition: Patchy rain nearby

**Astronomy**
Sunrise: 05:37 AM
Sunset: 07:11 PM


UI (http://localhost:8501):
White background, black text, light blue text boxes.
Bar chart (blue bars) for temperature, feels-like, humidity, wind speed, pressure, visibility.




Optional Daily Scheduling:Install schedule:
pip install schedule

Modify weather_agent.py to add:
import schedule
import time
if __name__ == "__main__":
    print(f"Weather agent started. Sending updates for {CITY} at 08:00 daily.")
    schedule.every().day.at("08:00").do(weather_job)
    while True:
        schedule.run_pending()
        time.sleep(60)

Or use cron:
crontab -e

Add:
0 8 * * * /bin/bash -c "cd ~/weather-agent && source venv/bin/activate && python weather_agent.py >> log.txt 2>&1"



Troubleshooting

Invisible Text in UI:
Ensure browser is in light mode (Chrome: chrome://flags > Disable “Force Dark Mode”).
Check .stApp CSS (background-color: #ffffff, color: #000000) via browser Inspect tool.
Update Streamlit:pip install streamlit --upgrade




Chart Issues:
Verify pandas is installed (pip show pandas).
Check terminal for Error rendering chart.


API Errors:
Test API key:curl "http://api.weatherapi.com/v1/current.json?key=your_weatherapi_key&q=Sehore&aqi=no"


If 401, get a new key from weatherapi.com.


Email Errors:
Verify App Password in Google Account > Security > App Passwords.
Check spam/junk in bhabeshbk.7@gmail.com.



Security

Credentials: Stored in .env, excluded via .gitignore.
Email: Uses Gmail SMTP (port 465) with App Password.
Repository: Set to private on GitHub for sensitive projects.

Future Enhancements

Add support for other WeatherAPI endpoints (e.g., /alerts.json, /history.json).
Include interactive UI features (e.g., city input, refresh button).
Add more chart metrics (e.g., precipitation, UV index).
Deploy to Streamlit Cloud for remote access.

Contributing

Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit changes (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a pull request.

License
MIT License (or choose your preferred license).
Contact
For issues, open a GitHub issue or contact the repository owner.
Last updated: June 21, 2025
