import geopandas
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(30, 30))
world.plot(ax=ax)

df = pd.read_parquet('assets/pipeline_data_full.parquet')
points_df = df.copy()
points_df['heading_deg2'] = points_df.heading_deg.shift(-1)
points_df['heading_deg_diff'] = np.sqrt(2 - 2 * np.cos(points_df.heading_deg2 - points_df.heading_deg))
points_df = points_df[points_df.heading_deg_diff > 1.95]
plt.scatter(points_df.longitude_deg, points_df.latitude_deg, s=1, c='red')
plt.show()
