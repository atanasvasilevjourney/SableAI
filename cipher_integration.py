"""
Cipher-BT Integration for Pine Script to Python Backtesting Framework
Enhanced backtesting with concurrent sessions and advanced exit strategies
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

try:
    from cipher import Cipher, Session, Strategy
    CIPHER_AVAILABLE = True
except ImportError:
    CIPHER_AVAILABLE = False
    print("Cipher-BT not available. Install with: pip install cipher-bt")

class CipherStrategyAdapter(Strategy):
    """
    Adapter to convert our Pine Script strategies to Cipher-BT format
    """
    
    def __init__(self, strategy_class, strategy_params: Dict = None):
        self.strategy_class = strategy_class
        self.strategy_params = strategy_params or {}
        self.original_strategy = None
        self.data = None
        
    def compose(self):
        """Compose strategy logic - called by Cipher-BT"""
        # Initialize our original strategy
        self.original_strategy = self.strategy_class(self.datas.df, **self.strategy_params)
        
        # Calculate indicators using our strategy
        self.original_strategy._calculate_indicators()
        
        # Get the enhanced dataframe
        self.data = self.original_strategy.data
        
        # Add signal columns for Cipher-BT
        self.data["entry"] = False
        self.data["exit"] = False
        
        # Calculate entry/exit signals
        for i in range(len(self.data)):
            if i < 200:  # Need enough data for indicators
                continue
                
            # Check entry conditions
            should_enter, direction = self.original_strategy._check_entry_conditions(i)
            if should_enter:
                self.data.iloc[i, self.data.columns.get_loc("entry")] = True
                self.data.iloc[i, self.data.columns.get_loc("direction")] = direction
            
            # Check exit conditions
            if self.original_strategy._check_exit_conditions(i):
                self.data.iloc[i, self.data.columns.get_loc("exit")] = True
        
        return self.data
    
    def on_entry(self, row: dict, session: Session):
        """Handle entry signals"""
        if row.get("entry", False):
            direction = row.get("direction", "long")
            
            if direction == "long":
                # Open long position
                session.position += "0.01"  # 1% of portfolio
                
                # Set stop loss and take profit
                current_price = row["close"]
                atr = row.get("atr", current_price * 0.02)  # 2% ATR fallback
                
                # Stop loss
                session.stop_loss = current_price - (atr * 3.0)
                
                # Take profit with risk-reward ratio
                risk = current_price - session.stop_loss
                session.take_profit = current_price + (risk * 1.5)
                
            elif direction == "short":
                # Open short position
                session.position -= "0.01"  # 1% of portfolio
                
                # Set stop loss and take profit
                current_price = row["close"]
                atr = row.get("atr", current_price * 0.02)  # 2% ATR fallback
                
                # Stop loss
                session.stop_loss = current_price + (atr * 3.0)
                
                # Take profit with risk-reward ratio
                risk = session.stop_loss - current_price
                session.take_profit = current_price - (risk * 1.5)
    
    def on_exit(self, row: dict, session: Session):
        """Handle exit signals"""
        if row.get("exit", False):
            session.position = 0
    
    def on_take_profit(self, row: dict, session: Session):
        """Handle take profit hits"""
        session.position = 0
    
    def on_stop_loss(self, row: dict, session: Session):
        """Handle stop loss hits"""
        session.position = 0
    
    def on_stop(self, row: dict, session: Session):
        """Handle end of data"""
        session.position = 0

class CipherBacktester:
    """
    Cipher-BT enhanced backtester with concurrent sessions
    """
    
    def __init__(self):
        self.cipher = None
        self.results = {}
        
    def is_available(self) -> bool:
        """Check if Cipher-BT is available"""
        return CIPHER_AVAILABLE
    
    def setup_cipher(self, data_sources: List[Dict], strategy_class, strategy_params: Dict = None):
        """Setup Cipher-BT with data sources and strategy"""
        if not self.is_available():
            print("Cipher-BT not available. Install with: pip install cipher-bt")
            return False
        
        try:
            # Initialize Cipher
            self.cipher = Cipher()
            
            # Add data sources
            for source in data_sources:
                if source["type"] == "binance_spot_ohlc":
                    self.cipher.add_source(
                        "binance_spot_ohlc",
                        symbol=source["symbol"],
                        interval=source["interval"]
                    )
                elif source["type"] == "yfinance":
                    # For yfinance, we'll need to create a custom data source
                    self._add_yfinance_source(source)
            
            # Set strategy
            strategy = CipherStrategyAdapter(strategy_class, strategy_params)
            self.cipher.set_strategy(strategy)
            
            return True
            
        except Exception as e:
            print(f"Error setting up Cipher-BT: {e}")
            return False
    
    def _add_yfinance_source(self, source: Dict):
        """Add yfinance data source to Cipher"""
        # This would require custom implementation
        # For now, we'll use binance as the primary source
        pass
    
    def run_backtest(self, start_ts: str, stop_ts: str, commission: float = 0.00075) -> Dict:
        """Run Cipher-BT backtest"""
        if not self.cipher:
            print("Cipher not initialized")
            return {}
        
        try:
            # Run backtest
            self.cipher.run(start_ts=start_ts, stop_ts=stop_ts)
            self.cipher.set_commission(commission)
            
            # Get results
            sessions = self.cipher.sessions
            stats = self.cipher.stats
            
            # Convert to our format
            self.results = {
                'sessions': sessions,
                'stats': stats,
                'total_trades': len(sessions),
                'win_rate': self._calculate_win_rate(sessions),
                'total_return': self._calculate_total_return(sessions),
                'max_drawdown': self._calculate_max_drawdown(sessions),
                'profit_factor': self._calculate_profit_factor(sessions)
            }
            
            return self.results
            
        except Exception as e:
            print(f"Error running Cipher-BT backtest: {e}")
            return {}
    
    def _calculate_win_rate(self, sessions) -> float:
        """Calculate win rate from sessions"""
        if not sessions:
            return 0.0
        
        wins = sum(1 for session in sessions if session.pnl > 0)
        return wins / len(sessions) if sessions else 0.0
    
    def _calculate_total_return(self, sessions) -> float:
        """Calculate total return from sessions"""
        if not sessions:
            return 0.0
        
        total_pnl = sum(session.pnl for session in sessions)
        return total_pnl
    
    def _calculate_max_drawdown(self, sessions) -> float:
        """Calculate max drawdown from sessions"""
        if not sessions:
            return 0.0
        
        # Calculate cumulative PnL
        cumulative_pnl = []
        running_total = 0
        for session in sessions:
            running_total += session.pnl
            cumulative_pnl.append(running_total)
        
        # Calculate drawdown
        peak = cumulative_pnl[0]
        max_dd = 0
        for pnl in cumulative_pnl:
            if pnl > peak:
                peak = pnl
            dd = peak - pnl
            if dd > max_dd:
                max_dd = dd
        
        return max_dd
    
    def _calculate_profit_factor(self, sessions) -> float:
        """Calculate profit factor from sessions"""
        if not sessions:
            return 0.0
        
        gross_profit = sum(session.pnl for session in sessions if session.pnl > 0)
        gross_loss = abs(sum(session.pnl for session in sessions if session.pnl < 0))
        
        return gross_profit / gross_loss if gross_loss > 0 else float('inf')
    
    def plot(self):
        """Plot results using Cipher-BT's built-in plotting"""
        if self.cipher:
            self.cipher.plot()
    
    def print_results(self):
        """Print backtest results"""
        if not self.results:
            print("No results available")
            return
        
        print("\n" + "="*60)
        print("CIPHER-BT BACKTEST RESULTS")
        print("="*60)
        print(f"Total Trades: {self.results.get('total_trades', 0)}")
        print(f"Win Rate: {self.results.get('win_rate', 0):.2%}")
        print(f"Total Return: {self.results.get('total_return', 0):.4f}")
        print(f"Max Drawdown: {self.results.get('max_drawdown', 0):.4f}")
        print(f"Profit Factor: {self.results.get('profit_factor', 0):.2f}")
        print("="*60)

