"""
Example Usage - Pine Script to Python Backtesting System
Comprehensive example demonstrating the entire system
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import os
import sys

# Import our custom modules
from pinescript_translator import PineScriptTranslator
from multi_data_backtester import MultiDataBacktester
from tsa_enhanced_strategy import TSAEnhancedStrategy
from strategy_launcher import StrategyLauncher
from results_analyzer import ResultsAnalyzer

def example_single_backtest():
    """Example: Single backtest on BTC-USD"""
    print("="*60)
    print("EXAMPLE 1: Single Backtest on BTC-USD")
    print("="*60)
    
    # Initialize launcher
    launcher = StrategyLauncher()
    
    # Run single backtest
    results = launcher.run_tsa_enhanced_backtest(
        symbol="BTC-USD",
        timeframe="1d",
        start_date="2020-01-01",
        end_date="2024-01-01",
        strategy_params={
            'atr_length': 14,
            'atr_multiplier': 3.0,
            'risk_reward_ratio': 1.5,
            'adx_length': 14,
            'adx_threshold': 25
        }
    )
    
    if results:
        print("Single backtest completed successfully!")
        print(f"Total Return: {results.get('total_return', 0):.4f}")
        print(f"Win Rate: {results.get('win_rate', 0):.2%}")
        print(f"Profit Factor: {results.get('profit_factor', 0):.2f}")
    else:
        print("Single backtest failed!")

def example_comprehensive_backtest():
    """Example: Comprehensive backtest across multiple data sources"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Comprehensive Backtest (25+ Data Sources)")
    print("="*60)
    
    # Initialize launcher
    launcher = StrategyLauncher()
    
    # Run comprehensive backtest
    results = launcher.run_comprehensive_backtest(
        strategy_params={
            'atr_length': 14,
            'atr_multiplier': 3.0,
            'risk_reward_ratio': 1.5,
            'adx_length': 14,
            'adx_threshold': 25,
            'max_length': 50,
            'accel_multiplier': 5.0,
            'collen': 100
        },
        max_workers=4
    )
    
    if results:
        print("Comprehensive backtest completed successfully!")
        
        # Analyze results
        analysis = launcher.analyze_results(results)
        launcher.print_analysis(analysis)
        
        # Save detailed report
        analyzer = ResultsAnalyzer()
        analyzer.results = results
        analyzer.analyze_performance()
        
        # Generate report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"tsa_enhanced_analysis_{timestamp}.txt"
        analyzer.generate_report(report_file)
        
        # Create visualizations
        analyzer.create_visualizations(f"charts_{timestamp}")
        
    else:
        print("Comprehensive backtest failed!")

def example_pinescript_translation():
    """Example: Translate Pine Script to Python"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Pine Script Translation")
    print("="*60)
    
    # Initialize translator
    translator = PineScriptTranslator()
    
    # Example Pine Script code (simplified)
    pinescript_code = '''
//@version=6
strategy("Example Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Input Parameters
atr_length = input.int(14, "ATR Length", minval=1)
atr_multiplier = input.float(3.0, "ATR Multiplier", minval=0.1, maxval=10.0)
risk_reward_ratio = input.float(1.5, "Risk Reward Ratio", minval=0.5, maxval=5.0)

// ATR Calculation
atr_value = ta.atr(atr_length)

// Entry Conditions
long_condition = close > ta.sma(close, 20) and ta.rsi(close, 14) > 50
short_condition = close < ta.sma(close, 20) and ta.rsi(close, 14) < 50

// Strategy Logic
if long_condition and strategy.position_size == 0
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long", stop=close - atr_value * atr_multiplier, limit=close + atr_value * atr_multiplier * risk_reward_ratio)

if short_condition and strategy.position_size == 0
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", "Short", stop=close + atr_value * atr_multiplier, limit=close - atr_value * atr_multiplier * risk_reward_ratio)
'''
    
    # Translate to Python
    python_code = translator.translate_to_python(pinescript_code)
    
    if python_code:
        print("Pine Script translation completed!")
        print("Translated Python code:")
        print("-" * 40)
        print(python_code[:500] + "..." if len(python_code) > 500 else python_code)
        
        # Save translated code
        with open("translated_strategy.py", "w") as f:
            f.write(python_code)
        print("\nTranslated code saved to 'translated_strategy.py'")
    else:
        print("Pine Script translation failed!")

def example_custom_strategy():
    """Example: Custom strategy implementation"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Custom Strategy Implementation")
    print("="*60)
    
    # Create a simple custom strategy
    class SimpleMAStrategy:
        def __init__(self, data, **params):
            self.data = data.copy()
            self.parameters = params
            self.results = {}
            self.trades = []
            
            # Parameters
            self.fast_period = params.get('fast_period', 10)
            self.slow_period = params.get('slow_period', 20)
            self.risk_reward = params.get('risk_reward', 2.0)
            
            # Initialize
            self._calculate_indicators()
        
        def _calculate_indicators(self):
            """Calculate technical indicators"""
            self.data['sma_fast'] = self.data['close'].rolling(self.fast_period).mean()
            self.data['sma_slow'] = self.data['close'].rolling(self.slow_period).mean()
            self.data['atr'] = self.data['high'].rolling(14).max() - self.data['low'].rolling(14).min()
        
        def run_backtest(self):
            """Run backtest"""
            position = 0
            entry_price = 0
            stop_loss = 0
            take_profit = 0
            
            for i in range(len(self.data)):
                if i < self.slow_period:
                    continue
                
                current = self.data.iloc[i]
                
                # Entry conditions
                if position == 0:
                    if current['sma_fast'] > current['sma_slow']:
                        position = 1
                        entry_price = current['close']
                        stop_loss = entry_price - current['atr'] * 2
                        take_profit = entry_price + (entry_price - stop_loss) * self.risk_reward
                    elif current['sma_fast'] < current['sma_slow']:
                        position = -1
                        entry_price = current['close']
                        stop_loss = entry_price + current['atr'] * 2
                        take_profit = entry_price - (stop_loss - entry_price) * self.risk_reward
                
                # Exit conditions
                elif position > 0:  # Long position
                    if current['low'] <= stop_loss or current['high'] >= take_profit:
                        pnl = (current['close'] - entry_price) / entry_price
                        self.trades.append({'pnl': pnl, 'entry': entry_price, 'exit': current['close']})
                        position = 0
                elif position < 0:  # Short position
                    if current['high'] >= stop_loss or current['low'] <= take_profit:
                        pnl = (entry_price - current['close']) / entry_price
                        self.trades.append({'pnl': pnl, 'entry': entry_price, 'exit': current['close']})
                        position = 0
            
            # Calculate results
            if self.trades:
                returns = [t['pnl'] for t in self.trades]
                self.results = {
                    'total_trades': len(self.trades),
                    'total_return': sum(returns),
                    'win_rate': sum(1 for r in returns if r > 0) / len(returns),
                    'avg_trade': np.mean(returns)
                }
            else:
                self.results = {'total_trades': 0, 'total_return': 0, 'win_rate': 0, 'avg_trade': 0}
            
            return self.results
    
    # Test custom strategy
    print("Testing custom Simple MA Strategy...")
    
    # Load data
    ticker = yf.Ticker("BTC-USD")
    data = ticker.history(start="2020-01-01", end="2024-01-01", interval="1d")
    data.columns = [col.lower() for col in data.columns]
    
    # Run strategy
    strategy = SimpleMAStrategy(data, fast_period=10, slow_period=20, risk_reward=2.0)
    results = strategy.run_backtest()
    
    print("Custom Strategy Results:")
    print(f"Total Trades: {results['total_trades']}")
    print(f"Total Return: {results['total_return']:.4f}")
    print(f"Win Rate: {results['win_rate']:.2%}")
    print(f"Average Trade: {results['avg_trade']:.4f}")

