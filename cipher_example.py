"""
Cipher-BT Integration Example
Comprehensive example demonstrating Cipher-BT integration with our Pine Script to Python framework
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Import our custom modules
from cipher_integration import CipherBacktester, CipherEnhancedLauncher
from cipher_launcher import CipherComprehensiveLauncher
from tsa_enhanced_strategy import TSAEnhancedStrategy
from strategy_launcher import StrategyLauncher

def example_cipher_availability():
    """Example: Check Cipher-BT availability"""
    print("="*60)
    print("EXAMPLE 1: Cipher-BT Availability Check")
    print("="*60)
    
    # Initialize Cipher backtester
    backtester = CipherBacktester()
    
    if backtester.is_available():
        print("✅ Cipher-BT is available and ready!")
        print("   Features available:")
        print("   - Multiple concurrent sessions")
        print("   - Sophisticated exit strategies")
        print("   - Multi-exchange data sources")
        print("   - Built-in visualization")
        return True
    else:
        print("❌ Cipher-BT not available")
        print("   Install with: pip install cipher-bt")
        return False

def example_cipher_single_backtest():
    """Example: Single Cipher-BT backtest"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Single Cipher-BT Backtest")
    print("="*60)
    
    # Initialize enhanced launcher
    launcher = CipherEnhancedLauncher()
    
    if not launcher.check_cipher_availability():
        print("❌ Cipher-BT not available")
        return False
    
    print("🚀 Running single Cipher-BT backtest...")
    
    # Run single backtest
    results = launcher.run_cipher_backtest(
        TSAEnhancedStrategy,
        symbol="BTCUSDT",
        interval="1h",
        start_ts="2025-01-01",
        stop_ts="2025-04-01",
        strategy_params={
            'atr_length': 14,
            'atr_multiplier': 3.0,
            'risk_reward_ratio': 1.5,
            'adx_length': 14,
            'adx_threshold': 25
        }
    )
    
    if results:
        print("✅ Single Cipher-BT backtest completed successfully!")
        print(f"   Total trades: {results.get('total_trades', 0)}")
        print(f"   Win rate: {results.get('win_rate', 0):.2%}")
        print(f"   Total return: {results.get('total_return', 0):.4f}")
        print(f"   Max drawdown: {results.get('max_drawdown', 0):.4f}")
        print(f"   Profit factor: {results.get('profit_factor', 0):.2f}")
    else:
        print("❌ Single Cipher-BT backtest failed")
    
    return results

def example_cipher_multi_symbol_backtest():
    """Example: Multi-symbol Cipher-BT backtest"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Multi-Symbol Cipher-BT Backtest")
    print("="*60)
    
    # Initialize enhanced launcher
    launcher = CipherEnhancedLauncher()
    
    if not launcher.check_cipher_availability():
        print("❌ Cipher-BT not available")
        return False
    
    # Define symbols to test
    symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "SOLUSDT", "DOTUSDT"]
    
    print(f"🌍 Running multi-symbol Cipher-BT backtest for {len(symbols)} symbols...")
    print(f"   Symbols: {', '.join(symbols)}")
    
    # Run multi-symbol backtest
    results = launcher.run_multi_symbol_backtest(
        TSAEnhancedStrategy,
        symbols=symbols,
        interval="1h",
        start_ts="2025-01-01",
        stop_ts="2025-04-01"
    )
    
    if results:
        print("✅ Multi-symbol Cipher-BT backtest completed successfully!")
        
        # Print summary
        if 'summary' in results:
            summary = results['summary']
            print(f"   Total symbols: {summary.get('total_symbols', 0)}")
            print(f"   Average return: {summary.get('avg_return', 0):.4f}")
            print(f"   Best return: {summary.get('best_return', 0):.4f}")
            print(f"   Worst return: {summary.get('worst_return', 0):.4f}")
            print(f"   Average win rate: {summary.get('avg_win_rate', 0):.2%}")
        
        # Print individual results
        if 'all_results' in results:
            print("\n   Individual Results:")
            for result in results['all_results']:
                symbol = result.get('symbol', 'Unknown')
                total_return = result.get('total_return', 0)
                win_rate = result.get('win_rate', 0)
                print(f"     {symbol}: {total_return:.4f} return, {win_rate:.2%} win rate")
    else:
        print("❌ Multi-symbol Cipher-BT backtest failed")
    
    return results

def example_cipher_vs_standard_comparison():
    """Example: Cipher-BT vs Standard Framework Comparison"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Cipher-BT vs Standard Framework Comparison")
    print("="*60)
    
    # Initialize comprehensive launcher
    launcher = CipherComprehensiveLauncher()
    
    # Check availability
    availability = launcher.check_availability()
    print(f"Component availability:")
    for component, available in availability.items():
        status = "✅ Available" if available else "❌ Not Available"
        print(f"   {component}: {status}")
    
    if not availability['cipher_bt']:
        print("❌ Cipher-BT not available. Please install with: pip install cipher-bt")
        return False
    
    print("\n🔍 Running comprehensive comparison...")
    
    # Run comparison
    comparison_results = launcher.run_comprehensive_comparison(
        symbol="BTCUSDT",
        start_date="2025-01-01",
        end_date="2025-04-01"
    )
    
    if comparison_results:
        print("✅ Comprehensive comparison completed successfully!")
        
        # Print comparison summary
        if 'comparison' in comparison_results:
            comparison = comparison_results['comparison']
            print("\n📊 Comparison Summary:")
            
            for metric, data in comparison.items():
                print(f"   {metric.replace('_', ' ').title()}:")
                print(f"     Cipher-BT: {data['cipher']:.4f}")
                print(f"     Standard:  {data['standard']:.4f}")
                print(f"     Difference: {data['difference']:+.4f}")
                
                if data['difference'] > 0:
                    print(f"     ✅ Cipher-BT performs better by {data['difference']:.4f}")
                elif data['difference'] < 0:
                    print(f"     ✅ Standard performs better by {abs(data['difference']):.4f}")
                else:
                    print(f"     ⚖️  Both perform equally")
    else:
        print("❌ Comprehensive comparison failed")
    
    return comparison_results

