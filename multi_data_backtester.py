"""
Multi-Data Source Backtesting Framework
Comprehensive backtesting system for testing strategies across multiple data sources
"""

import pandas as pd
import numpy as np
import yfinance as yf
import talib
from typing import Dict, List, Tuple, Optional, Any
import warnings
import os
import json
from datetime import datetime, timedelta
import concurrent.futures
from dataclasses import dataclass
import time

warnings.filterwarnings('ignore')

@dataclass
class DataSource:
    """Data source configuration"""
    symbol: str
    timeframe: str
    start_date: str
    end_date: str
    source: str = "yfinance"  # yfinance, alpha_vantage, etc.

class MultiDataBacktester:
    """
    Advanced multi-data source backtesting framework
    Tests strategies across 25+ data sources as mentioned in the transcript
    """
    
    def __init__(self):
        self.data_sources = self._initialize_data_sources()
        self.results = {}
        self.strategy_class = None
        self.strategy_params = {}
        
    def _initialize_data_sources(self) -> List[DataSource]:
        """Initialize comprehensive data sources for testing"""
        
        # Crypto data sources
        crypto_symbols = [
            'BTC-USD', 'ETH-USD', 'BNB-USD', 'ADA-USD', 'SOL-USD',
            'XRP-USD', 'DOT-USD', 'DOGE-USD', 'AVAX-USD', 'MATIC-USD'
        ]
        
        # Traditional market symbols
        traditional_symbols = [
            'SPY', 'QQQ', 'IWM', 'GLD', 'SLV', 'TLT', 'VTI', 'EFA', 'EEM', 'VEA'
        ]
        
        # Forex pairs
        forex_symbols = [
            'EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X'
        ]
        
        # Timeframes to test
        timeframes = ['1m', '5m', '15m', '1h', '4h', '1d']
        
        data_sources = []
        
        # Add crypto sources
        for symbol in crypto_symbols:
            for tf in timeframes:
                data_sources.append(DataSource(
                    symbol=symbol,
                    timeframe=tf,
                    start_date='2020-01-01',
                    end_date='2024-01-01',
                    source='yfinance'
                ))
        
        # Add traditional market sources
        for symbol in traditional_symbols:
            for tf in ['1h', '4h', '1d']:  # Traditional markets don't have 1m data
                data_sources.append(DataSource(
                    symbol=symbol,
                    timeframe=tf,
                    start_date='2020-01-01',
                    end_date='2024-01-01',
                    source='yfinance'
                ))
        
        # Add forex sources
        for symbol in forex_symbols:
            for tf in ['1h', '4h', '1d']:
                data_sources.append(DataSource(
                    symbol=symbol,
                    timeframe=tf,
                    start_date='2020-01-01',
                    end_date='2024-01-01',
                    source='yfinance'
                ))
        
        return data_sources
    
    def load_data(self, data_source: DataSource) -> Optional[pd.DataFrame]:
        """Load data for a specific source"""
        try:
            if data_source.source == 'yfinance':
                ticker = yf.Ticker(data_source.symbol)
                
                # Map timeframes
                interval_map = {
                    '1m': '1m', '5m': '5m', '15m': '15m',
                    '1h': '1h', '4h': '4h', '1d': '1d'
                }
                
                interval = interval_map.get(data_source.timeframe, '1d')
                
                # Download data
                data = ticker.history(
                    start=data_source.start_date,
                    end=data_source.end_date,
                    interval=interval
                )
                
                if data.empty:
                    return None
                
                # Standardize column names
                data.columns = [col.lower() for col in data.columns]
                
                # Ensure we have the required columns
                required_cols = ['open', 'high', 'low', 'close', 'volume']
                if not all(col in data.columns for col in required_cols):
                    return None
                
                # Clean data
                data = data.dropna()
                data = data[data['volume'] > 0]  # Remove zero volume bars
                
                return data
                
        except Exception as e:
            print(f"Error loading data for {data_source.symbol} {data_source.timeframe}: {e}")
            return None
    
    def run_single_backtest(self, data_source: DataSource, strategy_class, strategy_params: Dict) -> Dict:
        """Run backtest on a single data source"""
        try:
            # Load data
            data = self.load_data(data_source)
            if data is None or len(data) < 200:  # Need minimum data for indicators
                return {
                    'symbol': data_source.symbol,
                    'timeframe': data_source.timeframe,
                    'status': 'failed',
                    'error': 'Insufficient data',
                    'results': {}
                }
            
            # Initialize strategy
            strategy = strategy_class(data, **strategy_params)
            
            # Run backtest
            start_time = time.time()
            results = strategy.run_backtest()
            end_time = time.time()
            
            # Add metadata
            results.update({
                'symbol': data_source.symbol,
                'timeframe': data_source.timeframe,
                'status': 'success',
                'execution_time': end_time - start_time,
                'data_points': len(data),
                'start_date': data.index[0].strftime('%Y-%m-%d'),
                'end_date': data.index[-1].strftime('%Y-%m-%d')
            })
            
            return results
            
        except Exception as e:
            return {
                'symbol': data_source.symbol,
                'timeframe': data_source.timeframe,
                'status': 'failed',
                'error': str(e),
                'results': {}
            }
    
    def run_comprehensive_backtest(self, strategy_class, strategy_params: Dict = None, 
                                 max_workers: int = 4) -> Dict:
        """
        Run comprehensive backtest across all data sources
        
        Args:
            strategy_class: Strategy class to test
            strategy_params: Parameters for the strategy
            max_workers: Maximum number of parallel workers
        """
        if strategy_params is None:
            strategy_params = {}
        
        print(f"Starting comprehensive backtest...")
        print(f"Testing {len(self.data_sources)} data sources")
        print(f"Using {max_workers} parallel workers")
        
        all_results = []
        
        # Run backtests in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_source = {
                executor.submit(self.run_single_backtest, source, strategy_class, strategy_params): source
                for source in self.data_sources
            }
            
            # Collect results
            for future in concurrent.futures.as_completed(future_to_source):
                source = future_to_source[future]
                try:
                    result = future.result()
                    all_results.append(result)
                    
                    # Print progress
                    success_count = sum(1 for r in all_results if r['status'] == 'success')
                    total_count = len(all_results)
                    print(f"Progress: {total_count}/{len(self.data_sources)} "
                          f"(Success: {success_count}, Failed: {total_count - success_count})")
                    
                except Exception as e:
                    print(f"Error processing {source.symbol} {source.timeframe}: {e}")
                    all_results.append({
                        'symbol': source.symbol,
                        'timeframe': source.timeframe,
                        'status': 'failed',
                        'error': str(e),
                        'results': {}
                    })
        
        # Organize results
        self.results = {
            'all_results': all_results,
            'successful_results': [r for r in all_results if r['status'] == 'success'],
            'failed_results': [r for r in all_results if r['status'] == 'failed'],
            'summary': self._calculate_summary(all_results)
        }
        
        return self.results
    
    def _calculate_summary(self, results: List[Dict]) -> Dict:
        """Calculate summary statistics"""
        successful = [r for r in results if r['status'] == 'success']
        
        if not successful:
            return {
                'total_tests': len(results),
                'successful_tests': 0,
                'success_rate': 0,
                'avg_return': 0,
                'best_performer': None,
                'worst_performer': None
            }
        
        # Calculate metrics
        returns = [r['results'].get('total_return', 0) for r in successful if 'total_return' in r['results']]
        win_rates = [r['results'].get('win_rate', 0) for r in successful if 'win_rate' in r['results']]
        profit_factors = [r['results'].get('profit_factor', 0) for r in successful if 'profit_factor' in r['results']]
        
        # Find best and worst performers
        best_idx = np.argmax(returns) if returns else 0
        worst_idx = np.argmin(returns) if returns else 0
        
        return {
            'total_tests': len(results),
            'successful_tests': len(successful),
            'success_rate': len(successful) / len(results),
            'avg_return': np.mean(returns) if returns else 0,
            'median_return': np.median(returns) if returns else 0,
            'avg_win_rate': np.mean(win_rates) if win_rates else 0,
            'avg_profit_factor': np.mean(profit_factors) if profit_factors else 0,
            'best_performer': {
                'symbol': successful[best_idx]['symbol'],
                'timeframe': successful[best_idx]['timeframe'],
                'return': returns[best_idx] if returns else 0
            },
            'worst_performer': {
                'symbol': successful[worst_idx]['symbol'],
                'timeframe': successful[worst_idx]['timeframe'],
                'return': returns[worst_idx] if returns else 0
            }
        }
    
    def save_results(self, filename: str = None):
        """Save results to CSV and JSON files"""
        if not self.results:
            print("No results to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if filename is None:
            filename = f"backtest_results_{timestamp}"
        
        # Save detailed results as JSON
        json_filename = f"{filename}.json"
        with open(json_filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Save successful results as CSV
        if self.results['successful_results']:
            csv_data = []
            for result in self.results['successful_results']:
                row = {
                    'symbol': result['symbol'],
                    'timeframe': result['timeframe'],
                    'status': result['status'],
                    'execution_time': result.get('execution_time', 0),
                    'data_points': result.get('data_points', 0),
                    'start_date': result.get('start_date', ''),
                    'end_date': result.get('end_date', '')
                }
                row.update(result.get('results', {}))
                csv_data.append(row)
            
            df = pd.DataFrame(csv_data)
            csv_filename = f"{filename}.csv"
            df.to_csv(csv_filename, index=False)
            print(f"Results saved to {json_filename} and {csv_filename}")
        
        return json_filename
    
    def print_summary(self):
        """Print comprehensive summary of results"""
        if not self.results:
            print("No results available")
            return
        
        summary = self.results['summary']
        
        print("\n" + "="*80)
        print("COMPREHENSIVE BACKTEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Successful Tests: {summary['successful_tests']}")
        print(f"Success Rate: {summary['success_rate']:.2%}")
        print(f"Average Return: {summary['avg_return']:.4f}")
        print(f"Median Return: {summary['median_return']:.4f}")
        print(f"Average Win Rate: {summary['avg_win_rate']:.2%}")
        print(f"Average Profit Factor: {summary['avg_profit_factor']:.2f}")
        
        if summary['best_performer']:
            print(f"\nBest Performer:")
            print(f"  Symbol: {summary['best_performer']['symbol']}")
            print(f"  Timeframe: {summary['best_performer']['timeframe']}")
            print(f"  Return: {summary['best_performer']['return']:.4f}")
        
        if summary['worst_performer']:
            print(f"\nWorst Performer:")
            print(f"  Symbol: {summary['worst_performer']['symbol']}")
            print(f"  Timeframe: {summary['worst_performer']['timeframe']}")
            print(f"  Return: {summary['worst_performer']['return']:.4f}")
        
        print("="*80)
    
    def get_top_performers(self, n: int = 10) -> List[Dict]:
        """Get top N performing strategies"""
        if not self.results or not self.results['successful_results']:
            return []
        
        successful = self.results['successful_results']
        
        # Sort by total return
        sorted_results = sorted(
            successful,
            key=lambda x: x.get('results', {}).get('total_return', 0),
            reverse=True
        )
        
        return sorted_results[:n]
    
    def get_strategy_analysis(self) -> Dict:
        """Get detailed strategy analysis"""
        if not self.results or not self.results['successful_results']:
            return {}
        
        successful = self.results['successful_results']
        
        # Collect all metrics
        all_returns = []
        all_win_rates = []
        all_profit_factors = []
        all_sharpe_ratios = []
        all_max_drawdowns = []
        
        for result in successful:
            results = result.get('results', {})
            all_returns.append(results.get('total_return', 0))
            all_win_rates.append(results.get('win_rate', 0))
            all_profit_factors.append(results.get('profit_factor', 0))
            all_sharpe_ratios.append(results.get('sharpe_ratio', 0))
            all_max_drawdowns.append(results.get('max_drawdown', 0))
        
        return {
            'returns_stats': {
                'mean': np.mean(all_returns),
                'std': np.std(all_returns),
                'min': np.min(all_returns),
                'max': np.max(all_returns),
                'median': np.median(all_returns)
            },
            'win_rate_stats': {
                'mean': np.mean(all_win_rates),
                'std': np.std(all_win_rates),
                'min': np.min(all_win_rates),
                'max': np.max(all_win_rates),
                'median': np.median(all_win_rates)
            },
            'profit_factor_stats': {
                'mean': np.mean(all_profit_factors),
                'std': np.std(all_profit_factors),
                'min': np.min(all_profit_factors),
                'max': np.max(all_profit_factors),
                'median': np.median(all_profit_factors)
            },
            'sharpe_ratio_stats': {
                'mean': np.mean(all_sharpe_ratios),
                'std': np.std(all_sharpe_ratios),
                'min': np.min(all_sharpe_ratios),
                'max': np.max(all_sharpe_ratios),
                'median': np.median(all_sharpe_ratios)
            },
            'max_drawdown_stats': {
                'mean': np.mean(all_max_drawdowns),
                'std': np.std(all_max_drawdowns),
                'min': np.min(all_max_drawdowns),
                'max': np.max(all_max_drawdowns),
                'median': np.median(all_max_drawdowns)
            }
        }
