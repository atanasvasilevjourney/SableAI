"""
BTA-Lib Enhanced Launcher for Pine Script to Python Backtesting Framework
Command-line interface for BTA-Lib enhanced backtesting
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any
from decimal import Decimal

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bta_integration import BTALauncher
from domain_models import (
    Strategy, StrategyParameters, MarketData, Money, Price, Quantity,
    Timeframe, StrategyType, Percentage
)

def main():
    """Main CLI interface for BTA-Lib enhanced backtesting"""
    parser = argparse.ArgumentParser(
        description="BTA-Lib enhanced backtesting with comprehensive technical analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run BTA-Lib demo
  python bta_launcher.py --mode demo
  
  # Run enhanced backtest
  python bta_launcher.py --mode backtest --strategy tsa_enhanced --symbol BTC-USD
  
  # Analyze market conditions
  python bta_launcher.py --mode analyze --symbol AAPL
  
  # Run multi-strategy backtest
  python bta_launcher.py --mode multi --strategies tsa_enhanced,rsi,macd --symbol ETH-USD
        """
    )
    
    # Mode selection
    parser.add_argument(
        '--mode',
        choices=['demo', 'backtest', 'analyze', 'multi', 'compare'],
        default='demo',
        help='Mode to run (default: demo)'
    )
    
    # Strategy selection
    parser.add_argument(
        '--strategy',
        type=str,
        default='tsa_enhanced',
        choices=['tsa_enhanced', 'rsi', 'macd', 'bollinger_bands', 'stochastic'],
        help='Strategy to use (default: tsa_enhanced)'
    )
    
    parser.add_argument(
        '--strategies',
        type=str,
        help='Comma-separated list of strategies for multi-mode'
    )
    
    # Trading parameters
    parser.add_argument(
        '--symbol',
        type=str,
        default='BTC-USD',
        help='Trading symbol (default: BTC-USD)'
    )
    
    parser.add_argument(
        '--timeframe',
        type=str,
        default='1d',
        choices=['1m', '5m', '15m', '1h', '4h', '1d', '1w'],
        help='Data timeframe (default: 1d)'
    )
    
    parser.add_argument(
        '--start-date',
        type=str,
        default='2020-01-01',
        help='Start date for backtesting (default: 2020-01-01)'
    )
    
    parser.add_argument(
        '--end-date',
        type=str,
        default='2024-01-01',
        help='End date for backtesting (default: 2024-01-01)'
    )
    
    parser.add_argument(
        '--initial-capital',
        type=float,
        default=10000.0,
        help='Initial capital for backtesting (default: 10000.0)'
    )
    
    # Strategy parameters
    parser.add_argument(
        '--atr-length',
        type=int,
        default=14,
        help='ATR length (default: 14)'
    )
    
    parser.add_argument(
        '--atr-multiplier',
        type=float,
        default=3.0,
        help='ATR multiplier (default: 3.0)'
    )
    
    parser.add_argument(
        '--adx-length',
        type=int,
        default=14,
        help='ADX length (default: 14)'
    )
    
    parser.add_argument(
        '--adx-threshold',
        type=float,
        default=25.0,
        help='ADX threshold (default: 25.0)'
    )
    
    # Output options
    parser.add_argument(
        '--output-file',
        type=str,
        help='Output file for results'
    )
    
    parser.add_argument(
        '--save-results',
        action='store_true',
        help='Save results to file'
    )
    
    args = parser.parse_args()
    
    # Initialize BTA launcher
    launcher = BTALauncher()
    
    # Check availability
    if not launcher.check_availability():
        print("❌ BTA-Lib integration not available. Please install BTA-Lib.")
        return
    
    print("🚀 BTA-Lib Enhanced Backtesting")
    print("="*50)
    
    # Run based on mode
    if args.mode == 'demo':
        run_demo_mode(launcher)
    elif args.mode == 'backtest':
        run_backtest_mode(launcher, args)
    elif args.mode == 'analyze':
        run_analyze_mode(launcher, args)
    elif args.mode == 'multi':
        run_multi_mode(launcher, args)
    elif args.mode == 'compare':
        run_compare_mode(launcher, args)
    else:
        print(f"❌ Unknown mode: {args.mode}")
        return

