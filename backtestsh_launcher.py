"""
Backtest.sh AI Launcher for Pine Script to Python Backtesting Framework
Command-line interface for AI-powered strategy generation and backtesting
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backtestsh_integration import BacktestSHAILauncher

def main():
    """Main CLI interface for Backtest.sh AI integration"""
    parser = argparse.ArgumentParser(
        description="AI-powered strategy generation and backtesting using OpenAI API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate strategy from description
  python backtestsh_launcher.py --mode generate --description "Buy when RSI < 30, sell when RSI > 70" --symbol BTC-USD
  
  # Run AI backtest
  python backtestsh_launcher.py --mode backtest --description "Moving average crossover strategy" --symbol AAPL
  
  # Batch generation
  python backtestsh_launcher.py --mode batch --descriptions-file strategies.txt
  
  # Demo mode
  python backtestsh_launcher.py --mode demo
        """
    )
    
    # Mode selection
    parser.add_argument(
        '--mode',
        choices=['generate', 'backtest', 'batch', 'demo'],
        default='demo',
        help='Mode to run (default: demo)'
    )
    
    # Strategy description
    parser.add_argument(
        '--description',
        type=str,
        help='Plain text strategy description'
    )
    
    # Descriptions file for batch mode
    parser.add_argument(
        '--descriptions-file',
        type=str,
        help='File containing strategy descriptions (one per line)'
    )
    
    # Trading parameters
    parser.add_argument(
        '--symbol',
        type=str,
        default='BTC-USD',
        help='Trading symbol (default: BTC-USD)'
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
        '--strategy-type',
        type=str,
        default='momentum',
        choices=['momentum', 'mean_reversion', 'trend_following', 'breakout', 'scalping'],
        help='Strategy type (default: momentum)'
    )
    
    # Output options
    parser.add_argument(
        '--output-file',
        type=str,
        help='Output file for generated strategy'
    )
    
    parser.add_argument(
        '--save-results',
        action='store_true',
        help='Save results to file'
    )
    
    # API configuration
    parser.add_argument(
        '--api-key',
        type=str,
        help='OpenAI API key (if not set, will use OPENAI_API_KEY environment variable)'
    )
    
    args = parser.parse_args()
    
    # Initialize launcher
    launcher = BacktestSHAILauncher(api_key=args.api_key)
    
    # Check availability
    if not launcher.check_availability():
        print("❌ AI integration not available. Please check your OpenAI API key.")
        return
    
    print("🤖 Backtest.sh AI Integration")
    print("="*50)
    
    # Run based on mode
    if args.mode == 'demo':
        run_demo_mode(launcher)
    elif args.mode == 'generate':
        run_generate_mode(launcher, args)
    elif args.mode == 'backtest':
        run_backtest_mode(launcher, args)
    elif args.mode == 'batch':
        run_batch_mode(launcher, args)
    else:
        print(f"❌ Unknown mode: {args.mode}")
        return

def run_demo_mode(launcher: BacktestSHAILauncher):
    """Run demo mode with example strategies"""
    print("🎯 Demo Mode - AI Strategy Generation")
    print("="*50)
    
    # Example strategies
    demo_strategies = [
        {
            'description': "Buy when RSI is below 30 and price is above 20-day moving average, sell when RSI is above 70",
            'symbol': 'BTC-USD',
            'strategy_type': 'mean_reversion'
        },
        {
            'description': "Buy when 50-day moving average crosses above 200-day moving average, sell when it crosses below",
            'symbol': 'AAPL',
            'strategy_type': 'trend_following'
        },
        {
            'description': "Buy when price breaks above upper Bollinger Band, sell when it breaks below lower band",
            'symbol': 'ETH-USD',
            'strategy_type': 'breakout'
        }
    ]
    
    print(f"📊 Running {len(demo_strategies)} demo strategies...")
    
    for i, strategy in enumerate(demo_strategies):
        print(f"\n🚀 Demo Strategy {i+1}/{len(demo_strategies)}")
        print(f"   Description: {strategy['description']}")
        print(f"   Symbol: {strategy['symbol']}")
        print(f"   Type: {strategy['strategy_type']}")
        
        result = launcher.run_ai_strategy_generation(
            description=strategy['description'],
            symbol=strategy['symbol'],
            start_date='2020-01-01',
            end_date='2024-01-01',
            strategy_type=strategy['strategy_type']
        )
        
        if result and "error" not in result:
            print(f"✅ Demo strategy {i+1} generated successfully")
        else:
            print(f"❌ Demo strategy {i+1} generation failed")
    
    print(f"\n🎉 Demo completed! Check generated files for results.")

