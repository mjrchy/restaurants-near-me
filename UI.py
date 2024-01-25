import tkinter as tk
from tkinter import ttk
from data import Data
from map import Map
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class UI(tk.Tk):

    def __init__(self):
        super().__init__()
        # data
        self.data = Data('restaurants-near-me\Lineman_Shops.csv')
        self.dataframe = self.data.df

        # map widget
        self.map = Map(self)
        self.configure(background="#FEFAE0")

        # variable to search data
        self.category_select = tk.StringVar()
        self.distance_select = tk.IntVar()
        self.city_select = tk.StringVar()
        self.rating_select = tk.StringVar()
        self.graph_type = tk.StringVar()

        self.figure = Figure(figsize=(5, 4), dpi=100)

        self.clean_df = self.clean_dataframe()

        # default page
        self.main_page()

    def hide_widget(self, widget_list: tk.Button):
        """to hide widget in window"""
        for widget in widget_list:
            widget.place_forget()

    def main_page(self):
        # show map
        self.map.show_map()
        try:
            self.figure.clear()
            self.graph_box.place_forget()
            self.label5.place_forget()
            self.label6.place_forget()
            self.label7.place_forget()
        except:
            pass

        # set window
        self.title("Restaurants Near Me")
        self.attributes('-fullscreen',True)

        # button
        self.search_btn = tk.Button(self, text="Search", font=("Century Gothic",10), command=self.search)
        self.search_btn.place(x=930, y=145)
        self.clear_btn = tk.Button(self, text="Clear", font=("Century Gothic",10), command=self.clear)
        self.clear_btn.place(x=995, y=145)
        self.menu_button()

        # label
        self.label0 = tk.Label(self, text="Restaurants Near Me", font=("Century Gothic",30), background="#FEFAE0")
        self.label0.place(x=450, y=40)

        self.label1 = tk.Label(self, text="Category", font=("Century Gothic",10), background="#FEFAE0")
        self.label1.place(x=225, y=125)

        self.label2 = tk.Label(self, text="Distance from you (km)", font=("Century Gothic",10), background="#FEFAE0")
        self.label2.place(x=400, y=125)

        self.label3 = tk.Label(self, text="City", font=("Century Gothic",10), background="#FEFAE0")
        self.label3.place(x=575, y=125)

        self.label4 = tk.Label(self, text="Rating Star", font=("Century Gothic",10), background="#FEFAE0")
        self.label4.place(x=750, y=125)

        # category combobox
        category_list = self.data.get_columns(self.dataframe, "category_international")
        self.category_box = ttk.Combobox(self, text="select", textvariable=self.category_select, values=category_list, font=("Century Gothic",10), state="readonly")
        self.category_box.bind('<<ComboboxSelected>>', lambda event: self.category_selected())
        self.category_box.place(x=225, y=150)

        # distance combobox
        self.distance_box = ttk.Combobox(self, text="select", textvariable=self.distance_select, font=("Century Gothic",10), state="readonly")
        self.distance_box.bind('<<ComboboxSelected>>', lambda event: self.distance_selected())
        self.distance_box.place(x=400, y=150)

        # city combobox
        self.city_box = ttk.Combobox(self, text="select", textvariable=self.city_select, font=("Century Gothic",10), state="readonly")
        self.city_box.bind('<<ComboboxSelected>>', lambda event: self.city_selected())
        self.city_box.place(x=575, y=150)                                         

        # rating combobox
        self.rating_box = ttk.Combobox(self, text="select", textvariable=self.rating_select, font=("Century Gothic",10), state="readonly")
        self.rating_box.bind('<<ComboboxSelected>>', lambda event: self.rating_selected())
        self.rating_box.place(x=750, y=150)

        # set all search to default
        self.clear()

    def menu_button(self):
        """create menu button"""
        self.menu_btn = ttk.Menubutton(self, text="Menu")
        menu = tk.Menu(self.menu_btn, tearoff = 0)
        self.menu_btn["menu"] = menu
        menu.add_command(label="Main Page", command=self.main_page, font=("Century Gothic",10))
        menu.add_command(label="Data Analysis", command=self.data_analysis_page,font=("Century Gothic",10))
        menu.add_command(label="Exit Program", command=self.destroy, font=("Century Gothic",10))
        self.menu_btn.place(x=10, y=10)

    def category_selected(self):
        """category search"""
        df_category = self.data.search_by_category(self.category_select.get())
        self.distance_box.configure(values=self.data.get_columns(df_category, "distance_range"))
        self.category_box.configure(state="disable")

    def distance_selected(self):
        """distance search"""
        df_distance = self.data.search_by_distance(self.category_select.get(), self.distance_select.get())
        self.city_box.configure(values=self.data.get_columns(df_distance, "city"))
        self.distance_box.configure(state="disable")

    def city_selected(self):
        """city search"""
        df_city = self.data.search_by_city(self.category_select.get(), self.distance_select.get(), self.city_select.get())
        self.rating_box.configure(values=self.data.get_columns(df_city, "rating_star"))
        self.city_box.configure(state="disable")
    
    def rating_selected(self):
        """rating search"""
        self.rating_box.configure(state="disable")

    def search(self):
        """command for search button"""
        df_rating = self.data.search_by_rating(self.category_select.get(), self.distance_select.get(), self.city_select.get(), self.rating_select.get())
        lat_list = list(df_rating["lat"])
        lon_list = list(df_rating["lon"])
        name_list = list(df_rating["name"])
        for i in range(0, len(lat_list) - 1):
            self.map.marker(float(lat_list[i]), float(lon_list[i]), name_list[i])

    def clear(self):
        """command for clear all search"""
        # clear all marker in the map
        self.map.clear_marker()

        # mark my location
        self.map.my_location()

        # clear combo box
        self.category_box.configure(state="normal")
        self.distance_box.configure(values=[], state="normal")
        self.city_box.configure(values=[], state="normal")
        self.rating_box.configure(values=[], state="normal")

        # set variable to ""
        self.category_select.set("")
        self.distance_select.set(0)
        self.city_select.set("")
        self.rating_select.set("")

    def clean_dataframe(self):
        # cut outliers of rating
        #Find quartile 1
        q1 = self.dataframe["rating"].quantile(0.25)
        #Find quartile 3
        q3 = self.dataframe["rating"].quantile(0.75)
        #Find iqr
        iqr = q3-q1
        #Put values that are NOT below q1-1.5*iqr and above q3+1.5*iqr in dataframe clean_df
        self.clean_df = self.dataframe[~((self.dataframe["rating"] < q1-1.5*iqr) | (self.dataframe["rating"] > q3+1.5*iqr))]

        # cut outliers of distance
        #Find quartile 1
        q1 = self.dataframe["distance"].quantile(0.25)
        #Find quartile 3
        q3 = self.dataframe["distance"].quantile(0.75)
        #Find iqr
        iqr = q3-q1
        #Put values that are NOT below q1-1.5*iqr and above q3+1.5*iqr in dataframe clean_df
        self.clean_df = self.dataframe[~((self.dataframe["distance"] < q1-1.5*iqr) | (self.dataframe["distance"] > q3+1.5*iqr))]
        return self.clean_df

    def data_analysis_page(self):
        """create Data Analysis page"""
        # hide widget
        widget_list = [self.search_btn, self.clear_btn, self.category_box, self.distance_box, self.city_box,
                        self.rating_box, self.label1, self.label2, self.label3, self.label4]
        self.hide_widget(widget_list)
        self.map.hide_map()

        # default graph
        self.statistics_selected()

        self.label5 = tk.Label(self, text="Select Graph", font=("Century Gothic",15), background="#FEFAE0")
        self.label5.place(x=600, y=137)  

        self.label5 = tk.Label(self, text="Data Analysis", font=("Century Gothic",20), background="#FEFAE0")
        self.label5.place(x=400, y=130) 

        self.graph_box = ttk.Combobox(self, text="select", textvariable=self.graph_type,
                                     values=["Descriptive statistics", "Correlation and Scatter Plot", "Part to Whole"],
                                      font=("Century Gothic",10), state="readonly")
        self.graph_box.bind('<<ComboboxSelected>>', lambda event: self.graph_selected())
        self.graph_box.place(x=750, y=143)

    def graph_selected(self):
        if self.graph_type.get() == "Descriptive statistics":
            self.statistics_selected()
        elif self.graph_type.get() == "Correlation and Scatter Plot":
            self.correlation_selected()
        elif self.graph_type.get() == "Part to Whole":
            self.part_to_whole_selected()

    def statistics_selected(self):
        self.figure.clear()
        axes = self.figure.add_subplot()
        self.histogram = FigureCanvasTkAgg(self.figure, master=self)
        self.histogram.get_tk_widget().place(x=400, y=210)
        self.rowconfigure(1, weight=1) 
        self.clean_df.hist(ax=axes, column="distance", density=True, range=(0, 350), color='#FF6464')
        axes.set_xlabel("Distance")
        axes.set_ylabel("Frequency")
        axes.set_title(f"Histogram of Distance")
        self.histogram.draw()       

        mean = self.clean_df["distance"].mean()
        self.label6 = tk.Label(self, text=f"Mean = {mean}", font=("Century Gothic",15), background="#FEFAE0")
        self.label6.place(x=400, y=650) 
        self.label7 = tk.Label(self, text=f"Exponential Distribution", font=("Century Gothic",15), background="#FEFAE0")
        self.label7.place(x=670, y=650) 

    def correlation_selected(self):
        self.figure.clear()
        self.hide_widget([self.label6, self.label7])

        axes = self.figure.add_subplot()

        axes.scatter(self.clean_df["rating"], self.clean_df["distance"], color='#6EDCD9')
        self.scatter = FigureCanvasTkAgg(self.figure, self)
        self.scatter.get_tk_widget().place(x=400, y=210)
        axes.legend(["distance"])
        axes.set_xlabel('Rating')
        axes.set_title('Scatter Plot of Rating and Distance')
        self.scatter.draw()

    def part_to_whole_selected(self):
        self.figure.clear()
        self.hide_widget([self.label6, self.label7])

        self.bar = FigureCanvasTkAgg(self.figure, self)
        self.bar.get_tk_widget().place(x=400, y=210)
        axes = self.figure.add_subplot()

        df = self.dataframe['category_international'].value_counts().sort_values(ascending=False)
        df.head(30).plot(kind='bar', legend=True, ax=axes, fontsize=7, color='#FF7F50')

        axes.set_xlabel('Categories')
        axes.set_ylabel('Frequency')
        axes.set_title('Bar Graph of Categories')
        self.bar.draw()
