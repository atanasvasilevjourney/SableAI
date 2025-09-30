# SableAI - Pine Script to Python Backtesting Framework

## 🎯 **Overview**

 SableAI is a comprehensive Domain-Driven Design (DDD) framework for translating TradingView Pine Script strategies into Python code and running professional-grade backtests across multiple data sources. This framework implements the **RBI method** (Research, Backtest, Implement) with enterprise-grade architecture.

## 🚀 **Key Features**

- **Pine Script Translation** - Convert TradingView Pine Script to Python
- **Multi-Data Source Testing** - Test across 25+ data sources and timeframes
- **AI-Powered Strategy Generation** - Natural language to code conversion
- **Professional Data Access** - OpenBB integration for enhanced financial data
- **Concurrent Session Management** - Cipher-BT integration for advanced trading
- **Technical Analysis** - BTA-Lib integration with 100+ indicators
- **Domain-Driven Design** - Clean, maintainable, enterprise-grade architecture
- **Risk Management** - Advanced risk controls and position sizing
- **Performance Analysis** - Comprehensive metrics and reporting

## 📁 **Project Structure**

```
 SableAI/
├── domain_models.py              # Core domain models and value objects
├── domain_services.py            # Domain services for business logic
├── technical_analysis_service.py # BTA-Lib technical analysis service
├── bta_integration.py            # BTA-Lib integration
├── bta_launcher.py              # BTA-Lib command-line interface
├── pinescript_translator.py      # Pine Script to Python translator
├── multi_data_backtester.py     # Multi-data source backtesting framework
├── tsa_enhanced_strategy.py     # TSA Enhanced Strategy implementation
├── strategy_launcher.py         # Main launcher and orchestration
├── results_analyzer.py          # Results analysis and visualization
├── openbb_integration.py        # OpenBB integration for enhanced data
├── openbb_launcher.py           # Enhanced launcher with OpenBB
├── openbb_example.py            # OpenBB integration examples
├── cipher_integration.py        # Cipher-BT integration for concurrent sessions
├── cipher_launcher.py           # Enhanced launcher with Cipher-BT
├── cipher_example.py            # Cipher-BT integration examples
├── backtestsh_integration.py    # Backtest.sh AI integration
├── backtestsh_launcher.py       # AI-powered strategy launcher
├── backtestsh_example.py        # AI strategy generation examples
├── example_usage.py             # Comprehensive usage examples
├── test_system.py               # System testing
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore file
├── LICENSE                      # MIT License
├── OPENBB_SETUP.md              # OpenBB integration setup guide
├── CIPHER_SETUP.md              # Cipher-BT integration setup guide
├── BACKTESTSH_SETUP.md          # Backtest.sh AI integration setup guide
├── SYSTEM_SUMMARY.md            # Complete system summary
└── README.md                    # This file
```

## 🛠️ **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/ScypherAI.git
cd  SableAI
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Install TA-Lib (if needed)**
```bash
# On Windows
pip install TA-Lib

# On macOS
brew install ta-lib
pip install TA-Lib

# On Linux
sudo apt-get install libta-lib-dev
pip install TA-Lib
```

### **4. Install Optional Integrations**

#### **OpenBB for Enhanced Data Access**
```bash
pip install openbb
# Or with all extensions
pip install "openbb[all]"
```

#### **Cipher-BT for Concurrent Sessions**
```bash
pip install cipher-bt
# Or with all extensions
pip install "cipher-bt[finplot,talib]"
```

#### **Backtest.sh AI for Strategy Generation**
```bash
pip install openai
# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

## 🚀 **Quick Start**

### **1. Basic Pine Script Translation**
```python
from pinescript_translator import PineScriptTranslator

translator = PineScriptTranslator()
python_code = translator.translate_to_python(pinescript_code)
```

### **2. Single Strategy Backtest**
```python
from strategy_launcher import StrategyLauncher

launcher = StrategyLauncher()
results = launcher.run_tsa_enhanced_backtest(
    symbol="BTC-USD",
    timeframe="1d",
    start_date="2020-01-01",
    end_date="2024-01-01"
)
```

### **3. Comprehensive Multi-Data Source Testing**
```python
results = launcher.run_comprehensive_backtest(
    strategy_params={'atr_length': 14, 'atr_multiplier': 3.0},
    max_workers=4
)
```

### **4. AI-Powered Strategy Generation**
```python
from backtestsh_launcher import BacktestSHAILauncher

ai_launcher = BacktestSHAILauncher()
result = ai_launcher.run_ai_strategy_generation(
    description="Buy when RSI < 30, sell when RSI > 70",
    symbol="BTC-USD",
    strategy_type="mean_reversion"
)
```

### **5. Enhanced Technical Analysis**
```python
from bta_launcher import BTALauncher

bta_launcher = BTALauncher()
results = bta_launcher.run_enhanced_backtest(
    strategy, market_data, Money(Decimal('10000'), "USD")
)
```

## 📊 **Command Line Interface**

### **Core Framework**
```bash
# Run comprehensive backtest
python strategy_launcher.py --mode comprehensive --workers 4

# Run single backtest
python strategy_launcher.py --mode single --symbol BTC-USD --timeframe 1d

# Translate Pine Script
python strategy_launcher.py --mode translate --pinescript-file strategy.pine
```

### **OpenBB Enhanced**
```bash
# Run OpenBB demo
python openbb_launcher.py --mode demo

