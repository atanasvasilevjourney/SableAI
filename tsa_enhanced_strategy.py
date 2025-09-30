"""
TSA Enhanced Strategy - Python Implementation
Translated from Pine Script with comprehensive backtesting capabilities
"""

import pandas as pd
import numpy as np
import talib
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class TSAEnhancedStrategy:
    """
    TSA Enhanced Strategy - No Repainting
    Translated from Pine Script with advanced trend analysis
    """
    
    def __init__(self, data: pd.DataFrame, **params):
        """
        Initialize TSA Enhanced Strategy
        
        Args:
            data: OHLCV DataFrame with columns ['open', 'high', 'low', 'close', 'volume']
            **params: Strategy parameters
        """
        self.data = data.copy()
        self.parameters = params
        self.results = {}
        self.trades = []
        self.positions = []
        
        # Strategy Parameters
        self.atr_length = params.get('atr_length', 14)
        self.atr_multiplier = params.get('atr_multiplier', 3.0)
        self.risk_reward_ratio = params.get('risk_reward_ratio', 1.5)
        self.adx_length = params.get('adx_length', 14)
        self.adx_threshold = params.get('adx_threshold', 25)
        self.max_length = params.get('max_length', 50)
        self.accel_multiplier = params.get('accel_multiplier', 5.0)
        self.collen = params.get('collen', 100)
        
        # Initialize strategy variables
        self._initialize_variables()
        
    def _initialize_variables(self):
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
        
    def _calculate_indicators(self):
        """Calculate all technical indicators"""
        # ATR
        self.data['atr'] = talib.ATR(
            self.data['high'].values, 
            self.data['low'].values, 
            self.data['close'].values, 
            timeperiod=self.atr_length
        )
        
        # ADX and DMI
        self.data['adx'] = talib.ADX(
            self.data['high'].values,
            self.data['low'].values, 
            self.data['close'].values,
            timeperiod=self.adx_length
        )
        
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
        
        # TSA Dynamic EMA and Trend Analysis
        self._calculate_tsa_indicators()
        
    def _calculate_tsa_indicators(self):
        """Calculate TSA (Trend Speed Analysis) indicators"""
        # TSA Core Logic - Dynamic Length Calculation
        counts_diff = self.data['close']
        max_abs_counts_diff = counts_diff.rolling(200).apply(lambda x: np.abs(x).max())
        counts_diff_norm = (counts_diff + max_abs_counts_diff) / (2 * max_abs_counts_diff)
        dyn_length = 5 + counts_diff_norm * (self.max_length - 5)
        
        # Dynamic EMA calculation with acceleration factor
        self.data['dyn_ema'] = 0.0
        self.data['trend_speed'] = 0.0
        self.data['normalized_speed'] = 0.0
        
        # Initialize variables for TSA calculation
        prev_counts_diff = 0
        dyn_ema_prev = 0
        speed = 0
        pos = 0
        x1 = 0
        y1 = 0
        
        for i in range(len(self.data)):
            if i == 0:
                # First value initialization
                x1 = i
                y1 = self.data['open'].iloc[i]
                dyn_ema_prev = self.data['close'].iloc[i]
                self.data.iloc[i, self.data.columns.get_loc('dyn_ema')] = dyn_ema_prev
                continue
            
            # Calculate acceleration factor
            current_counts_diff = counts_diff.iloc[i]
            delta_counts_diff = abs(current_counts_diff - prev_counts_diff)
            max_delta_counts_diff = counts_diff.rolling(200).apply(lambda x: abs(x).max()).iloc[i]
            max_delta_counts_diff = max(max_delta_counts_diff, 1)
            accel_factor = delta_counts_diff / max_delta_counts_diff
            
            # Adjust alpha using acceleration factor
            alpha_base = 2 / (dyn_length.iloc[i] + 1)
            alpha = alpha_base * (1 + accel_factor * self.accel_multiplier)
            alpha = min(1, alpha)
            
            # Compute dynamic EMA
            current_close = self.data['close'].iloc[i]
            dyn_ema = alpha * current_close + (1 - alpha) * dyn_ema_prev
            self.data.iloc[i, self.data.columns.get_loc('dyn_ema')] = dyn_ema
            
            # Trend direction detection
            current_close = self.data['close'].iloc[i]
            prev_close = self.data['close'].iloc[i-1]
            current_open = self.data['open'].iloc[i]
            
            # Bullish crossover
            if current_close > dyn_ema and prev_close <= dyn_ema:
                x1 = i
                y1 = current_close
                pos = 1
                speed = current_close - current_open
            
            # Bearish crossover
            elif current_close < dyn_ema and prev_close >= dyn_ema:
                x1 = i
                y1 = current_close
                pos = -1
                speed = current_close - current_open
            
            # Update speed
            speed += current_close - current_open
            trend_speed = self._calculate_hma(speed, 5, i)
            self.data.iloc[i, self.data.columns.get_loc('trend_speed')] = trend_speed
            
            # Normalize speed for histogram colors
            if i >= self.collen:
                speed_window = self.data['trend_speed'].iloc[i-self.collen+1:i+1]
                min_speed = speed_window.min()
                max_speed = speed_window.max()
                if max_speed != min_speed:
                    normalized_speed = (trend_speed - min_speed) / (max_speed - min_speed)
                else:
                    normalized_speed = 0.5
            else:
                normalized_speed = 0.5
            
            self.data.iloc[i, self.data.columns.get_loc('normalized_speed')] = normalized_speed
            
            # Update for next iteration
            prev_counts_diff = current_counts_diff
            dyn_ema_prev = dyn_ema
    
    def _calculate_hma(self, value, period, current_idx):
        """Calculate Hull Moving Average"""
        if current_idx < period - 1:
            return value
        
        # Get the last 'period' values
        start_idx = max(0, current_idx - period + 1)
        values = self.data['trend_speed'].iloc[start_idx:current_idx+1].values
        
        if len(values) < period:
            return value
        
        # Hull Moving Average calculation
        wma_half = np.average(values[-period//2:], weights=range(1, period//2+1))
        wma_full = np.average(values, weights=range(1, period+1))
        
        hma = 2 * wma_half - wma_full
        return hma
    
    def _check_entry_conditions(self, i: int) -> Tuple[bool, str]:
        """Check entry conditions for current bar"""
        if i < 200:  # Need enough data for indicators
            return False, ""
        
        current = self.data.iloc[i]
        
        # TSA Signal Detection (No Repainting)
        tsa_green = (current['trend_speed'] > 0 and current['normalized_speed'] > 0.5)
        tsa_red = (current['trend_speed'] < 0 and current['normalized_speed'] > 0.5)
        tsa_consolidation = (abs(current['trend_speed']) < 0.1 or current['normalized_speed'] < 0.3)
        
        # ADX Filter Logic
        adx_bullish = current['plus_di'] > current['minus_di']
        adx_bearish = current['minus_di'] > current['plus_di']
        adx_strong = current['adx'] > self.adx_threshold
        
        # EMA Trend Confirmation
        ema_bullish = current['ema_fast'] > current['ema_slow']
        ema_bearish = current['ema_slow'] > current['ema_fast']
        
        # Combined ADX Filter
        adx_long_filter = adx_bullish and adx_strong and ema_bullish
        adx_short_filter = adx_bearish and adx_strong and ema_bearish
        
        # ATR Band Confirmation
        atr_long_confirmation = current['close'] > (current['close'] - current['atr'] * self.atr_multiplier)
        atr_short_confirmation = current['close'] < (current['close'] + current['atr'] * self.atr_multiplier)
        
        # Enhanced Entry Conditions (All filters must align)
        long_condition = (
            current['close'] > current['dyn_ema'] and 
            tsa_green and 
            adx_long_filter and 
            atr_long_confirmation and 
            not tsa_consolidation
        )
        
        short_condition = (
            current['close'] < current['dyn_ema'] and 
            tsa_red and 
            adx_short_filter and 
            atr_short_confirmation and 
            not tsa_consolidation
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
            'take_profit': self.take_profit,
            'entry_date': self.data.index[i],
            'exit_date': self.data.index[i]
        }
        self.trades.append(trade)
        
        # Reset position
        self.in_position = False
        self.position_size = 0
    
    def run_backtest(self) -> Dict:
        """Run the backtest"""
        print(f"Running TSA Enhanced Strategy backtest...")
        
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
                'sharpe_ratio': 0,
                'avg_trade': 0,
                'gross_profit': 0,
                'gross_loss': 0
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
        
        # Sharpe ratio
        returns = [t['pnl'] for t in self.trades]
        sharpe_ratio = np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
        
        # Average trade
        avg_trade = np.mean(returns) if returns else 0
        
        self.results = {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'total_return': total_return,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'avg_trade': avg_trade,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'win_count': self.win_count,
            'loss_count': self.loss_count
        }
    
    def print_results(self):
        """Print backtest results"""
        print("\n" + "="*60)
        print("TSA ENHANCED STRATEGY - BACKTEST RESULTS")
        print("="*60)
        
        for key, value in self.results.items():
            if isinstance(value, float):
                print(f"{key.replace('_', ' ').title()}: {value:.4f}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")
        
        print("="*60)
    
    def get_trades_dataframe(self) -> pd.DataFrame:
        """Get trades as DataFrame"""
        if not self.trades:
            return pd.DataFrame()
        
        return pd.DataFrame(self.trades)
    
    def get_strategy_metrics(self) -> Dict:
        """Get detailed strategy metrics"""
        if not self.trades:
            return {}
        
        trades_df = self.get_trades_dataframe()
        
        # Calculate additional metrics
        consecutive_wins = 0
        consecutive_losses = 0
        max_consecutive_wins = 0
        max_consecutive_losses = 0
        
        current_wins = 0
        current_losses = 0
        
        for pnl in trades_df['pnl']:
            if pnl > 0:
                current_wins += 1
                current_losses = 0
                max_consecutive_wins = max(max_consecutive_wins, current_wins)
            else:
                current_losses += 1
                current_wins = 0
                max_consecutive_losses = max(max_consecutive_losses, current_losses)
        
        return {
            'max_consecutive_wins': max_consecutive_wins,
            'max_consecutive_losses': max_consecutive_losses,
            'avg_win': np.mean([t['pnl'] for t in self.trades if t['pnl'] > 0]) if any(t['pnl'] > 0 for t in self.trades) else 0,
            'avg_loss': np.mean([t['pnl'] for t in self.trades if t['pnl'] < 0]) if any(t['pnl'] < 0 for t in self.trades) else 0,
            'largest_win': max([t['pnl'] for t in self.trades]) if self.trades else 0,
            'largest_loss': min([t['pnl'] for t in self.trades]) if self.trades else 0
        }
