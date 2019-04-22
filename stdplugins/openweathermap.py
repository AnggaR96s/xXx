"""Get weather data using OpenWeatherMap
Syntax: .weather <Location> """

import requests
import time
from telethon import events
from uniborg.util import admin_cmd


@borg.on(admin_cmd("weather (.*)"))
async def _(event):
    if event.fwd_from:
        return
    sample_url = "https://api.openweathermap.org/data/2.5/weather?q={}&APPID={}&units=metric"
    input_str = event.pattern_match.group(1)
    response_api = requests.get(sample_url.format(input_str, Config.OPEN_WEATHER_MAP_APPID)).json()
    if response_api["cod"] == 200:
        await event.edit(
            """**{}**
**Temperature**: {}°С
    **Min**: {}°С
    **Max**: {}°С
**Humidity**: {}%
**wind**: {}m/s
**Clouds**: {}hpa
**Sunrise**: {} UTC
**Sunset**: {} UTC""".format(
                input_str,
                response_api["main"]["temp"],
                response_api["main"]["temp_min"],
                response_api["main"]["temp_max"],
                response_api["main"]["humidity"],
                response_api["wind"]["speed"],
                response_api["clouds"]["all"],
                # response_api["main"]["pressure"],
                time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(response_api["sys"]["sunrise"])),
                time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(response_api["sys"]["sunset"]))
            )
        )
    else:
        await event.edit(response_api["message"])
