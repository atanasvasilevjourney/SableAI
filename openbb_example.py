"""
OpenBB Integration Example
Comprehensive example demonstrating OpenBB integration with Pine Script to Python backtesting
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Import our custom modules
from openbb_integration import OpenBBDataProvider, OpenBBEnhancedBacktester
from openbb_launcher import OpenBBEnhancedLauncher
from tsa_enhanced_strategy import TSAEnhancedStrategy
from results_analyzer import ResultsAnalyzer

def example_openbb_data_access():
    """Example: OpenBB data access capabilities"""
    print("="*60)
    print("EXAMPLE 1: OpenBB Data Access")
    print("="*60)
    
    # Initialize OpenBB data provider
    provider = OpenBBDataProvider()
    
    if not provider.is_available():
        print("❌ OpenBB not available. Please install with: pip install openbb")
        return False
    
    print("✅ OpenBB is available and ready!")
    
    # Example 1: Equity data
    print("\n📊 Getting equity data for AAPL...")
    equity_data = provider.get_equity_data("AAPL", "2023-01-01", "2023-12-31", "1d")
    if equity_data is not None:
        print(f"✅ Equity data loaded: {len(equity_data)} bars")
        print(f"   Columns: {list(equity_data.columns)}")
        print(f"   Date range: {equity_data.index[0]} to {equity_data.index[-1]}")
    else:
        print("❌ Failed to load equity data")
    
    # Example 2: Crypto data
    print("\n₿ Getting crypto data for BTC-USD...")
    crypto_data = provider.get_crypto_data("BTC-USD", "2023-01-01", "2023-12-31", "1d")
    if crypto_data is not None:
        print(f"✅ Crypto data loaded: {len(crypto_data)} bars")
        print(f"   Columns: {list(crypto_data.columns)}")
    else:
        print("❌ Failed to load crypto data")
    
    # Example 3: Forex data
    print("\n💱 Getting forex data for EURUSD...")
    forex_data = provider.get_forex_data("EURUSD", "2023-01-01", "2023-12-31", "1d")
    if forex_data is not None:
        print(f"✅ Forex data loaded: {len(forex_data)} bars")
        print(f"   Columns: {list(forex_data.columns)}")
    else:
        print("❌ Failed to load forex data")
    
    # Example 4: Technical indicators
    print("\n📈 Adding technical indicators...")
    if equity_data is not None:
        enhanced_data = provider.get_technical_indicators(
            equity_data, 
            ['rsi', 'macd', 'bollinger', 'atr', 'adx']
        )
        print(f"✅ Technical indicators added")
        print(f"   Enhanced columns: {[col for col in enhanced_data.columns if col not in ['open', 'high', 'low', 'close', 'volume']]}")
    
    # Example 5: Market sentiment
    print("\n😊 Getting market sentiment...")
    sentiment = provider.get_market_sentiment("AAPL")
    if sentiment:
        print(f"✅ Market sentiment: {sentiment}")
    else:
        print("❌ Failed to get market sentiment")
    
    return True

def example_enhanced_backtesting():
    """Example: Enhanced backtesting with OpenBB"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Enhanced Backtesting with OpenBB")
    print("="*60)
    
    # Initialize enhanced backtester
    backtester = OpenBBEnhancedBacktester()
    
    if not backtester.data_provider.is_available():
        print("❌ OpenBB not available. Please install with: pip install openbb")
        return False
    
    print("✅ Enhanced backtester initialized with OpenBB")
    
    # Example 1: Single enhanced backtest
    print("\n🚀 Running single enhanced backtest...")
    results = backtester.run_enhanced_backtest(
        TSAEnhancedStrategy,
        symbol="AAPL",
        start_date="2023-01-01",
        end_date="2023-12-31",
        market_type="equity"
    )
    
    if results:
        print("✅ Single enhanced backtest completed")
        print(f"   Data source: {results.get('data_source', 'unknown')}")
        print(f"   Enhanced features: {results.get('enhanced_features', False)}")
        print(f"   Total return: {results.get('total_return', 0):.4f}")
        print(f"   Win rate: {results.get('win_rate', 0):.2%}")
        print(f"   Profit factor: {results.get('profit_factor', 0):.2f}")
    else:
        print("❌ Single enhanced backtest failed")
    
    # Example 2: Multi-market backtest
    print("\n🌍 Running multi-market backtest...")
    multi_results = backtester.run_multi_market_backtest(
        TSAEnhancedStrategy,
        symbols=["AAPL", "BTC-USD", "EURUSD"],
        start_date="2023-01-01",
        end_date="2023-12-31",
        market_types=["equity", "crypto", "forex"]
    )
    
    if multi_results:
        print("✅ Multi-market backtest completed")
        print(f"   Total tests: {multi_results['summary'].get('total_tests', 0)}")
        print(f"   Successful tests: {multi_results['summary'].get('successful_tests', 0)}")
        print(f"   Success rate: {multi_results['summary'].get('success_rate', 0):.2%}")
        print(f"   Average return: {multi_results['summary'].get('avg_return', 0):.4f}")
    else:
        print("❌ Multi-market backtest failed")
    
    return results

