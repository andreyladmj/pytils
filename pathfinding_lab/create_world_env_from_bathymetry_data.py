import sys
from os.path import basename, join

import numpy as np
import pandas as pd

bathymetry = np.load(sys.argv[1])

base_dir = basename(sys.argv[1])
lats = np.load(join(base_dir, 'latitudes_1x1_tiles_resolution.npy'))
lons = np.load(join(base_dir, 'longitudes_1x1_tiles_resolution.npy'))

with open("data/NOAA_bathymetry_1x1_final_resolution.bin", 'wb') as f:
    f.write(bytearray(bathymetry))

with open("data/latitudes_1x1_tiles_resolution.bin", 'wb') as f:
    f.write(bytearray(lats))

with open("data/longitudes_1x1_tiles_resolution.bin", 'wb') as f:
    f.write(bytearray(lons))


df = pd.read_parquet('data/pipeline_data_full.parquet')
points_df = df.copy()
points_df['heading_deg2'] = points_df.heading_deg.shift(-1)
points_df['heading_deg_diff'] = np.sqrt(2 - 2 * np.cos(points_df.heading_deg2 - points_df.heading_deg))
points_df = points_df[points_df.heading_deg_diff > 1.95]
points_df['latitude_rad'] = np.deg2rad(points_df['latitude_deg'])
points_df['longitude_rad'] = np.deg2rad(points_df['longitude_deg'])
lat_lons = points_df[['latitude_rad', 'longitude_rad']].values

with open("data/ships_lat_lons.bin", 'wb') as f:
    f.write(bytearray(lat_lons))


import matplotlib.pyplot as plt
fig = plt.figure()
plt.imshow(bathymetry)
plt.show()
