# !pip install cdsapi

import cdsapi
import os

# Initialize the CDS API client
client = cdsapi.Client()

# Define the years from which to download data
years = list(range(2011,2025))

# Define the path where you want to save the .nc files
save_path = "./era5_data/"
os.makedirs(save_path, exist_ok=True)

for year in years:
    dataset = "reanalysis-era5-single-levels"
    request = {
        "product_type": ["reanalysis"],
        "variable": ["total_precipitation"],
        "year": str(year),
        "month": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12"
        ],
        "day": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12",
            "13", "14", "15",
            "16", "17", "18",
            "19", "20", "21",
            "22", "23", "24",
            "25", "26", "27",
            "28", "29", "30",
            "31"
        ],
        "time": [
            "00:00", "01:00", "02:00",
            "03:00", "04:00", "05:00",
            "06:00", "07:00", "08:00",
            "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00",
            "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00",
            "21:00", "22:00", "23:00"
        ],
        "data_format": "grib",
        "download_format": "unarchived",
        "area": [13, 74.5, 8, 77.5],         # North, West, South, East. Adjust as needed.
    }

    client.retrieve(dataset, request, os.path.join(save_path, f"era5_{year}.grib"))
    print(f"Downloaded data for {year} and saved to {save_path}era5_{year}.grib")
