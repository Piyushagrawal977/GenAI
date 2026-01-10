import requests

def get_weather(city):
    try:
        response = requests.get(f"https://wttr.in/{city}?format=%C+%t")
        return response
    except:
        return "something went wrong"


city=input("Enter the city ")
print(get_weather(city).text)