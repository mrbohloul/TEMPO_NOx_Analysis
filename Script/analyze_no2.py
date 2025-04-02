import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import glob

# Path to NetCDF files
folder_path = "path/to/your/netcdf/files/*.nc"
nc_files = sorted(glob.glob(folder_path))  # Get all 13 files

# Initialize lists
no2_datasets = []
lat_lon_loaded = False

# Load NO₂ data from all files
for file in nc_files:
    # Load geolocation (latitude, longitude) once
    if not lat_lon_loaded:
        geo_ds = xr.open_dataset(file, group="geolocation")
        lat = geo_ds["latitude"]
        lon = geo_ds["longitude"]
        lat_lon_loaded = True

    # Load NO₂ product data
    no2_ds = xr.open_dataset(file, group="product")
    no2_data = no2_ds["vertical_column_troposphere"]

    # Assign coordinates
    no2_data = no2_data.assign_coords({"latitude": lat, "longitude": lon})

    # Remove invalid values (negative and extreme high values)
    no2_data = no2_data.where((no2_data > 0) & (no2_data < np.nanpercentile(no2_data, 99.9)))

    # Append to list
    no2_datasets.append(no2_data)

# Merge datasets along a new dimension
combined_no2 = xr.concat(no2_datasets, dim="dataset", join="override")

# Compute mean NO₂ values, ignoring NaNs
mean_no2 = combined_no2.mean(dim="dataset", skipna=True)

# --- Visualization ---
fig, ax = plt.subplots(figsize=(12, 6), subplot_kw={'projection': ccrs.PlateCarree()})

# Ensure proper lat/lon dimensions for pcolormesh
img = ax.pcolormesh(
    mean_no2.longitude, mean_no2.latitude, mean_no2,
    cmap="plasma", shading="auto", transform=ccrs.PlateCarree(),
    vmin=0, vmax=np.nanpercentile(mean_no2, 99)
)

# Add map features
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.set_title("TEMPO NO₂")

# **Add Latitude and Longitude Gridlines**
gl = ax.gridlines(draw_labels=True, linestyle="--", linewidth=0.5, color="gray")
gl.right_labels = False  # Hide right-side longitude labels
gl.top_labels = False    # Hide top latitude labels

# Improved colorbar
cbar = plt.colorbar(img, ax=ax, orientation="horizontal", fraction=0.05)
cbar.set_label("NO₂ (molecules/cm²)")

# Show plot
plt.show()

