# Database Seeding Guide

## 🎯 **Automatic Development Setup**

The application automatically seeds the database on startup. No manual intervention needed!

## 📁 **Data Format**

### CSV Format (`data/names.csv`)
```csv
source,name,gender,rank,count
Austria,Emma,f,1,1200
Austria,Liam,m,1,1300
Germany,Sofia,f,1,2000
```

**Required columns:**
- `source` - Country/region (e.g., "Austria", "Germany")
- `name` - The actual name (e.g., "Emma", "Liam")

**Optional columns:**
- `gender` - "m", "f", or empty
- `rank` - Integer ranking (can be empty)
- `count` - Number of occurrences (can be empty)

## 🚀 **Usage Methods**

### 1. **Automatic (Recommended for Development)**
Just start the application - data loads automatically:
```bash
docker-compose up -d
```

### 2. **Manual Script Execution**
```bash
# Load data (skips if already exists)
python init_db.py

# Force reload (clears and reloads all data)
python init_db.py --force
```

### 3. **Docker Container**
```bash
# Initialize data in running container
docker-compose exec backend python init_db.py

# Force reload
docker-compose exec backend python init_db.py --force
```

## 📊 **Data Sources Priority**

1. **CSV File**: `data/names.csv` (if exists)
2. **Fallback**: Hardcoded sample data (if no CSV)

## 🔄 **Development Workflow**

### Adding New Data:
1. Update `data/names.csv`
2. Restart containers: `docker-compose up --build -d`
3. Data automatically reloads on startup

### Force Refresh During Development:
```bash
docker-compose exec backend python init_db.py --force
```

## 🎛️ **Environment Variables**

Control behavior via environment variables:
```env
# In .env file
AUTO_SEED_DB=true          # Auto-seed on startup (default: true)
SEED_DATA_PATH=data/names.csv  # Path to CSV file
```

## 📝 **Sample Data Included**

The system includes sample data from:
- Austria (6 names)
- Germany (6 names) 
- Switzerland (6 names)
- France (6 names)
- Italy (6 names)

**Default users created:**
- Username: `admin`, Password: `admin123`
- Username: `testuser`, Password: `password123`

## 🏗️ **For Production/Kubernetes**

For production deployments:

### Option 1: Init Container
```yaml
initContainers:
- name: db-init
  image: your-backend-image
  command: ["python", "init_db.py", "--force"]
```

### Option 2: Job
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-seed
spec:
  template:
    spec:
      containers:
      - name: seeder
        image: your-backend-image
        command: ["python", "init_db.py"]
```

### Option 3: ConfigMap + Volume
Mount CSV data as ConfigMap and load from there.

## 🔍 **Troubleshooting**

**Data not loading?**
```bash
# Check if CSV exists
docker-compose exec backend ls -la data/

# Check logs
docker-compose logs backend

# Manual test
docker-compose exec backend python -c "from init_db import init_db; init_db(force_reload=True)"
```

**Need to reset everything?**
```bash
# Stop containers and remove volumes
docker-compose down -v

# Restart (fresh database)
docker-compose up -d
```
