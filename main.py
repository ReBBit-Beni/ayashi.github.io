import os
import requests
import discord
import traceback
import time
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["API_KEY"]
TOKEN = os.environ["DISCORD_TOKEN"]

intents=discord.Intents.all()
intents.members = True
intents.typing = False

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def 天気(ctx, city, dt=None):
    """
    市町村名と日時(オプション)を引数に、天気情報を取得するコマンド
    """
    if dt:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&dt={dt}"
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    await asyncio.sleep(10)

    response = requests.get(url)
    data = response.json()

    if dt:
        description = data['current']['weather'][0]['description']
        temp = round(data['current']['temp'] - 273.15, 1)
        feels_like = round(data['current']['feels_like'] - 273.15, 1)
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_speed']
        wind_deg = data['current']['wind_deg']
        dt_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dt))
        message = f"{city}の{dt_str}の天気は、{description}で、気温は{temp}℃、体感温度は{feels_like}℃、湿度は{humidity}%、風速は{wind_speed}m/s、風向きは{wind_deg}度です。"
      
    else:
        description = data['weather'][0]['description']
        temp = round(data['main']['temp'] - 273.15, 1)
        feels_like = round(data['main']['feels_like'] - 273.15, 1)
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        wind_deg = data['wind']['deg']
        message = f"{city}の現在の天気は、{description}で、気温は{temp}℃、体感温度は{feels_like}℃、湿度は{humidity}%、風速は{wind_speed}m/s、風向きは{wind_deg}度です。"

    description = data['weather'][0]['description']
    temp = round(data['main']['temp'] - 273.15, 1)
    feels_like = round(data['main']['feels_like'] - 273.15, 1)
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    wind_deg = data['wind']['deg']

    if "clear" in description:
        description_ja = "晴れ"
    elif "clouds" in description:
        description_ja = "曇り"
    elif "rain" in description:
        description_ja = "雨"
    elif "snow" in description:
        description_ja = "雪"
    elif "mist" in description:
        description_ja = "霧"
    else:
        description_ja = description

    if dt:
        dt_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dt))
        message = f"{city}の{dt_str}の天気は、{description_ja}で、気温は{temp}℃、体感温度は{feels_like}℃、湿度は{humidity}%、風速は{wind_speed}m/s、風向きは{wind_deg}度です。"
    else:
        message = f"{city}の現在の天気は、{description_ja}で、気温は{temp}℃、体感温度は{feels_like}℃、湿度は{humidity}%、風速は{wind_speed}m/s、風向きは{wind_deg}度です。"

    await ctx.send(message)

bot.run(TOKEN)
