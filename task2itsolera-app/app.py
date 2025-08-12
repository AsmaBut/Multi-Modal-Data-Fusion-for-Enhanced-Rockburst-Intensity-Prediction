from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import pandas as pd
import pickle
import os
import json
from datetime import datetime
import plotly.graph_objs as go
import plotly.utils
import base64
import io
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# Load the data
def load_data():
    """Load all the data files"""
    try:
        # Load CSV data
        df = pd.read_csv('task2itsolera/synchronized_dataset.csv')
        print(f"✅ CSV data loaded successfully: {len(df)} records")
        
        # Load NumPy arrays with error handling
        geo_maps = None
        tabular_features = None
        thermal_images = None
        scaler = None
        
        try:
            geo_maps = np.load('task2itsolera/geo_maps.npy', allow_pickle=True)
            print(f"✅ Geo maps loaded: {geo_maps.shape if hasattr(geo_maps, 'shape') else 'N/A'}")
        except Exception as e:
            print(f"⚠️  Warning: Could not load geo_maps.npy: {e}")
            
        try:
            tabular_features = np.load('task2itsolera/tabular_features.npy', allow_pickle=True)
            print(f"✅ Tabular features loaded: {tabular_features.shape if hasattr(tabular_features, 'shape') else 'N/A'}")
        except Exception as e:
            print(f"⚠️  Warning: Could not load tabular_features.npy: {e}")
            
        try:
            thermal_images = np.load('task2itsolera/thermal_images.npy', allow_pickle=True)
            print(f"✅ Thermal images loaded: {thermal_images.shape if hasattr(thermal_images, 'shape') else 'N/A'}")
        except Exception as e:
            print(f"⚠️  Warning: Could not load thermal_images.npy: {e}")
            
        try:
            with open('task2itsolera/tabular_scaler.pkl', 'rb') as f:
                scaler = pickle.load(f)
            print("✅ Scaler loaded successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not load tabular_scaler.pkl: {e}")
            
        return df, geo_maps, tabular_features, thermal_images, scaler
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None, None, None, None, None

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API endpoint to get dataset information"""
    try:
        df, _, _, _, _ = load_data()
        if df is not None:
            return jsonify({
                'total_records': len(df),
                'columns': df.columns.tolist(),
                'sample_data': df.head(5).to_dict('records'),
                'statistics': {
                    'rockburst_intensity_counts': df['rockburst_intensity'].value_counts().to_dict(),
                    'avg_sandstone': float(df['sandstone_%'].mean()),
                    'avg_granite': float(df['granite_%'].mean()),
                    'avg_shale': float(df['shale_%'].mean()),
                    'avg_fault_density': float(df['fault_density'].mean())
                }
            })
        else:
            return jsonify({'error': 'Failed to load data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/<analysis_type>')
def get_analysis(analysis_type):
    """API endpoint for different types of analysis"""
    try:
        df, _, _, _, _ = load_data()
        if df is None:
            return jsonify({'error': 'Failed to load data'}), 500
            
        if analysis_type == 'composition':
            # Geological composition analysis
            composition_data = {
                'sandstone': df['sandstone_%'].tolist(),
                'granite': df['granite_%'].tolist(),
                'shale': df['shale_%'].tolist()
            }
            return jsonify(composition_data)
            
        elif analysis_type == 'rockburst':
            # Rockburst intensity analysis
            rockburst_data = df['rockburst_intensity'].value_counts().to_dict()
            return jsonify(rockburst_data)
            
        elif analysis_type == 'mechanical':
            # Mechanical properties analysis
            mechanical_data = {
                'compressive_strength': df['compressive_strength_MPa'].tolist(),
                'tensile_strength': df['tensile_strength_MPa'].tolist(),
                'brittleness_ratio': df['brittleness_ratio'].tolist()
            }
            return jsonify(mechanical_data)
            
        else:
            return jsonify({'error': 'Invalid analysis type'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/record/<int:record_id>')
def get_record(record_id):
    """Get specific record details"""
    try:
        df, geo_maps, tabular_features, thermal_images, scaler = load_data()
        if df is None:
            return jsonify({'error': 'Failed to load data'}), 500
            
        if record_id >= len(df):
            return jsonify({'error': 'Record ID out of range'}), 400
            
        record = df.iloc[record_id].to_dict()
        
        # Get corresponding arrays if available
        if geo_maps is not None and record_id < len(geo_maps):
            record['geo_map_shape'] = geo_maps[record_id].shape if hasattr(geo_maps[record_id], 'shape') else 'N/A'
            
        if thermal_images is not None and record_id < len(thermal_images):
            record['thermal_image_shape'] = thermal_images[record_id].shape if hasattr(thermal_images[record_id], 'shape') else 'N/A'
            
        return jsonify(record)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search')
def search_records():
    """Search records based on criteria"""
    try:
        df, _, _, _, _ = load_data()
        if df is None:
            return jsonify({'error': 'Failed to load data'}), 500
            
        # Get search parameters
        min_sandstone = request.args.get('min_sandstone', type=float)
        max_sandstone = request.args.get('max_sandstone', type=float)
        rockburst_class = request.args.get('rockburst_class', type=str)
        
        # Apply filters
        filtered_df = df.copy()
        
        if min_sandstone is not None:
            filtered_df = filtered_df[filtered_df['sandstone_%'] >= min_sandstone]
        if max_sandstone is not None:
            filtered_df = filtered_df[filtered_df['sandstone_%'] <= max_sandstone]
        if rockburst_class:
            filtered_df = filtered_df[filtered_df['rockburst_intensity'] == rockburst_class]
            
        return jsonify({
            'total_matches': len(filtered_df),
            'results': filtered_df.head(20).to_dict('records')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export')
def export_data():
    """Export filtered data to CSV"""
    try:
        df, _, _, _, _ = load_data()
        if df is None:
            return jsonify({'error': 'Failed to load data'}), 500
            
        # Get filter parameters
        min_sandstone = request.args.get('min_sandstone', type=float)
        max_sandstone = request.args.get('max_sandstone', type=float)
        rockburst_class = request.args.get('rockburst_class', type=str)
        
        # Apply filters
        filtered_df = df.copy()
        
        if min_sandstone is not None:
            filtered_df = filtered_df[filtered_df['sandstone_%'] >= min_sandstone]
        if max_sandstone is not None:
            filtered_df = filtered_df[filtered_df['sandstone_%'] <= max_sandstone]
        if rockburst_class:
            filtered_df = filtered_df[filtered_df['rockburst_intensity'] == rockburst_class]
            
        # Create CSV in memory
        output = io.StringIO()
        filtered_df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'geological_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
