"""
Results Analyzer - Advanced analysis and reporting for backtesting results
Comprehensive analysis system for strategy performance evaluation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ResultsAnalyzer:
    """
    Advanced results analyzer for backtesting results
    Provides comprehensive analysis and visualization
    """
    
    def __init__(self):
        self.results = None
        self.analysis = {}
        
    def load_results(self, results_file: str):
        """Load results from JSON file"""
        try:
            with open(results_file, 'r') as f:
                self.results = json.load(f)
            print(f"Loaded results from {results_file}")
            return True
        except Exception as e:
            print(f"Error loading results: {e}")
            return False
    
    def analyze_performance(self) -> Dict:
        """Analyze strategy performance across all data sources"""
        if not self.results:
            return {}
        
        successful = self.results.get('successful_results', [])
        if not successful:
            return {}
        
        # Extract metrics
        metrics = self._extract_metrics(successful)
        
        # Calculate performance statistics
        performance_stats = self._calculate_performance_stats(metrics)
        
        # Market analysis
        market_analysis = self._analyze_by_market(successful)
        
        # Timeframe analysis
        timeframe_analysis = self._analyze_by_timeframe(successful)
        
        # Risk analysis
        risk_analysis = self._analyze_risk_metrics(metrics)
        
        self.analysis = {
            'performance_stats': performance_stats,
            'market_analysis': market_analysis,
            'timeframe_analysis': timeframe_analysis,
            'risk_analysis': risk_analysis,
            'top_performers': self._get_top_performers(successful, 10),
            'worst_performers': self._get_worst_performers(successful, 10)
        }
        
        return self.analysis
    
    def _extract_metrics(self, results: List[Dict]) -> Dict:
        """Extract metrics from results"""
        metrics = {
            'returns': [],
            'win_rates': [],
            'profit_factors': [],
            'sharpe_ratios': [],
            'max_drawdowns': [],
            'total_trades': [],
            'avg_trades': [],
            'symbols': [],
            'timeframes': []
        }
        
        for result in results:
            results_data = result.get('results', {})
            metrics['returns'].append(results_data.get('total_return', 0))
            metrics['win_rates'].append(results_data.get('win_rate', 0))
            metrics['profit_factors'].append(results_data.get('profit_factor', 0))
            metrics['sharpe_ratios'].append(results_data.get('sharpe_ratio', 0))
            metrics['max_drawdowns'].append(results_data.get('max_drawdown', 0))
            metrics['total_trades'].append(results_data.get('total_trades', 0))
            metrics['avg_trades'].append(results_data.get('avg_trade', 0))
            metrics['symbols'].append(result.get('symbol', ''))
            metrics['timeframes'].append(result.get('timeframe', ''))
        
        return metrics
    
    def _calculate_performance_stats(self, metrics: Dict) -> Dict:
        """Calculate performance statistics"""
        returns = np.array(metrics['returns'])
        win_rates = np.array(metrics['win_rates'])
        profit_factors = np.array(metrics['profit_factors'])
        sharpe_ratios = np.array(metrics['sharpe_ratios'])
        max_drawdowns = np.array(metrics['max_drawdowns'])
        
        return {
            'returns': {
                'mean': np.mean(returns),
                'std': np.std(returns),
                'min': np.min(returns),
                'max': np.max(returns),
                'median': np.median(returns),
                'q25': np.percentile(returns, 25),
                'q75': np.percentile(returns, 75)
            },
            'win_rates': {
                'mean': np.mean(win_rates),
                'std': np.std(win_rates),
                'min': np.min(win_rates),
                'max': np.max(win_rates),
                'median': np.median(win_rates)
            },
            'profit_factors': {
                'mean': np.mean(profit_factors),
                'std': np.std(profit_factors),
                'min': np.min(profit_factors),
                'max': np.max(profit_factors),
                'median': np.median(profit_factors)
            },
            'sharpe_ratios': {
                'mean': np.mean(sharpe_ratios),
                'std': np.std(sharpe_ratios),
                'min': np.min(sharpe_ratios),
                'max': np.max(sharpe_ratios),
                'median': np.median(sharpe_ratios)
            },
            'max_drawdowns': {
                'mean': np.mean(max_drawdowns),
                'std': np.std(max_drawdowns),
                'min': np.min(max_drawdowns),
                'max': np.max(max_drawdowns),
                'median': np.median(max_drawdowns)
            }
        }
    
    def _analyze_by_market(self, results: List[Dict]) -> Dict:
        """Analyze performance by market type"""
        crypto_results = []
        traditional_results = []
        forex_results = []
        
        for result in results:
            symbol = result.get('symbol', '')
            if 'USD' in symbol and symbol not in ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X']:
                crypto_results.append(result)
            elif symbol in ['SPY', 'QQQ', 'IWM', 'GLD', 'SLV', 'TLT', 'VTI', 'EFA', 'EEM', 'VEA']:
                traditional_results.append(result)
            elif 'USD' in symbol or 'EUR' in symbol or 'GBP' in symbol or 'JPY' in symbol:
                forex_results.append(result)
        
        market_analysis = {}
        
        if crypto_results:
            crypto_returns = [r.get('results', {}).get('total_return', 0) for r in crypto_results]
            market_analysis['crypto'] = {
                'count': len(crypto_results),
                'avg_return': np.mean(crypto_returns),
                'median_return': np.median(crypto_returns),
                'win_rate': np.mean([r.get('results', {}).get('win_rate', 0) for r in crypto_results])
            }
        
        if traditional_results:
            traditional_returns = [r.get('results', {}).get('total_return', 0) for r in traditional_results]
            market_analysis['traditional'] = {
                'count': len(traditional_results),
                'avg_return': np.mean(traditional_returns),
                'median_return': np.median(traditional_returns),
                'win_rate': np.mean([r.get('results', {}).get('win_rate', 0) for r in traditional_results])
            }
        
        if forex_results:
            forex_returns = [r.get('results', {}).get('total_return', 0) for r in forex_results]
            market_analysis['forex'] = {
                'count': len(forex_results),
                'avg_return': np.mean(forex_returns),
                'median_return': np.median(forex_returns),
                'win_rate': np.mean([r.get('results', {}).get('win_rate', 0) for r in forex_results])
            }
        
        return market_analysis
    
    def _analyze_by_timeframe(self, results: List[Dict]) -> Dict:
        """Analyze performance by timeframe"""
        timeframe_groups = {}
        
        for result in results:
            timeframe = result.get('timeframe', '')
            if timeframe not in timeframe_groups:
                timeframe_groups[timeframe] = []
            timeframe_groups[timeframe].append(result)
        
        timeframe_analysis = {}
        
        for timeframe, group_results in timeframe_groups.items():
            returns = [r.get('results', {}).get('total_return', 0) for r in group_results]
            win_rates = [r.get('results', {}).get('win_rate', 0) for r in group_results]
            
            timeframe_analysis[timeframe] = {
                'count': len(group_results),
                'avg_return': np.mean(returns),
                'median_return': np.median(returns),
                'win_rate': np.mean(win_rates),
                'std_return': np.std(returns)
            }
        
        return timeframe_analysis
    
    def _analyze_risk_metrics(self, metrics: Dict) -> Dict:
        """Analyze risk metrics"""
        returns = np.array(metrics['returns'])
        max_drawdowns = np.array(metrics['max_drawdowns'])
        sharpe_ratios = np.array(metrics['sharpe_ratios'])
        
        # Calculate risk-adjusted returns
        risk_adjusted_returns = returns / (max_drawdowns + 1e-8)  # Avoid division by zero
        
        return {
            'volatility': np.std(returns),
            'max_drawdown_avg': np.mean(max_drawdowns),
            'max_drawdown_max': np.max(max_drawdowns),
            'sharpe_ratio_avg': np.mean(sharpe_ratios),
            'risk_adjusted_return_avg': np.mean(risk_adjusted_returns),
            'downside_deviation': np.std(returns[returns < 0]) if np.any(returns < 0) else 0,
            'sortino_ratio': np.mean(returns) / (np.std(returns[returns < 0]) + 1e-8) if np.any(returns < 0) else 0
        }
    
    def _get_top_performers(self, results: List[Dict], n: int = 10) -> List[Dict]:
        """Get top N performers"""
        sorted_results = sorted(
            results,
            key=lambda x: x.get('results', {}).get('total_return', 0),
            reverse=True
        )
        return sorted_results[:n]
    
    def _get_worst_performers(self, results: List[Dict], n: int = 10) -> List[Dict]:
        """Get worst N performers"""
        sorted_results = sorted(
            results,
            key=lambda x: x.get('results', {}).get('total_return', 0)
        )
        return sorted_results[:n]
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate comprehensive analysis report"""
        if not self.analysis:
            self.analyze_performance()
        
        if not self.analysis:
            return "No analysis available"
        
        # Generate report
        report = self._create_report()
        
        # Save report
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to {output_file}")
        
        return report
    
    def _create_report(self) -> str:
        """Create comprehensive analysis report"""
        report = []
        
        # Header
        report.append("="*80)
        report.append("COMPREHENSIVE STRATEGY ANALYSIS REPORT")
        report.append("="*80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        if 'performance_stats' in self.analysis:
            stats = self.analysis['performance_stats']
            report.append("PERFORMANCE SUMMARY")
            report.append("-" * 40)
            report.append(f"Average Return: {stats['returns']['mean']:.4f}")
            report.append(f"Median Return: {stats['returns']['median']:.4f}")
            report.append(f"Return Std Dev: {stats['returns']['std']:.4f}")
            report.append(f"Best Return: {stats['returns']['max']:.4f}")
            report.append(f"Worst Return: {stats['returns']['min']:.4f}")
            report.append("")
        
        # Market Analysis
        if 'market_analysis' in self.analysis:
            report.append("MARKET ANALYSIS")
            report.append("-" * 40)
            for market, data in self.analysis['market_analysis'].items():
                report.append(f"{market.upper()} MARKETS:")
                report.append(f"  Count: {data['count']}")
                report.append(f"  Average Return: {data['avg_return']:.4f}")
                report.append(f"  Win Rate: {data['win_rate']:.2%}")
                report.append("")
        
        # Timeframe Analysis
        if 'timeframe_analysis' in self.analysis:
            report.append("TIMEFRAME ANALYSIS")
            report.append("-" * 40)
            for timeframe, data in self.analysis['timeframe_analysis'].items():
                report.append(f"{timeframe.upper()} TIMEFRAME:")
                report.append(f"  Count: {data['count']}")
                report.append(f"  Average Return: {data['avg_return']:.4f}")
                report.append(f"  Win Rate: {data['win_rate']:.2%}")
                report.append("")
        
        # Top Performers
        if 'top_performers' in self.analysis:
            report.append("TOP PERFORMERS")
            report.append("-" * 40)
            for i, performer in enumerate(self.analysis['top_performers'][:5], 1):
                symbol = performer.get('symbol', 'Unknown')
                timeframe = performer.get('timeframe', 'Unknown')
                return_val = performer.get('results', {}).get('total_return', 0)
                win_rate = performer.get('results', {}).get('win_rate', 0)
                report.append(f"{i}. {symbol} ({timeframe}): {return_val:.4f} (WR: {win_rate:.2%})")
            report.append("")
        
        # Risk Analysis
        if 'risk_analysis' in self.analysis:
            risk = self.analysis['risk_analysis']
            report.append("RISK ANALYSIS")
            report.append("-" * 40)
            report.append(f"Volatility: {risk['volatility']:.4f}")
            report.append(f"Average Max Drawdown: {risk['max_drawdown_avg']:.4f}")
            report.append(f"Worst Max Drawdown: {risk['max_drawdown_max']:.4f}")
            report.append(f"Average Sharpe Ratio: {risk['sharpe_ratio_avg']:.4f}")
            report.append(f"Sortino Ratio: {risk['sortino_ratio']:.4f}")
            report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 40)
        recommendations = self._generate_recommendations()
        for i, rec in enumerate(recommendations, 1):
            report.append(f"{i}. {rec}")
        
        report.append("="*80)
        
        return "\n".join(report)
    
    def _generate_recommendations(self) -> List[str]:
        """Generate trading recommendations"""
        recommendations = []
        
        if not self.analysis:
            return ["No analysis available for recommendations"]
        
        # Performance-based recommendations
        if 'performance_stats' in self.analysis:
            stats = self.analysis['performance_stats']
            avg_return = stats['returns']['mean']
            win_rate = stats['win_rates']['mean']
            profit_factor = stats['profit_factors']['mean']
            
            if avg_return > 0.2:
                recommendations.append("Strong positive returns - consider live trading")
            elif avg_return > 0.1:
                recommendations.append("Moderate returns - monitor closely before live trading")
            elif avg_return > 0:
                recommendations.append("Weak positive returns - optimize before live trading")
            else:
                recommendations.append("Negative returns - significant optimization needed")
            
            if win_rate > 0.6:
                recommendations.append("High win rate indicates good entry/exit logic")
            elif win_rate > 0.5:
                recommendations.append("Moderate win rate - consider improving entry conditions")
            else:
                recommendations.append("Low win rate - review entry/exit logic")
            
            if profit_factor > 2.0:
                recommendations.append("Strong profit factor - good risk/reward ratio")
            elif profit_factor > 1.5:
                recommendations.append("Moderate profit factor - consider improving risk management")
            else:
                recommendations.append("Weak profit factor - review risk management")
        
        # Market-specific recommendations
        if 'market_analysis' in self.analysis:
            market_analysis = self.analysis['market_analysis']
            
            if 'crypto' in market_analysis and 'traditional' in market_analysis:
                crypto_return = market_analysis['crypto']['avg_return']
                traditional_return = market_analysis['traditional']['avg_return']
                
                if crypto_return > traditional_return:
                    recommendations.append("Strategy performs better on crypto markets")
                elif traditional_return > crypto_return:
                    recommendations.append("Strategy performs better on traditional markets")
        
        # Timeframe recommendations
        if 'timeframe_analysis' in self.analysis:
            timeframe_analysis = self.analysis['timeframe_analysis']
            
            # Find best timeframe
            best_timeframe = max(
                timeframe_analysis.items(),
                key=lambda x: x[1]['avg_return']
            )
            
            recommendations.append(f"Best performing timeframe: {best_timeframe[0]} "
                               f"(Return: {best_timeframe[1]['avg_return']:.4f})")
        
        return recommendations
    
    def create_visualizations(self, output_dir: str = "charts"):
        """Create visualization charts"""
        if not self.analysis:
            self.analyze_performance()
        
        if not self.analysis:
            print("No analysis available for visualization")
            return
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8')
        
        # 1. Returns distribution
        self._plot_returns_distribution(output_dir)
        
        # 2. Market comparison
        self._plot_market_comparison(output_dir)
        
        # 3. Timeframe comparison
        self._plot_timeframe_comparison(output_dir)
        
        # 4. Risk-return scatter
        self._plot_risk_return_scatter(output_dir)
        
        # 5. Performance heatmap
        self._plot_performance_heatmap(output_dir)
        
        print(f"Visualizations saved to {output_dir}/")
    
    def _plot_returns_distribution(self, output_dir: str):
        """Plot returns distribution"""
        if 'performance_stats' not in self.analysis:
            return
        
        # This would need the actual returns data
        # For now, create a placeholder
        plt.figure(figsize=(10, 6))
        plt.title("Returns Distribution")
        plt.xlabel("Return")
        plt.ylabel("Frequency")
        plt.savefig(f"{output_dir}/returns_distribution.png")
        plt.close()
    
    def _plot_market_comparison(self, output_dir: str):
        """Plot market comparison"""
        if 'market_analysis' not in self.analysis:
            return
        
        markets = list(self.analysis['market_analysis'].keys())
        returns = [self.analysis['market_analysis'][m]['avg_return'] for m in markets]
        
        plt.figure(figsize=(10, 6))
        plt.bar(markets, returns)
        plt.title("Average Returns by Market Type")
        plt.xlabel("Market Type")
        plt.ylabel("Average Return")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/market_comparison.png")
        plt.close()
    
    def _plot_timeframe_comparison(self, output_dir: str):
        """Plot timeframe comparison"""
        if 'timeframe_analysis' not in self.analysis:
            return
        
        timeframes = list(self.analysis['timeframe_analysis'].keys())
        returns = [self.analysis['timeframe_analysis'][t]['avg_return'] for t in timeframes]
        
        plt.figure(figsize=(12, 6))
        plt.bar(timeframes, returns)
        plt.title("Average Returns by Timeframe")
        plt.xlabel("Timeframe")
        plt.ylabel("Average Return")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/timeframe_comparison.png")
        plt.close()
    
    def _plot_risk_return_scatter(self, output_dir: str):
        """Plot risk-return scatter plot"""
        # Placeholder for risk-return scatter plot
        plt.figure(figsize=(10, 6))
        plt.title("Risk-Return Scatter Plot")
        plt.xlabel("Risk (Max Drawdown)")
        plt.ylabel("Return")
        plt.savefig(f"{output_dir}/risk_return_scatter.png")
        plt.close()
    
    def _plot_performance_heatmap(self, output_dir: str):
        """Plot performance heatmap"""
        # Placeholder for performance heatmap
        plt.figure(figsize=(12, 8))
        plt.title("Performance Heatmap")
        plt.savefig(f"{output_dir}/performance_heatmap.png")
        plt.close()
