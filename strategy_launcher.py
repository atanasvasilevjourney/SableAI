"""
Strategy Launcher - Main entry point for Pine Script to Python backtesting
Comprehensive launcher for testing strategies across multiple data sources
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import os
import sys
import argparse
import json
from typing import Dict, List, Optional

# Import our custom modules
from pinescript_translator import PineScriptTranslator
from multi_data_backtester import MultiDataBacktester
from tsa_enhanced_strategy import TSAEnhancedStrategy

class StrategyLauncher:
    """
    Main launcher for Pine Script to Python backtesting system
    Handles strategy translation, data loading, and comprehensive testing
    """
    
    def __init__(self):
        self.translator = PineScriptTranslator()
        self.backtester = MultiDataBacktester()
        self.results = {}
        
    def translate_pinescript_strategy(self, pinescript_file: str, output_file: str = None) -> str:
        """
        Translate Pine Script strategy to Python
        
        Args:
            pinescript_file: Path to Pine Script file
            output_file: Output file for translated Python code
            
        Returns:
            Translated Python code as string
        """
        try:
            # Read Pine Script file
            with open(pinescript_file, 'r') as f:
                pinescript_code = f.read()
            
            # Translate to Python
            python_code = self.translator.translate_to_python(pinescript_code)
            
            # Save translated code
            if output_file:
                with open(output_file, 'w') as f:
                    f.write(python_code)
                print(f"Translated strategy saved to: {output_file}")
            
            return python_code
            
        except Exception as e:
            print(f"Error translating Pine Script: {e}")
            return None
    
    def run_tsa_enhanced_backtest(self, symbol: str = "BTC-USD", timeframe: str = "1d", 
                                 start_date: str = "2020-01-01", end_date: str = "2024-01-01",
                                 strategy_params: Dict = None) -> Dict:
        """
        Run TSA Enhanced Strategy backtest on single data source
        
        Args:
            symbol: Trading symbol
            timeframe: Data timeframe
            start_date: Start date for backtest
            end_date: End date for backtest
            strategy_params: Strategy parameters
            
        Returns:
            Backtest results
        """
        try:
            # Load data
            print(f"Loading data for {symbol} {timeframe}...")
            ticker = yf.Ticker(symbol)
            
            # Map timeframes
            interval_map = {
                '1m': '1m', '5m': '5m', '15m': '15m',
                '1h': '1h', '4h': '4h', '1d': '1d'
            }
            
            interval = interval_map.get(timeframe, '1d')
            data = ticker.history(start=start_date, end=end_date, interval=interval)
            
            if data.empty:
                print(f"No data available for {symbol}")
                return {}
            
            # Standardize column names
            data.columns = [col.lower() for col in data.columns]
            
            # Initialize strategy
            if strategy_params is None:
                strategy_params = {
                    'atr_length': 14,
                    'atr_multiplier': 3.0,
                    'risk_reward_ratio': 1.5,
                    'adx_length': 14,
                    'adx_threshold': 25,
                    'max_length': 50,
                    'accel_multiplier': 5.0,
                    'collen': 100
                }
            
            strategy = TSAEnhancedStrategy(data, **strategy_params)
            
            # Run backtest
            results = strategy.run_backtest()
            
            # Print results
            strategy.print_results()
            
            return results
            
        except Exception as e:
            print(f"Error running TSA Enhanced backtest: {e}")
            return {}
    
    def run_comprehensive_backtest(self, strategy_params: Dict = None, 
                                 max_workers: int = 4) -> Dict:
        """
        Run comprehensive backtest across all data sources
        
        Args:
            strategy_params: Strategy parameters
            max_workers: Number of parallel workers
            
        Returns:
            Comprehensive backtest results
        """
        try:
            print("Starting comprehensive TSA Enhanced Strategy backtest...")
            print("Testing across 25+ data sources...")
            
            # Run comprehensive backtest
            results = self.backtester.run_comprehensive_backtest(
                TSAEnhancedStrategy, 
                strategy_params, 
                max_workers
            )
            
            # Print summary
            self.backtester.print_summary()
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tsa_enhanced_comprehensive_{timestamp}"
            self.backtester.save_results(filename)
            
            return results
            
        except Exception as e:
            print(f"Error running comprehensive backtest: {e}")
            return {}
    
    def run_custom_strategy_backtest(self, strategy_class, strategy_params: Dict = None,
                                   max_workers: int = 4) -> Dict:
        """
        Run backtest with custom strategy class
        
        Args:
            strategy_class: Custom strategy class
            strategy_params: Strategy parameters
            max_workers: Number of parallel workers
            
        Returns:
            Backtest results
        """
        try:
            print(f"Running comprehensive backtest for {strategy_class.__name__}...")
            
            # Run comprehensive backtest
            results = self.backtester.run_comprehensive_backtest(
                strategy_class, 
                strategy_params, 
                max_workers
            )
            
            # Print summary
            self.backtester.print_summary()
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{strategy_class.__name__.lower()}_comprehensive_{timestamp}"
            self.backtester.save_results(filename)
            
            return results
            
        except Exception as e:
            print(f"Error running custom strategy backtest: {e}")
            return {}
    
    def analyze_results(self, results: Dict) -> Dict:
        """
        Analyze backtest results and provide insights
        
        Args:
            results: Backtest results dictionary
            
        Returns:
            Analysis results
        """
        if not results or 'successful_results' not in results:
            return {}
        
        successful = results['successful_results']
        
        # Get top performers
        top_performers = self.backtester.get_top_performers(10)
        
        # Get strategy analysis
        strategy_analysis = self.backtester.get_strategy_analysis()
        
        # Create analysis report
        analysis = {
            'summary': results['summary'],
            'top_performers': top_performers,
            'strategy_analysis': strategy_analysis,
            'recommendations': self._generate_recommendations(successful, strategy_analysis)
        }
        
        return analysis
    
    def _generate_recommendations(self, successful_results: List[Dict], 
                                 strategy_analysis: Dict) -> List[str]:
        """Generate trading recommendations based on results"""
        recommendations = []
        
        if not successful_results:
            recommendations.append("No successful backtests - strategy needs optimization")
            return recommendations
        
        # Analyze performance
        returns = [r.get('results', {}).get('total_return', 0) for r in successful_results]
        win_rates = [r.get('results', {}).get('win_rate', 0) for r in successful_results]
        profit_factors = [r.get('results', {}).get('profit_factor', 0) for r in successful_results]
        
        avg_return = np.mean(returns)
        avg_win_rate = np.mean(win_rates)
        avg_profit_factor = np.mean(profit_factors)
        
        # Generate recommendations
        if avg_return > 0.2:
            recommendations.append("Strategy shows strong positive returns - consider live trading")
        elif avg_return > 0.1:
            recommendations.append("Strategy shows moderate positive returns - monitor closely")
        elif avg_return > 0:
            recommendations.append("Strategy shows weak positive returns - consider optimization")
        else:
            recommendations.append("Strategy shows negative returns - needs significant optimization")
        
        if avg_win_rate > 0.6:
            recommendations.append("High win rate indicates good entry/exit logic")
        elif avg_win_rate > 0.5:
            recommendations.append("Moderate win rate - consider improving entry conditions")
        else:
            recommendations.append("Low win rate - review entry/exit logic")
        
        if avg_profit_factor > 2.0:
            recommendations.append("Strong profit factor indicates good risk/reward ratio")
        elif avg_profit_factor > 1.5:
            recommendations.append("Moderate profit factor - consider improving risk management")
        else:
            recommendations.append("Weak profit factor - review risk management")
        
        # Market-specific recommendations
        crypto_results = [r for r in successful_results if 'USD' in r.get('symbol', '')]
        traditional_results = [r for r in successful_results if r.get('symbol', '') in ['SPY', 'QQQ', 'IWM']]
        
        if crypto_results:
            crypto_returns = [r.get('results', {}).get('total_return', 0) for r in crypto_results]
            if np.mean(crypto_returns) > avg_return:
                recommendations.append("Strategy performs better on crypto markets")
        
        if traditional_results:
            traditional_returns = [r.get('results', {}).get('total_return', 0) for r in traditional_results]
            if np.mean(traditional_returns) > avg_return:
                recommendations.append("Strategy performs better on traditional markets")
        
        return recommendations
    
    def print_analysis(self, analysis: Dict):
        """Print detailed analysis results"""
        if not analysis:
            print("No analysis results available")
            return
        
        print("\n" + "="*80)
        print("STRATEGY ANALYSIS REPORT")
        print("="*80)
        
        # Summary
        summary = analysis.get('summary', {})
        print(f"Total Tests: {summary.get('total_tests', 0)}")
        print(f"Successful Tests: {summary.get('successful_tests', 0)}")
        print(f"Success Rate: {summary.get('success_rate', 0):.2%}")
        print(f"Average Return: {summary.get('avg_return', 0):.4f}")
        
        # Top performers
        top_performers = analysis.get('top_performers', [])
        if top_performers:
            print(f"\nTop {len(top_performers)} Performers:")
            for i, performer in enumerate(top_performers[:5], 1):
                symbol = performer.get('symbol', 'Unknown')
                timeframe = performer.get('timeframe', 'Unknown')
                return_val = performer.get('results', {}).get('total_return', 0)
                print(f"  {i}. {symbol} ({timeframe}): {return_val:.4f}")
        
        # Recommendations
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            print(f"\nRecommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        
        print("="*80)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Pine Script to Python Backtesting Launcher')
    parser.add_argument('--mode', choices=['single', 'comprehensive', 'translate'], 
                       default='comprehensive', help='Backtesting mode')
    parser.add_argument('--symbol', default='BTC-USD', help='Trading symbol for single mode')
    parser.add_argument('--timeframe', default='1d', help='Timeframe for single mode')
    parser.add_argument('--start-date', default='2020-01-01', help='Start date')
    parser.add_argument('--end-date', default='2024-01-01', help='End date')
    parser.add_argument('--workers', type=int, default=4, help='Number of parallel workers')
    parser.add_argument('--pinescript-file', help='Pine Script file to translate')
    parser.add_argument('--output-file', help='Output file for translated code')
    
    args = parser.parse_args()
    
    # Initialize launcher
    launcher = StrategyLauncher()
    
    if args.mode == 'translate':
        if not args.pinescript_file:
            print("Error: --pinescript-file required for translate mode")
            return
        
        print(f"Translating Pine Script file: {args.pinescript_file}")
        launcher.translate_pinescript_strategy(args.pinescript_file, args.output_file)
        
    elif args.mode == 'single':
        print(f"Running single backtest for {args.symbol} {args.timeframe}")
        results = launcher.run_tsa_enhanced_backtest(
            symbol=args.symbol,
            timeframe=args.timeframe,
            start_date=args.start_date,
            end_date=args.end_date
        )
        
        if results:
            print("Single backtest completed successfully")
        else:
            print("Single backtest failed")
            
    elif args.mode == 'comprehensive':
        print("Running comprehensive backtest across all data sources...")
        results = launcher.run_comprehensive_backtest(max_workers=args.workers)
        
        if results:
            # Analyze results
            analysis = launcher.analyze_results(results)
            launcher.print_analysis(analysis)
            print("Comprehensive backtest completed successfully")
        else:
            print("Comprehensive backtest failed")

if __name__ == "__main__":
    main()
