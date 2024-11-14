from cProfile import label
from tkinter import  *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk,messagebox
from timezonefinder import TimezoneFinder
from datetime import  datetime
import requests
import pytz

root=Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False,False)

def getWeather():
    try:
        city=textField.get()

        geolocator = Nominatim(user_agent="weather_app")
        location= geolocator.geocode(city)
        if location is None:
            name.config(text="Location not found.")
            return


        reverse_location = geolocator.reverse((location.latitude, location.longitude), language='en')
        if reverse_location:
            city_name = reverse_location.raw.get('address', {}).get('city', 'Unknown City')
        else:
            city_name = 'Unknown City'

        print(f"City Name: {city_name}")

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        home=pytz.timezone(result)
        local_time=datetime.now(home)
        current_time=local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")



        api = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid=a3841746c0f007e20e1a5165d94759c6"

        try:
            json_data = requests.get(api).json()
            print(json_data)
            if 'weather' in json_data and 'main' in json_data:
                condition = json_data['weather'][0]['main']
                description = json_data['weather'][0]['description']
                temp = int(json_data['main']['temp'] - 273.15)  # Convert Kelvin to Celsius
                pressure = json_data['main']['pressure']
                humidity = json_data['main']['humidity']
                wind = json_data['wind']['speed']

                # Update the tkinter labels with weather data
                t.config(text=f"{temp}\u00B0")
                c.config(text=(condition, "|", "FEELS LIKE", temp, "°"))
                w.config(text=wind)
                h.config(text=humidity)
                d.config(text=description)
                p.config(text=pressure)

                # Also display the city name
                name.config(text=f"Weather for {city_name}")
            else:
                # If the 'weather' or 'main' key is missing, show this message
                name.config(text="Weather data not available. Please check the coordinates.")
        except Exception as e:
            print(f"Error retrieving weather data: {e}")
            name.config(text="Error retrieving weather data.")
    except Exception as e:
        messagebox.showerror("Weather App", "Invalid Entry!!")



#search box
Search_image=PhotoImage(file="search.png")
myimage=Label(image=Search_image)
myimage.place(x=20, y=20)

textField=tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0,fg="white")
textField.place(x=50, y=40)
textField.focus()


Search_icon=PhotoImage(file="search_icon.png")
myimage_icon=Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
myimage_icon.place(x=400, y=34)

#logo
Logo_image=PhotoImage(file="logo.png")
Logo=Label(image=Logo_image)
Logo.place(x=150, y=100)

#bottom box
Frame_image=PhotoImage(file="box.png")
frame_myimage=Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

#time
name=Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock=Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)


#label
label1=Label(root, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2=Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3=Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4=Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

t=Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c=Label(font=("arial", 15, 'bold'))
c.place(x=400, y=250)

w=Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)
h=Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)
d=Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)
p=Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)


root.mainloop()
