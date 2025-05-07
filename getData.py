import pandas as pd
import os

def load_data(filename):
    # Dapatkan path folder file ini
    base_path = os.path.dirname(__file__)
    
    # Gabungkan dengan nama file (relatif ke lokasi file .py)
    full_path = os.path.join(base_path, filename)
    
    # Baca CSV
    df = pd.read_csv(full_path)
    return df
