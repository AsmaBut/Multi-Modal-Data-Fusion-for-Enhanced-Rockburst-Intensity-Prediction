

# Multi-Modal Data Fusion for Enhanced Rockburst Intensity Prediction

## Project Description

This repository contains the complete pipeline and resources for predicting rockburst intensity by fusing multi-modal geological data. The project integrates vibration signals, thermal imaging, and geological maps using advanced machine learning techniques for accurate rockburst classification.

The workflow includes data preprocessing, feature engineering, multi-modal fusion model training, and deployment of a web application for geological data analysis.

---

## Project Structure

```
Dataset/                         # Raw and source datasets
├── Geological Maps/             # Geological map files
├── Thermal Images/              # Thermal image files
├── Geological Maps.csv          # Geological maps data CSV
├── Static Mechanical tests.csv  # Mechanical tests data CSV
├── Vibration dataset.csv        # Vibration data CSV
└── synchronized_dataset.csv     # Combined dataset with labels

preprocessed_data/               # Preprocessed and scaled data
├── fused_features.npy           # Fused multi-modal features (NumPy)
├── geo_maps.npy                 # Geological map features (NumPy)
├── tabular_features.npy         # Tabular vibration features (NumPy)
├── tabular_scaler.pkl           # Scaler object for tabular data
└── thermal_images.npy           # Thermal image features (NumPy)

processed_data/                  # Additional processed feature files
├── geo_features.npy             # Processed geological features (NumPy)
├── tabular_scaled.npy           # Scaled tabular features (NumPy)
└── thermal_features.npy         # Processed thermal features (NumPy)

task2itsolera-app/               # Web application source code and configs
├── task2itsolera/               # Additional project scripts or data inside app folder
├── templates/                  # HTML templates for the Flask app
├── .gitignore                  # Git ignore rules
├── Dockerfile                  # Docker container build instructions
├── README.md                   # Project README file for the app
├── app.py                     # Main Flask application script
├── deploy.bat                 # Windows deployment script
├── deploy.sh                  # Linux/Mac deployment script
├── docker-compose.yml         # Docker Compose config
├── nginx.conf                 # Nginx reverse proxy config
├── requirements.txt           # Python dependencies list
└── test_app.py                # App test scripts

featureengineering.py          # Feature extraction and fusion pipeline
preprocess_data.py             # Raw data cleaning and preprocessing
sync_data.py                  # Data synchronization utilities
model.py                      # Multi-modal fusion model implementation
train.py                      # Model training script
utils.py                      # Helper functions
task2itsolera.ipynb            # Jupyter notebook for analysis and experiments
```

## Setup & Usage

### Prerequisites

* Python 3.8 or above
* pip package manager
* (Optional) Docker and Docker Compose for containerized deployment

### Install Dependencies

1. Clone the repository:

``bash
git clone https://github.com/AsmaBut/Multi-Modal-Data-Fusion-for-Enhanced-Rockburst-Intensity-Prediction.git
cd Multi-Modal-Data-Fusion-for-Enhanced-Rockburst-Intensity-Prediction
``

2. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

### Running the Model Training

To train the multi-modal fusion model on preprocessed data, run:

``bash
run task2itsolera.ipynb 
``

---

### Running the Flask Web Application

The Flask app is located in the `task2itsolera-app/` directory. Navigate to it and run:

```bash
cd task2itsolera-app
python app.py
```

The application will be accessible at [http://localhost:5000](http://localhost:5000).

---

### Using Docker (Optional)

To build and run the entire application stack with Docker:

```bash
docker-compose up --build
```

---

## Contributing

Feel free to fork the repository, make your changes, and submit pull requests. Please make sure to follow best practices and test your changes.

---