def example_enhanced_launcher():
    """Example: Enhanced launcher with OpenBB"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Enhanced Launcher with OpenBB")
    print("="*60)
    
    # Initialize enhanced launcher
    launcher = OpenBBEnhancedLauncher()
    
    if not launcher.check_openbb_availability():
        print("❌ OpenBB not available. Please install with: pip install openbb")
        return False
    
    print("✅ Enhanced launcher initialized with OpenBB")
    
    # Example 1: Enhanced data sample
    print("\n📊 Getting enhanced data samples...")
    equity_data = launcher.get_enhanced_data_sample("AAPL", "equity")
    crypto_data = launcher.get_enhanced_data_sample("BTC-USD", "crypto")
    
    # Example 2: Enhanced single backtest
    print("\n🚀 Running enhanced single backtest...")
    results = launcher.run_enhanced_single_backtest(
        symbol="AAPL",
        start_date="2023-01-01",
        end_date="2023-12-31",
        market_type="equity"
    )
    
    # Example 3: Enhanced multi-market backtest
    print("\n🌍 Running enhanced multi-market backtest...")
    multi_results = launcher.run_enhanced_multi_market_backtest(
        symbols=["AAPL", "BTC-USD", "EURUSD"],
        start_date="2023-01-01",
        end_date="2023-12-31",
        market_types=["equity", "crypto", "forex"]
    )
    
    # Example 4: Enhanced analysis
    print("\n📈 Running enhanced analysis...")
    if multi_results:
        analysis = launcher.analyze_enhanced_results(multi_results)
        launcher.print_enhanced_analysis(analysis)
    
    return results

def example_comprehensive_demo():
    """Example: Comprehensive OpenBB demo"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Comprehensive OpenBB Demo")
    print("="*60)
    
    # Initialize enhanced launcher
    launcher = OpenBBEnhancedLauncher()
    
    # Run comprehensive demo
    print("🎯 Running comprehensive OpenBB demo...")
    results = launcher.run_demo()
    
    if results:
        print("✅ Comprehensive demo completed successfully")
    else:
        print("❌ Comprehensive demo failed")
    
    return results

