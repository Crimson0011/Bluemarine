import discord
import requests

# ใส่ API Key ของ WeatherAPI
WEATHER_API_KEY = "MY_API"
DISCORD_TOKEN = "MY_DISCORD_TOKEN"

# สร้างคลาสสำหรับบอท
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# ฟังก์ชันดึงข้อมูลสภาพอากาศ
def get_weather_data(location):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&lang=th"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# ฟังก์ชันแสดงผลสภาพอากาศ
def display_weather(data):
    if data:
        city_name = data["location"]["name"]
        region = data["location"]["region"]
        country = data["location"]["country"]
        temperature = data["current"]["temp_c"]
        weather_desc = data["current"]["condition"]["text"]
        wind_speed = data["current"]["wind_kph"]
        humidity = data["current"]["humidity"]
        visibility = data["current"]["vis_km"]
        
        weather_info = (f"📍 สภาพอากาศใน **{city_name}, {region}, {country}**\n"
                        f"🌤️ สภาพอากาศ: {weather_desc}\n"
                        f"🌡️ อุณหภูมิ: {temperature}°C\n"
                        f"💨 ความเร็วลม: {wind_speed} km/h\n"
                        f"💧 ความชื้น: {humidity}%\n"
                        f"👀 ระยะการมองเห็น: {visibility} km")
        
        return weather_info
    else:
        return "❌ ไม่สามารถดึงข้อมูลสภาพอากาศได้"

# Event เมื่อบอทพร้อมใช้งาน
@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

# Event เมื่อมีข้อความเข้ามา
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # ค้นหาข้อมูลสภาพอากาศจากข้อความ
    if message.content.startswith("!weather "):
        location_query = message.content[9:].strip()  # ตัด "!weather " ออก
        data = get_weather_data(location_query)
        weather_message = display_weather(data)
        await message.channel.send(weather_message)

# เริ่มรันบอท
client.run(DISCORD_TOKEN)
