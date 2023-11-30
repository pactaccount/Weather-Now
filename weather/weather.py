import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

#to get weather information from API
def get_weather(city):
    API_key = "4b45df21b8423bddb92b464a3613024e"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror('Error','City not found')
        return None
    
    # Parse the response JSON to get weather information
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    #get icon URL and return all weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)


#function to search weather for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    #if the city not found
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    #get the weather icon
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    #update
    temperature_label.configure(text=f"Temperature: {temperature:.2f}℃")
    description_label.configure(text=f"Description: {description}")


root = ttkbootstrap.Window(themename="morph")
root.title("Weather Now")
root.geometry("400x400")

# to enter the city name
city_entry = ttkbootstrap.Entry(root, font='Helventica, 18')
city_entry.pack(pady=10)

# to search weather information
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

# to show city/country
location_label = tk.Label(root, font="Helventica, 25")
location_label.pack(pady=20)

# to show weather icon
icon_label = tk.Label(root)
icon_label.pack()

#to show temperature
temperature_label = tk.Label(root, font="Helventica, 20")
temperature_label.pack()

#to show the weather description
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()