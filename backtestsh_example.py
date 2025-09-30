"""
Backtest.sh AI Integration Examples
Demonstrates AI-powered strategy generation and backtesting
"""

import os
import sys
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backtestsh_integration import BacktestSHAILauncher

def example_1_simple_strategy_generation():
    """Example 1: Simple strategy generation from description"""
    print("🎯 Example 1: Simple Strategy Generation")
    print("="*60)
    
    # Initialize AI launcher
    launcher = BacktestSHAILauncher()
    
    if not launcher.check_availability():
        print("❌ AI integration not available. Please check your OpenAI API key.")
        return
    
    # Strategy description
    description = "Buy when RSI is below 30 and price is above 20-day moving average, sell when RSI is above 70"
    
    print(f"📝 Strategy Description: {description}")
    print(f"🎯 Symbol: BTC-USD")
    print(f"📅 Date Range: 2020-01-01 to 2024-01-01")
    print(f"🔧 Strategy Type: Mean Reversion")
    
    # Generate strategy
    result = launcher.run_ai_strategy_generation(
        description=description,
        symbol="BTC-USD",
        start_date="2020-01-01",
        end_date="2024-01-01",
        strategy_type="mean_reversion"
    )
    
    if result and "error" not in result:
        print("✅ Strategy generated successfully!")
        print(f"📁 Generated strategy saved to file")
    else:
        print("❌ Strategy generation failed")
        if result and "error" in result:
            print(f"   Error: {result['error']}")

def example_2_trend_following_strategy():
    """Example 2: Trend following strategy generation"""
    print("\n🎯 Example 2: Trend Following Strategy")
    print("="*60)
    
    launcher = BacktestSHAILauncher()
    
    if not launcher.check_availability():
        print("❌ AI integration not available. Please check your OpenAI API key.")
        return
    
    # Trend following strategy
    description = "Buy when 50-day moving average crosses above 200-day moving average, sell when it crosses below"
    
    print(f"📝 Strategy Description: {description}")
    print(f"🎯 Symbol: AAPL")
    print(f"📅 Date Range: 2020-01-01 to 2024-01-01")
    print(f"🔧 Strategy Type: Trend Following")
    
    result = launcher.run_ai_strategy_generation(
        description=description,
        symbol="AAPL",
        start_date="2020-01-01",
        end_date="2024-01-01",
        strategy_type="trend_following"
    )
    
    if result and "error" not in result:
        print("✅ Trend following strategy generated successfully!")
    else:
        print("❌ Strategy generation failed")
        if result and "error" in result:
            print(f"   Error: {result['error']}")

def example_3_breakout_strategy():
    """Example 3: Breakout strategy generation"""
    print("\n🎯 Example 3: Breakout Strategy")
    print("="*60)
    
    launcher = BacktestSHAILauncher()
    
    if not launcher.check_availability():
        print("❌ AI integration not available. Please check your OpenAI API key.")
        return
    
    # Breakout strategy
    description = "Buy when price breaks above upper Bollinger Band, sell when it breaks below lower band"
    
    print(f"📝 Strategy Description: {description}")
    print(f"🎯 Symbol: ETH-USD")
    print(f"📅 Date Range: 2020-01-01 to 2024-01-01")
    print(f"🔧 Strategy Type: Breakout")
    
    result = launcher.run_ai_strategy_generation(
        description=description,
        symbol="ETH-USD",
        start_date="2020-01-01",
        end_date="2024-01-01",
        strategy_type="breakout"
    )
    
    if result and "error" not in result:
        print("✅ Breakout strategy generated successfully!")
    else:
        print("❌ Strategy generation failed")
        if result and "error" in result:
            print(f"   Error: {result['error']}")

def example_4_momentum_strategy():
    """Example 4: Momentum strategy generation"""
    print("\n🎯 Example 4: Momentum Strategy")
    print("="*60)
    
    launcher = BacktestSHAILauncher()
    
    if not launcher.check_availability():
        print("❌ AI integration not available. Please check your OpenAI API key.")
        return
    
    # Momentum strategy
    description = "Buy when MACD line crosses above signal line, sell when it crosses below"
    
    print(f"📝 Strategy Description: {description}")
    print(f"🎯 Symbol: SPY")
    print(f"📅 Date Range: 2020-01-01 to 2024-01-01")
    print(f"🔧 Strategy Type: Momentum")
    
    result = launcher.run_ai_strategy_generation(
        description=description,
        symbol="SPY",
        start_date="2020-01-01",
        end_date="2024-01-01",
        strategy_type="momentum"
    )
    
    if result and "error" not in result:
        print("✅ Momentum strategy generated successfully!")
    else:
        print("❌ Strategy generation failed")
        if result and "error" in result:
            print(f"   Error: {result['error']}")