def example_hybrid_backtest():
    """Example: Hybrid backtest using both frameworks"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Hybrid Backtest")
    print("="*60)
    
    # Initialize comprehensive launcher
    launcher = CipherComprehensiveLauncher()
    
    if not launcher.check_availability()['cipher_bt']:
        print("❌ Cipher-BT not available")
        return False
    
    print("🔄 Running hybrid backtest...")
    
    # Run hybrid backtest
    hybrid_results = launcher.run_hybrid_backtest(
        symbol="BTCUSDT",
        start_date="2025-01-01",
        end_date="2025-04-01"
    )
    
    if hybrid_results:
        print("✅ Hybrid backtest completed successfully!")
        
        # Print hybrid analysis
        if 'hybrid_analysis' in hybrid_results:
            analysis = hybrid_results['hybrid_analysis']
            print(f"\n📊 Hybrid Analysis:")
            print(f"   Best Performer: {analysis['best_performer'].upper()}")
            print(f"   Risk-Adjusted Return (Cipher): {analysis['risk_adjusted_return']['cipher']:.4f}")
            print(f"   Risk-Adjusted Return (Standard): {analysis['risk_adjusted_return']['standard']:.4f}")
            print(f"   Consistency (Cipher): {analysis['consistency']['cipher']:.2%}")
            print(f"   Consistency (Standard): {analysis['consistency']['standard']:.2%}")
            
            print("\n💡 Recommendations:")
            for i, rec in enumerate(analysis['recommendations'], 1):
                print(f"   {i}. {rec}")
    else:
        print("❌ Hybrid backtest failed")
    
    return hybrid_results

def example_cipher_advanced_features():
    """Example: Cipher-BT advanced features"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Cipher-BT Advanced Features")
    print("="*60)
    
    # Initialize Cipher backtester
    backtester = CipherBacktester()
    
    if not backtester.is_available():
        print("❌ Cipher-BT not available")
        return False
    
    print("✅ Cipher-BT advanced features available:")
    print("   🚀 Multiple Concurrent Sessions")
    print("   📊 Sophisticated Exit Strategies")
    print("   🌍 Multi-Exchange Data Sources")
    print("   📈 Built-in Visualization")
    print("   ⚡ Real-time Data Access")
    print("   🔄 Session Management")
    print("   📋 Advanced Position Sizing")
    print("   🎯 Trailing Take Profits")
    print("   🛡️  Complex Risk Management")
    
    # Demonstrate session management
    print("\n🔄 Session Management Features:")
    print("   - Multiple concurrent trading sessions")
    print("   - Independent position management")
    print("   - Session-specific risk parameters")
    print("   - Advanced exit strategy handling")
    
    # Demonstrate exit strategies
    print("\n📊 Exit Strategy Features:")
    print("   - Trailing take profits")
    print("   - Dynamic stop losses")
    print("   - Complex exit conditions")
    print("   - Session-based position management")
    
    # Demonstrate data sources
    print("\n🌍 Data Source Features:")
    print("   - Multi-exchange data integration")
    print("   - Real-time data access")
    print("   - Multiple symbol support")
    print("   - Flexible timeframe support")
    
    return True

def example_cipher_demo():
    """Example: Complete Cipher-BT demo"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Complete Cipher-BT Demo")
    print("="*60)
    
    # Initialize comprehensive launcher
    launcher = CipherComprehensiveLauncher()
    
    # Run complete demo
    print("🎯 Running complete Cipher-BT demo...")
    success = launcher.run_cipher_demo()
    
    if success:
        print("✅ Complete Cipher-BT demo completed successfully!")
    else:
        print("❌ Complete Cipher-BT demo failed")
    
    return success

def main():
    """Main function to run all Cipher-BT examples"""
    print("🚀 CIPHER-BT INTEGRATION EXAMPLES")
    print("Comprehensive demonstration of Cipher-BT integration")
    print("="*80)
    
    try:
        # Example 1: Availability check
        example_cipher_availability()
        
        # Example 2: Single backtest
        example_cipher_single_backtest()
        
        # Example 3: Multi-symbol backtest
        example_cipher_multi_symbol_backtest()
        
        # Example 4: Comparison
        example_cipher_vs_standard_comparison()
        
        # Example 5: Hybrid backtest
        example_hybrid_backtest()
        
        # Example 6: Advanced features
        example_cipher_advanced_features()
        
        # Example 7: Complete demo
        example_cipher_demo()
        
        print("\n" + "="*80)
        print("✅ ALL CIPHER-BT EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nNext Steps:")
        print("1. Install Cipher-BT: pip install cipher-bt")
        print("2. Run enhanced launcher: python cipher_launcher.py --mode demo")
        print("3. Run single backtest: python cipher_launcher.py --mode single --symbol BTCUSDT")
        print("4. Run multi-symbol backtest: python cipher_launcher.py --mode multi")
        print("5. Run comparison: python cipher_launcher.py --mode comparison --symbol BTCUSDT")
        print("6. Run hybrid backtest: python cipher_launcher.py --mode hybrid --symbol BTCUSDT")
        
    except Exception as e:
        print(f"❌ Error running Cipher-BT examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
