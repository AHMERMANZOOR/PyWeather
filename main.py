from customtkinter import *
from darkdetect import isDark
from data import *
from settigns import *
from PIL import Image
from ttkbootstrap import DateEntry
from tkintermapview import *
from CTkMessagebox import CTkMessagebox
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="PyWeather")

class App(CTk):
    def __init__(self, is_dark):
        super().__init__(fg_color=MAIN_BG_COLOR)
        set_appearance_mode('dark' if is_dark else 'light')
        
        self.title('PyWeather')
        self.geometry('500x700')
            
        # Creating the date picker drop-down menu
        self.cal = DateEntry(self, dateformat='%Y-%m-%d')
        self.cal.pack(side='top', padx=5, pady=5)
        
        self.sv = self.cal.entry.get()
        self.cal.entry.bind('<FocusIn>', self.func)
        
        # Getting the coordinates and Defining the initial variables
        self.coordinates_address()
        
        # Widgets creation
        self.widgets(self.cal.entry.get())
        
        # Checking whether the user has chosen a location on the map
        self.x_coord.trace_add('write', lambda *args: self.widgets(self.cal.entry.get(), forget=True))
        self.y_coord.trace_add('write', lambda *args: self.widgets(self.cal.entry.get(), forget=True))
        
        self.mainloop()
    
    # Function: To reconfigure the app when the date changes
    def func(self, event):
        if self.sv != self.cal.entry.get():
            self.sv = self.cal.entry.get()
            self.widgets(self.sv, forget=True)
        
    # Function: To configure the DateEntry and create the widgets
    def date(self,sv):
        self.cal.entry.configure(textvariable=sv)
        print(self.cal.entry.get())
        self.widgets(self.cal.entry.get(), forget=True)
        
    # Function: To get coordinates and the location
    def coordinates_address(self):
        # Trying to get the coordinates if get error than use some random coords
        try:
            coordinates = get_coordinates() # Getting the coordinates
        except ConnectionError:
            coordinates = (41.40338, 2.17403)
            
        # Defining variables to record the x and y value of the user selected locations
        self.x_coord = DoubleVar(value=coordinates[0])
        self.y_coord = DoubleVar(value=coordinates[1])     
        
    # Function: To create all the widgets
    def widgets(self, date, forget=False):
        
        # Forgetting the previous layout to create a new one
        if forget==True:
            self.label.place_forget()
            self.labels.pack_forget()
            self.icon.pack_forget()
            self.graphs.pack_forget()
            self.temp_change.pack_forget()
                
        # Creating Widgets

        # Getting the data for the coordintates
        
        dat = data(self.x_coord.get(), self.y_coord.get(), date)
        
        # Storing the data
        self.temp = DoubleVar(value=dat[0])
        weather_code = dat[1]
        precipitation = dat[2]
        humidity = dat[3]
        wind_speed = dat[4]
        temp_var = dat[5]
        prep_var = dat[6]
        
        # Creating the temperature widget
        self.labels = TempLabel(self, 
                    self.temp, 
                    WEATHER_CODES[weather_code]['text'], 
                    prepcipitation=precipitation, 
                    humidity=humidity,
                    wind_speed=wind_speed)
        
        # Creating the weather symbol widget
        self.icon = WeatherIcon(self, weather_code)
        
        # Creating the graph for temperature and precipitation
        self.graphs = Graph(self, temp_var, prep_var)
        
        # Creating the button to change the temperature from Celsius to Farenheit
        self.img_celsius = CTkImage(light_image=Image.open("assets/celsius.png"), 
                                    dark_image=Image.open("assets/celsius.png"))
        self.img_farenheit = CTkImage(light_image=Image.open("assets/farenheit.png"), 
                                        dark_image=Image.open("assets/farenheit.png"))
        self.temp_change = CTkButton(
            self, 
            text="", 
            width=50, 
            height=50, 
            bg_color='transparent',
            command=self.celsius_farenheit,
            image=self.img_farenheit)
        self.temp_change.place(relx=0.98, rely=0.01, anchor='ne')
        self.is_celsius = True
        
        # Creating a button to open a new window for the map.
        self.map_img = CTkImage(light_image=Image.open('assets/map.png'),
                                dark_image=Image.open('assets/map.png'))
        self.map_view = CTkButton(self, 
                                    text="", 
                                    image=self.map_img, 
                                    width=50, 
                                    height=50, 
                                    command=lambda:self.mapping(self.x_coord,self.y_coord,self.address))
        self.map_view.place(relx=0.98, rely=0.09, anchor='ne')
        
        # Creating the Label to Show the Current selected location
        
            # Changing the coordinates into a proper address        
        self.address = geolocator.reverse(f'{self.x_coord.get()}, {self.y_coord.get()}').raw['address']
        self.address = StringVar(
            value=(f"{self.address.get('country')}, {self.address.get('city')}"))
        
        self.label = CTkLabel(self, text=self.address.get())
        self.label.place(relx=0.02, rely=0.01, anchor='nw')
        
    # Function: To create the Map window and get the address
    def mapping(self, x_var, y_var, address_var):
        self.maps = Map(self, x_var, y_var, address_var)

    # Function: To convert celsius to farenheit
    def celsius_farenheit(self):
        if self.is_celsius:
            self.temp.set(value=round(((self.temp.get() * 9/5) + 32),2))
            self.is_celsius = False
            self.temp_change.configure(image=self.img_celsius)
        else:
            self.temp.set(value=round(((self.temp.get() - 32) * 5/9),2))
            self.is_celsius = True
            self.temp_change.configure(image=self.img_celsius)
       