def run_demo_mode(launcher: BTALauncher):
    """Run demo mode with example strategies"""
    print("🎯 Demo Mode - BTA-Lib Enhanced Backtesting")
    print("="*50)
    
    # Create demo strategies
    demo_strategies = [
        create_tsa_enhanced_strategy(),
        create_rsi_strategy(),
        create_macd_strategy()
    ]
    
    # Create demo market data
    demo_market_data = create_demo_market_data()
    
    print(f"📊 Running {len(demo_strategies)} demo strategies...")
    
    # Run multi-strategy backtest
    results = launcher.run_multi_strategy_backtest(
        demo_strategies, 
        demo_market_data,
        Money(Decimal('10000'), "USD")
    )
    
    if results:
        print(f"🎉 Demo completed! {len(results)} strategies tested")
    
    # Analyze market conditions
    print("\n📈 Analyzing market conditions...")
    analysis = launcher.analyze_market_conditions(demo_market_data)
    
    if analysis:
        print("✅ Market analysis completed!")

def run_backtest_mode(launcher: BTALauncher, args):
    """Run single strategy backtest mode"""
    print("🚀 BTA-Lib Enhanced Backtest Mode")
    print("="*50)
    print(f"Strategy: {args.strategy}")
    print(f"Symbol: {args.symbol}")
    print(f"Timeframe: {args.timeframe}")
    print(f"Date Range: {args.start_date} to {args.end_date}")
    
    # Create strategy
    strategy = create_strategy_from_args(args)
    
    # Create market data
    market_data = create_market_data_from_args(args)
    
    # Run backtest
    result = launcher.run_enhanced_backtest(
        strategy, 
        market_data,
        Money(Decimal(str(args.initial_capital)), "USD")
    )
    
    if result:
        print("✅ BTA-Lib enhanced backtest completed successfully!")
        
        if args.save_results:
            save_results_to_file(result, args.output_file)
    else:
        print("❌ BTA-Lib enhanced backtest failed")

def run_analyze_mode(launcher: BTALauncher, args):
    """Run market analysis mode"""
    print("📊 BTA-Lib Market Analysis Mode")
    print("="*50)
    print(f"Symbol: {args.symbol}")
    print(f"Timeframe: {args.timeframe}")
    print(f"Date Range: {args.start_date} to {args.end_date}")
    
    # Create market data
    market_data = create_market_data_from_args(args)
    
    # Analyze market conditions
    analysis = launcher.analyze_market_conditions(market_data)
    
    if analysis:
        print("✅ Market analysis completed successfully!")
        
        if args.save_results:
            save_analysis_to_file(analysis, args.output_file)
    else:
        print("❌ Market analysis failed")

def run_multi_mode(launcher: BTALauncher, args):
    """Run multi-strategy backtest mode"""
    if not args.strategies:
        print("❌ Strategies required for multi-mode")
        print("   Use --strategies tsa_enhanced,rsi,macd")
        return
    
    print("🔄 BTA-Lib Multi-Strategy Backtest Mode")
    print("="*50)
    print(f"Strategies: {args.strategies}")
    print(f"Symbol: {args.symbol}")
    print(f"Timeframe: {args.timeframe}")
    
    # Parse strategies
    strategy_names = [s.strip() for s in args.strategies.split(',')]
    
    # Create strategies
    strategies = []
    for strategy_name in strategy_names:
        strategy = create_strategy_by_name(strategy_name, args)
        if strategy:
            strategies.append(strategy)
    
    if not strategies:
        print("❌ No valid strategies created")
        return
    
    # Create market data
    market_data = create_market_data_from_args(args)
    
    # Run multi-strategy backtest
    results = launcher.run_multi_strategy_backtest(
        strategies, 
        market_data,
        Money(Decimal(str(args.initial_capital)), "USD")
    )
    
    if results:
        print(f"✅ Multi-strategy backtest completed: {len(results)} strategies")
        
        if args.save_results:
            save_multi_results_to_file(results, args.output_file)
    else:
        print("❌ Multi-strategy backtest failed")

