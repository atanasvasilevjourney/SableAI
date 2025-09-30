# SableAI Deployment Guide

## 🚀 **Complete Deployment Instructions**

This guide provides step-by-step instructions for deploying SableAI in various environments.

## 📋 **Prerequisites**

### **System Requirements**
- **Python 3.8+** (recommended: Python 3.11)
- **Git** for version control
- **8GB+ RAM** for comprehensive backtesting
- **10GB+ disk space** for data and results

### **Optional Dependencies**
- **GitHub CLI** for automated repository setup
- **Docker** for containerized deployment
- **Redis** for caching (production)
- **PostgreSQL** for data persistence (production)

## 🛠️ **Installation Methods**

### **Method 1: Automated Installation (Recommended)**

```bash
# Clone the repository
git clone https://github.com/yourusername/ScypherAI.git
cd ScypherAI

# Run automated installation
python install.py
```

### **Method 2: Manual Installation**

```bash
# Clone the repository
git clone https://github.com/yourusername/ScypherAI.git
cd ScypherAI

# Install dependencies
pip install -r requirements.txt

# Install optional integrations
pip install openbb cipher-bt bta-lib openai

# Create directories
mkdir -p data results strategies logs backtest_results strategy_results generated_strategies

# Copy environment file
cp .env.example .env
# Edit .env with your API keys
```

### **Method 3: Development Installation**

```bash
# Clone the repository
git clone https://github.com/yourusername/ScypherAI.git
cd ScypherAI

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e .[all]

# Run tests
python test_system.py
```

## 🔧 **Configuration**

### **Environment Variables**

Create a `.env` file with the following configuration:

```bash
# OpenAI API Key (for AI strategy generation)
OPENAI_API_KEY=your-openai-api-key-here

# OpenBB API Key (optional)
OPENBB_API_KEY=your-openbb-api-key-here

# Trading API Keys (optional)
BINANCE_API_KEY=your-binance-api-key-here
BINANCE_SECRET_KEY=your-binance-secret-key-here

# Database Configuration (optional)
DATABASE_URL=sqlite:///scypherai.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/scypherai.log

# Backtesting Configuration
DEFAULT_INITIAL_CAPITAL=10000
DEFAULT_COMMISSION=0.001
DEFAULT_SLIPPAGE=0.0005

# Risk Management
MAX_POSITION_SIZE=0.1
MAX_DAILY_LOSS=0.05
MAX_DRAWDOWN=0.2
```

### **API Keys Setup**

#### **OpenAI API Key**
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and get your API key
3. Add to `.env` file: `OPENAI_API_KEY=sk-...`

