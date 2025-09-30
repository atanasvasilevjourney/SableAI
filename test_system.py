"""
Test System - Verify all components work correctly
Simple test script to ensure the system is functioning properly
"""

import sys
import traceback
from datetime import datetime

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        import pandas as pd
        import numpy as np
        import yfinance as yf
        print("✓ Basic libraries imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import basic libraries: {e}")
        return False
    
    try:
        from pinescript_translator import PineScriptTranslator
        from multi_data_backtester import MultiDataBacktester
        from tsa_enhanced_strategy import TSAEnhancedStrategy
        from strategy_launcher import StrategyLauncher
        from results_analyzer import ResultsAnalyzer
        print("✓ Custom modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import custom modules: {e}")
        return False
    
    return True

def test_data_loading():
    """Test data loading functionality"""
    print("\nTesting data loading...")
    
    try:
        import yfinance as yf
        
        # Test loading BTC data
        ticker = yf.Ticker("BTC-USD")
        data = ticker.history(start="2023-01-01", end="2023-12-31", interval="1d")
        
        if data.empty:
            print("✗ No data loaded")
            return False
        
        print(f"✓ Data loaded successfully: {len(data)} bars")
        print(f"  Date range: {data.index[0]} to {data.index[-1]}")
        print(f"  Columns: {list(data.columns)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Data loading failed: {e}")
        return False

def test_strategy_initialization():
    """Test strategy initialization"""
    print("\nTesting strategy initialization...")
    
    try:
        import yfinance as yf
        from tsa_enhanced_strategy import TSAEnhancedStrategy
        
        # Load sample data
        ticker = yf.Ticker("BTC-USD")
        data = ticker.history(start="2023-01-01", end="2023-12-31", interval="1d")
        data.columns = [col.lower() for col in data.columns]
        
        # Initialize strategy
        strategy = TSAEnhancedStrategy(data, 
            atr_length=14,
            atr_multiplier=3.0,
            risk_reward_ratio=1.5
        )
        
        print("✓ Strategy initialized successfully")
        print(f"  Data points: {len(strategy.data)}")
        print(f"  Parameters: {strategy.parameters}")
        
        return True
        
    except Exception as e:
        print(f"✗ Strategy initialization failed: {e}")
        traceback.print_exc()
        return False

def test_simple_backtest():
    """Test simple backtest execution"""
    print("\nTesting simple backtest...")
    
    try:
        import yfinance as yf
        from tsa_enhanced_strategy import TSAEnhancedStrategy
        
        # Load sample data
        ticker = yf.Ticker("BTC-USD")
        data = ticker.history(start="2023-01-01", end="2023-12-31", interval="1d")
        data.columns = [col.lower() for col in data.columns]
        
        # Initialize and run strategy
        strategy = TSAEnhancedStrategy(data, 
            atr_length=14,
            atr_multiplier=3.0,
            risk_reward_ratio=1.5
        )
        
        results = strategy.run_backtest()
        
        print("✓ Backtest completed successfully")
        print(f"  Total trades: {results.get('total_trades', 0)}")
        print(f"  Total return: {results.get('total_return', 0):.4f}")
        print(f"  Win rate: {results.get('win_rate', 0):.2%}")
        
        return True
        
    except Exception as e:
        print(f"✗ Backtest failed: {e}")
        traceback.print_exc()
        return False

def test_translator():
    """Test Pine Script translator"""
    print("\nTesting Pine Script translator...")
    
    try:
        from pinescript_translator import PineScriptTranslator
        
        # Simple Pine Script example
        pinescript_code = '''
//@version=6
strategy("Test Strategy", overlay=true)

atr_length = input.int(14, "ATR Length")
atr_value = ta.atr(atr_length)

long_condition = close > ta.sma(close, 20)
if long_condition and strategy.position_size == 0
    strategy.entry("Long", strategy.long)
'''
        
        translator = PineScriptTranslator()
        config = translator.parse_pinescript(pinescript_code)
        
        print("✓ Pine Script parsed successfully")
        print(f"  Strategy name: {config.name}")
        print(f"  Parameters: {list(config.parameters.keys())}")
        
        return True
        
    except Exception as e:
        print(f"✗ Pine Script translation failed: {e}")
        traceback.print_exc()
        return False

def test_backtester():
    """Test multi-data backtester"""
    print("\nTesting multi-data backtester...")
    
    try:
        from multi_data_backtester import MultiDataBacktester
        
        backtester = MultiDataBacktester()
        
        print("✓ Multi-data backtester initialized")
        print(f"  Data sources: {len(backtester.data_sources)}")
        
        # Test data source loading
        test_source = backtester.data_sources[0]
        data = backtester.load_data(test_source)
        
        if data is not None:
            print(f"✓ Data loaded for {test_source.symbol} {test_source.timeframe}")
            print(f"  Data points: {len(data)}")
        else:
            print(f"⚠ No data available for {test_source.symbol} {test_source.timeframe}")
        
        return True
        
    except Exception as e:
        print(f"✗ Multi-data backtester failed: {e}")
        traceback.print_exc()
        return False

def test_results_analyzer():
    """Test results analyzer"""
    print("\nTesting results analyzer...")
    
    try:
        from results_analyzer import ResultsAnalyzer
        
        # Create sample results
        sample_results = {
            'successful_results': [
                {
                    'symbol': 'BTC-USD',
                    'timeframe': '1d',
                    'status': 'success',
                    'results': {
                        'total_return': 0.15,
                        'win_rate': 0.6,
                        'profit_factor': 1.8,
                        'total_trades': 30
                    }
                }
            ],
            'failed_results': [],
            'summary': {
                'total_tests': 1,
                'successful_tests': 1,
                'success_rate': 1.0
            }
        }
        
        analyzer = ResultsAnalyzer()
        analyzer.results = sample_results
        
        analysis = analyzer.analyze_performance()
        
        print("✓ Results analyzer working")
        print(f"  Analysis keys: {list(analysis.keys())}")
        
        return True
        
    except Exception as e:
        print(f"✗ Results analyzer failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("PINE SCRIPT TO PYTHON BACKTESTING SYSTEM - TEST SUITE")
    print("="*60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Import Test", test_imports),
        ("Data Loading Test", test_data_loading),
        ("Strategy Initialization Test", test_strategy_initialization),
        ("Simple Backtest Test", test_simple_backtest),
        ("Translator Test", test_translator),
        ("Backtester Test", test_backtester),
        ("Results Analyzer Test", test_results_analyzer)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                print(f"✓ {test_name} PASSED")
                passed += 1
            else:
                print(f"✗ {test_name} FAILED")
                failed += 1
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is ready to use.")
        print("\nNext steps:")
        print("1. Run: python example_usage.py")
        print("2. Run: python strategy_launcher.py --mode single --symbol BTC-USD")
        print("3. Run: python strategy_launcher.py --mode comprehensive")
    else:
        print(f"\n⚠ {failed} tests failed. Please check the errors above.")
    
    print("="*60)

if __name__ == "__main__":
    main()
