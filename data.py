import math
import requests
import pandas as pd

class Data():

    def __init__(self, file_name):
        self.df = pd.read_csv(file_name, low_memory=False)
        
        self.df["city"] = self.df["address"].apply(self.get_city).astype(str)
        self.df["rating_star"] = self.df["rating"].apply(self.get_rating_star)
        self.current_longitude = 0.0
        self.current_latitude = 0.0
        self.my_location()
        self.df["distance"] = self.df.apply(lambda row: self.get_distance(row["lat"], row["lon"]), axis=1).astype(float)
        self.df["distance_range"] = self.df["distance"].apply(self.get_distance_range).astype(float)
        lst = ["No data", 0.0]
        self.df.dropna()
        self.df = self.df[~(self.df['city'].isin(lst) & ~(self.df['distance'].isin(lst)) & (~(self.df['rating_star'].isin(lst))) & self.df['rating'].isna())]

    def get_columns(self, dataframe, column_name):
        return list(dataframe[column_name].unique())

    def search_by_category(self, category):
        return self.df[self.df["category_international"] == category]
    
    def search_by_distance(self, category, distance):
        return self.df[(self.df["category_international"] == category) & (self.df["distance_range"] <= distance)]
    
    def search_by_city(self, category, distance, city):
        return self.df[(self.df["category_international"] == category) & (self.df["distance_range"] <= distance) & (self.df["city"] == city)]
    
    def search_by_rating(self, category, distance, city, rating):
        return self.df[(self.df["category_international"] == category) & (self.df["distance_range"] <= distance) & (self.df["city"] == city) & (self.df["rating_star"] == rating)]
    
    def get_city(self, obj):
        try:
            return eval(obj)["city"]["name"]
        except:
            return "No data"
        
    def my_location(self):
        response0 = requests.get('https://api64.ipify.org/?format=json').json()
        ip_address = response0["ip"]
        response1 = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        self.current_latitude = response1.get('latitude')
        self.current_longitude = response1.get('longitude')

    def get_distance(self, obj1, obj2):
        try:
            lat_source = self.current_latitude
            lon_source = self.current_longitude
            lat_dest = float(obj1)
            lon_dest = float(obj2)
            lat_source, lon_source, lat_dest, lon_dest = map(math.radians, [lat_source, lon_source, lat_dest, lon_dest])
            dlon = lon_dest - lon_source
            dlat = lat_dest - lat_source
            a = math.sin(dlat/2)**2 + math.cos(lon_source) * math.cos(lat_dest) * math.sin(dlon/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = 6371 * c  # Earth's radius in kilometers
            return float(distance)
        except:
            return 0.0

    def get_distance_range(self, obj):
        try:
            if obj <= 0.8:
                return 0.8
            elif obj <= 2:
                return 2
            elif obj <= 10:
                return 10
            elif obj <= 30:
                return 30
            elif obj <= 50:
                return 50
            elif obj <= 100:
                return 100
            elif obj <= 200:
                return 200
            elif obj <= 300:
                return 300
            elif obj <= 400:
                return 400
            elif obj <= 500:
                return 500
            elif obj <= 600:
                return 600
            elif obj <= 700:
                return 700
            elif obj <= 800:
                return 800
            elif obj <= 1000:
                return 1000
        except:
            return 0.0
        
    def get_rating_star(self, obj):
        try:
            if obj <= 2:
                return "1 Star"
            elif obj <= 4:
                return "2 Stars"
            elif obj <= 6:
                return "3 Stars"
            elif obj <= 8:
                return "4 Stars"
            elif obj <= 10:
                return "5 Stars"
        except:
            return "No data"
        