# Class to display all written info on weather 
class TempLabel(CTkFrame):
    def __init__(self, parent, temp, weather, prepcipitation, humidity, wind_speed):
        super().__init__(master=parent, fg_color='transparent')

        CTkLabel(master=self, text=f"Wind: {wind_speed} Km/h", font=("Arial", 20)).pack(side='bottom')        
        CTkLabel(master=self, text=f"Humidity: {humidity} %", font=("Arial", 20)).pack(side='bottom')
        CTkLabel(master=self, text=f"Precipitation: {prepcipitation} %", font=("Arial", 20)).pack(side='bottom')
        CTkLabel(master=self, text=weather, font=("Arial", 30)).pack(side='bottom')
        CTkLabel(master=self, textvariable=temp, font=("Arial", 100)).pack(side='bottom')

        self.pack(expand=True, fill='both', padx=30, pady=10)

# Class to display the weather code image               
class WeatherIcon(CTkFrame):
    def __init__(self, parent, weather_condition):
        super().__init__(parent, width=300,height=300, fg_color='transparent')

        self.pack(expand=True)
        self.img = Image.open(WEATHER_CODES[weather_condition]['image']).resize((200,200))
        self.img_tk = CTkImage(self.img, self.img, size=(200,200))
        CTkLabel(
            self, 
            width=200, 
            height=200, 
            text="",
            image=self.img_tk).pack(expand=True, fill='both')
       
# Class to create the tab view menu and display the graphs 
class Graph(CTkTabview):
    def __init__(self, parent, temp_var, prep_var):
        super().__init__(master=parent, height=300, width=500, fg_color=MAIN_BG_COLOR)
        
        self.pack(expand=True, fill='x')
        
        # Adding the tabs
        self.add('Temperature')
        self.add('Precipitation')
        
        # Creating the graphs
        Temp(self.tab('Temperature'), temp_var)
        Prep(self.tab('Precipitation'), prep_var)
  