def run_generate_mode(launcher: BacktestSHAILauncher, args):
    """Run strategy generation mode"""
    if not args.description:
        print("❌ Description required for generate mode")
        print("   Use --description 'Your strategy description'")
        return
    
    print("🤖 AI Strategy Generation Mode")
    print("="*50)
    print(f"Description: {args.description}")
    print(f"Symbol: {args.symbol}")
    print(f"Strategy Type: {args.strategy_type}")
    print(f"Date Range: {args.start_date} to {args.end_date}")
    
    result = launcher.run_ai_strategy_generation(
        description=args.description,
        symbol=args.symbol,
        start_date=args.start_date,
        end_date=args.end_date,
        strategy_type=args.strategy_type
    )
    
    if result and "error" not in result:
        print("✅ Strategy generation completed successfully!")
        
        if args.save_results:
            # Save results to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f"ai_strategy_results_{timestamp}.json"
            
            with open(results_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            
            print(f"📁 Results saved to: {results_file}")
    else:
        print("❌ Strategy generation failed")
        if result and "error" in result:
            print(f"   Error: {result['error']}")

def run_backtest_mode(launcher: BacktestSHAILauncher, args):
    """Run backtest mode"""
    if not args.description:
        print("❌ Description required for backtest mode")
        print("   Use --description 'Your strategy description'")
        return
    
    print("🚀 AI Backtest Mode")
    print("="*50)
    print(f"Description: {args.description}")
    print(f"Symbol: {args.symbol}")
    print(f"Strategy Type: {args.strategy_type}")
    print(f"Date Range: {args.start_date} to {args.end_date}")
    
    result = launcher.run_ai_strategy_generation(
        description=args.description,
        symbol=args.symbol,
        start_date=args.start_date,
        end_date=args.end_date,
        strategy_type=args.strategy_type
    )
    
    if result and "error" not in result:
        print("✅ AI backtest completed successfully!")
        
        # Save generated strategy if requested
        if args.output_file:
            filename = launcher.ai.save_generated_strategy(result, args.output_file)
            if filename:
                print(f"📁 Generated strategy saved to: {filename}")
        
        if args.save_results:
            # Save results to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f"ai_backtest_results_{timestamp}.json"
            
            with open(results_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            
            print(f"📁 Results saved to: {results_file}")
    else:
        print("❌ AI backtest failed")
        if result and "error" in result:
            print(f"   Error: {result['error']}")

def run_batch_mode(launcher: BacktestSHAILauncher, args):
    """Run batch generation mode"""
    if not args.descriptions_file:
        print("❌ Descriptions file required for batch mode")
        print("   Use --descriptions-file strategies.txt")
        return
    
    if not os.path.exists(args.descriptions_file):
        print(f"❌ Descriptions file not found: {args.descriptions_file}")
        return
    
    print("🔄 AI Batch Generation Mode")
    print("="*50)
    print(f"Descriptions file: {args.descriptions_file}")
    print(f"Symbol: {args.symbol}")
    print(f"Strategy Type: {args.strategy_type}")
    print(f"Date Range: {args.start_date} to {args.end_date}")
    
    # Read descriptions from file
    try:
        with open(args.descriptions_file, 'r') as f:
            descriptions = [line.strip() for line in f if line.strip()]
        
        print(f"📊 Found {len(descriptions)} strategy descriptions")
        
        # Run batch generation
        result = launcher.run_batch_ai_generation(
            descriptions=descriptions,
            symbols=[args.symbol] * len(descriptions),
            start_date=args.start_date,
            end_date=args.end_date,
            strategy_types=[args.strategy_type] * len(descriptions)
        )
        
        if result:
            print(f"✅ Batch generation completed!")
            print(f"   Total descriptions: {result.get('total_descriptions', 0)}")
            print(f"   Successful generations: {result.get('successful_generations', 0)}")
            print(f"   Success rate: {result.get('success_rate', 0):.2%}")
        
    except Exception as e:
        print(f"❌ Error reading descriptions file: {e}")

def create_sample_descriptions_file():
    """Create a sample descriptions file for batch mode"""
    sample_descriptions = [
        "Buy when RSI is below 30 and price is above 20-day moving average, sell when RSI is above 70",
        "Buy when 50-day moving average crosses above 200-day moving average, sell when it crosses below",
        "Buy when price breaks above upper Bollinger Band, sell when it breaks below lower band",
        "Buy when MACD line crosses above signal line, sell when it crosses below",
        "Buy when price is above 20-day moving average and volume is above average, sell when price is below 20-day moving average"
    ]
    
    filename = "sample_strategies.txt"
    with open(filename, 'w') as f:
        for desc in sample_descriptions:
            f.write(desc + '\n')
    
    print(f"📁 Sample descriptions file created: {filename}")
    return filename

if __name__ == "__main__":
    # Check if OpenAI API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OpenAI API key not found!")
        print("   Set OPENAI_API_KEY environment variable or use --api-key parameter")
        print("   Get your API key from: https://platform.openai.com/api-keys")
        
        # Create sample descriptions file
        create_sample_descriptions_file()
        
        print("\n📝 Sample usage:")
        print("   python backtestsh_launcher.py --mode demo")
        print("   python backtestsh_launcher.py --mode generate --description 'Your strategy here'")
        print("   python backtestsh_launcher.py --mode batch --descriptions-file sample_strategies.txt")
        
        sys.exit(1)
    
    main()