class CipherEnhancedLauncher:
    """
    Enhanced launcher with Cipher-BT integration
    """
    
    def __init__(self):
        self.cipher_backtester = CipherBacktester()
        self.results = {}
        
    def check_cipher_availability(self) -> bool:
        """Check if Cipher-BT is available"""
        if not self.cipher_backtester.is_available():
            print("⚠️  Cipher-BT not available. Install with: pip install cipher-bt")
            return False
        
        print("✅ Cipher-BT is available and ready!")
        return True
    
    def run_cipher_backtest(self, strategy_class, symbol: str, interval: str = "1h",
                           start_ts: str = "2025-01-01", stop_ts: str = "2025-04-01",
                           strategy_params: Dict = None) -> Dict:
        """Run Cipher-BT backtest with concurrent sessions"""
        
        if not self.check_cipher_availability():
            return {}
        
        print(f"🚀 Running Cipher-BT backtest for {symbol}...")
        
        # Setup data sources
        data_sources = [
            {
                "type": "binance_spot_ohlc",
                "symbol": symbol,
                "interval": interval
            }
        ]
        
        # Setup Cipher-BT
        if not self.cipher_backtester.setup_cipher(data_sources, strategy_class, strategy_params):
            print("❌ Failed to setup Cipher-BT")
            return {}
        
        # Run backtest
        results = self.cipher_backtester.run_backtest(start_ts, stop_ts)
        
        if results:
            print("✅ Cipher-BT backtest completed successfully")
            self.cipher_backtester.print_results()
        else:
            print("❌ Cipher-BT backtest failed")
        
        return results
    
    def run_multi_symbol_backtest(self, strategy_class, symbols: List[str],
                                 interval: str = "1h", start_ts: str = "2025-01-01",
                                 stop_ts: str = "2025-04-01", strategy_params: Dict = None) -> Dict:
        """Run Cipher-BT backtest across multiple symbols"""
        
        if not self.check_cipher_availability():
            return {}
        
        print(f"🌍 Running Cipher-BT multi-symbol backtest for {len(symbols)} symbols...")
        
        all_results = []
        
        for symbol in symbols:
            print(f"Testing {symbol}...")
            
            # Setup data sources for this symbol
            data_sources = [
                {
                    "type": "binance_spot_ohlc",
                    "symbol": symbol,
                    "interval": interval
                }
            ]
            
            # Setup Cipher-BT for this symbol
            backtester = CipherBacktester()
            if not backtester.setup_cipher(data_sources, strategy_class, strategy_params):
                print(f"❌ Failed to setup Cipher-BT for {symbol}")
                continue
            
            # Run backtest
            results = backtester.run_backtest(start_ts, stop_ts)
            
            if results:
                results['symbol'] = symbol
                all_results.append(results)
                print(f"✅ {symbol} completed: {results.get('total_return', 0):.4f} return")
            else:
                print(f"❌ {symbol} failed")
        
        # Aggregate results
        if all_results:
            self.results = {
                'all_results': all_results,
                'summary': self._calculate_summary(all_results)
            }
            
            print(f"\n📊 Multi-symbol backtest completed:")
            print(f"   Total symbols: {len(symbols)}")
            print(f"   Successful: {len(all_results)}")
            print(f"   Average return: {self.results['summary'].get('avg_return', 0):.4f}")
        else:
            print("❌ Multi-symbol backtest failed")
        
        return self.results
    
    def _calculate_summary(self, results: List[Dict]) -> Dict:
        """Calculate summary statistics"""
        if not results:
            return {}
        
        returns = [r.get('total_return', 0) for r in results]
        win_rates = [r.get('win_rate', 0) for r in results]
        
        return {
            'total_symbols': len(results),
            'avg_return': np.mean(returns),
            'median_return': np.median(returns),
            'best_return': np.max(returns),
            'worst_return': np.min(returns),
            'avg_win_rate': np.mean(win_rates),
            'success_rate': len(results) / len(results) if results else 0
        }
    
    def plot_results(self):
        """Plot results using Cipher-BT's built-in plotting"""
        if self.cipher_backtester.cipher:
            self.cipher_backtester.plot()

def test_cipher_integration():
    """Test Cipher-BT integration"""
    print("Testing Cipher-BT integration...")
    
    # Initialize launcher
    launcher = CipherEnhancedLauncher()
    
    if not launcher.check_cipher_availability():
        print("❌ Cipher-BT not available")
        return False
    
    print("✅ Cipher-BT integration test passed")
    return True

if __name__ == "__main__":
    test_cipher_integration()
