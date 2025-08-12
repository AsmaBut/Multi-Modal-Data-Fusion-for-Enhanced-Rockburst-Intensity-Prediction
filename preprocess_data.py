import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from PIL import Image

# =========================
# CONFIG
# =========================
DATASET_CSV = os.path.join("Dataset", "synchronized_dataset.csv")
THERMAL_SIZE = (224, 224)  # For ResNet or similar CNN
OUTPUT_DIR = "preprocessed_data"

# Create output dir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(DATASET_CSV)

# =========================
# 1. Preprocess TABULAR (Vibration + Static Mechanical)
# =========================
# Drop columns that are file paths
tabular_df = df.drop(columns=["filename", "geo_map_path", "thermal_image_path"])

# Separate categorical and numerical
categorical_cols = ["seismic", "seismoacoustic", "shift", "hazard", "class", "rockburst_intensity"]
numerical_cols = [col for col in tabular_df.columns if col not in categorical_cols and col != "event_id"]

# Replace 'a' and other non-numeric placeholders with NaN
tabular_df[numerical_cols] = tabular_df[numerical_cols].apply(pd.to_numeric, errors="coerce")

# Build preprocessing pipeline
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numerical_cols),
        ("cat", categorical_transformer, categorical_cols)
    ]
)

tabular_features = preprocessor.fit_transform(tabular_df)
np.save(os.path.join(OUTPUT_DIR, "tabular_features.npy"), tabular_features.toarray() if hasattr(tabular_features, "toarray") else tabular_features)

print(f"[✔] Tabular features saved: {tabular_features.shape}")
#print(tabular_features)
# =========================
# 2. Preprocess THERMAL IMAGES
# =========================
thermal_features = []
for img_path in df["thermal_image_path"]:
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image not found: {img_path}")
    img = Image.open(img_path).convert("RGB")
    img = img.resize(THERMAL_SIZE)
    img_arr = np.array(img) / 255.0  # Normalize
    thermal_features.append(img_arr)

thermal_features = np.array(thermal_features, dtype=np.float32)
np.save(os.path.join(OUTPUT_DIR, "thermal_images.npy"), thermal_features)
print(f"[✔] Thermal images saved: {thermal_features.shape}")
#print(thermal_features)
# =========================
# 3. Preprocess GEOLOGICAL MAPS
# =========================
geo_features = []
for npy_path in df["geo_map_path"]:
    if not os.path.exists(npy_path):
        raise FileNotFoundError(f"Numpy file not found: {npy_path}")
    arr = np.load(npy_path)
    arr = arr.astype(np.float32)
    arr = (arr - np.min(arr)) / (np.ptp(arr) + 1e-8)  # Normalize 0-1
    geo_features.append(arr)

geo_features = np.array(geo_features, dtype=np.float32)
np.save(os.path.join(OUTPUT_DIR, "geo_maps.npy"), geo_features)
print(f"[✔] Geological maps saved: {geo_features.shape}")
print(geo_features.dtype)
print("[🎯] Preprocessing complete. Data ready for modeling!")
