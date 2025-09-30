"""
Pine Script to Python Trading Strategy Translator
Advanced framework for converting TradingView Pine Script strategies to Python backtesting code
"""

import pandas as pd
import numpy as np
import yfinance as yf
import talib
from typing import Dict, List, Tuple, Optional, Any
import re
import ast
from dataclasses import dataclass
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

@dataclass
class StrategyConfig:
    """Configuration for strategy parameters"""
    name: str
    version: str = "1.0"
    overlay: bool = True
    default_qty_type: str = "percent_of_equity"
    default_qty_value: float = 10.0
    parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}

class PineScriptTranslator:
    """
    Advanced Pine Script to Python translator for trading strategies
    Handles complex Pine Script syntax and converts to backtesting framework
    """
    
    def __init__(self):
        self.strategy_config = None
        self.parameters = {}
        self.translated_code = ""
        self.imports = set()
        self.functions = {}
        self.variables = {}
        
    def parse_pinescript(self, pinescript_code: str) -> StrategyConfig:
        """Parse Pine Script code and extract strategy configuration"""
        
        # Extract strategy name
        strategy_match = re.search(r'strategy\("([^"]+)"', pinescript_code)
        strategy_name = strategy_match.group(1) if strategy_match else "Unknown Strategy"
        
        # Extract version
        version_match = re.search(r'@version=(\d+)', pinescript_code)
        version = version_match.group(1) if version_match else "1.0"
        
        # Extract overlay setting
        overlay_match = re.search(r'overlay=(\w+)', pinescript_code)
        overlay = overlay_match.group(1) == 'true' if overlay_match else True
        
        # Extract default quantity settings
        qty_type_match = re.search(r'default_qty_type=strategy\.(\w+)', pinescript_code)
        qty_type = qty_type_match.group(1) if qty_type_match else "percent_of_equity"
        
        qty_value_match = re.search(r'default_qty_value=(\d+(?:\.\d+)?)', pinescript_code)
        qty_value = float(qty_value_match.group(1)) if qty_value_match else 10.0
        
        # Extract input parameters
        parameters = self._extract_parameters(pinescript_code)
        
        self.strategy_config = StrategyConfig(
            name=strategy_name,
            version=version,
            overlay=overlay,
            default_qty_type=qty_type,
            default_qty_value=qty_value,
            parameters=parameters
        )
        
        return self.strategy_config
    
    def _extract_parameters(self, code: str) -> Dict[str, Any]:
        """Extract input parameters from Pine Script"""
        parameters = {}
        
        # Find all input declarations
        input_pattern = r'(\w+)\s*=\s*input\.(\w+)\(([^)]+)\)'
        matches = re.findall(input_pattern, code)
        
        for var_name, input_type, args in matches:
            # Parse arguments
            args_dict = self._parse_input_args(args)
            parameters[var_name] = {
                'type': input_type,
                'args': args_dict
            }
        
        return parameters
    
    def _parse_input_args(self, args_str: str) -> Dict[str, Any]:
        """Parse input arguments string"""
        args = {}
        
        # Simple parsing - can be enhanced for complex cases
        if 'title=' in args_str:
            title_match = re.search(r"title='([^']+)'", args_str)
            if title_match:
                args['title'] = title_match.group(1)
        
        if 'minval=' in args_str:
            minval_match = re.search(r'minval=(\d+(?:\.\d+)?)', args_str)
            if minval_match:
                args['minval'] = float(minval_match.group(1))
        
        if 'maxval=' in args_str:
            maxval_match = re.search(r'maxval=(\d+(?:\.\d+)?)', args_str)
            if maxval_match:
                args['maxval'] = float(maxval_match.group(1))
        
        if 'step=' in args_str:
            step_match = re.search(r'step=(\d+(?:\.\d+)?)', args_str)
            if step_match:
                args['step'] = float(step_match.group(1))
        
        if 'group=' in args_str:
            group_match = re.search(r"group='([^']+)'", args_str)
            if group_match:
                args['group'] = group_match.group(1)
        
        return args
    
    def translate_to_python(self, pinescript_code: str) -> str:
        """Translate Pine Script to Python backtesting code"""
        
        # Parse the Pine Script
        config = self.parse_pinescript(pinescript_code)
        
        # Start building Python code
        python_code = self._generate_imports()
        python_code += self._generate_class_header(config)
        python_code += self._generate_parameters(config)
        python_code += self._generate_initialization()
        python_code += self._translate_strategy_logic(pinescript_code)
        python_code += self._generate_backtest_method()
        python_code += self._generate_results_method()
        python_code += "}\n"
        
        return python_code
    
    def _generate_imports(self) -> str:
        """Generate necessary imports"""
        return '''"""
Auto-generated Python backtesting code from Pine Script
Generated by Pine Script Translator
"""

import pandas as pd
import numpy as np
import yfinance as yf
import talib
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

'''
    
    def _generate_class_header(self, config: StrategyConfig) -> str:
        """Generate class header"""
        class_name = config.name.replace(" ", "").replace("-", "")
        return f'''
class {class_name}Strategy:
    """
    {config.name} - Translated from Pine Script
    Version: {config.version}
    """
    
    def __init__(self, data: pd.DataFrame, **params):
        """
        Initialize strategy with data and parameters
        
        Args:
            data: OHLCV DataFrame with columns ['open', 'high', 'low', 'close', 'volume']
            **params: Strategy parameters
        """
        self.data = data.copy()
        self.parameters = params
        self.results = {{}}
        self.trades = []
        self.positions = []
        
        # Initialize strategy-specific variables
        self._initialize_variables()
        
'''
    
    def _generate_parameters(self, config: StrategyConfig) -> str:
        """Generate parameter initialization"""
        param_code = "        # Strategy Parameters\n"
        
        for param_name, param_info in config.parameters.items():
            param_type = param_info['type']
            args = param_info['args']
            
            if param_type == 'int':
                default = args.get('minval', 14)
                param_code += f"        self.{param_name} = params.get('{param_name}', {default})\n"
            elif param_type == 'float':
                default = args.get('minval', 1.0)
                param_code += f"        self.{param_name} = params.get('{param_name}', {default})\n"
            else:
                param_code += f"        self.{param_name} = params.get('{param_name}', None)\n"
        
        return param_code + "\n"
    
    def _generate_initialization(self) -> str:
        """Generate initialization method"""
        return '''    def _initialize_variables(self):
        """Initialize strategy variables"""
        self.position_size = 0
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.in_position = False
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.total_pnl = 0
        
        # Initialize technical indicators
        self._calculate_indicators()
        
'''
    
    def _translate_strategy_logic(self, pinescript_code: str) -> str:
        """Translate Pine Script strategy logic to Python"""
        
        # This is a simplified translation - in practice, you'd need a full parser
        # For now, I'll create a template that can be customized
        
        logic_code = '''    def _calculate_indicators(self):
        """Calculate all technical indicators"""
        # ATR
        self.data['atr'] = talib.ATR(
            self.data['high'].values, 
            self.data['low'].values, 
            self.data['close'].values, 
            timeperiod=self.atr_length
        )
        
        # ADX
        self.data['adx'] = talib.ADX(
            self.data['high'].values,
            self.data['low'].values, 
            self.data['close'].values,
            timeperiod=self.adx_length
        )
        
        # DMI
        self.data['plus_di'] = talib.PLUS_DI(
            self.data['high'].values,
            self.data['low'].values,
            self.data['close'].values,
            timeperiod=self.adx_length
        )
        
        self.data['minus_di'] = talib.MINUS_DI(
            self.data['high'].values,
            self.data['low'].values,
            self.data['close'].values,
            timeperiod=self.adx_length
        )
        
        # EMA
        self.data['ema_fast'] = talib.EMA(self.data['close'].values, timeperiod=12)
        self.data['ema_slow'] = talib.EMA(self.data['close'].values, timeperiod=50)
        
        # TSA Dynamic EMA (simplified version)
        self._calculate_tsa_indicators()
        
    def _calculate_tsa_indicators(self):
        """Calculate TSA (Trend Speed Analysis) indicators"""
        # Simplified TSA implementation
        # In practice, you'd implement the full TSA logic from the Pine Script
        
        # Dynamic length calculation
        counts_diff = self.data['close']
        max_abs_counts_diff = counts_diff.rolling(200).apply(lambda x: np.abs(x).max())
        counts_diff_norm = (counts_diff + max_abs_counts_diff) / (2 * max_abs_counts_diff)
        dyn_length = 5 + counts_diff_norm * (self.max_length - 5)
        
        # Dynamic EMA calculation (simplified)
        alpha = 2 / (dyn_length + 1)
        self.data['dyn_ema'] = self.data['close'].ewm(alpha=alpha).mean()
        
        # Trend speed calculation
        self.data['trend_speed'] = self.data['close'].diff().rolling(5).mean()
        
    def _check_entry_conditions(self, i: int) -> Tuple[bool, str]:
        """Check entry conditions for current bar"""
        if i < 200:  # Need enough data for indicators
            return False, ""
        
        current = self.data.iloc[i]
        
        # Long conditions
        long_condition = (
            current['close'] > current['dyn_ema'] and
            current['trend_speed'] > 0 and
            current['plus_di'] > current['minus_di'] and
            current['adx'] > self.adx_threshold and
            current['ema_fast'] > current['ema_slow'] and
            current['close'] > (current['close'] - current['atr'] * self.atr_multiplier)
        )
        
        # Short conditions  
        short_condition = (
            current['close'] < current['dyn_ema'] and
            current['trend_speed'] < 0 and
            current['minus_di'] > current['plus_di'] and
            current['adx'] > self.adx_threshold and
            current['ema_slow'] > current['ema_fast'] and
            current['close'] < (current['close'] + current['atr'] * self.atr_multiplier)
        )
        
        if long_condition and not self.in_position:
            return True, "long"
        elif short_condition and not self.in_position:
            return True, "short"
        
        return False, ""
    
    def _check_exit_conditions(self, i: int) -> bool:
        """Check exit conditions for current bar"""
        if not self.in_position:
            return False
            
        current = self.data.iloc[i]
        
        # Stop loss or take profit hit
        if self.position_size > 0:  # Long position
            if current['low'] <= self.stop_loss or current['high'] >= self.take_profit:
                return True
        else:  # Short position
            if current['high'] >= self.stop_loss or current['low'] <= self.take_profit:
                return True
                
        return False
    
    def _enter_position(self, i: int, direction: str):
        """Enter a new position"""
        current = self.data.iloc[i]
        self.entry_price = current['close']
        self.position_size = 1 if direction == "long" else -1
        self.in_position = True
        
        # Calculate stop loss and take profit
        atr_value = current['atr']
        
        if direction == "long":
            self.stop_loss = self.entry_price - (atr_value * self.atr_multiplier)
            self.take_profit = self.entry_price + ((self.entry_price - self.stop_loss) * self.risk_reward_ratio)
        else:
            self.stop_loss = self.entry_price + (atr_value * self.atr_multiplier)
            self.take_profit = self.entry_price - ((self.stop_loss - self.entry_price) * self.risk_reward_ratio)
        
        self.trade_count += 1
        
    def _exit_position(self, i: int):
        """Exit current position"""
        if not self.in_position:
            return
            
        current = self.data.iloc[i]
        exit_price = current['close']
        
        # Calculate P&L
        if self.position_size > 0:  # Long position
            pnl = (exit_price - self.entry_price) / self.entry_price
        else:  # Short position
            pnl = (self.entry_price - exit_price) / self.entry_price
        
        self.total_pnl += pnl
        
        # Update win/loss count
        if pnl > 0:
            self.win_count += 1
        else:
            self.loss_count += 1
        
        # Record trade
        trade = {
            'entry_bar': i - len(self.data) + len(self.data),
            'exit_bar': i,
            'entry_price': self.entry_price,
            'exit_price': exit_price,
            'position_size': self.position_size,
            'pnl': pnl,
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit
        }
        self.trades.append(trade)
        
        # Reset position
        self.in_position = False
        self.position_size = 0
        
'''
    
    def _generate_backtest_method(self) -> str:
        """Generate backtesting method"""
        return '''    def run_backtest(self) -> Dict:
        """Run the backtest"""
        print(f"Running backtest for {self.__class__.__name__}...")
        
        for i in range(len(self.data)):
            # Check exit conditions first
            if self.in_position and self._check_exit_conditions(i):
                self._exit_position(i)
            
            # Check entry conditions
            if not self.in_position:
                should_enter, direction = self._check_entry_conditions(i)
                if should_enter:
                    self._enter_position(i, direction)
        
        # Close any remaining position
        if self.in_position:
            self._exit_position(len(self.data) - 1)
        
        # Calculate results
        self._calculate_results()
        
        return self.results
    
    def _calculate_results(self):
        """Calculate backtest results"""
        if not self.trades:
            self.results = {
                'total_trades': 0,
                'win_rate': 0,
                'total_return': 0,
                'profit_factor': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0
            }
            return
        
        # Basic metrics
        total_trades = len(self.trades)
        win_rate = self.win_count / total_trades if total_trades > 0 else 0
        total_return = self.total_pnl
        
        # Profit factor
        gross_profit = sum([t['pnl'] for t in self.trades if t['pnl'] > 0])
        gross_loss = abs(sum([t['pnl'] for t in self.trades if t['pnl'] < 0]))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Max drawdown
        cumulative_returns = np.cumsum([t['pnl'] for t in self.trades])
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = cumulative_returns - running_max
        max_drawdown = abs(np.min(drawdown)) if len(drawdown) > 0 else 0
        
        # Sharpe ratio (simplified)
        returns = [t['pnl'] for t in self.trades]
        sharpe_ratio = np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
        
        self.results = {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'total_return': total_return,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'avg_trade': np.mean(returns) if returns else 0
        }
        
'''
    
    def _generate_results_method(self) -> str:
        """Generate results display method"""
        return '''    def print_results(self):
        """Print backtest results"""
        print("\\n" + "="*50)
        print(f"BACKTEST RESULTS - {self.__class__.__name__}")
        print("="*50)
        
        for key, value in self.results.items():
            if isinstance(value, float):
                print(f"{key.replace('_', ' ').title()}: {value:.4f}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")
        
        print("="*50)
        
    def get_trades_dataframe(self) -> pd.DataFrame:
        """Get trades as DataFrame"""
        if not self.trades:
            return pd.DataFrame()
        
        return pd.DataFrame(self.trades)

'''
