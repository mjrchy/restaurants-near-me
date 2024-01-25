import requests
import tkintermapview 

class Map():

    def __init__(self, frame):
        self.frame = frame
        self.map_widget = tkintermapview.TkinterMapView(frame, width=820, height=450, corner_radius=0)
        self.show_map()
        self.map_widget.set_position(13.736717, 100.523186)  # Thailand
        self.map_widget.set_zoom(6)
        self.current_latitude = 0.0
        self.current_longitude = 0.0
        self.my_location()

    def show_map(self):
        self.map_widget.place(x=225, y=210)

    def hide_map(self):
        self.map_widget.place_forget()

    def marker(self, latitude, longitude, location_name):
        self.map_widget.set_marker(latitude, longitude, location_name)

    def clear_marker(self):
        self.map_widget.delete_all_marker()

    def my_location(self):
        response0 = requests.get('https://api64.ipify.org/?format=json').json()
        ip_address = response0["ip"]
        response1 = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        self.current_latitude = response1.get('latitude')
        self.current_longitude = response1.get('longitude')
        self.map_widget.set_marker(self.current_latitude, self.current_longitude, text="My location")
