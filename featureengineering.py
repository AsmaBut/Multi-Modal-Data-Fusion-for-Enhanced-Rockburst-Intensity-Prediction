# featureengineering.py
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, Input
from sklearn.preprocessing import StandardScaler
import joblib
import os

# ==== Paths ====
TABULAR_PATH = "preprocessed_data/tabular_features.npy"
THERMAL_PATH = "preprocessed_data/thermal_images.npy"
GEO_MAPS_PATH = "preprocessed_data/geo_maps.npy"
SYNC_CSV_PATH = "Dataset/synchronized_dataset.csv"

OUTPUT_FEATURES_PATH = "preprocessed_data/fused_features.npy"


# ==== Load preprocessed data ====
print("[📂] Loading preprocessed data...")
tabular_data = np.load(TABULAR_PATH)
thermal_images = np.load(THERMAL_PATH)
geo_maps = np.load(GEO_MAPS_PATH)
df = pd.read_csv(SYNC_CSV_PATH)

print(f"Tabular shape: {tabular_data.shape}")
print(f"Thermal shape: {thermal_images.shape}")
print(f"Geo maps shape: {geo_maps.shape}")

# ==== Process thermal images with ResNet50 ====
print("[🔥] Extracting thermal image features using ResNet50...")
resnet_base = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
resnet_model = Model(inputs=resnet_base.input, outputs=Flatten()(resnet_base.output))

thermal_images_prep = preprocess_input(thermal_images.astype(np.float32))
thermal_features = resnet_model.predict(thermal_images_prep, verbose=1)
print(f"Thermal features shape: {thermal_features.shape}")

# ==== Process geological maps with small CNN ====
print("[🗺] Extracting geological map features using small CNN...")
geo_input = Input(shape=(32, 32, 5))
geo_cnn = Sequential([
    Conv2D(16, (3,3), activation='relu', padding='same', input_shape=(32, 32, 5)),
    MaxPooling2D((2,2)),
    Conv2D(32, (3,3), activation='relu', padding='same'),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.3)
])

geo_features = geo_cnn(geo_maps)
geo_extractor = Model(inputs=geo_input, outputs=geo_cnn(geo_input))
geo_features = geo_extractor.predict(geo_maps, verbose=1)
print(f"Geological features shape: {geo_features.shape}")

# ==== Scale tabular features ====
print("[📊] Scaling tabular features...")
scaler = StandardScaler()
tabular_scaled = scaler.fit_transform(tabular_data)
joblib.dump(scaler, "preprocessed_data/tabular_scaler.pkl")

# Create the folder if it doesn't exist
os.makedirs("processed_data", exist_ok=True)

# Save the processed features
np.save("processed_data/thermal_features.npy", thermal_features)
np.save("processed_data/geo_features.npy", geo_features)
np.save("processed_data/tabular_scaled.npy", tabular_scaled)

# ==== Fuse all features ====
print("[🔗] Fusing all features...")
fused_features = np.concatenate([thermal_features, geo_features, tabular_scaled], axis=1)
print(f"Final fused features shape: {fused_features.shape}")

# ==== Save fused features ====

np.save(OUTPUT_FEATURES_PATH, fused_features)
print(f"[✅] Fused features saved to: {OUTPUT_FEATURES_PATH}")
