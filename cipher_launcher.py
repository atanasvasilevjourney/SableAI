"""
Cipher-BT Enhanced Launcher
Comprehensive launcher integrating Cipher-BT with our Pine Script to Python framework
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import argparse
import sys
import os
from typing import Dict, List, Optional

# Import our custom modules
from cipher_integration import CipherEnhancedLauncher, CipherBacktester
from tsa_enhanced_strategy import TSAEnhancedStrategy
from strategy_launcher import StrategyLauncher
from results_analyzer import ResultsAnalyzer

class CipherComprehensiveLauncher:
    """
    Comprehensive launcher integrating Cipher-BT with our existing framework
    """
    
    def __init__(self):
        self.cipher_launcher = CipherEnhancedLauncher()
        self.standard_launcher = StrategyLauncher()
        self.results = {}
        
    def check_availability(self) -> Dict[str, bool]:
        """Check availability of all components"""
        return {
            'cipher_bt': self.cipher_launcher.check_cipher_availability(),
            'standard': True,  # Our standard framework is always available
        }
    
    def run_comprehensive_comparison(self, symbol: str, start_date: str, end_date: str,
                                   strategy_params: Dict = None) -> Dict:
        """
        Run comprehensive comparison between Cipher-BT and standard framework
        
        Args:
            symbol: Symbol to test
            start_date: Start date
            end_date: End date
            strategy_params: Strategy parameters
            
        Returns:
            Comparison results
        """
        print("🔍 Running comprehensive comparison...")
        
        comparison_results = {
            'symbol': symbol,
            'start_date': start_date,
            'end_date': end_date,
            'cipher_results': {},
            'standard_results': {},
            'comparison': {}
        }
        
        # Run Cipher-BT backtest
        if self.cipher_launcher.check_cipher_availability():
            print("🚀 Running Cipher-BT backtest...")
            cipher_results = self.cipher_launcher.run_cipher_backtest(
                TSAEnhancedStrategy,
                symbol=symbol,
                interval="1h",
                start_ts=start_date,
                stop_ts=end_date,
                strategy_params=strategy_params
            )
            comparison_results['cipher_results'] = cipher_results
        
        # Run standard backtest
        print("📊 Running standard backtest...")
        standard_results = self.standard_launcher.run_tsa_enhanced_backtest(
            symbol=symbol,
            timeframe="1d",
            start_date=start_date,
            end_date=end_date,
            strategy_params=strategy_params
        )
        comparison_results['standard_results'] = standard_results
        
        # Compare results
        if cipher_results and standard_results:
            comparison_results['comparison'] = self._compare_results(cipher_results, standard_results)
            self._print_comparison(comparison_results['comparison'])
        
        return comparison_results
    
    def _compare_results(self, cipher_results: Dict, standard_results: Dict) -> Dict:
        """Compare Cipher-BT and standard results"""
        comparison = {
            'total_trades': {
                'cipher': cipher_results.get('total_trades', 0),
                'standard': standard_results.get('total_trades', 0),
                'difference': cipher_results.get('total_trades', 0) - standard_results.get('total_trades', 0)
            },
            'win_rate': {
                'cipher': cipher_results.get('win_rate', 0),
                'standard': standard_results.get('win_rate', 0),
                'difference': cipher_results.get('win_rate', 0) - standard_results.get('win_rate', 0)
            },
            'total_return': {
                'cipher': cipher_results.get('total_return', 0),
                'standard': standard_results.get('total_return', 0),
                'difference': cipher_results.get('total_return', 0) - standard_results.get('total_return', 0)
            },
            'max_drawdown': {
                'cipher': cipher_results.get('max_drawdown', 0),
                'standard': standard_results.get('max_drawdown', 0),
                'difference': cipher_results.get('max_drawdown', 0) - standard_results.get('max_drawdown', 0)
            },
            'profit_factor': {
                'cipher': cipher_results.get('profit_factor', 0),
                'standard': standard_results.get('profit_factor', 0),
                'difference': cipher_results.get('profit_factor', 0) - standard_results.get('profit_factor', 0)
            }
        }
        
        return comparison
    
    def _print_comparison(self, comparison: Dict):
        """Print comparison results"""
        print("\n" + "="*80)
        print("CIPHER-BT vs STANDARD FRAMEWORK COMPARISON")
        print("="*80)
        
        for metric, data in comparison.items():
            print(f"\n{metric.replace('_', ' ').title()}:")
            print(f"  Cipher-BT: {data['cipher']:.4f}")
            print(f"  Standard:  {data['standard']:.4f}")
            print(f"  Difference: {data['difference']:+.4f}")
            
            if data['difference'] > 0:
                print(f"  ✅ Cipher-BT performs better by {data['difference']:.4f}")
            elif data['difference'] < 0:
                print(f"  ✅ Standard performs better by {abs(data['difference']):.4f}")
            else:
                print(f"  ⚖️  Both perform equally")
        
        print("="*80)
    
    def run_cipher_multi_symbol_backtest(self, symbols: List[str], interval: str = "1h",
                                        start_ts: str = "2025-01-01", stop_ts: str = "2025-04-01",
                                        strategy_params: Dict = None) -> Dict:
        """Run Cipher-BT multi-symbol backtest"""
        
        if not self.cipher_launcher.check_cipher_availability():
            print("❌ Cipher-BT not available")
            return {}
        
        print(f"🌍 Running Cipher-BT multi-symbol backtest for {len(symbols)} symbols...")
        
        results = self.cipher_launcher.run_multi_symbol_backtest(
            TSAEnhancedStrategy,
            symbols=symbols,
            interval=interval,
            start_ts=start_ts,
            stop_ts=stop_ts,
            strategy_params=strategy_params
        )
        
        if results:
            print("✅ Cipher-BT multi-symbol backtest completed")
            self._print_multi_symbol_summary(results)
        else:
            print("❌ Cipher-BT multi-symbol backtest failed")
        
        return results
    
    def _print_multi_symbol_summary(self, results: Dict):
        """Print multi-symbol backtest summary"""
        if 'summary' not in results:
            return
        
        summary = results['summary']
        print(f"\n📊 Multi-Symbol Summary:")
        print(f"  Total symbols: {summary.get('total_symbols', 0)}")
        print(f"  Average return: {summary.get('avg_return', 0):.4f}")
        print(f"  Median return: {summary.get('median_return', 0):.4f}")
        print(f"  Best return: {summary.get('best_return', 0):.4f}")
        print(f"  Worst return: {summary.get('worst_return', 0):.4f}")
        print(f"  Average win rate: {summary.get('avg_win_rate', 0):.2%}")
    
    def run_cipher_demo(self):
        """Run comprehensive Cipher-BT demo"""
        print("🎯 Cipher-BT Integration Demo")
        print("="*50)
        
        # Check availability
        availability = self.check_availability()
        print(f"Component availability:")
        for component, available in availability.items():
            status = "✅ Available" if available else "❌ Not Available"
            print(f"  {component}: {status}")
        
        if not availability['cipher_bt']:
            print("\n❌ Cipher-BT not available. Please install with: pip install cipher-bt")
            return False
        
        # Demo 1: Single symbol backtest
        print("\n🚀 Demo 1: Single Symbol Backtest")
        print("-" * 30)
        single_results = self.cipher_launcher.run_cipher_backtest(
            TSAEnhancedStrategy,
            symbol="BTCUSDT",
            interval="1h",
            start_ts="2025-01-01",
            stop_ts="2025-04-01"
        )
        
        # Demo 2: Multi-symbol backtest
        print("\n🌍 Demo 2: Multi-Symbol Backtest")
        print("-" * 30)
        symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "SOLUSDT", "DOTUSDT"]
        multi_results = self.cipher_launcher.run_multi_symbol_backtest(
            TSAEnhancedStrategy,
            symbols=symbols,
            interval="1h",
            start_ts="2025-01-01",
            stop_ts="2025-04-01"
        )
        
        # Demo 3: Comprehensive comparison
        print("\n🔍 Demo 3: Comprehensive Comparison")
        print("-" * 30)
        comparison_results = self.run_comprehensive_comparison(
            symbol="BTCUSDT",
            start_date="2025-01-01",
            end_date="2025-04-01"
        )
        
        print("\n✅ Cipher-BT demo completed successfully!")
        return True
    
    def run_hybrid_backtest(self, symbol: str, start_date: str, end_date: str,
                           strategy_params: Dict = None) -> Dict:
        """
        Run hybrid backtest using both Cipher-BT and standard framework
        
        Args:
            symbol: Symbol to test
            start_date: Start date
            end_date: End date
            strategy_params: Strategy parameters
            
        Returns:
            Hybrid backtest results
        """
        print("🔄 Running hybrid backtest...")
        
        hybrid_results = {
            'symbol': symbol,
            'start_date': start_date,
            'end_date': end_date,
            'cipher_results': {},
            'standard_results': {},
            'hybrid_analysis': {}
        }
        
        # Run both backtests
        if self.cipher_launcher.check_cipher_availability():
            print("🚀 Running Cipher-BT backtest...")
            cipher_results = self.cipher_launcher.run_cipher_backtest(
                TSAEnhancedStrategy,
                symbol=symbol,
                interval="1h",
                start_ts=start_date,
                stop_ts=end_date,
                strategy_params=strategy_params
            )
            hybrid_results['cipher_results'] = cipher_results
        
        print("📊 Running standard backtest...")
        standard_results = self.standard_launcher.run_tsa_enhanced_backtest(
            symbol=symbol,
            timeframe="1d",
            start_date=start_date,
            end_date=end_date,
            strategy_params=strategy_params
        )
        hybrid_results['standard_results'] = standard_results
        
        # Perform hybrid analysis
        if cipher_results and standard_results:
            hybrid_results['hybrid_analysis'] = self._perform_hybrid_analysis(
                cipher_results, standard_results
            )
            self._print_hybrid_analysis(hybrid_results['hybrid_analysis'])
        
        return hybrid_results
    
    def _perform_hybrid_analysis(self, cipher_results: Dict, standard_results: Dict) -> Dict:
        """Perform hybrid analysis combining both results"""
        analysis = {
            'best_performer': 'cipher' if cipher_results.get('total_return', 0) > standard_results.get('total_return', 0) else 'standard',
            'risk_adjusted_return': {
                'cipher': cipher_results.get('total_return', 0) / (cipher_results.get('max_drawdown', 0) + 1e-8),
                'standard': standard_results.get('total_return', 0) / (standard_results.get('max_drawdown', 0) + 1e-8)
            },
            'consistency': {
                'cipher': cipher_results.get('win_rate', 0),
                'standard': standard_results.get('win_rate', 0)
            },
            'recommendations': []
        }
        
        # Generate recommendations
        if analysis['best_performer'] == 'cipher':
            analysis['recommendations'].append("Cipher-BT shows better performance for this symbol")
        else:
            analysis['recommendations'].append("Standard framework shows better performance for this symbol")
        
        if analysis['risk_adjusted_return']['cipher'] > analysis['risk_adjusted_return']['standard']:
            analysis['recommendations'].append("Cipher-BT provides better risk-adjusted returns")
        else:
            analysis['recommendations'].append("Standard framework provides better risk-adjusted returns")
        
        if analysis['consistency']['cipher'] > analysis['consistency']['standard']:
            analysis['recommendations'].append("Cipher-BT shows more consistent performance")
        else:
            analysis['recommendations'].append("Standard framework shows more consistent performance")
        
        return analysis
    
    def _print_hybrid_analysis(self, analysis: Dict):
        """Print hybrid analysis results"""
        print("\n" + "="*80)
        print("HYBRID ANALYSIS RESULTS")
        print("="*80)
        
        print(f"Best Performer: {analysis['best_performer'].upper()}")
        print(f"Risk-Adjusted Return (Cipher): {analysis['risk_adjusted_return']['cipher']:.4f}")
        print(f"Risk-Adjusted Return (Standard): {analysis['risk_adjusted_return']['standard']:.4f}")
        print(f"Consistency (Cipher): {analysis['consistency']['cipher']:.2%}")
        print(f"Consistency (Standard): {analysis['consistency']['standard']:.2%}")
        
        print("\nRecommendations:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        print("="*80)

def main():
    """Main entry point for Cipher-BT enhanced launcher"""
    parser = argparse.ArgumentParser(description='Cipher-BT Enhanced Pine Script to Python Backtesting')
    parser.add_argument('--mode', choices=['demo', 'single', 'multi', 'comparison', 'hybrid'], 
                       default='demo', help='Operation mode')
    parser.add_argument('--symbol', default='BTCUSDT', help='Symbol for single mode')
    parser.add_argument('--symbols', nargs='+', help='Symbols for multi mode')
    parser.add_argument('--start-date', default='2025-01-01', help='Start date')
    parser.add_argument('--end-date', default='2025-04-01', help='End date')
    parser.add_argument('--interval', default='1h', help='Data interval')
    
    args = parser.parse_args()
    
    # Initialize comprehensive launcher
    launcher = CipherComprehensiveLauncher()
    
    if args.mode == 'demo':
        print("🎯 Running Cipher-BT Integration Demo...")
        launcher.run_cipher_demo()
        
    elif args.mode == 'single':
        print(f"🚀 Running Cipher-BT single backtest for {args.symbol}...")
        results = launcher.cipher_launcher.run_cipher_backtest(
            TSAEnhancedStrategy,
            symbol=args.symbol,
            interval=args.interval,
            start_ts=args.start_date,
            stop_ts=args.end_date
        )
        
    elif args.mode == 'multi':
        if not args.symbols:
            symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "SOLUSDT", "DOTUSDT"]
        else:
            symbols = args.symbols
        
        print(f"🌍 Running Cipher-BT multi-symbol backtest for {len(symbols)} symbols...")
        results = launcher.run_cipher_multi_symbol_backtest(
            symbols=symbols,
            interval=args.interval,
            start_ts=args.start_date,
            stop_ts=args.end_date
        )
        
    elif args.mode == 'comparison':
        print(f"🔍 Running comprehensive comparison for {args.symbol}...")
        results = launcher.run_comprehensive_comparison(
            symbol=args.symbol,
            start_date=args.start_date,
            end_date=args.end_date
        )
        
    elif args.mode == 'hybrid':
        print(f"🔄 Running hybrid backtest for {args.symbol}...")
        results = launcher.run_hybrid_backtest(
            symbol=args.symbol,
            start_date=args.start_date,
            end_date=args.end_date
        )
    
    print("\n✅ Cipher-BT Enhanced Launcher completed!")

if __name__ == "__main__":
    main()