# Single enhanced backtest
python openbb_launcher.py --mode single --symbol AAPL --market-type equity

# Comprehensive enhanced backtest
python openbb_launcher.py --mode comprehensive
```

### **Cipher-BT Enhanced**
```bash
# Run Cipher-BT demo
python cipher_launcher.py --mode demo

# Single backtest with concurrent sessions
python cipher_launcher.py --mode single --symbol BTCUSDT --interval 1h

# Multi-symbol backtest
python cipher_launcher.py --mode multi --symbols BTCUSDT ETHUSDT ADAUSDT
```

### **AI-Powered Strategy Generation**
```bash
# Run AI demo
python backtestsh_launcher.py --mode demo

# Generate strategy from description
python backtestsh_launcher.py --mode generate --description "Your strategy here" --symbol BTC-USD

# Run AI backtest
python backtestsh_launcher.py --mode backtest --description "Moving average crossover" --symbol AAPL
```

### **BTA-Lib Enhanced**
```bash
# Run BTA-Lib demo
python bta_launcher.py --mode demo

# Enhanced backtest with technical analysis
python bta_launcher.py --mode backtest --strategy tsa_enhanced --symbol BTC-USD

# Compare strategies
python bta_launcher.py --mode compare --symbol BTC-USD
```

## 🎯 **Domain-Driven Design Architecture**

### **Core Domain Models**
- **Strategy** - Trading strategy entities
- **Trade** - Individual trade execution
- **Portfolio** - Portfolio management
- **MarketData** - Market data entities
- **BacktestResults** - Backtest results

### **Value Objects**
- **Money** - Monetary amounts with currency
- **Price** - Price with currency validation
- **Quantity** - Trade quantities
- **Percentage** - Percentage calculations
- **Timeframe** - Time frame validation

### **Domain Services**
- **RiskManager** - Risk management logic
- **StrategyAnalyzer** - Strategy analysis
- **BacktestExecutor** - Backtest execution
- **TechnicalIndicatorService** - Technical analysis

## 🔧 **Integrations**

### **1. OpenBB Integration**
- Professional-grade financial data
- Technical indicators (RSI, MACD, Bollinger Bands, ATR, ADX)
- Market sentiment analysis
- Fundamental data access
- Real-time data integration

### **2. Cipher-BT Integration**
- Multiple concurrent trading sessions
- Sophisticated exit strategies
- Multi-exchange data sources
- Built-in visualization
- Advanced session management

### **3. Backtest.sh AI Integration**
- AI-powered strategy generation
- Natural language to code conversion
- OpenAI GPT-3.5-turbo integration
- Batch strategy generation
- Strategy enhancement

### **4. BTA-Lib Integration**
- Comprehensive technical analysis
- 100+ technical indicators
- Pandas-based calculations
- Performance optimized
- Backtrader ecosystem integration

## 📈 **Performance Features**

### **Multi-Data Source Testing**
- **25+ Data Sources** across multiple timeframes
- **Parallel Processing** for fast execution
- **Comprehensive Results** collection
- **Statistical Analysis** across markets

### **Risk Management**
- **Position Sizing** based on risk parameters
- **Stop Loss** and **Take Profit** mechanisms
- **Portfolio Risk** analysis
- **Correlation Analysis** between positions
- **Drawdown Protection**

### **Performance Metrics**
- **Net Profit** and **Total Return**
- **Win Rate** and **Profit Factor**
- **Sharpe Ratio** and **Sortino Ratio**
- **Maximum Drawdown** analysis
- **Expectancy** calculations
- **Trade Analysis** and statistics

## 🎯 **Use Cases**

### **1. Strategy Research**
- Convert Pine Script strategies to Python
- Test across multiple data sources
- Analyze performance metrics
- Compare strategy variations

### **2. AI-Powered Development**
- Generate strategies from natural language
- Enhance existing strategies with AI
- Batch process multiple strategies
- Automated strategy optimization

### **3. Professional Trading**
- Enterprise-grade backtesting
- Risk management systems
- Portfolio optimization
- Performance monitoring

### **4. Educational**
- Learn algorithmic trading
- Understand strategy development
- Study market behavior
- Practice risk management

## 📚 **Documentation**

- **README.md** - This file
- **OPENBB_SETUP.md** - OpenBB integration setup
- **CIPHER_SETUP.md** - Cipher-BT integration setup
- **BACKTESTSH_SETUP.md** - Backtest.sh AI setup
- **SYSTEM_SUMMARY.md** - Complete system overview

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 **Acknowledgments**

- **TradingView** for Pine Script platform
- **OpenBB** for professional financial data
- **Cipher-BT** for concurrent session management
- **BTA-Lib** for technical analysis
- **Backtest.sh** for AI-powered strategy generation

## 🚀 **Getting Started**

1. **Install the framework** - Follow the installation guide
2. **Run tests** - `python test_system.py`
3. **Try examples** - `python example_usage.py`
4. **Translate your Pine Script** - Use the translator
5. **Run comprehensive backtests** - Test across multiple data sources
6. **Analyze results** - Use the analysis tools
7. **Deploy professionally** - Use OpenBB and Cipher-BT for production

This framework transforms your Pine Script strategies into a **professional-grade Python backtesting system** with access to the best financial data and analysis tools available! 🚀