def example_results_analysis():
    """Example: Results analysis and visualization"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Results Analysis and Visualization")
    print("="*60)
    
    # Create sample results for demonstration
    sample_results = {
        'successful_results': [
            {
                'symbol': 'BTC-USD',
                'timeframe': '1d',
                'status': 'success',
                'results': {
                    'total_return': 0.25,
                    'win_rate': 0.65,
                    'profit_factor': 2.1,
                    'sharpe_ratio': 1.8,
                    'max_drawdown': 0.15,
                    'total_trades': 45
                }
            },
            {
                'symbol': 'ETH-USD',
                'timeframe': '1d',
                'status': 'success',
                'results': {
                    'total_return': 0.18,
                    'win_rate': 0.58,
                    'profit_factor': 1.9,
                    'sharpe_ratio': 1.5,
                    'max_drawdown': 0.12,
                    'total_trades': 38
                }
            },
            {
                'symbol': 'SPY',
                'timeframe': '1d',
                'status': 'success',
                'results': {
                    'total_return': 0.12,
                    'win_rate': 0.55,
                    'profit_factor': 1.6,
                    'sharpe_ratio': 1.2,
                    'max_drawdown': 0.08,
                    'total_trades': 32
                }
            }
        ],
        'failed_results': [],
        'summary': {
            'total_tests': 3,
            'successful_tests': 3,
            'success_rate': 1.0,
            'avg_return': 0.183,
            'median_return': 0.18
        }
    }
    
    # Initialize analyzer
    analyzer = ResultsAnalyzer()
    analyzer.results = sample_results
    
    # Analyze performance
    analysis = analyzer.analyze_performance()
    
    # Generate report
    report = analyzer.generate_report("sample_analysis_report.txt")
    print("Analysis report generated!")
    print("\nSample Analysis Report:")
    print("-" * 40)
    print(report[:500] + "..." if len(report) > 500 else report)
    
    # Create visualizations
    analyzer.create_visualizations("sample_charts")
    print("\nVisualizations created in 'sample_charts/' directory")

def main():
    """Main function to run all examples"""
    print("PINE SCRIPT TO PYTHON BACKTESTING SYSTEM")
    print("Comprehensive Examples and Demonstrations")
    print("="*80)
    
    try:
        # Example 1: Single backtest
        example_single_backtest()
        
        # Example 2: Comprehensive backtest (commented out for demo - takes time)
        # example_comprehensive_backtest()
        
        # Example 3: Pine Script translation
        example_pinescript_translation()
        
        # Example 4: Custom strategy
        example_custom_strategy()
        
        # Example 5: Results analysis
        example_results_analysis()
        
        print("\n" + "="*80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nNext Steps:")
        print("1. Run comprehensive backtest: python strategy_launcher.py --mode comprehensive")
        print("2. Test single symbol: python strategy_launcher.py --mode single --symbol BTC-USD")
        print("3. Translate Pine Script: python strategy_launcher.py --mode translate --pinescript-file your_strategy.pine")
        print("4. Analyze results: python results_analyzer.py")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
