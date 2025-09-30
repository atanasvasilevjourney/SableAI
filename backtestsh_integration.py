"""
Backtest.sh Integration for Pine Script to Python Backtesting Framework
AI-powered strategy description to backtest conversion using OpenAI API
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI not available. Install with: pip install openai")

class BacktestSHAI:
    """
    AI-powered strategy description to backtest converter
    Uses OpenAI API to transform plain text descriptions into executable backtests
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Backtest.sh AI integration
        
        Args:
            api_key: OpenAI API key (if None, will try to get from environment)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        self.results = {}
        
        if not self.api_key:
            print("⚠️  OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass api_key parameter")
            return
        
        if OPENAI_AVAILABLE:
            try:
                openai.api_key = self.api_key
                self.client = openai
                print("✅ OpenAI API initialized successfully")
            except Exception as e:
                print(f"❌ Error initializing OpenAI API: {e}")
        else:
            print("❌ OpenAI not available. Install with: pip install openai")
    
    def is_available(self) -> bool:
        """Check if OpenAI API is available and configured"""
        return OPENAI_AVAILABLE and self.client is not None and self.api_key is not None
    
    def generate_strategy_from_description(self, description: str, 
                                         strategy_type: str = "momentum",
                                         timeframe: str = "1d",
                                         symbol: str = "BTC-USD") -> Dict:
        """
        Generate trading strategy from plain text description
        
        Args:
            description: Plain text strategy description
            strategy_type: Type of strategy (momentum, mean_reversion, trend_following, etc.)
            timeframe: Data timeframe
            symbol: Trading symbol
            
        Returns:
            Generated strategy code and metadata
        """
        if not self.is_available():
            return {"error": "OpenAI API not available"}
        
        try:
            # Create prompt for strategy generation
            prompt = self._create_strategy_prompt(description, strategy_type, timeframe, symbol)
            
            # Generate strategy using OpenAI
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert quantitative trader and Python developer. Generate executable trading strategies based on descriptions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            # Parse response
            strategy_code = response.choices[0].message.content
            
            # Extract strategy components
            strategy_components = self._parse_strategy_response(strategy_code)
            
            return {
                'strategy_code': strategy_code,
                'components': strategy_components,
                'description': description,
                'strategy_type': strategy_type,
                'timeframe': timeframe,
                'symbol': symbol,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating strategy: {e}")
            return {"error": str(e)}
    
    def _create_strategy_prompt(self, description: str, strategy_type: str, 
                              timeframe: str, symbol: str) -> str:
        """Create prompt for strategy generation"""
        return f"""
Generate a complete Python trading strategy based on this description:

DESCRIPTION: {description}

STRATEGY TYPE: {strategy_type}
TIMEFRAME: {timeframe}
SYMBOL: {symbol}

Requirements:
1. Create a complete Python class that inherits from a base strategy class
2. Include all necessary imports (pandas, numpy, talib, etc.)
3. Implement the strategy logic with clear entry/exit conditions
4. Include risk management (stop loss, take profit)
5. Add position sizing
6. Include technical indicators as needed
7. Make the code executable and well-documented
8. Use the following structure:

```python
import pandas as pd
import numpy as np
import talib
from typing import Dict, List, Tuple, Optional

class GeneratedStrategy:
    def __init__(self, data: pd.DataFrame, **params):
        self.data = data.copy()
        self.parameters = params
        self.results = {{}}
        self.trades = []
        
    def _calculate_indicators(self):
        # Calculate technical indicators
        pass
        
    def _check_entry_conditions(self, i: int) -> Tuple[bool, str]:
        # Check entry conditions
        pass
        
    def _check_exit_conditions(self, i: int) -> bool:
        # Check exit conditions
        pass
        
    def run_backtest(self) -> Dict:
        # Run the backtest
        pass
```

Generate the complete strategy code:
"""
    
    def _parse_strategy_response(self, strategy_code: str) -> Dict:
        """Parse the generated strategy response"""
        components = {
            'imports': [],
            'class_name': '',
            'methods': [],
            'indicators': [],
            'entry_conditions': [],
            'exit_conditions': []
        }
        
        # Extract imports
        lines = strategy_code.split('\n')
        for line in lines:
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                components['imports'].append(line.strip())
            elif 'class ' in line and ':' in line:
                components['class_name'] = line.split('class ')[1].split('(')[0].strip()
            elif 'def ' in line and ':' in line:
                method_name = line.split('def ')[1].split('(')[0].strip()
                components['methods'].append(method_name)
        
        return components
    
    def generate_backtest_from_strategy(self, strategy_code: str, 
                                      data_source: str = "yfinance",
                                      symbol: str = "BTC-USD",
                                      start_date: str = "2020-01-01",
                                      end_date: str = "2024-01-01") -> Dict:
        """
        Generate complete backtest from strategy code
        
        Args:
            strategy_code: Generated strategy code
            data_source: Data source to use
            symbol: Trading symbol
            start_date: Start date
            end_date: End date
            
        Returns:
            Complete backtest implementation
        """
        if not self.is_available():
            return {"error": "OpenAI API not available"}
        
        try:
            # Create prompt for backtest generation
            prompt = self._create_backtest_prompt(strategy_code, data_source, symbol, start_date, end_date)
            
            # Generate backtest using OpenAI
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert quantitative trader. Generate complete backtesting implementations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.5
            )
            
            # Parse response
            backtest_code = response.choices[0].message.content
            
            return {
                'backtest_code': backtest_code,
                'data_source': data_source,
                'symbol': symbol,
                'start_date': start_date,
                'end_date': end_date,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating backtest: {e}")
            return {"error": str(e)}
    
    def _create_backtest_prompt(self, strategy_code: str, data_source: str, 
                              symbol: str, start_date: str, end_date: str) -> str:
        """Create prompt for backtest generation"""
        return f"""
Generate a complete backtesting implementation for this strategy:

STRATEGY CODE:
{strategy_code}

DATA SOURCE: {data_source}
SYMBOL: {symbol}
START DATE: {start_date}
END DATE: {end_date}

Requirements:
1. Create a complete backtesting script
2. Include data loading from {data_source}
3. Implement the strategy execution
4. Calculate performance metrics (return, win rate, Sharpe ratio, max drawdown)
5. Include trade logging
6. Add visualization capabilities
7. Make the code executable
8. Use this structure:

```python
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

def load_data(symbol, start_date, end_date):
    # Load data from {data_source}
    pass

def run_backtest(strategy, data):
    # Run the backtest
    pass

def calculate_metrics(trades):
    # Calculate performance metrics
    pass

def plot_results(data, trades):
    # Plot the results
    pass

def main():
    # Main execution
    pass

if __name__ == "__main__":
    main()
```

Generate the complete backtesting implementation:
"""
    
    def run_ai_backtest(self, description: str, symbol: str = "BTC-USD",
                       start_date: str = "2020-01-01", end_date: str = "2024-01-01",
                       strategy_type: str = "momentum") -> Dict:
        """
        Complete AI-powered backtest from description to results
        
        Args:
            description: Plain text strategy description
            symbol: Trading symbol
            start_date: Start date
            end_date: End date
            strategy_type: Type of strategy
            
        Returns:
            Complete backtest results
        """
        if not self.is_available():
            return {"error": "OpenAI API not available"}
        
        print(f"🤖 Generating AI strategy from description...")
        print(f"   Description: {description[:100]}...")
        print(f"   Symbol: {symbol}")
        print(f"   Strategy Type: {strategy_type}")
        
        # Step 1: Generate strategy from description
        strategy_result = self.generate_strategy_from_description(
            description, strategy_type, "1d", symbol
        )
        
        if "error" in strategy_result:
            return strategy_result
        
        print("✅ Strategy generated successfully")
        
        # Step 2: Generate backtest implementation
        backtest_result = self.generate_backtest_from_strategy(
            strategy_result['strategy_code'],
            "yfinance",
            symbol,
            start_date,
            end_date
        )
        
        if "error" in backtest_result:
            return backtest_result
        
        print("✅ Backtest implementation generated successfully")
        
        # Step 3: Combine results
        complete_result = {
            'strategy': strategy_result,
            'backtest': backtest_result,
            'description': description,
            'symbol': symbol,
            'start_date': start_date,
            'end_date': end_date,
            'strategy_type': strategy_type,
            'generated_at': datetime.now().isoformat()
        }
        
        return complete_result
    
    def save_generated_strategy(self, result: Dict, filename: str = None) -> str:
        """Save generated strategy to file"""
        if not result or "error" in result:
            print("❌ No valid result to save")
            return ""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_generated_strategy_{timestamp}.py"
        
        # Extract strategy code
        strategy_code = result.get('strategy', {}).get('strategy_code', '')
        backtest_code = result.get('backtest', {}).get('backtest_code', '')
        
        # Combine strategy and backtest code
        full_code = f"""
# AI Generated Trading Strategy
# Generated at: {result.get('generated_at', '')}
# Description: {result.get('description', '')}
# Symbol: {result.get('symbol', '')}
# Strategy Type: {result.get('strategy_type', '')}

{strategy_code}

# Backtest Implementation
{backtest_code}
"""
        
        # Save to file
        with open(filename, 'w') as f:
            f.write(full_code)
        
        print(f"✅ Generated strategy saved to: {filename}")
        return filename
    
    def print_generated_strategy(self, result: Dict):
        """Print generated strategy information"""
        if not result or "error" in result:
            print("❌ No valid result to display")
            return
        
        print("\n" + "="*80)
        print("AI GENERATED STRATEGY")
        print("="*80)
        print(f"Description: {result.get('description', 'N/A')}")
        print(f"Symbol: {result.get('symbol', 'N/A')}")
        print(f"Strategy Type: {result.get('strategy_type', 'N/A')}")
        print(f"Start Date: {result.get('start_date', 'N/A')}")
        print(f"End Date: {result.get('end_date', 'N/A')}")
        print(f"Generated At: {result.get('generated_at', 'N/A')}")
        
        if 'strategy' in result:
            strategy = result['strategy']
            if 'components' in strategy:
                components = strategy['components']
                print(f"\nStrategy Components:")
                print(f"  Class Name: {components.get('class_name', 'N/A')}")
                print(f"  Methods: {', '.join(components.get('methods', []))}")
                print(f"  Imports: {len(components.get('imports', []))} imports")
        
        print("="*80)

class BacktestSHAILauncher:
    """
    Launcher for AI-powered strategy generation and backtesting
    """
    
    def __init__(self, api_key: str = None):
        self.ai = BacktestSHAI(api_key)
        self.results = {}
        
    def check_availability(self) -> bool:
        """Check if AI integration is available"""
        if not self.ai.is_available():
            print("❌ AI integration not available")
            print("   Requirements:")
            print("   1. Install OpenAI: pip install openai")
            print("   2. Set OPENAI_API_KEY environment variable")
            return False
        
        print("✅ AI integration is available and ready!")
        return True
    
    def run_ai_strategy_generation(self, description: str, symbol: str = "BTC-USD",
                                  start_date: str = "2020-01-01", end_date: str = "2024-01-01",
                                  strategy_type: str = "momentum") -> Dict:
        """Run AI strategy generation and backtesting"""
        
        if not self.check_availability():
            return {}
        
        print(f"🚀 Running AI strategy generation...")
        print(f"   Description: {description[:100]}...")
        
        # Generate strategy and backtest
        result = self.ai.run_ai_backtest(
            description=description,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            strategy_type=strategy_type
        )
        
        if result and "error" not in result:
            print("✅ AI strategy generation completed successfully!")
            self.ai.print_generated_strategy(result)
            
            # Save generated strategy
            filename = self.ai.save_generated_strategy(result)
            if filename:
                print(f"📁 Generated strategy saved to: {filename}")
        else:
            print("❌ AI strategy generation failed")
            if result and "error" in result:
                print(f"   Error: {result['error']}")
        
        return result
    
    def run_batch_ai_generation(self, descriptions: List[str], symbols: List[str] = None,
                                start_date: str = "2020-01-01", end_date: str = "2024-01-01",
                                strategy_types: List[str] = None) -> Dict:
        """Run batch AI strategy generation"""
        
        if not self.check_availability():
            return {}
        
        if symbols is None:
            symbols = ["BTC-USD"] * len(descriptions)
        if strategy_types is None:
            strategy_types = ["momentum"] * len(descriptions)
        
        print(f"🔄 Running batch AI strategy generation for {len(descriptions)} strategies...")
        
        batch_results = []
        
        for i, description in enumerate(descriptions):
            print(f"\n📊 Processing strategy {i+1}/{len(descriptions)}...")
            
            result = self.ai.run_ai_backtest(
                description=description,
                symbol=symbols[i] if i < len(symbols) else symbols[0],
                start_date=start_date,
                end_date=end_date,
                strategy_type=strategy_types[i] if i < len(strategy_types) else strategy_types[0]
            )
            
            if result and "error" not in result:
                batch_results.append(result)
                print(f"✅ Strategy {i+1} generated successfully")
            else:
                print(f"❌ Strategy {i+1} generation failed")
        
        # Save batch results
        if batch_results:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            batch_filename = f"ai_batch_results_{timestamp}.json"
            
            with open(batch_filename, 'w') as f:
                json.dump(batch_results, f, indent=2, default=str)
            
            print(f"\n📁 Batch results saved to: {batch_filename}")
            print(f"✅ Batch generation completed: {len(batch_results)}/{len(descriptions)} successful")
        
        return {
            'batch_results': batch_results,
            'total_descriptions': len(descriptions),
            'successful_generations': len(batch_results),
            'success_rate': len(batch_results) / len(descriptions) if descriptions else 0
        }

def test_backtestsh_integration():
    """Test Backtest.sh AI integration"""
    print("Testing Backtest.sh AI integration...")
    
    # Initialize AI launcher
    launcher = BacktestSHAILauncher()
    
    if not launcher.check_availability():
        print("❌ Backtest.sh AI integration not available")
        return False
    
    print("✅ Backtest.sh AI integration test passed")
    return True

if __name__ == "__main__":
    test_backtestsh_integration()