def run_compare_mode(launcher: BTALauncher, args):
    """Run strategy comparison mode"""
    print("⚖️ BTA-Lib Strategy Comparison Mode")
    print("="*50)
    print(f"Symbol: {args.symbol}")
    print(f"Timeframe: {args.timeframe}")
    
    # Create comparison strategies
    comparison_strategies = [
        create_tsa_enhanced_strategy(),
        create_rsi_strategy(),
        create_macd_strategy(),
        create_bollinger_bands_strategy()
    ]
    
    # Create market data
    market_data = create_market_data_from_args(args)
    
    # Run comparison
    results = launcher.run_multi_strategy_backtest(
        comparison_strategies, 
        market_data,
        Money(Decimal(str(args.initial_capital)), "USD")
    )
    
    if results:
        print("✅ Strategy comparison completed!")
        
        # Rank strategies
        ranked_strategies = rank_strategies(results)
        print_ranked_strategies(ranked_strategies)
        
        if args.save_results:
            save_comparison_to_file(results, ranked_strategies, args.output_file)
    else:
        print("❌ Strategy comparison failed")

def create_strategy_from_args(args) -> Strategy:
    """Create strategy from command line arguments"""
    return create_strategy_by_name(args.strategy, args)

def create_strategy_by_name(strategy_name: str, args) -> Strategy:
    """Create strategy by name"""
    parameters = StrategyParameters(
        atr_length=args.atr_length,
        atr_multiplier=Decimal(str(args.atr_multiplier)),
        adx_length=args.adx_length,
        adx_threshold=Decimal(str(args.adx_threshold))
    )
    
    if strategy_name == 'tsa_enhanced':
        return create_tsa_enhanced_strategy(parameters)
    elif strategy_name == 'rsi':
        return create_rsi_strategy(parameters)
    elif strategy_name == 'macd':
        return create_macd_strategy(parameters)
    elif strategy_name == 'bollinger_bands':
        return create_bollinger_bands_strategy(parameters)
    elif strategy_name == 'stochastic':
        return create_stochastic_strategy(parameters)
    else:
        return None

def create_tsa_enhanced_strategy(parameters: StrategyParameters = None) -> Strategy:
    """Create TSA Enhanced Strategy"""
    if parameters is None:
        parameters = StrategyParameters()
    
    return Strategy(
        name="TSA Enhanced Strategy",
        strategy_type=StrategyType.MOMENTUM,
        parameters=parameters,
        description="TSA Enhanced Strategy with ATR and ADX filters using BTA-Lib"
    )

def create_rsi_strategy(parameters: StrategyParameters = None) -> Strategy:
    """Create RSI Strategy"""
    if parameters is None:
        parameters = StrategyParameters()
    
    return Strategy(
        name="RSI Strategy",
        strategy_type=StrategyType.MEAN_REVERSION,
        parameters=parameters,
        description="RSI mean reversion strategy using BTA-Lib"
    )

def create_macd_strategy(parameters: StrategyParameters = None) -> Strategy:
    """Create MACD Strategy"""
    if parameters is None:
        parameters = StrategyParameters()
    
    return Strategy(
        name="MACD Strategy",
        strategy_type=StrategyType.MOMENTUM,
        parameters=parameters,
        description="MACD momentum strategy using BTA-Lib"
    )

def create_bollinger_bands_strategy(parameters: StrategyParameters = None) -> Strategy:
    """Create Bollinger Bands Strategy"""
    if parameters is None:
        parameters = StrategyParameters()
    
    return Strategy(
        name="Bollinger Bands Strategy",
        strategy_type=StrategyType.MEAN_REVERSION,
        parameters=parameters,
        description="Bollinger Bands mean reversion strategy using BTA-Lib"
    )

def create_stochastic_strategy(parameters: StrategyParameters = None) -> Strategy:
    """Create Stochastic Strategy"""
    if parameters is None:
        parameters = StrategyParameters()
    
    return Strategy(
        name="Stochastic Strategy",
        strategy_type=StrategyType.MEAN_REVERSION,
        parameters=parameters,
        description="Stochastic oscillator strategy using BTA-Lib"
    )

def create_market_data_from_args(args) -> MarketData:
    """Create market data from command line arguments"""
    # This would contain actual data loading logic
    # For now, create demo data
    return create_demo_market_data()

def create_demo_market_data() -> MarketData:
    """Create demo market data"""
    # Generate sample OHLCV data
    import random
    from datetime import datetime, timedelta
    
    data = []
    base_price = 100.0
    current_price = base_price
    
    for i in range(100):
        # Generate realistic price movement
        change = random.uniform(-0.02, 0.02)  # ±2% change
        current_price *= (1 + change)
        
        # Generate OHLCV
        open_price = current_price * random.uniform(0.99, 1.01)
        high_price = max(open_price, current_price) * random.uniform(1.0, 1.02)
        low_price = min(open_price, current_price) * random.uniform(0.98, 1.0)
        close_price = current_price
        volume = random.randint(1000, 10000)
        
        data.append({
            'timestamp': (datetime.now() - timedelta(days=100-i)).isoformat(),
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume
        })
    
    return MarketData(
        symbol="BTC-USD",
        timeframe=Timeframe("1d"),
        data=data,
        start_date=datetime.now() - timedelta(days=100),
        end_date=datetime.now()
    )

