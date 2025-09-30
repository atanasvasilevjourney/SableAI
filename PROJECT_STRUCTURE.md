# SableAI Project Structure

## 📁 **Complete Project Structure**

```
SableAI/
├── 📄 README.md                           # Main project documentation
├── 📄 LICENSE                             # MIT License
├── 📄 requirements.txt                    # Python dependencies
├── 📄 setup.py                           # Package setup configuration
├── 📄 install.py                         # Automated installation script
├── 📄 init_github.py                     # GitHub repository initialization
├── 📄 .gitignore                         # Git ignore patterns
├── 📄 PROJECT_STRUCTURE.md               # This file
├── 📄 CONTRIBUTING.md                     # Contributing guidelines
│
├── 🏗️ **Core Framework**
│   ├── domain_models.py                  # Domain models and value objects
│   ├── domain_services.py                # Domain services for business logic
│   ├── pinescript_translator.py          # Pine Script to Python translator
│   ├── multi_data_backtester.py          # Multi-data source backtesting
│   ├── tsa_enhanced_strategy.py          # TSA Enhanced Strategy implementation
│   ├── strategy_launcher.py              # Main launcher and orchestration
│   ├── results_analyzer.py               # Results analysis and visualization
│   └── test_system.py                    # System testing
│
├── 🔧 **Technical Analysis**
│   ├── technical_analysis_service.py     # BTA-Lib technical analysis service
│   ├── bta_integration.py                # BTA-Lib integration
│   └── bta_launcher.py                   # BTA-Lib command-line interface
│
├── 📊 **OpenBB Integration**
│   ├── openbb_integration.py             # OpenBB integration for enhanced data
│   ├── openbb_launcher.py                # Enhanced launcher with OpenBB
│   ├── openbb_example.py                 # OpenBB integration examples
│   └── OPENBB_SETUP.md                   # OpenBB integration setup guide
│
├── 🔄 **Cipher-BT Integration**
│   ├── cipher_integration.py             # Cipher-BT integration for concurrent sessions
│   ├── cipher_launcher.py                # Enhanced launcher with Cipher-BT
│   ├── cipher_example.py                 # Cipher-BT integration examples
│   └── CIPHER_SETUP.md                   # Cipher-BT integration setup guide
│
├── 🤖 **AI Integration**
│   ├── backtestsh_integration.py         # Backtest.sh AI integration
│   ├── backtestsh_launcher.py            # AI-powered strategy launcher
│   ├── backtestsh_example.py             # AI strategy generation examples
│   └── BACKTESTSH_SETUP.md               # Backtest.sh AI integration setup guide
│
├── 📚 **Documentation**
│   ├── SYSTEM_SUMMARY.md                 # Complete system summary
│   ├── BACKTESTSH_INTEGRATION_SUMMARY.md # Backtest.sh integration summary
│   └── example_usage.py                  # Comprehensive usage examples
│
├── 📁 **Generated Directories**
│   ├── data/                             # Market data storage
│   ├── results/                          # Backtest results
│   ├── strategies/                       # Generated strategies
│   ├── logs/                             # Application logs
│   ├── backtest_results/                 # Backtest output files
│   ├── strategy_results/                 # Strategy-specific results
│   └── generated_strategies/             # AI-generated strategies
│
└── 🔧 **GitHub Configuration**
    ├── .github/
    │   ├── workflows/
    │   │   ├── ci.yml                    # Continuous Integration
    │   │   └── release.yml               # Release automation
    │   └── ISSUE_TEMPLATE/
    │       ├── bug_report.md             # Bug report template
    │       └── feature_request.md        # Feature request template
    └── .env.example                      # Environment configuration template
```

## 🎯 **File Descriptions**

### **Core Framework Files**

| File | Purpose | Key Features |
|------|---------|--------------|
| `domain_models.py` | Core domain models and value objects | Strategy, Trade, Portfolio, Money, Price, Quantity |
| `domain_services.py` | Domain services for business logic | StrategyExecutionService, RiskManagementService |
| `pinescript_translator.py` | Pine Script to Python translator | Automated conversion, syntax mapping |
| `multi_data_backtester.py` | Multi-data source backtesting | 25+ data sources, parallel processing |
| `tsa_enhanced_strategy.py` | TSA Enhanced Strategy implementation | ATR, ADX, EMA, risk management |
| `strategy_launcher.py` | Main launcher and orchestration | CLI interface, comprehensive testing |
| `results_analyzer.py` | Results analysis and visualization | Performance metrics, reporting |
| `test_system.py` | System testing | Automated testing, validation |

