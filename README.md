# TEMPO NO₂ Analysis
This project processes and visualizes tropospheric NO₂ column data from TEMPO satellite NetCDF files.

## 📂 Folder Structure
- `src/analyze_no2.py` – Main script for processing and plotting.
- `data/` - NetCDF (.nc) files produced by the TEMPO
- `results` - # 📸 Example output plot

🧾 Script Overview
The script analyze_no2.py is designed to process and visualize tropospheric NO₂ vertical column densities from a set of NetCDF (.nc) files produced by the TEMPO (Tropospheric Emissions: Monitoring of Pollution) satellite.

🔍 What it does:
Loads NO₂ data from the product group of multiple NetCDF files.
Extracts and applies geolocation data (latitude and longitude) from the geolocation group.
Filters out invalid NO₂ values (negative or extreme outliers).
Merges all NO₂ datasets into a single xarray object.
Computes the mean NO₂ column across all files.
Visualizes the result using Cartopy with a color-mapped pcolormesh and map features.

📦 Required Modules
Here’s what each package does in the script:

Module	Purpose
xarray: For reading NetCDF files and handling multi-dimensional datasets
numpy:	For numerical operations and percentile-based filtering
matplotlib.pyplot:	For creating the NO₂ plot
cartopy.crs:	For defining map projection (e.g. PlateCarree)
cartopy.feature:	For adding coastlines, borders, and gridlines to the map
glob:	For file handling — collects all .nc files from the given directory
