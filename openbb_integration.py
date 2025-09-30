"""
OpenBB Integration for Pine Script to Python Backtesting Framework
Enhanced data access and analysis using OpenBB Platform
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

try:
    from openbb import obb
    OPENBB_AVAILABLE = True
except ImportError:
    OPENBB_AVAILABLE = False
    print("OpenBB not available. Install with: pip install openbb")

class OpenBBDataProvider:
    """
    OpenBB data provider for enhanced financial data access
    Integrates with our Pine Script to Python backtesting framework
    """
    
    def __init__(self):
        self.obb = obb if OPENBB_AVAILABLE else None
        self.data_cache = {}
        
    def is_available(self) -> bool:
        """Check if OpenBB is available"""
        return OPENBB_AVAILABLE and self.obb is not None
    
    def get_equity_data(self, symbol: str, start_date: str, end_date: str, 
                       interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Get equity data using OpenBB
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            interval: Data interval (1m, 5m, 15m, 1h, 1d)
            
        Returns:
            DataFrame with OHLCV data
        """
        if not self.is_available():
            print("OpenBB not available")
            return None
        
        try:
            # Get historical data
            output = self.obb.equity.price.historical(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                interval=interval
            )
            
            df = output.to_dataframe()
            
            # Standardize column names
            df.columns = [col.lower() for col in df.columns]
            
            # Ensure we have required columns
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            if not all(col in df.columns for col in required_cols):
                print(f"Missing required columns for {symbol}")
                return None
            
            return df
            
        except Exception as e:
            print(f"Error getting equity data for {symbol}: {e}")
            return None
    
    def get_crypto_data(self, symbol: str, start_date: str, end_date: str,
                       interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Get cryptocurrency data using OpenBB
        
        Args:
            symbol: Crypto symbol (e.g., 'BTC-USD')
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            interval: Data interval
            
        Returns:
            DataFrame with OHLCV data
        """
        if not self.is_available():
            print("OpenBB not available")
            return None
        
        try:
            # Get crypto data
            output = self.obb.crypto.price.historical(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                interval=interval
            )
            
            df = output.to_dataframe()
            
            # Standardize column names
            df.columns = [col.lower() for col in df.columns]
            
            return df
            
        except Exception as e:
            print(f"Error getting crypto data for {symbol}: {e}")
            return None
    
    def get_forex_data(self, symbol: str, start_date: str, end_date: str,
                      interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Get forex data using OpenBB
        
        Args:
            symbol: Forex pair (e.g., 'EURUSD')
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            interval: Data interval
            
        Returns:
            DataFrame with OHLCV data
        """
        if not self.is_available():
            print("OpenBB not available")
            return None
        
        try:
            # Get forex data
            output = self.obb.forex.price.historical(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                interval=interval
            )
            
            df = output.to_dataframe()
            
            # Standardize column names
            df.columns = [col.lower() for col in df.columns]
            
            return df
            
        except Exception as e:
            print(f"Error getting forex data for {symbol}: {e}")
            return None
    
    def get_macro_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        Get macroeconomic data using OpenBB
        
        Args:
            symbol: Macro indicator symbol
            start_date: Start date
            end_date: End date
            
        Returns:
            DataFrame with macro data
        """
        if not self.is_available():
            print("OpenBB not available")
            return None
        
        try:
            # Get macro data
            output = self.obb.economy.macro(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date
            )
            
            df = output.to_dataframe()
            return df
            
        except Exception as e:
            print(f"Error getting macro data for {symbol}: {e}")
            return None
    
    def get_technical_indicators(self, data: pd.DataFrame, indicators: List[str]) -> pd.DataFrame:
        """
        Get technical indicators using OpenBB
        
        Args:
            data: OHLCV DataFrame
            indicators: List of indicator names
            
        Returns:
            DataFrame with technical indicators
        """
        if not self.is_available():
            print("OpenBB not available")
            return data
        
        try:
            # Add technical indicators
            for indicator in indicators:
                if indicator == 'rsi':
                    data['rsi'] = self.obb.technical.rsi(data)
                elif indicator == 'macd':
                    macd_data = self.obb.technical.macd(data)
                    data['macd'] = macd_data['macd']
                    data['macd_signal'] = macd_data['signal']
                    data['macd_histogram'] = macd_data['histogram']
                elif indicator == 'bollinger':
                    bb_data = self.obb.technical.bollinger_bands(data)
                    data['bb_upper'] = bb_data['upper']
                    data['bb_middle'] = bb_data['middle']
                    data['bb_lower'] = bb_data['lower']
                elif indicator == 'atr':
                    data['atr'] = self.obb.technical.atr(data)
                elif indicator == 'adx':
                    data['adx'] = self.obb.technical.adx(data)
            
            return data
            
        except Exception as e:
            print(f"Error calculating technical indicators: {e}")
            return data
    
    def get_market_sentiment(self, symbol: str) -> Dict:
        """
        Get market sentiment data using OpenBB
        
        Args:
            symbol: Symbol to analyze
            
        Returns:
            Dictionary with sentiment data
        """
        if not self.is_available():
            print("OpenBB not available")
            return {}
        
        try:
            # Get sentiment data
            sentiment_data = self.obb.news.sentiment(symbol=symbol)
            
            return {
                'sentiment_score': sentiment_data.get('sentiment_score', 0),
                'sentiment_label': sentiment_data.get('sentiment_label', 'neutral'),
                'news_count': sentiment_data.get('news_count', 0)
            }
            
        except Exception as e:
            print(f"Error getting sentiment data for {symbol}: {e}")
            return {}
    
    def get_earnings_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        Get earnings data using OpenBB
        
        Args:
            symbol: Stock symbol
            
        Returns:
            DataFrame with earnings data
        """
        if not self.is_available():
            print("OpenBB not available")
            return None
        
        try:
            # Get earnings data
            output = self.obb.equity.fundamental.earnings(symbol=symbol)
            df = output.to_dataframe()
            return df
            
        except Exception as e:
            print(f"Error getting earnings data for {symbol}: {e}")
            return None
    
    def get_financial_ratios(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        Get financial ratios using OpenBB
        
        Args:
            symbol: Stock symbol
            
        Returns:
            DataFrame with financial ratios
        """
        if not self.is_available():
            print("OpenBB not available")
            return None
        
        try:
            # Get financial ratios
            output = self.obb.equity.fundamental.ratios(symbol=symbol)
            df = output.to_dataframe()
            return df
            
        except Exception as e:
            print(f"Error getting financial ratios for {symbol}: {e}")
            return None

class OpenBBEnhancedBacktester:
    """
    Enhanced backtester with OpenBB integration
    Extends our existing backtesting framework with OpenBB data
    """
    
    def __init__(self):
        self.data_provider = OpenBBDataProvider()
        self.results = {}
        
    def get_enhanced_data(self, symbol: str, start_date: str, end_date: str,
                         interval: str = "1d", market_type: str = "equity") -> Optional[pd.DataFrame]:
        """
        Get enhanced data with OpenBB integration
        
        Args:
            symbol: Symbol to get data for
            start_date: Start date
            end_date: End date
            interval: Data interval
            market_type: Type of market (equity, crypto, forex)
            
        Returns:
            Enhanced DataFrame with additional data
        """
        # Get base OHLCV data
        if market_type == "equity":
            data = self.data_provider.get_equity_data(symbol, start_date, end_date, interval)
        elif market_type == "crypto":
            data = self.data_provider.get_crypto_data(symbol, start_date, end_date, interval)
        elif market_type == "forex":
            data = self.data_provider.get_forex_data(symbol, start_date, end_date, interval)
        else:
            print(f"Unknown market type: {market_type}")
            return None
        
        if data is None:
            return None
        
        # Add technical indicators
        indicators = ['rsi', 'macd', 'bollinger', 'atr', 'adx']
        data = self.data_provider.get_technical_indicators(data, indicators)
        
        # Add sentiment data (for equity markets)
        if market_type == "equity":
            sentiment = self.data_provider.get_market_sentiment(symbol)
            if sentiment:
                data['sentiment_score'] = sentiment.get('sentiment_score', 0)
                data['sentiment_label'] = sentiment.get('sentiment_label', 'neutral')
        
        return data
    
    def run_enhanced_backtest(self, strategy_class, symbol: str, start_date: str, end_date: str,
                             interval: str = "1d", market_type: str = "equity",
                             strategy_params: Dict = None) -> Dict:
        """
        Run enhanced backtest with OpenBB data
        
        Args:
            strategy_class: Strategy class to test
            symbol: Symbol to test
            start_date: Start date
            end_date: End date
            interval: Data interval
            market_type: Market type
            strategy_params: Strategy parameters
            
        Returns:
            Backtest results
        """
        if not self.data_provider.is_available():
            print("OpenBB not available. Falling back to yfinance...")
            # Fallback to yfinance
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date, interval=interval)
            data.columns = [col.lower() for col in data.columns]
        else:
            # Use OpenBB enhanced data
            data = self.get_enhanced_data(symbol, start_date, end_date, interval, market_type)
        
        if data is None or data.empty:
            print(f"No data available for {symbol}")
            return {}
        
        # Initialize strategy
        if strategy_params is None:
            strategy_params = {}
        
        strategy = strategy_class(data, **strategy_params)
        
        # Run backtest
        results = strategy.run_backtest()
        
        # Add OpenBB-specific metrics
        if self.data_provider.is_available():
            results['data_source'] = 'OpenBB'
            results['enhanced_features'] = True
        else:
            results['data_source'] = 'yfinance'
            results['enhanced_features'] = False
        
        return results
    
    def run_multi_market_backtest(self, strategy_class, symbols: List[str], 
                                 start_date: str, end_date: str,
                                 interval: str = "1d", market_types: List[str] = None,
                                 strategy_params: Dict = None) -> Dict:
        """
        Run backtest across multiple markets with OpenBB
        
        Args:
            strategy_class: Strategy class to test
            symbols: List of symbols to test
            start_date: Start date
            end_date: End date
            interval: Data interval
            market_types: List of market types
            strategy_params: Strategy parameters
            
        Returns:
            Comprehensive backtest results
        """
        if market_types is None:
            market_types = ['equity'] * len(symbols)
        
        results = {
            'all_results': [],
            'successful_results': [],
            'failed_results': [],
            'summary': {}
        }
        
        for symbol, market_type in zip(symbols, market_types):
            print(f"Testing {symbol} ({market_type})...")
            
            try:
                result = self.run_enhanced_backtest(
                    strategy_class, symbol, start_date, end_date,
                    interval, market_type, strategy_params
                )
                
                if result:
                    result['symbol'] = symbol
                    result['market_type'] = market_type
                    results['all_results'].append(result)
                    results['successful_results'].append(result)
                else:
                    results['failed_results'].append({
                        'symbol': symbol,
                        'market_type': market_type,
                        'error': 'No data available'
                    })
                    
            except Exception as e:
                results['failed_results'].append({
                    'symbol': symbol,
                    'market_type': market_type,
                    'error': str(e)
                })
        
        # Calculate summary
        if results['successful_results']:
            returns = [r.get('total_return', 0) for r in results['successful_results']]
            results['summary'] = {
                'total_tests': len(results['all_results']),
                'successful_tests': len(results['successful_results']),
                'success_rate': len(results['successful_results']) / len(results['all_results']),
                'avg_return': np.mean(returns),
                'median_return': np.median(returns),
                'best_return': np.max(returns),
                'worst_return': np.min(returns)
            }
        
        return results

def test_openbb_integration():
    """Test OpenBB integration"""
    print("Testing OpenBB integration...")
    
    # Initialize OpenBB data provider
    provider = OpenBBDataProvider()
    
    if not provider.is_available():
        print("OpenBB not available. Please install with: pip install openbb")
        return False
    
    print("✓ OpenBB is available")
    
    # Test equity data
    print("Testing equity data...")
    equity_data = provider.get_equity_data("AAPL", "2023-01-01", "2023-12-31", "1d")
    if equity_data is not None:
        print(f"✓ Equity data loaded: {len(equity_data)} bars")
    else:
        print("✗ Failed to load equity data")
    
    # Test crypto data
    print("Testing crypto data...")
    crypto_data = provider.get_crypto_data("BTC-USD", "2023-01-01", "2023-12-31", "1d")
    if crypto_data is not None:
        print(f"✓ Crypto data loaded: {len(crypto_data)} bars")
    else:
        print("✗ Failed to load crypto data")
    
    # Test enhanced backtester
    print("Testing enhanced backtester...")
    backtester = OpenBBEnhancedBacktester()
    
    # Test with TSA Enhanced Strategy
    from tsa_enhanced_strategy import TSAEnhancedStrategy
    
    results = backtester.run_enhanced_backtest(
        TSAEnhancedStrategy,
        symbol="AAPL",
        start_date="2023-01-01",
        end_date="2023-12-31",
        market_type="equity"
    )
    
    if results:
        print("✓ Enhanced backtest completed")
        print(f"  Total return: {results.get('total_return', 0):.4f}")
        print(f"  Data source: {results.get('data_source', 'unknown')}")
        print(f"  Enhanced features: {results.get('enhanced_features', False)}")
    else:
        print("✗ Enhanced backtest failed")
    
    return True

if __name__ == "__main__":
    test_openbb_integration()
