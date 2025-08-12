import pandas as pd
import os


dataset_dir = "Dataset"
geo_csv_path = os.path.join(dataset_dir, "Geological Maps.csv")
vib_csv_path = os.path.join(dataset_dir, "Vibration dataset.csv")
static_csv_path = os.path.join(dataset_dir, "Static Mechanical tests.csv")
geo_folder = os.path.join(dataset_dir, "Geological Maps")
thermal_folder = os.path.join(dataset_dir, "Thermal Images")


geo_df = pd.read_csv(geo_csv_path)
vib_df = pd.read_csv(vib_csv_path)
static_df = pd.read_csv(static_csv_path)


geo_df["event_index"] = geo_df.index
vib_df["event_index"] = vib_df.index
static_df["event_index"] = static_df.index  

# Map geological .npy file paths
geo_df["geo_map_path"] = geo_df["filename"].apply(lambda f: os.path.join(geo_folder, f))

# Map thermal image file paths
geo_df["thermal_image_path"] = geo_df["filename"].apply(
    lambda f: os.path.join(thermal_folder, f.replace("geological_map_small_", "thermal_image_").replace(".npy", ".JPEG"))
)

# Merge all dataframes on event_index
merged_df = geo_df.merge(vib_df, on="event_index", suffixes=("_geo", "_vib"))
merged_df = merged_df.merge(static_df, on="event_index", suffixes=("", "_static"))

# Save final synchronized CSV
output_csv = os.path.join(dataset_dir, "synchronized_dataset.csv")
merged_df.to_csv(output_csv, index=False)

print(f"Synchronized dataset saved to: {output_csv}")
print(merged_df.head())
