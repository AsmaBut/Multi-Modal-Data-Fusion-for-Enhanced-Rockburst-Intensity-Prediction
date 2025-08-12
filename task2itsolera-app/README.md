# Geological Analysis Dashboard

A comprehensive web application for analyzing geological and geotechnical data, featuring advanced visualization, search capabilities, and data export functionality.

## 🏗️ Features

- **Interactive Dashboard**: Modern, responsive web interface with real-time data visualization
- **Geological Analysis**: Comprehensive analysis of rock composition, mechanical properties, and rockburst intensity
- **Advanced Search**: Filter data by geological composition, rockburst class, and other parameters
- **Data Visualization**: Interactive charts using Plotly for geological composition, rockburst distribution, and mechanical properties
- **Data Export**: Export filtered results to CSV format
- **API Endpoints**: RESTful API for data access and analysis
- **Containerized Deployment**: Docker-based deployment with Nginx reverse proxy

## 📊 Data Structure

The application processes the following geological data:

- **Geological Composition**: Sandstone, granite, and shale percentages
- **Fault Analysis**: Fault density and support coverage metrics
- **Mechanical Properties**: Compressive strength, tensile strength, and brittleness ratio
- **Rockburst Classification**: Intensity levels (I, II, III, IV)
- **Seismic Data**: Seismic and seismoacoustic parameters
- **Thermal Imaging**: Thermal image data for geological analysis

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose
- At least 4GB RAM available for Docker

### Deployment Options

#### Option 1: Automated Deployment (Recommended)

**Windows:**
```bash
deploy.bat
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

#### Option 2: Manual Docker Deployment

```bash
# Build and start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

#### Option 3: Local Development

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## 🌐 Access Points

After successful deployment, access the application at:

- **Main Dashboard**: http://localhost:5000
- **Through Nginx**: http://localhost:80
- **Health Check**: http://localhost:5000/health
- **API Base**: http://localhost:5000/api/

## 📁 Project Structure

```
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker container configuration
├── docker-compose.yml             # Multi-service orchestration
├── nginx.conf                     # Nginx reverse proxy configuration
├── deploy.sh                      # Linux/Mac deployment script
├── deploy.bat                     # Windows deployment script
├── README.md                      # This file
├── templates/
│   └── index.html                # Main dashboard template
└── task2itsolera/                # Data directory
    ├── synchronized_dataset.csv   # Main dataset
    ├── geo_maps.npy              # Geological maps data
    ├── tabular_features.npy      # Tabular features
    ├── tabular_scaler.pkl        # Data scaler
    └── thermal_images.npy        # Thermal imaging data
```

## 🔧 Configuration

### Environment Variables

The application supports the following environment variables:

- `FLASK_ENV`: Set to `production` for production deployment
- `PYTHONUNBUFFERED`: Set to `1` for better logging in containers

### Nginx Configuration

The Nginx configuration includes:

- Reverse proxy to Flask application
- Rate limiting for API endpoints
- Gzip compression
- Security headers
- Static file caching

## 📈 API Endpoints

### Data Endpoints

- `GET /api/data` - Get dataset overview and statistics
- `GET /api/analysis/{type}` - Get analysis data (composition, rockburst, mechanical)
- `GET /api/record/{id}` - Get specific record details
- `GET /api/search` - Search records with filters
- `GET /api/export` - Export filtered data to CSV

### Query Parameters for Search

- `min_sandstone`: Minimum sandstone percentage (0.0-1.0)
- `max_sandstone`: Maximum sandstone percentage (0.0-1.0)
- `rockburst_class`: Rockburst intensity class (I, II, III, IV)

## 🐳 Docker Commands

### Management Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Rebuild and restart
docker-compose up -d --build
```

### Container Management

```bash
# Access application container
docker exec -it geological-analysis-app bash

# Access nginx container
docker exec -it geological-nginx sh

# View container resources
docker stats
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   netstat -ano | findstr :5000  # Windows
   lsof -i :5000                 # Linux/Mac
   
   # Stop conflicting services or change ports in docker-compose.yml
   ```

2. **Container Build Failures**
   ```bash
   # Clean Docker cache
   docker system prune -a
   
   # Rebuild without cache
   docker-compose build --no-cache
   ```

3. **Data Loading Issues**
   - Ensure `task2itsolera` directory contains all required data files
   - Check file permissions and ownership
   - Verify data file integrity

4. **Memory Issues**
   - Increase Docker memory allocation in Docker Desktop settings
   - Reduce number of workers in Dockerfile (change `--workers 4` to `--workers 2`)

### Health Checks

```bash
# Check application health
curl http://localhost:5000/health

# Check nginx status
curl http://localhost:80/health

# Check container health
docker-compose ps
```

## 📊 Performance Optimization

### Production Recommendations

1. **Resource Allocation**
   - Allocate at least 4GB RAM to Docker
   - Use SSD storage for better I/O performance

2. **Scaling**
   - Increase worker processes in Dockerfile
   - Use multiple application instances behind load balancer

3. **Caching**
   - Enable Redis for session storage
   - Implement data caching for frequently accessed datasets

4. **Monitoring**
   - Use Docker monitoring tools
   - Implement application performance monitoring

## 🔒 Security Considerations

- **Rate Limiting**: API endpoints are rate-limited to prevent abuse
- **Security Headers**: Nginx adds security headers to all responses
- **Container Security**: Non-root user execution in containers
- **Input Validation**: All user inputs are validated and sanitized

## 📝 Development

### Adding New Features

1. **New API Endpoints**: Add routes in `app.py`
2. **Frontend Changes**: Modify `templates/index.html`
3. **Data Processing**: Extend analysis functions in `app.py`
4. **Styling**: Update CSS in the HTML template

### Testing

```bash
# Run basic tests
python -m pytest tests/

# Test API endpoints
curl http://localhost:5000/api/data
curl http://localhost:5000/api/analysis/composition
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the troubleshooting section above
2. Review container logs: `docker-compose logs`
3. Check application health: `curl http://localhost:5000/health`
4. Open an issue in the repository

## 🔄 Updates and Maintenance

### Regular Maintenance

- Monitor container health and logs
- Update dependencies regularly
- Backup data directory
- Monitor system resources

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and redeploy
./deploy.sh  # or deploy.bat on Windows
```

---

**Note**: This application is designed for geological and geotechnical data analysis. Ensure you have proper data validation and backup procedures in place before using in production environments.
