import os
from UI import UI
from data import Data

if __name__ == '__main__':
    ui = UI()
    file_path = 'Lineman_Shops.csv'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:  
            data = Data(file_path)
    ui.mainloop()