#### **OpenBB API Key**
1. Visit [OpenBB Platform](https://openbb.co/)
2. Sign up for an account
3. Get your API key from the dashboard
4. Add to `.env` file: `OPENBB_API_KEY=your-key-here`

#### **Trading API Keys**
1. **Binance**: Get API key from [Binance](https://www.binance.com/)
2. **Other exchanges**: Follow their respective API documentation

## 🚀 **Deployment Options**

### **Option 1: Local Development**

```bash
# Basic setup
python install.py

# Run examples
python example_usage.py

# Run comprehensive backtest
python strategy_launcher.py --mode comprehensive
```

### **Option 2: Production Server**

```bash
# Install with all integrations
pip install -e .[all]

# Configure environment
cp .env.example .env
# Edit .env with production values

# Run as service
python strategy_launcher.py --mode comprehensive --daemon
```

### **Option 3: Docker Deployment**

#### **Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libta-lib-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data results strategies logs backtest_results strategy_results generated_strategies

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port (if needed)
EXPOSE 8000

# Run the application
CMD ["python", "strategy_launcher.py", "--mode", "comprehensive"]
```

#### **Create docker-compose.yml**
```yaml
version: '3.8'

services:
  scypherai:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENBB_API_KEY=${OPENBB_API_KEY}
    volumes:
      - ./data:/app/data
      - ./results:/app/results
      - ./logs:/app/logs
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=scypherai
      - POSTGRES_USER=scypherai
      - POSTGRES_PASSWORD=your-password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

#### **Deploy with Docker**
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f scypherai

# Stop services
docker-compose down
```

### **Option 4: Cloud Deployment**

#### **AWS Deployment**
```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Deploy to EC2
# 1. Launch EC2 instance
# 2. Install Docker
# 3. Clone repository
# 4. Run docker-compose up -d
```

#### **Google Cloud Deployment**
```bash
# Install Google Cloud SDK
# Configure gcloud
gcloud auth login

# Deploy to Cloud Run
gcloud run deploy scypherai --source .
```

#### **Azure Deployment**
```bash
# Install Azure CLI
pip install azure-cli

# Login to Azure
az login

# Deploy to Container Instances
az container create --resource-group myResourceGroup --name scypherai --image scypherai:latest
```

## 🔧 **GitHub Repository Setup**

### **Automated Setup**
```bash
# Run GitHub initialization script
python init_github.py
```

### **Manual Setup**
```bash
# Create repository on GitHub
# Add remote origin
git remote add origin https://github.com/yourusername/ScypherAI.git

# Push to GitHub
git push -u origin main
```

### **GitHub Actions Setup**
1. Go to repository settings
2. Navigate to "Secrets and variables" → "Actions"
3. Add the following secrets:
   - `PYPI_API_TOKEN` (for PyPI publishing)
   - `OPENAI_API_KEY` (for AI features)
   - `OPENBB_API_KEY` (for enhanced data)

## 📊 **Monitoring and Logging**

### **Logging Configuration**
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scypherai.log'),
        logging.StreamHandler()
    ]
)
```

### **Performance Monitoring**
```bash
# Monitor system resources
htop

# Monitor Python processes
ps aux | grep python

# Monitor disk usage
df -h

# Monitor memory usage
free -h
```

## 🔒 **Security Considerations**

### **API Key Security**
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Use least-privilege access

### **Network Security**
- Use HTTPS for all external communications
- Implement rate limiting for API calls
- Use VPN for sensitive operations
- Monitor for suspicious activity

### **Data Security**
- Encrypt sensitive data at rest
- Use secure connections for data transmission
- Implement access controls
- Regular security audits

## 🚀 **Production Checklist**

### **Pre-Deployment**
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] API keys secured
- [ ] Database configured
- [ ] Monitoring setup
- [ ] Backup strategy implemented

### **Post-Deployment**
- [ ] Health checks passing
- [ ] Logs being generated
- [ ] Performance metrics collected
- [ ] Alerts configured
- [ ] Documentation updated

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
# Check Python path
echo $PYTHONPATH

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### **API Key Issues**
```bash
# Check environment variables
env | grep API

# Test API connectivity
python -c "import openai; print('OpenAI connected')"
```

#### **Memory Issues**
```bash
# Monitor memory usage
free -h

# Increase swap space
sudo swapon --show
```

#### **Performance Issues**
```bash
# Profile Python code
python -m cProfile strategy_launcher.py

# Monitor system resources
htop
```

### **Debug Mode**
```bash
# Run with debug logging
LOG_LEVEL=DEBUG python strategy_launcher.py --mode comprehensive

# Run with verbose output
python strategy_launcher.py --mode comprehensive --verbose
```

## 📚 **Additional Resources**

- **Documentation**: [README.md](README.md)
- **Project Structure**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **OpenBB Setup**: [OPENBB_SETUP.md](OPENBB_SETUP.md)
- **Cipher-BT Setup**: [CIPHER_SETUP.md](CIPHER_SETUP.md)
- **AI Setup**: [BACKTESTSH_SETUP.md](BACKTESTSH_SETUP.md)

## 🎉 **Success Indicators**

After successful deployment, you should be able to:

1. **Run comprehensive backtests** across multiple data sources
2. **Generate AI-powered strategies** from natural language
3. **Access professional financial data** through OpenBB
4. **Manage concurrent trading sessions** with Cipher-BT
5. **Perform advanced technical analysis** with BTA-Lib
6. **Monitor performance** through comprehensive logging
7. **Scale horizontally** for production workloads

## 🚀 **Next Steps**

1. **Test the installation** with `python test_system.py`
2. **Run examples** with `python example_usage.py`
3. **Configure your API keys** in `.env`
4. **Start with simple backtests** and gradually increase complexity
5. **Monitor performance** and optimize as needed
6. **Contribute to the project** by submitting pull requests

This deployment guide ensures you can successfully deploy ScypherAI in any environment! 🚀
