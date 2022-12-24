import requests

# Replace YOUR_API_KEY with your actual API key
API_KEY = 'YOUR_API_KEY'

def get_weather(city):
    # Send a request to the OpenWeather API to get the weather data for the given city
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}')
    
    # Check if the request was successful
    if r.status_code == 200:
        # Convert the response to a JSON object
        data = r.json()
        
        # Get the temperature, humidity, and description from the JSON object
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        
        # Return a string with the weather data
        return f'Temperature: {temperature}°C, Humidity: {humidity}%, Description: {description}'
    else:
        # Return an error message if the request was not successful
        return 'Error getting weather data'
