# Backtest.sh AI Integration Setup Guide

## 🎯 Overview

This guide explains how to integrate [Backtest.sh](https://github.com/nanvel/backtestsh) AI-powered strategy generation into your Pine Script to Python backtesting framework. Backtest.sh transforms plain text trading strategy descriptions into executable backtests using OpenAI's GPT-3.5-turbo model.

## 🚀 Features

- **AI-Powered Strategy Generation**: Transform plain text descriptions into executable Python strategies
- **OpenAI Integration**: Uses GPT-3.5-turbo for strategy generation
- **Multiple Strategy Types**: Support for momentum, mean reversion, trend following, breakout, and scalping strategies
- **Batch Processing**: Generate multiple strategies from descriptions file
- **Risk Management**: AI-generated strategies include stop loss, take profit, and position sizing
- **Technical Indicators**: Automatic inclusion of relevant technical indicators
- **Backtest Generation**: Complete backtesting implementation with performance metrics

## 📋 Prerequisites

### 1. OpenAI API Key
- Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Set the `OPENAI_API_KEY` environment variable

### 2. Python Dependencies
```bash
pip install openai pandas numpy yfinance matplotlib
```

## 🛠️ Installation

### Step 1: Install Dependencies
```bash
# Install OpenAI
pip install openai

# Install additional dependencies
pip install pandas numpy yfinance matplotlib talib
```

### Step 2: Set Environment Variables
```bash
# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Or create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### Step 3: Test Installation
```bash
python backtestsh_integration.py
```

## 🎯 Usage Examples

### 1. Basic Strategy Generation

```python
from backtestsh_integration import BacktestSHAILauncher

# Initialize AI launcher
launcher = BacktestSHAILauncher()

# Generate strategy from description
result = launcher.run_ai_strategy_generation(
    description="Buy when RSI is below 30 and price is above 20-day moving average, sell when RSI is above 70",
    symbol="BTC-USD",
    start_date="2020-01-01",
    end_date="2024-01-01",
    strategy_type="mean_reversion"
)

if result and "error" not in result:
    print("✅ Strategy generated successfully!")
else:
    print("❌ Strategy generation failed")
```

### 2. Command Line Usage

```bash
# Demo mode
python backtestsh_launcher.py --mode demo

# Generate single strategy
python backtestsh_launcher.py --mode generate \
    --description "Buy when RSI < 30, sell when RSI > 70" \
    --symbol BTC-USD

# Run AI backtest
python backtestsh_launcher.py --mode backtest \
    --description "Moving average crossover strategy" \
    --symbol AAPL

# Batch generation
python backtestsh_launcher.py --mode batch \
    --descriptions-file strategies.txt
```

### 3. Batch Strategy Generation

```python
# Create descriptions file
descriptions = [
    "Buy when RSI is below 30 and price is above 20-day moving average, sell when RSI is above 70",
    "Buy when 50-day moving average crosses above 200-day moving average, sell when it crosses below",
    "Buy when price breaks above upper Bollinger Band, sell when it breaks below lower band"
]

# Save to file
with open("strategies.txt", "w") as f:
    for desc in descriptions:
        f.write(desc + "\n")

# Run batch generation
result = launcher.run_batch_ai_generation(
    descriptions=descriptions,
    symbols=["BTC-USD", "AAPL", "ETH-USD"],
    start_date="2020-01-01",
    end_date="2024-01-01",
    strategy_types=["mean_reversion", "trend_following", "breakout"]
)
```

## 🔧 Configuration

### Strategy Types
- **momentum**: Momentum-based strategies
- **mean_reversion**: Mean reversion strategies
- **trend_following**: Trend following strategies
- **breakout**: Breakout strategies
- **scalping**: High-frequency scalping strategies

### Supported Symbols
- **Cryptocurrency**: BTC-USD, ETH-USD, BNB-USD, ADA-USD, SOL-USD
- **Stocks**: AAPL, MSFT, GOOGL, AMZN, TSLA, SPY, QQQ, IWM
- **Forex**: EURUSD=X, GBPUSD=X, USDJPY=X, AUDUSD=X, USDCAD=X

### Date Formats
- **Start/End Dates**: YYYY-MM-DD format
- **Default Range**: 2020-01-01 to 2024-01-01

## 📊 Generated Strategy Structure

The AI generates complete Python strategies with:

```python
class GeneratedStrategy:
    def __init__(self, data: pd.DataFrame, **params):
        self.data = data.copy()
        self.parameters = params
        self.results = {}
        self.trades = []
        
    def _calculate_indicators(self):
        # Calculate technical indicators
        pass
        
    def _check_entry_conditions(self, i: int) -> Tuple[bool, str]:
        # Check entry conditions
        pass
        
    def _check_exit_conditions(self, i: int) -> bool:
        # Check exit conditions
        pass
        
    def run_backtest(self) -> Dict:
        # Run the backtest
        pass
```

## 🎯 Advanced Features

### 1. Custom Strategy Descriptions
```python
# Multi-timeframe strategy
description = """
Create a multi-timeframe strategy that:
1. Uses 1-hour chart for entry signals
2. Uses 4-hour chart for trend confirmation
3. Buys when 1h RSI < 30 and 4h trend is bullish
4. Sells when 1h RSI > 70 or 4h trend turns bearish
5. Uses ATR for stop loss and take profit
6. Includes position sizing based on volatility
"""
```

### 2. Risk Management Strategies
```python
# Risk management strategy
description = """
Create a risk-managed strategy that:
1. Uses 2% risk per trade
2. Implements trailing stop loss
3. Uses position sizing based on account balance
4. Includes maximum drawdown protection
5. Uses correlation analysis to avoid overexposure
6. Implements portfolio heat management
"""
```

### 3. Technical Indicator Strategies
```python
# Technical indicator strategy
description = """
Create a strategy using multiple technical indicators:
1. RSI for overbought/oversold conditions
2. MACD for momentum signals
3. Bollinger Bands for volatility
4. Moving averages for trend direction
5. Volume analysis for confirmation
6. ATR for stop loss and take profit levels
"""
```

## 📁 File Structure

```
├── backtestsh_integration.py      # Core AI integration
├── backtestsh_launcher.py         # Command-line interface
├── backtestsh_example.py          # Usage examples
├── BACKTESTSH_SETUP.md            # This setup guide
├── sample_strategies.txt          # Sample strategy descriptions
└── generated_strategies/          # Generated strategy files
    ├── ai_generated_strategy_*.py
    └── ai_batch_results_*.json
```

## 🚀 Quick Start

### 1. Set up OpenAI API Key
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 2. Run Demo
```bash
python backtestsh_launcher.py --mode demo
```

### 3. Generate Custom Strategy
```bash
python backtestsh_launcher.py --mode generate \
    --description "Your strategy description here" \
    --symbol BTC-USD
```

### 4. Run Examples
```bash
python backtestsh_example.py
```

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key Not Found**
   ```bash
   # Set environment variable
   export OPENAI_API_KEY="your-api-key-here"
   
   # Or use --api-key parameter
   python backtestsh_launcher.py --api-key "your-api-key-here" --mode demo
   ```

2. **OpenAI Not Available**
   ```bash
   # Install OpenAI
   pip install openai
   ```

3. **Rate Limiting**
   - OpenAI has rate limits
   - Use batch mode for multiple strategies
   - Add delays between requests if needed

4. **API Errors**
   - Check your API key is valid
   - Ensure you have sufficient credits
   - Check OpenAI service status

### Debug Mode
```bash
# Enable debug output
python backtestsh_launcher.py --mode demo --debug
```

## 📈 Performance Tips

1. **Batch Processing**: Use batch mode for multiple strategies
2. **API Optimization**: Cache results to avoid repeated API calls
3. **Error Handling**: Implement retry logic for API failures
4. **Cost Management**: Monitor OpenAI API usage and costs

## 🎯 Integration with Existing Framework

The Backtest.sh AI integration works seamlessly with:

- **Pine Script Translator**: Convert Pine Script to Python, then enhance with AI
- **Multi-Data Backtester**: Test AI-generated strategies across multiple data sources
- **OpenBB Integration**: Use professional-grade data for AI strategies
- **Cipher-BT Integration**: Run AI strategies with concurrent sessions

### Example Integration
```python
# 1. Translate Pine Script to Python
from pinescript_translator import PineScriptTranslator
translator = PineScriptTranslator()
python_code = translator.translate_to_python(pinescript_code)

# 2. Enhance with AI
from backtestsh_integration import BacktestSHAILauncher
ai_launcher = BacktestSHAILauncher()
enhanced_strategy = ai_launcher.run_ai_strategy_generation(
    description="Enhance the translated strategy with risk management",
    symbol="BTC-USD"
)

# 3. Run comprehensive backtest
from strategy_launcher import StrategyLauncher
launcher = StrategyLauncher()
results = launcher.run_comprehensive_backtest()
```

## 🎉 Benefits

1. **Rapid Prototyping**: Generate strategies from plain text descriptions
2. **AI Enhancement**: Improve existing strategies with AI suggestions
3. **Risk Management**: Automatic inclusion of risk management features
4. **Technical Indicators**: Smart selection of relevant indicators
5. **Backtest Generation**: Complete backtesting implementation
6. **Batch Processing**: Generate multiple strategies efficiently

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Backtest.sh GitHub Repository](https://github.com/nanvel/backtestsh)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [OpenAI Pricing](https://openai.com/pricing)

## 🎯 Next Steps

1. **Set up OpenAI API key**
2. **Run the demo mode**
3. **Generate your first AI strategy**
4. **Integrate with existing framework**
5. **Create custom strategy descriptions**
6. **Run batch generation**
7. **Analyze and optimize results**

This AI integration transforms your Pine Script to Python backtesting framework into a powerful AI-driven strategy development platform! 🚀