def rank_strategies(results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Rank strategies by performance"""
    ranked = []
    
    for strategy_name, result in results.items():
        score = (
            result.total_return.value * 0.4 +
            result.win_rate.value * 0.3 +
            float(result.profit_factor) * 10 * 0.2 +
            (100 - result.max_drawdown.value) * 0.1
        )
        
        ranked.append({
            'strategy_name': strategy_name,
            'score': float(score),
            'total_return': float(result.total_return.value),
            'win_rate': float(result.win_rate.value),
            'profit_factor': float(result.profit_factor),
            'max_drawdown': float(result.max_drawdown.value),
            'total_trades': result.total_trades
        })
    
    return sorted(ranked, key=lambda x: x['score'], reverse=True)

def print_ranked_strategies(ranked_strategies: List[Dict[str, Any]]):
    """Print ranked strategies"""
    print("\n" + "="*80)
    print("STRATEGY RANKING")
    print("="*80)
    
    for i, strategy in enumerate(ranked_strategies, 1):
        print(f"{i}. {strategy['strategy_name']}")
        print(f"   Score: {strategy['score']:.2f}")
        print(f"   Total Return: {strategy['total_return']:.2f}%")
        print(f"   Win Rate: {strategy['win_rate']:.2f}%")
        print(f"   Profit Factor: {strategy['profit_factor']:.2f}")
        print(f"   Max Drawdown: {strategy['max_drawdown']:.2f}%")
        print(f"   Total Trades: {strategy['total_trades']}")
        print()
    
    print("="*80)

def save_results_to_file(result: Any, filename: str = None):
    """Save results to file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bta_backtest_results_{timestamp}.json"
    
    # Convert result to serializable format
    result_dict = {
        'strategy_id': result.strategy_id,
        'symbol': result.symbol,
        'timeframe': result.timeframe.value,
        'start_date': result.start_date.isoformat(),
        'end_date': result.end_date.isoformat(),
        'initial_capital': float(result.initial_capital.amount),
        'final_capital': float(result.final_capital.amount),
        'total_return': float(result.total_return.value),
        'total_trades': result.total_trades,
        'winning_trades': result.winning_trades,
        'losing_trades': result.losing_trades,
        'win_rate': float(result.win_rate.value),
        'profit_factor': float(result.profit_factor),
        'max_drawdown': float(result.max_drawdown.value),
        'sharpe_ratio': float(result.sharpe_ratio)
    }
    
    with open(filename, 'w') as f:
        json.dump(result_dict, f, indent=2)
    
    print(f"📁 Results saved to: {filename}")

def save_analysis_to_file(analysis: Dict[str, Any], filename: str = None):
    """Save analysis to file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bta_market_analysis_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"📁 Analysis saved to: {filename}")

def save_multi_results_to_file(results: Dict[str, Any], filename: str = None):
    """Save multi-results to file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bta_multi_results_{timestamp}.json"
    
    # Convert results to serializable format
    serializable_results = {}
    for strategy_name, result in results.items():
        serializable_results[strategy_name] = {
            'strategy_id': result.strategy_id,
            'symbol': result.symbol,
            'total_return': float(result.total_return.value),
            'win_rate': float(result.win_rate.value),
            'profit_factor': float(result.profit_factor),
            'max_drawdown': float(result.max_drawdown.value),
            'total_trades': result.total_trades
        }
    
    with open(filename, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"📁 Multi-results saved to: {filename}")

def save_comparison_to_file(results: Dict[str, Any], ranked_strategies: List[Dict[str, Any]], filename: str = None):
    """Save comparison to file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bta_strategy_comparison_{timestamp}.json"
    
    comparison_data = {
        'results': results,
        'ranked_strategies': ranked_strategies,
        'comparison_timestamp': datetime.now().isoformat()
    }
    
    with open(filename, 'w') as f:
        json.dump(comparison_data, f, indent=2)
    
    print(f"📁 Comparison saved to: {filename}")

if __name__ == "__main__":
    main()