### **Integration Files**

| Integration | Files | Purpose |
|-------------|-------|---------|
| **OpenBB** | `openbb_*.py`, `OPENBB_SETUP.md` | Professional financial data access |
| **Cipher-BT** | `cipher_*.py`, `CIPHER_SETUP.md` | Concurrent session management |
| **BTA-Lib** | `technical_analysis_service.py`, `bta_*.py` | Technical analysis with 100+ indicators |
| **AI** | `backtestsh_*.py`, `BACKTESTSH_SETUP.md` | AI-powered strategy generation |

### **Documentation Files**

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `SYSTEM_SUMMARY.md` | Complete system overview |
| `PROJECT_STRUCTURE.md` | This file - project structure guide |
| `CONTRIBUTING.md` | Contributing guidelines |
| `*.md` | Setup guides for each integration |

## 🚀 **Quick Start Commands**

### **Installation**
```bash
# Install the framework
python install.py

# Install with all integrations
pip install -e .[all]
```

### **Basic Usage**
```bash
# Run comprehensive backtest
python strategy_launcher.py --mode comprehensive

# Run OpenBB enhanced backtest
python openbb_launcher.py --mode comprehensive

# Run Cipher-BT concurrent sessions
python cipher_launcher.py --mode multi --symbols BTCUSDT ETHUSDT

# Run AI strategy generation
python backtestsh_launcher.py --mode generate --description "Your strategy here"

# Run BTA-Lib enhanced backtest
python bta_launcher.py --mode compare --symbol BTC-USD
```

### **Development**
```bash
# Run tests
python test_system.py

# Run examples
python example_usage.py

# Initialize GitHub repository
python init_github.py
```

## 🔧 **Configuration Files**

### **Environment Configuration**
```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys
```

### **GitHub Actions**
- **CI/CD Pipeline** - Automated testing across Python versions
- **Release Automation** - Automated PyPI publishing
- **Issue Templates** - Standardized bug reports and feature requests

## 📊 **Data Flow**

```
Pine Script → Translator → Python Strategy → Backtester → Results → Analyzer
     ↓              ↓           ↓            ↓          ↓         ↓
  TradingView    Domain      Strategy    Multi-Data  Metrics  Reports
   Community     Models      Execution    Sources    Analysis  Export
```

## 🎯 **Integration Architecture**

```
ScypherAI Core Framework
├── Domain-Driven Design (DDD)
│   ├── Domain Models (Strategy, Trade, Portfolio)
│   ├── Value Objects (Money, Price, Quantity)
│   └── Domain Services (Risk, Execution, Analysis)
├── OpenBB Integration (Professional Data)
├── Cipher-BT Integration (Concurrent Sessions)
├── BTA-Lib Integration (Technical Analysis)
└── AI Integration (Strategy Generation)
```

## 🚀 **Deployment Options**

### **Local Development**
```bash
python install.py
python example_usage.py
```

### **Production Deployment**
```bash
pip install scypherai
scypherai --mode comprehensive
```

### **Docker Deployment**
```dockerfile
FROM python:3.11
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "strategy_launcher.py", "--mode", "comprehensive"]
```

## 📈 **Performance Features**

- **Parallel Processing** - Multi-core backtesting
- **Memory Optimization** - Efficient data handling
- **Caching** - Strategy and data caching
- **Profiling** - Performance monitoring
- **Scalability** - Horizontal scaling support

## 🔒 **Security Features**

- **API Key Management** - Secure credential storage
- **Input Validation** - Data sanitization
- **Error Handling** - Graceful failure management
- **Audit Trails** - Domain events and logging
- **Risk Controls** - Position and exposure limits

This comprehensive structure provides a **professional-grade, enterprise-ready trading framework** that can handle everything from Pine Script translation to AI-powered strategy generation! 🚀
