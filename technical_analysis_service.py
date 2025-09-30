"""
Technical Analysis Service using BTA-Lib
Domain service for comprehensive technical analysis with BTA-Lib integration
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from decimal import Decimal
from datetime import datetime

try:
    import btalib
    BTALIB_AVAILABLE = True
except ImportError:
    BTALIB_AVAILABLE = False
    print("BTA-Lib not available. Install with: pip install bta-lib")

from domain_models import (
    MarketData, StrategyParameters, TradingSignal, TradeSide, SignalType,
    Price, Quantity, Percentage, Timeframe
)

class BTAIndicatorService:
    """
    Domain service for technical analysis using BTA-Lib
    Provides comprehensive technical indicators for trading strategies
    """
    
    def __init__(self):
        if not BTALIB_AVAILABLE:
            raise ImportError("BTA-Lib is required. Install with: pip install bta-lib")
        
        self.indicators = {}
        self.cache = {}
    
    def prepare_market_data(self, market_data: MarketData) -> pd.DataFrame:
        """Convert MarketData to pandas DataFrame for BTA-Lib"""
        if not market_data.data:
            return pd.DataFrame()
        
        df = pd.DataFrame(market_data.data)
        
        # Ensure required columns exist
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                if col == 'volume':
                    df[col] = 1000  # Default volume
                else:
                    df[col] = df['close']  # Use close as fallback
        
        # Convert to numeric
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Set datetime index if timestamp column exists
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
        
        return df
    
    def calculate_atr(self, market_data: MarketData, period: int = 14) -> List[Decimal]:
        """Calculate Average True Range using BTA-Lib"""
        df = self.prepare_market_data(market_data)
        if df.empty:
            return []
        
        try:
            atr = btalib.atr(df, period=period)
            return [Decimal(str(val)) for val in atr.df['atr'].tolist() if not pd.isna(val)]
        except Exception as e:
            print(f"Error calculating ATR: {e}")
            return []
    
    def calculate_adx(self, market_data: MarketData, period: int = 14) -> List[Decimal]:
        """Calculate Average Directional Index using BTA-Lib"""
        df = self.prepare_market_data(market_data)
        if df.empty:
            return []
        
        try:
            adx = btalib.adx(df, period=period)
            return [Decimal(str(val)) for val in adx.df['adx'].tolist() if not pd.isna(val)]
        except Exception as e:
            print(f"Error calculating ADX: {e}")
            return []
    
    def calculate_rsi(self, market_data: MarketData, period: int = 14) -> List[Decimal]:
        """Calculate Relative Strength Index using BTA-Lib"""
        df = self.prepare_market_data(market_data)
        if df.empty:
            return []
        
        try:
            rsi = btalib.rsi(df, period=period)
            return [Decimal(str(val)) for val in rsi.df['rsi'].tolist() if not pd.isna(val)]
        except Exception as e:
            print(f"Error calculating RSI: {e}")
            return []
    
    def calculate_macd(self, market_data: MarketData, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, List[Decimal]]:
        """Calculate MACD using BTA-Lib"""
        df = self.prepare_market_data(market_data)
        if df.empty:
            return {'macd': [], 'signal': [], 'histogram': []}
        
        try:
            macd = btalib.macd(df, fast=fast, slow=slow, signal=signal)
            return {
                'macd': [Decimal(str(val)) for val in macd.df['macd'].tolist() if not pd.isna(val)],
                'signal': [Decimal(str(val)) for val in macd.df['signal'].tolist() if not pd.isna(val)],
                'histogram': [Decimal(str(val)) for val in macd.df['histogram'].tolist() if not pd.isna(val)]
            }
        except Exception as e:
            print(f"Error calculating MACD: {e}")
            return {'macd': [], 'signal': [], 'histogram': []}
    
    def calculate_bollinger_bands(self, market_data: MarketData, period: int = 20, std: float = 2.0) -> Dict[str, List[Decimal]]:
        """Calculate Bollinger Bands using BTA-Lib"""
        df = self.prepare_market_data(market_data)
        if df.empty:
            return {'upper': [], 'middle': [], 'lower': []}
        
        try:
            bb = btalib.bbands(df, period=period, std=std)
            return {
                'upper': [Decimal(str(val)) for val in bb.df['upper'].tolist() if not pd.isna(val)],
                'middle': [Decimal(str(val)) for val in bb.df['middle'].tolist() if not pd.isna(val)],
                'lower': [Decimal(str(val)) for val in bb.df['lower'].tolist() if not pd.isna(val)]
            }
        except Exception as e:
            print(f"Error calculating Bollinger Bands: {e}")
            return {'upper': [], 'middle': [], 'lower': []}
    
    def calculate_stochastic(self, market_data: MarketData, k_period: int = 14, d_period: int = 3) -> Dict[str, List[Decimal]]:
        """Calculate Stochastic Oscillator using BTA-Lib"""
        df = self.prepare_market_data(market_data)
        if df.empty:
            return {'k': [], 'd': []}
        
        try:
            stoch = btalib.stoch(df, k_period=k_period, d_period=d_period)
            return {
                'k': [Decimal(str(val)) for val in stoch.df['k'].tolist() if not pd.isna(val)],
                'd': [Decimal(str(val)) for val in stoch.df['d'].tolist() if not pd.isna(val)]
            }
        except Exception as e:
            print(f"Error calculating Stochastic: {e}")
            return {'k': [], 'd': []}
    
    def calculate_williams_r(self, market_data: MarketData, period: int = 14) -> List[Decimal]:
        """Calculate Williams %R using BTA-Lib"""
        df = self.prepare_market_data(market_data)
        if df.empty:
            return []
        
        try:
            willr = btalib.willr(df, period=period)
            return [Decimal(str(val)) for val in willr.df['willr'].tolist() if not pd.isna(val)]
        except Exception as e:
            print(f"Error calculating Williams %R: {e}")
            return []
    
    def calculate_cci(self, market_data: MarketData, period: int = 14) -> List[Decimal]:
        """Calculate Commodity Channel Index using BTA-Lib"""
        df = self.prepare_market_data(market_data)
        if df.empty:
            return []
        
        try:
            cci = btalib.cci(df, period=period)
            return [Decimal(str(val)) for val in cci.df['cci'].tolist() if not pd.isna(val)]
        except Exception as e:
            print(f"Error calculating CCI: {e}")
            return []
    
    def calculate_moving_averages(self, market_data: MarketData, periods: List[int]) -> Dict[str, List[Decimal]]:
        """Calculate multiple moving averages using BTA-Lib"""
        df = self.prepare_market_data(market_data)
        if df.empty:
            return {}
        
        results = {}
        
        for period in periods:
            try:
                ma = btalib.sma(df, period=period)
                results[f'sma_{period}'] = [Decimal(str(val)) for val in ma.df[f'sma_{period}'].tolist() if not pd.isna(val)]
            except Exception as e:
                print(f"Error calculating SMA {period}: {e}")
                results[f'sma_{period}'] = []
        
        return results
    
    def calculate_ema(self, market_data: MarketData, period: int) -> List[Decimal]:
        """Calculate Exponential Moving Average using BTA-Lib"""
        df = self.prepare_market_data(market_data)
        if df.empty:
            return []
        
        try:
            ema = btalib.ema(df, period=period)
            return [Decimal(str(val)) for val in ema.df[f'ema_{period}'].tolist() if not pd.isna(val)]
        except Exception as e:
            print(f"Error calculating EMA {period}: {e}")
            return []
    
    def calculate_volume_indicators(self, market_data: MarketData) -> Dict[str, List[Decimal]]:
        """Calculate volume-based indicators using BTA-Lib"""
        df = self.prepare_market_data(market_data)
        if df.empty:
            return {}
        
        results = {}
        
        try:
            # On Balance Volume
            obv = btalib.obv(df)
            results['obv'] = [Decimal(str(val)) for val in obv.df['obv'].tolist() if not pd.isna(val)]
        except Exception as e:
            print(f"Error calculating OBV: {e}")
            results['obv'] = []
        
        try:
            # Volume SMA
            vol_sma = btalib.sma(df['volume'], period=20)
            results['volume_sma'] = [Decimal(str(val)) for val in vol_sma.df['sma_20'].tolist() if not pd.isna(val)]
        except Exception as e:
            print(f"Error calculating Volume SMA: {e}")
            results['volume_sma'] = []
        
        return results
    
    def calculate_momentum_indicators(self, market_data: MarketData) -> Dict[str, List[Decimal]]:
        """Calculate momentum indicators using BTA-Lib"""
        df = self.prepare_market_data(market_data)
        if df.empty:
            return {}
        
        results = {}
        
        try:
            # Rate of Change
            roc = btalib.roc(df, period=10)
            results['roc'] = [Decimal(str(val)) for val in roc.df['roc'].tolist() if not pd.isna(val)]
        except Exception as e:
            print(f"Error calculating ROC: {e}")
            results['roc'] = []
        
        try:
            # Momentum
            mom = btalib.mom(df, period=10)
            results['momentum'] = [Decimal(str(val)) for val in mom.df['mom'].tolist() if not pd.isna(val)]
        except Exception as e:
            print(f"Error calculating Momentum: {e}")
            results['momentum'] = []
        
        return results
    
    def calculate_all_indicators(self, market_data: MarketData, 
                               strategy_params: StrategyParameters) -> Dict[str, Any]:
        """Calculate all indicators needed for strategy analysis"""
        indicators = {}
        
        # Basic indicators
        indicators['atr'] = self.calculate_atr(market_data, strategy_params.atr_length)
        indicators['adx'] = self.calculate_adx(market_data, strategy_params.adx_length)
        indicators['rsi'] = self.calculate_rsi(market_data, 14)
        
        # MACD
        indicators['macd'] = self.calculate_macd(market_data)
        
        # Bollinger Bands
        indicators['bb'] = self.calculate_bollinger_bands(market_data)
        
        # Stochastic
        indicators['stoch'] = self.calculate_stochastic(market_data)
        
        # Williams %R
        indicators['willr'] = self.calculate_williams_r(market_data)
        
        # CCI
        indicators['cci'] = self.calculate_cci(market_data)
        
        # Moving Averages
        indicators['ma'] = self.calculate_moving_averages(market_data, [20, 50, 200])
        indicators['ema'] = self.calculate_ema(market_data, 20)
        
        # Volume indicators
        indicators['volume'] = self.calculate_volume_indicators(market_data)
        
        # Momentum indicators
        indicators['momentum'] = self.calculate_momentum_indicators(market_data)
        
        return indicators

class BTASignalGenerator:
    """
    Domain service for generating trading signals using BTA-Lib indicators
    """
    
    def __init__(self, indicator_service: BTAIndicatorService):
        self.indicator_service = indicator_service
    
    def generate_tsa_enhanced_signals(self, strategy_params: StrategyParameters, 
                                     market_data: MarketData) -> List[TradingSignal]:
        """Generate TSA Enhanced Strategy signals using BTA-Lib indicators"""
        signals = []
        
        # Calculate all indicators
        indicators = self.indicator_service.calculate_all_indicators(market_data, strategy_params)
        
        # Get data length
        data_length = len(market_data.data)
        if data_length == 0:
            return signals
        
        # Generate signals based on TSA Enhanced Strategy logic
        for i in range(max(strategy_params.atr_length, strategy_params.adx_length, 20), data_length):
            try:
                # Get current price
                current_price = Decimal(str(market_data.data[i]['close']))
                
                # Get indicators (use latest available values)
                atr_idx = min(i - strategy_params.atr_length, len(indicators['atr']) - 1)
                adx_idx = min(i - strategy_params.adx_length, len(indicators['adx']) - 1)
                ma_idx = min(i - 20, len(indicators['ma'].get('sma_20', [])) - 1)
                
                if (atr_idx < 0 or adx_idx < 0 or ma_idx < 0 or 
                    atr_idx >= len(indicators['atr']) or 
                    adx_idx >= len(indicators['adx']) or 
                    ma_idx >= len(indicators['ma'].get('sma_20', []))):
                    continue
                
                atr = indicators['atr'][atr_idx]
                adx = indicators['adx'][adx_idx]
                sma_20 = indicators['ma']['sma_20'][ma_idx]
                
                # TSA Enhanced Strategy entry conditions
                if (current_price > sma_20 and 
                    adx > strategy_params.adx_threshold and
                    current_price > current_price - atr * strategy_params.atr_multiplier):
                    
                    signal = TradingSignal(
                        symbol=market_data.symbol,
                        side=TradeSide.BUY,
                        signal_type=SignalType.ENTRY_LONG,
                        price=Price(current_price),
                        quantity=Quantity(Decimal('1.0')),
                        timestamp=datetime.now(),
                        confidence=Percentage(Decimal('75.0')),
                        reason="TSA Enhanced Strategy - Long Entry (BTA-Lib)",
                        metadata={
                            'atr': float(atr),
                            'adx': float(adx),
                            'sma_20': float(sma_20),
                            'strategy': 'tsa_enhanced'
                        }
                    )
                    signals.append(signal)
                
            except Exception as e:
                print(f"Error generating signal at index {i}: {e}")
                continue
        
        return signals
    
    def generate_rsi_signals(self, market_data: MarketData, 
                           oversold: Decimal = Decimal('30'), 
                           overbought: Decimal = Decimal('70')) -> List[TradingSignal]:
        """Generate RSI-based signals using BTA-Lib"""
        signals = []
        
        rsi_values = self.indicator_service.calculate_rsi(market_data, 14)
        if not rsi_values:
            return signals
        
        for i, rsi in enumerate(rsi_values):
            if i >= len(market_data.data):
                break
            
            current_price = Decimal(str(market_data.data[i]['close']))
            
            # RSI oversold - buy signal
            if rsi < oversold:
                signal = TradingSignal(
                    symbol=market_data.symbol,
                    side=TradeSide.BUY,
                    signal_type=SignalType.ENTRY_LONG,
                    price=Price(current_price),
                    quantity=Quantity(Decimal('1.0')),
                    timestamp=datetime.now(),
                    confidence=Percentage(Decimal('80.0')),
                    reason=f"RSI Oversold - {float(rsi):.2f}",
                    metadata={'rsi': float(rsi), 'strategy': 'rsi_oversold'}
                )
                signals.append(signal)
            
            # RSI overbought - sell signal
            elif rsi > overbought:
                signal = TradingSignal(
                    symbol=market_data.symbol,
                    side=TradeSide.SELL,
                    signal_type=SignalType.ENTRY_SHORT,
                    price=Price(current_price),
                    quantity=Quantity(Decimal('1.0')),
                    timestamp=datetime.now(),
                    confidence=Percentage(Decimal('80.0')),
                    reason=f"RSI Overbought - {float(rsi):.2f}",
                    metadata={'rsi': float(rsi), 'strategy': 'rsi_overbought'}
                )
                signals.append(signal)
        
        return signals
    
    def generate_macd_signals(self, market_data: MarketData) -> List[TradingSignal]:
        """Generate MACD-based signals using BTA-Lib"""
        signals = []
        
        macd_data = self.indicator_service.calculate_macd(market_data)
        macd_values = macd_data.get('macd', [])
        signal_values = macd_data.get('signal', [])
        
        if not macd_values or not signal_values:
            return signals
        
        for i in range(1, min(len(macd_values), len(signal_values), len(market_data.data))):
            try:
                current_price = Decimal(str(market_data.data[i]['close']))
                macd = macd_values[i]
                signal = signal_values[i]
                prev_macd = macd_values[i-1]
                prev_signal = signal_values[i-1]
                
                # MACD crossover signals
                if (prev_macd <= prev_signal and macd > signal):  # Bullish crossover
                    signal = TradingSignal(
                        symbol=market_data.symbol,
                        side=TradeSide.BUY,
                        signal_type=SignalType.ENTRY_LONG,
                        price=Price(current_price),
                        quantity=Quantity(Decimal('1.0')),
                        timestamp=datetime.now(),
                        confidence=Percentage(Decimal('70.0')),
                        reason="MACD Bullish Crossover",
                        metadata={
                            'macd': float(macd),
                            'signal': float(signal),
                            'strategy': 'macd_crossover'
                        }
                    )
                    signals.append(signal)
                
                elif (prev_macd >= prev_signal and macd < signal):  # Bearish crossover
                    signal = TradingSignal(
                        symbol=market_data.symbol,
                        side=TradeSide.SELL,
                        signal_type=SignalType.ENTRY_SHORT,
                        price=Price(current_price),
                        quantity=Quantity(Decimal('1.0')),
                        timestamp=datetime.now(),
                        confidence=Percentage(Decimal('70.0')),
                        reason="MACD Bearish Crossover",
                        metadata={
                            'macd': float(macd),
                            'signal': float(signal),
                            'strategy': 'macd_crossover'
                        }
                    )
                    signals.append(signal)
                
            except Exception as e:
                print(f"Error generating MACD signal at index {i}: {e}")
                continue
        
        return signals
    
    def generate_bollinger_bands_signals(self, market_data: MarketData) -> List[TradingSignal]:
        """Generate Bollinger Bands signals using BTA-Lib"""
        signals = []
        
        bb_data = self.indicator_service.calculate_bollinger_bands(market_data)
        upper_band = bb_data.get('upper', [])
        lower_band = bb_data.get('lower', [])
        
        if not upper_band or not lower_band:
            return signals
        
        for i in range(len(upper_band)):
            if i >= len(market_data.data):
                break
            
            try:
                current_price = Decimal(str(market_data.data[i]['close']))
                upper = upper_band[i]
                lower = lower_band[i]
                
                # Price breaks above upper band - sell signal
                if current_price > upper:
                    signal = TradingSignal(
                        symbol=market_data.symbol,
                        side=TradeSide.SELL,
                        signal_type=SignalType.ENTRY_SHORT,
                        price=Price(current_price),
                        quantity=Quantity(Decimal('1.0')),
                        timestamp=datetime.now(),
                        confidence=Percentage(Decimal('75.0')),
                        reason="Price above Bollinger Upper Band",
                        metadata={
                            'upper_band': float(upper),
                            'lower_band': float(lower),
                            'strategy': 'bollinger_bands'
                        }
                    )
                    signals.append(signal)
                
                # Price breaks below lower band - buy signal
                elif current_price < lower:
                    signal = TradingSignal(
                        symbol=market_data.symbol,
                        side=TradeSide.BUY,
                        signal_type=SignalType.ENTRY_LONG,
                        price=Price(current_price),
                        quantity=Quantity(Decimal('1.0')),
                        timestamp=datetime.now(),
                        confidence=Percentage(Decimal('75.0')),
                        reason="Price below Bollinger Lower Band",
                        metadata={
                            'upper_band': float(upper),
                            'lower_band': float(lower),
                            'strategy': 'bollinger_bands'
                        }
                    )
                    signals.append(signal)
                
            except Exception as e:
                print(f"Error generating Bollinger Bands signal at index {i}: {e}")
                continue
        
        return signals

class BTAStrategyAnalyzer:
    """
    Domain service for comprehensive strategy analysis using BTA-Lib
    """
    
    def __init__(self, indicator_service: BTAIndicatorService, signal_generator: BTASignalGenerator):
        self.indicator_service = indicator_service
        self.signal_generator = signal_generator
    
    def analyze_market_conditions(self, market_data: MarketData) -> Dict[str, Any]:
        """Analyze overall market conditions using BTA-Lib indicators"""
        indicators = self.indicator_service.calculate_all_indicators(market_data, StrategyParameters())
        
        analysis = {
            'trend': self._analyze_trend(indicators),
            'momentum': self._analyze_momentum(indicators),
            'volatility': self._analyze_volatility(indicators),
            'volume': self._analyze_volume(indicators),
            'overall_sentiment': 'neutral'
        }
        
        # Determine overall sentiment
        if (analysis['trend'] == 'bullish' and 
            analysis['momentum'] == 'strong' and 
            analysis['volume'] == 'high'):
            analysis['overall_sentiment'] = 'very_bullish'
        elif (analysis['trend'] == 'bearish' and 
              analysis['momentum'] == 'weak' and 
              analysis['volume'] == 'high'):
            analysis['overall_sentiment'] = 'very_bearish'
        
        return analysis
    
    def _analyze_trend(self, indicators: Dict[str, Any]) -> str:
        """Analyze trend using moving averages and ADX"""
        sma_20 = indicators['ma'].get('sma_20', [])
        sma_50 = indicators['ma'].get('sma_50', [])
        adx = indicators['adx']
        
        if not sma_20 or not sma_50 or not adx:
            return 'neutral'
        
        # Use latest values
        latest_sma_20 = sma_20[-1] if sma_20 else Decimal('0')
        latest_sma_50 = sma_50[-1] if sma_50 else Decimal('0')
        latest_adx = adx[-1] if adx else Decimal('0')
        
        if latest_sma_20 > latest_sma_50 and latest_adx > 25:
            return 'bullish'
        elif latest_sma_20 < latest_sma_50 and latest_adx > 25:
            return 'bearish'
        else:
            return 'neutral'
    
    def _analyze_momentum(self, indicators: Dict[str, Any]) -> str:
        """Analyze momentum using RSI and MACD"""
        rsi = indicators['rsi']
        macd = indicators['macd']
        
        if not rsi or not macd:
            return 'neutral'
        
        latest_rsi = rsi[-1] if rsi else Decimal('50')
        latest_macd = macd['macd'][-1] if macd['macd'] else Decimal('0')
        latest_signal = macd['signal'][-1] if macd['signal'] else Decimal('0')
        
        if latest_rsi > 50 and latest_macd > latest_signal:
            return 'strong'
        elif latest_rsi < 50 and latest_macd < latest_signal:
            return 'weak'
        else:
            return 'neutral'
    
    def _analyze_volatility(self, indicators: Dict[str, Any]) -> str:
        """Analyze volatility using ATR and Bollinger Bands"""
        atr = indicators['atr']
        bb = indicators['bb']
        
        if not atr or not bb:
            return 'normal'
        
        latest_atr = atr[-1] if atr else Decimal('0')
        upper_band = bb['upper'][-1] if bb['upper'] else Decimal('0')
        lower_band = bb['lower'][-1] if bb['lower'] else Decimal('0')
        
        # Simplified volatility analysis
        bb_width = upper_band - lower_band
        if bb_width > latest_atr * 2:
            return 'high'
        elif bb_width < latest_atr * 0.5:
            return 'low'
        else:
            return 'normal'
    
    def _analyze_volume(self, indicators: Dict[str, Any]) -> str:
        """Analyze volume using volume indicators"""
        volume_indicators = indicators['volume']
        obv = volume_indicators.get('obv', [])
        volume_sma = volume_indicators.get('volume_sma', [])
        
        if not obv or not volume_sma:
            return 'normal'
        
        # Simplified volume analysis
        latest_obv = obv[-1] if obv else Decimal('0')
        latest_volume_sma = volume_sma[-1] if volume_sma else Decimal('0')
        
        if latest_obv > latest_volume_sma * 1.5:
            return 'high'
        elif latest_obv < latest_volume_sma * 0.5:
            return 'low'
        else:
            return 'normal'