def example_5_batch_generation():
    """Example 5: Batch strategy generation"""
    print("\n🎯 Example 5: Batch Strategy Generation")
    print("="*60)
    
    launcher = BacktestSHAILauncher()
    
    if not launcher.check_availability():
        print("❌ AI integration not available. Please check your OpenAI API key.")
        return
    
    # Multiple strategy descriptions
    descriptions = [
        "Buy when RSI is below 30 and price is above 20-day moving average, sell when RSI is above 70",
        "Buy when 50-day moving average crosses above 200-day moving average, sell when it crosses below",
        "Buy when price breaks above upper Bollinger Band, sell when it breaks below lower band",
        "Buy when MACD line crosses above signal line, sell when it crosses below",
        "Buy when price is above 20-day moving average and volume is above average, sell when price is below 20-day moving average"
    ]
    
    symbols = ["BTC-USD", "AAPL", "ETH-USD", "SPY", "QQQ"]
    strategy_types = ["mean_reversion", "trend_following", "breakout", "momentum", "momentum"]
    
    print(f"📊 Generating {len(descriptions)} strategies...")
    print(f"🎯 Symbols: {', '.join(symbols)}")
    print(f"🔧 Strategy Types: {', '.join(strategy_types)}")
    
    # Run batch generation
    result = launcher.run_batch_ai_generation(
        descriptions=descriptions,
        symbols=symbols,
        start_date="2020-01-01",
        end_date="2024-01-01",
        strategy_types=strategy_types
    )
    
    if result:
        print(f"✅ Batch generation completed!")
        print(f"   Total descriptions: {result.get('total_descriptions', 0)}")
        print(f"   Successful generations: {result.get('successful_generations', 0)}")
        print(f"   Success rate: {result.get('success_rate', 0):.2%}")
    else:
        print("❌ Batch generation failed")

def example_6_custom_strategy():
    """Example 6: Custom strategy with specific parameters"""
    print("\n🎯 Example 6: Custom Strategy")
    print("="*60)
    
    launcher = BacktestSHAILauncher()
    
    if not launcher.check_availability():
        print("❌ AI integration not available. Please check your OpenAI API key.")
        return
    
    # Custom strategy with specific parameters
    description = """
    Create a multi-timeframe strategy that:
    1. Uses 1-hour chart for entry signals
    2. Uses 4-hour chart for trend confirmation
    3. Buys when 1h RSI < 30 and 4h trend is bullish
    4. Sells when 1h RSI > 70 or 4h trend turns bearish
    5. Uses ATR for stop loss and take profit
    6. Includes position sizing based on volatility
    """
    
    print(f"📝 Strategy Description: {description.strip()}")
    print(f"🎯 Symbol: BTC-USD")
    print(f"📅 Date Range: 2020-01-01 to 2024-01-01")
    print(f"🔧 Strategy Type: Multi-timeframe")
    
    result = launcher.run_ai_strategy_generation(
        description=description,
        symbol="BTC-USD",
        start_date="2020-01-01",
        end_date="2024-01-01",
        strategy_type="momentum"
    )
    
    if result and "error" not in result:
        print("✅ Custom strategy generated successfully!")
    else:
        print("❌ Strategy generation failed")
        if result and "error" in result:
            print(f"   Error: {result['error']}")

def example_7_risk_management_strategy():
    """Example 7: Strategy with advanced risk management"""
    print("\n🎯 Example 7: Risk Management Strategy")
    print("="*60)
    
    launcher = BacktestSHAILauncher()
    
    if not launcher.check_availability():
        print("❌ AI integration not available. Please check your OpenAI API key.")
        return
    
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
    
    print(f"📝 Strategy Description: {description.strip()}")
    print(f"🎯 Symbol: SPY")
    print(f"📅 Date Range: 2020-01-01 to 2024-01-01")
    print(f"🔧 Strategy Type: Risk Management")
    
    result = launcher.run_ai_strategy_generation(
        description=description,
        symbol="SPY",
        start_date="2020-01-01",
        end_date="2024-01-01",
        strategy_type="momentum"
    )
    
    if result and "error" not in result:
        print("✅ Risk management strategy generated successfully!")
    else:
        print("❌ Strategy generation failed")
        if result and "error" in result:
            print(f"   Error: {result['error']}")

def run_all_examples():
    """Run all examples"""
    print("🚀 Backtest.sh AI Integration Examples")
    print("="*80)
    print("This demonstrates AI-powered strategy generation and backtesting")
    print("using OpenAI API to transform plain text descriptions into executable strategies.")
    print("="*80)
    
    # Check if OpenAI API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OpenAI API key not found!")
        print("   Set OPENAI_API_KEY environment variable")
        print("   Get your API key from: https://platform.openai.com/api-keys")
        return
    
    try:
        # Run examples
        example_1_simple_strategy_generation()
        example_2_trend_following_strategy()
        example_3_breakout_strategy()
        example_4_momentum_strategy()
        example_5_batch_generation()
        example_6_custom_strategy()
        example_7_risk_management_strategy()
        
        print("\n🎉 All examples completed!")
        print("📁 Check generated files for results")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")

def create_sample_descriptions_file():
    """Create a sample descriptions file for batch mode"""
    sample_descriptions = [
        "Buy when RSI is below 30 and price is above 20-day moving average, sell when RSI is above 70",
        "Buy when 50-day moving average crosses above 200-day moving average, sell when it crosses below",
        "Buy when price breaks above upper Bollinger Band, sell when it breaks below lower band",
        "Buy when MACD line crosses above signal line, sell when it crosses below",
        "Buy when price is above 20-day moving average and volume is above average, sell when price is below 20-day moving average",
        "Buy when Stochastic oscillator is oversold and price is above 50-day moving average, sell when Stochastic is overbought",
        "Buy when Williams %R is below -80 and price is above 20-day moving average, sell when Williams %R is above -20",
        "Buy when Commodity Channel Index (CCI) is below -100 and price is above 20-day moving average, sell when CCI is above 100"
    ]
    
    filename = "sample_strategies.txt"
    with open(filename, 'w') as f:
        for desc in sample_descriptions:
            f.write(desc + '\n')
    
    print(f"📁 Sample descriptions file created: {filename}")
    return filename

if __name__ == "__main__":
    # Create sample descriptions file
    create_sample_descriptions_file()
    
    # Run all examples
    run_all_examples()
