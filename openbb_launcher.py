"""
OpenBB Enhanced Launcher
Enhanced launcher with OpenBB integration for Pine Script to Python backtesting
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import argparse
import sys
import os

# Import our custom modules
from pinescript_translator import PineScriptTranslator
from multi_data_backtester import MultiDataBacktester
from tsa_enhanced_strategy import TSAEnhancedStrategy
from strategy_launcher import StrategyLauncher
from results_analyzer import ResultsAnalyzer
from openbb_integration import OpenBBDataProvider, OpenBBEnhancedBacktester

class OpenBBEnhancedLauncher:
    """
    Enhanced launcher with OpenBB integration
    Provides advanced data access and analysis capabilities
    """
    
    def __init__(self):
        self.openbb_provider = OpenBBDataProvider()
        self.enhanced_backtester = OpenBBEnhancedBacktester()
        self.standard_launcher = StrategyLauncher()
        self.results = {}
        
    def check_openbb_availability(self) -> bool:
        """Check if OpenBB is available and working"""
        if not self.openbb_provider.is_available():
            print("⚠️  OpenBB not available. Install with: pip install openbb")
            print("   Falling back to standard yfinance data provider")
            return False
        
        print("✅ OpenBB is available and ready to use")
        return True
    
    def run_enhanced_single_backtest(self, symbol: str, start_date: str, end_date: str,
                                   interval: str = "1d", market_type: str = "equity",
                                   strategy_params: Dict = None) -> Dict:
        """
        Run enhanced single backtest with OpenBB data
        
        Args:
            symbol: Symbol to test
            start_date: Start date
            end_date: End date
            interval: Data interval
            market_type: Market type (equity, crypto, forex)
            strategy_params: Strategy parameters
            
        Returns:
            Enhanced backtest results
        """
        print(f"Running enhanced backtest for {symbol} ({market_type})...")
        
        # Use enhanced backtester with OpenBB
        results = self.enhanced_backtester.run_enhanced_backtest(
            TSAEnhancedStrategy,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            market_type=market_type,
            strategy_params=strategy_params
        )
        
        if results:
            print("✅ Enhanced backtest completed successfully")
            print(f"   Data source: {results.get('data_source', 'unknown')}")
            print(f"   Enhanced features: {results.get('enhanced_features', False)}")
            print(f"   Total return: {results.get('total_return', 0):.4f}")
            print(f"   Win rate: {results.get('win_rate', 0):.2%}")
        else:
            print("❌ Enhanced backtest failed")
        
        return results
    
    def run_enhanced_multi_market_backtest(self, symbols: List[str], start_date: str, end_date: str,
                                         interval: str = "1d", market_types: List[str] = None,
                                         strategy_params: Dict = None) -> Dict:
        """
        Run enhanced multi-market backtest with OpenBB
        
        Args:
            symbols: List of symbols to test
            start_date: Start date
            end_date: End date
            interval: Data interval
            market_types: List of market types
            strategy_params: Strategy parameters
            
        Returns:
            Comprehensive backtest results
        """
        print(f"Running enhanced multi-market backtest for {len(symbols)} symbols...")
        
        # Use enhanced backtester
        results = self.enhanced_backtester.run_multi_market_backtest(
            TSAEnhancedStrategy,
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            market_types=market_types,
            strategy_params=strategy_params
        )
        
        if results:
            print("✅ Enhanced multi-market backtest completed")
            print(f"   Total tests: {results['summary'].get('total_tests', 0)}")
            print(f"   Successful tests: {results['summary'].get('successful_tests', 0)}")
            print(f"   Success rate: {results['summary'].get('success_rate', 0):.2%}")
            print(f"   Average return: {results['summary'].get('avg_return', 0):.4f}")
        else:
            print("❌ Enhanced multi-market backtest failed")
        
        return results
    
    def run_comprehensive_enhanced_backtest(self, strategy_params: Dict = None) -> Dict:
        """
        Run comprehensive enhanced backtest across multiple markets
        
        Args:
            strategy_params: Strategy parameters
            
        Returns:
            Comprehensive backtest results
        """
        print("🚀 Starting comprehensive enhanced backtest...")
        
        # Define comprehensive symbol lists
        equity_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC']
        crypto_symbols = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'ADA-USD', 'SOL-USD', 'XRP-USD', 'DOT-USD', 'DOGE-USD', 'AVAX-USD', 'MATIC-USD']
        forex_symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD']
        
        # Combine all symbols
        all_symbols = equity_symbols + crypto_symbols + forex_symbols
        all_market_types = ['equity'] * len(equity_symbols) + ['crypto'] * len(crypto_symbols) + ['forex'] * len(forex_symbols)
        
        # Run enhanced multi-market backtest
        results = self.run_enhanced_multi_market_backtest(
            symbols=all_symbols,
            start_date="2023-01-01",
            end_date="2023-12-31",
            interval="1d",
            market_types=all_market_types,
            strategy_params=strategy_params
        )
        
        return results
    
    def get_enhanced_data_sample(self, symbol: str, market_type: str = "equity") -> pd.DataFrame:
        """
        Get sample enhanced data to demonstrate OpenBB capabilities
        
        Args:
            symbol: Symbol to get data for
            market_type: Market type
            
        Returns:
            Enhanced DataFrame
        """
        print(f"Getting enhanced data sample for {symbol} ({market_type})...")
        
        # Get enhanced data
        data = self.enhanced_backtester.get_enhanced_data(
            symbol=symbol,
            start_date="2023-01-01",
            end_date="2023-12-31",
            interval="1d",
            market_type=market_type
        )
        
        if data is not None:
            print(f"✅ Enhanced data loaded: {len(data)} bars")
            print(f"   Columns: {list(data.columns)}")
            print(f"   Date range: {data.index[0]} to {data.index[-1]}")
            
            # Show sample of enhanced features
            enhanced_features = [col for col in data.columns if col not in ['open', 'high', 'low', 'close', 'volume']]
            if enhanced_features:
                print(f"   Enhanced features: {enhanced_features}")
        else:
            print("❌ Failed to load enhanced data")
        
        return data
    
    def analyze_enhanced_results(self, results: Dict) -> Dict:
        """
        Analyze enhanced backtest results
        
        Args:
            results: Backtest results
            
        Returns:
            Enhanced analysis
        """
        if not results or 'successful_results' not in results:
            return {}
        
        # Standard analysis
        analyzer = ResultsAnalyzer()
        analyzer.results = results
        analysis = analyzer.analyze_performance()
        
        # Enhanced analysis with OpenBB features
        enhanced_analysis = {
            'standard_analysis': analysis,
            'openbb_features': {
                'data_sources': list(set([r.get('data_source', 'unknown') for r in results.get('successful_results', [])])),
                'enhanced_features_used': any([r.get('enhanced_features', False) for r in results.get('successful_results', [])]),
                'market_types': list(set([r.get('market_type', 'unknown') for r in results.get('successful_results', [])]))
            }
        }
        
        return enhanced_analysis
    
    def print_enhanced_analysis(self, analysis: Dict):
        """Print enhanced analysis results"""
        if not analysis:
            print("No analysis results available")
            return
        
        print("\n" + "="*80)
        print("ENHANCED OPENBB ANALYSIS REPORT")
        print("="*80)
        
        # Standard analysis
        if 'standard_analysis' in analysis:
            standard = analysis['standard_analysis']
            if 'performance_stats' in standard:
                stats = standard['performance_stats']
                print(f"Average Return: {stats['returns']['mean']:.4f}")
                print(f"Median Return: {stats['returns']['median']:.4f}")
                print(f"Best Return: {stats['returns']['max']:.4f}")
                print(f"Worst Return: {stats['returns']['min']:.4f}")
        
        # OpenBB features
        if 'openbb_features' in analysis:
            features = analysis['openbb_features']
            print(f"\nOpenBB Features:")
            print(f"  Data sources: {features.get('data_sources', [])}")
            print(f"  Enhanced features used: {features.get('enhanced_features_used', False)}")
            print(f"  Market types: {features.get('market_types', [])}")
        
        print("="*80)
    
    def run_demo(self):
        """Run demonstration of OpenBB integration"""
        print("🎯 OpenBB Integration Demo")
        print("="*50)
        
        # Check OpenBB availability
        if not self.check_openbb_availability():
            print("Running demo with standard data provider...")
            return self.standard_launcher.run_tsa_enhanced_backtest("AAPL", "1d", "2023-01-01", "2023-12-31")
        
        # Demo 1: Enhanced data sample
        print("\n📊 Demo 1: Enhanced Data Sample")
        print("-" * 30)
        equity_data = self.get_enhanced_data_sample("AAPL", "equity")
        crypto_data = self.get_enhanced_data_sample("BTC-USD", "crypto")
        
        # Demo 2: Enhanced single backtest
        print("\n🚀 Demo 2: Enhanced Single Backtest")
        print("-" * 30)
        results = self.run_enhanced_single_backtest(
            symbol="AAPL",
            start_date="2023-01-01",
            end_date="2023-12-31",
            market_type="equity"
        )
        
        # Demo 3: Enhanced multi-market backtest
        print("\n🌍 Demo 3: Enhanced Multi-Market Backtest")
        print("-" * 30)
        multi_results = self.run_enhanced_multi_market_backtest(
            symbols=["AAPL", "BTC-USD", "EURUSD"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            market_types=["equity", "crypto", "forex"]
        )
        
        # Demo 4: Enhanced analysis
        print("\n📈 Demo 4: Enhanced Analysis")
        print("-" * 30)
        if multi_results:
            analysis = self.analyze_enhanced_results(multi_results)
            self.print_enhanced_analysis(analysis)
        
        print("\n✅ Demo completed successfully!")
        return results

def main():
    """Main entry point for OpenBB enhanced launcher"""
    parser = argparse.ArgumentParser(description='OpenBB Enhanced Pine Script to Python Backtesting')
    parser.add_argument('--mode', choices=['demo', 'single', 'multi', 'comprehensive'], 
                       default='demo', help='Operation mode')
    parser.add_argument('--symbol', default='AAPL', help='Symbol for single mode')
    parser.add_argument('--market-type', choices=['equity', 'crypto', 'forex'], 
                       default='equity', help='Market type for single mode')
    parser.add_argument('--start-date', default='2023-01-01', help='Start date')
    parser.add_argument('--end-date', default='2023-12-31', help='End date')
    parser.add_argument('--interval', default='1d', help='Data interval')
    parser.add_argument('--workers', type=int, default=4, help='Number of parallel workers')
    
    args = parser.parse_args()
    
    # Initialize enhanced launcher
    launcher = OpenBBEnhancedLauncher()
    
    if args.mode == 'demo':
        print("🎯 Running OpenBB Integration Demo...")
        launcher.run_demo()
        
    elif args.mode == 'single':
        print(f"🚀 Running enhanced single backtest for {args.symbol}...")
        results = launcher.run_enhanced_single_backtest(
            symbol=args.symbol,
            start_date=args.start_date,
            end_date=args.end_date,
            interval=args.interval,
            market_type=args.market_type
        )
        
    elif args.mode == 'multi':
        print("🌍 Running enhanced multi-market backtest...")
        symbols = ['AAPL', 'MSFT', 'BTC-USD', 'ETH-USD', 'EURUSD', 'GBPUSD']
        market_types = ['equity', 'equity', 'crypto', 'crypto', 'forex', 'forex']
        
        results = launcher.run_enhanced_multi_market_backtest(
            symbols=symbols,
            start_date=args.start_date,
            end_date=args.end_date,
            interval=args.interval,
            market_types=market_types
        )
        
    elif args.mode == 'comprehensive':
        print("🚀 Running comprehensive enhanced backtest...")
        results = launcher.run_comprehensive_enhanced_backtest()
        
        if results:
            analysis = launcher.analyze_enhanced_results(results)
            launcher.print_enhanced_analysis(analysis)
    
    print("\n✅ OpenBB Enhanced Launcher completed!")

if __name__ == "__main__":
    main()