# Class to generate the temp graph      
class Temp(CTkFrame):
    def __init__(self, parent, temp_var):
        super().__init__(parent, width=700, height=266, fg_color='transparent')
        
        self.pack()
        
        # Creating and allowing the image to resize
        
        self.img = Image.open(temp_var)
        self.img_tk = CTkImage(light_image=self.img, 
                          dark_image=self.img, 
                          size=(700, 266))
        parent.bind('<Configure>', lambda x : self.resize_img(parent)) 
        
        # Placing the image using a CTkLabel
               
        self.label = CTkLabel(self, 
                 image=self.img_tk, 
                 text="", 
                 bg_color='transparent',
                 width=700,
                 height=266)
        self.label.pack(expand=True, fill='both')
        
    # Function: to resize the image as the window resizes    
    
    def resize_img(self, parent):
        resize_img_tk = CTkImage(light_image=self.img, 
                        dark_image=self.img, 
                        size=(700 if parent.winfo_width() > 700 else parent.winfo_width(), 
                              266 if parent.winfo_height() > 266 else parent.winfo_height()))

        self.label.configure(image=resize_img_tk)
 
# Class the Precipitation graph       
class Prep(CTkFrame):
    def __init__(self, parent, prep_var):
        super().__init__(parent, width=700, height=266, fg_color='transparent')

        self.pack()
        
        # Creating and allowing the image to resize
        
        self.img = Image.open(prep_var)
        self.img_tk = CTkImage(light_image=self.img, 
                          dark_image=self.img, 
                          size=(700, 266))
        parent.bind('<Configure>', lambda x : self.resize_img(parent)) 
        
        # Placing the image using a CTkLabel
               
        self.label = CTkLabel(self, 
                 image=self.img_tk, 
                 text="", 
                 bg_color='transparent',
                 width=700,
                 height=266)
        self.label.pack(expand=True, fill='both')
        
    # Function: to resize the image as the window resizes    
    
    def resize_img(self, parent):
        resize_img_tk = CTkImage(light_image=self.img, 
                        dark_image=self.img, 
                        size=(700 if parent.winfo_width() > 700 else parent.winfo_width(), 
                              266 if parent.winfo_height() > 266 else parent.winfo_height()))

        self.label.configure(image=resize_img_tk)
 
# Class to make map window       
class Map(CTkToplevel):
    def __init__(self, parent, x_var, y_var, address_var):
        super().__init__(master=parent)
        
        self.title('Map')
        self.geometry('800x600')
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        
        self.f1 = CTkFrame(master=self)
        self.f1.grid(row=0, column=0, sticky='nsew')
        
        self.f2 = CTkFrame(master=self)
        self.f2.grid(row=0, column=1, sticky='nsew')
        
        self.map = TkinterMapView(self.f2, corner_radius=0)
        self.map.pack(expand=True, fill='both')
        
        self.map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
    
        self.map.add_right_click_menu_command(label="Add Marker",
                                        command=self.add_marker_event,
                                        pass_coords=True)
        self.address_var = StringVar()
        self.address = CTkEntry(self.f1, textvariable=self.address_var, height=40)
        self.address.pack(side='left',expand=True, fill='x', padx=5)
        self.search_img = CTkImage(light_image=Image.open('assets/search.png'),
                                   dark_image=Image.open('assets/search.png'), size=(30,30))
        self.search_bt = CTkButton(self.f1, 
                                   image=self.search_img, 
                                   text='', 
                                   command=self.search_event,
                                   bg_color='transparent',
                                   width=40,
                                   height=40)
        self.search_bt.pack(side='left', padx=5)
        
        self.last_marker = None
        self.x_var = x_var
        self.y_var = y_var
        self.var = address_var
        
    def add_marker_event(self,coords):
        if self.last_marker != None:
            self.last_marker.delete()
        try:
            
            # Setting the x and y variable values to get the proper data
            self.x_var.set(coords[0])
            self.y_var.set(coords[1])
            
            # Adding the marker on the map
            adr = geolocator.reverse(f'{coords[0]}, {coords[1]}')
            new_marker = self.map.set_marker(
                coords[0], 
                coords[1], 
                text=f"{adr.address}")
            
            self.last_marker = new_marker
        except (TypeError, AttributeError):
            CTkMessagebox(message="Please enter a valid address or locate it on the map and right click to add a marker.",
                  icon="info", option_1="Ok")
        
    def search_event(self, event=None):
        self.map.set_address(self.address_var.get())
        self.add_marker_event(convert_address_to_coordinates(self.address_var.get()))
       
if __name__ == '__main__': 
    App(isDark())