def example_data_comparison():
    """Example: Compare OpenBB vs yfinance data"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Data Quality Comparison")
    print("="*60)
    
    # Initialize providers
    openbb_provider = OpenBBDataProvider()
    
    # Get data from both sources
    print("📊 Comparing data sources...")
    
    if openbb_provider.is_available():
        # OpenBB data
        openbb_data = openbb_provider.get_equity_data("AAPL", "2023-01-01", "2023-12-31", "1d")
        if openbb_data is not None:
            print(f"✅ OpenBB data: {len(openbb_data)} bars")
            print(f"   Columns: {list(openbb_data.columns)}")
            print(f"   Date range: {openbb_data.index[0]} to {openbb_data.index[-1]}")
            
            # Show enhanced features
            enhanced_features = [col for col in openbb_data.columns if col not in ['open', 'high', 'low', 'close', 'volume']]
            if enhanced_features:
                print(f"   Enhanced features: {enhanced_features}")
    
    # yfinance data (fallback)
    try:
        import yfinance as yf
        ticker = yf.Ticker("AAPL")
        yfinance_data = ticker.history(start="2023-01-01", end="2023-12-31", interval="1d")
        yfinance_data.columns = [col.lower() for col in yfinance_data.columns]
        
        print(f"✅ yfinance data: {len(yfinance_data)} bars")
        print(f"   Columns: {list(yfinance_data.columns)}")
        print(f"   Date range: {yfinance_data.index[0]} to {yfinance_data.index[-1]}")
        
        # Compare data quality
        if openbb_provider.is_available() and openbb_data is not None:
            print(f"\n📈 Data Quality Comparison:")
            print(f"   OpenBB bars: {len(openbb_data)}")
            print(f"   yfinance bars: {len(yfinance_data)}")
            print(f"   OpenBB features: {len(enhanced_features) if enhanced_features else 0}")
            print(f"   yfinance features: 0")
            
    except ImportError:
        print("❌ yfinance not available for comparison")
    
    return True

def example_advanced_features():
    """Example: Advanced OpenBB features"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Advanced OpenBB Features")
    print("="*60)
    
    provider = OpenBBDataProvider()
    
    if not provider.is_available():
        print("❌ OpenBB not available. Please install with: pip install openbb")
        return False
    
    print("✅ OpenBB advanced features available")
    
    # Example 1: Market sentiment
    print("\n😊 Market sentiment analysis...")
    sentiment = provider.get_market_sentiment("AAPL")
    if sentiment:
        print(f"✅ Sentiment analysis: {sentiment}")
    else:
        print("❌ Sentiment analysis failed")
    
    # Example 2: Earnings data
    print("\n💰 Earnings data...")
    earnings = provider.get_earnings_data("AAPL")
    if earnings is not None:
        print(f"✅ Earnings data: {len(earnings)} records")
        print(f"   Columns: {list(earnings.columns)}")
    else:
        print("❌ Earnings data failed")
    
    # Example 3: Financial ratios
    print("\n📊 Financial ratios...")
    ratios = provider.get_financial_ratios("AAPL")
    if ratios is not None:
        print(f"✅ Financial ratios: {len(ratios)} records")
        print(f"   Columns: {list(ratios.columns)}")
    else:
        print("❌ Financial ratios failed")
    
    # Example 4: Macro data
    print("\n🌍 Macroeconomic data...")
    macro_data = provider.get_macro_data("GDP", "2023-01-01", "2023-12-31")
    if macro_data is not None:
        print(f"✅ Macro data: {len(macro_data)} records")
        print(f"   Columns: {list(macro_data.columns)}")
    else:
        print("❌ Macro data failed")
    
    return True

def main():
    """Main function to run all OpenBB examples"""
    print("🚀 OPENBB INTEGRATION EXAMPLES")
    print("Comprehensive demonstration of OpenBB integration")
    print("="*80)
    
    try:
        # Example 1: Data access
        example_openbb_data_access()
        
        # Example 2: Enhanced backtesting
        example_enhanced_backtesting()
        
        # Example 3: Enhanced launcher
        example_enhanced_launcher()
        
        # Example 4: Comprehensive demo
        example_comprehensive_demo()
        
        # Example 5: Data comparison
        example_data_comparison()
        
        # Example 6: Advanced features
        example_advanced_features()
        
        print("\n" + "="*80)
        print("✅ ALL OPENBB EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nNext Steps:")
        print("1. Install OpenBB: pip install openbb")
        print("2. Run enhanced launcher: python openbb_launcher.py --mode demo")
        print("3. Run comprehensive backtest: python openbb_launcher.py --mode comprehensive")
        print("4. Explore advanced features: python openbb_example.py")
        
    except Exception as e:
        print(f"❌ Error running OpenBB examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
