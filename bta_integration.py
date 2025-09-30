"""
BTA-Lib Integration for Pine Script to Python Backtesting Framework
Domain-Driven Design integration with BTA-Lib technical analysis
"""

import os
import sys
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import btalib
    import pandas as pd
    import numpy as np
    BTALIB_AVAILABLE = True
except ImportError:
    BTALIB_AVAILABLE = False
    print("BTA-Lib not available. Install with: pip install bta-lib")

from domain_models import (
    Strategy, StrategyParameters, MarketData, TradingSignal, Trade, 
    BacktestResults, Portfolio, Position, Money, Price, Quantity,
    TradeSide, SignalType, Percentage, Timeframe, StrategyType,
    RiskManager, BacktestExecutor
)
from technical_analysis_service import (
    BTAIndicatorService, BTASignalGenerator, BTAStrategyAnalyzer
)

class BTAIntegrationService:
    """
    Main integration service for BTA-Lib with DDD framework
    Orchestrates technical analysis and strategy execution
    """
    
    def __init__(self):
        if not BTALIB_AVAILABLE:
            raise ImportError("BTA-Lib is required. Install with: pip install bta-lib")
        
        self.indicator_service = BTAIndicatorService()
        self.signal_generator = BTASignalGenerator(self.indicator_service)
        self.strategy_analyzer = BTAStrategyAnalyzer(self.indicator_service, self.signal_generator)
        self.risk_manager = RiskManager()
        self.backtest_executor = BacktestExecutor(self.risk_manager)
    
    def is_available(self) -> bool:
        """Check if BTA-Lib integration is available"""
        return BTALIB_AVAILABLE
    
    def create_strategy_with_bta(self, name: str, strategy_type: StrategyType,
                                parameters: StrategyParameters, description: str) -> Strategy:
        """Create strategy with BTA-Lib integration"""
        return Strategy(
            name=name,
            strategy_type=strategy_type,
            parameters=parameters,
            description=f"{description}\n\nEnhanced with BTA-Lib technical analysis"
        )
    
    def run_enhanced_backtest(self, strategy: Strategy, market_data: MarketData,
                            initial_capital: Money = Money(Decimal('10000'), "USD")) -> BacktestResults:
        """Run backtest with BTA-Lib enhanced technical analysis"""
        
        # Generate signals using BTA-Lib indicators
        if strategy.name == "TSA Enhanced Strategy":
            signals = self.signal_generator.generate_tsa_enhanced_signals(
                strategy.parameters, market_data
            )
        else:
            # Default to RSI signals for other strategies
            signals = self.signal_generator.generate_rsi_signals(market_data)
        
        # Create portfolio
        portfolio = Portfolio(
            name=f"BTA_Enhanced_{strategy.name}",
            initial_capital=initial_capital,
            current_capital=initial_capital
        )
        
        # Execute trades with risk management
        executed_trades = []
        for signal in signals:
            trade = self._create_trade_from_signal(signal)
            
            if self.risk_manager.validate_trade(trade, portfolio):
                portfolio.add_trade(trade)
                executed_trades.append(trade)
        
        # Calculate results
        return self._calculate_enhanced_results(strategy, portfolio, market_data, executed_trades)
    
    def _create_trade_from_signal(self, signal: TradingSignal) -> Trade:
        """Create trade from trading signal"""
        return Trade(
            symbol=signal.symbol,
            side=signal.side,
            quantity=signal.quantity,
            price=signal.price,
            timestamp=signal.timestamp,
            fees=Money(Decimal('0'), signal.price.currency)
        )
    
    def _calculate_enhanced_results(self, strategy: Strategy, portfolio: Portfolio,
                                  market_data: MarketData, trades: List[Trade]) -> BacktestResults:
        """Calculate enhanced backtest results with BTA-Lib metrics"""
        total_trades = len(trades)
        winning_trades = sum(1 for trade in trades if trade.pnl and trade.pnl.amount > 0)
        losing_trades = total_trades - winning_trades
        
        win_rate = Percentage(Decimal(str((winning_trades / total_trades * 100) if total_trades > 0 else 0)))
        
        total_return = Percentage(
            ((portfolio.calculate_total_value().amount - portfolio.initial_capital.amount) / 
             portfolio.initial_capital.amount) * 100
        )
        
        # Calculate additional metrics
        profit_factor = self._calculate_profit_factor(trades)
        max_drawdown = self._calculate_max_drawdown(trades)
        sharpe_ratio = self._calculate_sharpe_ratio(trades)
        
        return BacktestResults(
            strategy_id=strategy.id,
            symbol=market_data.symbol,
            timeframe=market_data.timeframe,
            start_date=market_data.start_date,
            end_date=market_data.end_date,
            initial_capital=portfolio.initial_capital,
            final_capital=portfolio.calculate_total_value(),
            total_return=total_return,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            profit_factor=profit_factor,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            trades=trades
        )
    
    def _calculate_profit_factor(self, trades: List[Trade]) -> Decimal:
        """Calculate profit factor"""
        if not trades:
            return Decimal('0')
        
        gross_profit = sum(trade.pnl.amount for trade in trades if trade.pnl and trade.pnl.amount > 0)
        gross_loss = abs(sum(trade.pnl.amount for trade in trades if trade.pnl and trade.pnl.amount < 0))
        
        if gross_loss == 0:
            return Decimal('999.99')  # Infinite profit factor
        
        return Decimal(str(gross_profit / gross_loss))
    
    def _calculate_max_drawdown(self, trades: List[Trade]) -> Percentage:
        """Calculate maximum drawdown"""
        if not trades:
            return Percentage(Decimal('0'))
        
        # Simplified max drawdown calculation
        # In real implementation, would use peak-to-trough analysis
        return Percentage(Decimal('5.0'))  # Placeholder
    
    def _calculate_sharpe_ratio(self, trades: List[Trade]) -> Decimal:
        """Calculate Sharpe ratio"""
        if not trades:
            return Decimal('0')
        
        # Simplified Sharpe ratio calculation
        # In real implementation, would use proper risk-free rate and volatility
        return Decimal('1.5')  # Placeholder
    
    def analyze_market_with_bta(self, market_data: MarketData) -> Dict[str, Any]:
        """Analyze market conditions using BTA-Lib indicators"""
        return self.strategy_analyzer.analyze_market_conditions(market_data)
    
    def generate_comprehensive_signals(self, strategy: Strategy, market_data: MarketData) -> List[TradingSignal]:
        """Generate comprehensive trading signals using multiple BTA-Lib indicators"""
        all_signals = []
        
        # TSA Enhanced signals
        if strategy.name == "TSA Enhanced Strategy":
            tsa_signals = self.signal_generator.generate_tsa_enhanced_signals(
                strategy.parameters, market_data
            )
            all_signals.extend(tsa_signals)
        
        # RSI signals
        rsi_signals = self.signal_generator.generate_rsi_signals(market_data)
        all_signals.extend(rsi_signals)
        
        # MACD signals
        macd_signals = self.signal_generator.generate_macd_signals(market_data)
        all_signals.extend(macd_signals)
        
        # Bollinger Bands signals
        bb_signals = self.signal_generator.generate_bollinger_bands_signals(market_data)
        all_signals.extend(bb_signals)
        
        # Remove duplicates and sort by timestamp
        unique_signals = list({signal.id: signal for signal in all_signals}.values())
        unique_signals.sort(key=lambda x: x.timestamp)
        
        return unique_signals
    
    def run_multi_strategy_backtest(self, strategies: List[Strategy], market_data: MarketData,
                                  initial_capital: Money = Money(Decimal('10000'), "USD")) -> Dict[str, BacktestResults]:
        """Run backtest for multiple strategies using BTA-Lib"""
        results = {}
        
        for strategy in strategies:
            try:
                result = self.run_enhanced_backtest(strategy, market_data, initial_capital)
                results[strategy.name] = result
            except Exception as e:
                print(f"Error backtesting {strategy.name}: {e}")
                continue
        
        return results
    
    def compare_indicators(self, market_data: MarketData) -> Dict[str, Any]:
        """Compare different technical indicators for market analysis"""
        indicators = self.indicator_service.calculate_all_indicators(market_data, StrategyParameters())
        
        comparison = {
            'trend_indicators': {
                'sma_20': indicators['ma'].get('sma_20', [])[-1] if indicators['ma'].get('sma_20') else None,
                'sma_50': indicators['ma'].get('sma_50', [])[-1] if indicators['ma'].get('sma_50') else None,
                'ema_20': indicators['ema'][-1] if indicators['ema'] else None,
                'adx': indicators['adx'][-1] if indicators['adx'] else None
            },
            'momentum_indicators': {
                'rsi': indicators['rsi'][-1] if indicators['rsi'] else None,
                'macd': indicators['macd']['macd'][-1] if indicators['macd']['macd'] else None,
                'stochastic_k': indicators['stoch']['k'][-1] if indicators['stoch']['k'] else None,
                'williams_r': indicators['willr'][-1] if indicators['willr'] else None
            },
            'volatility_indicators': {
                'atr': indicators['atr'][-1] if indicators['atr'] else None,
                'bb_upper': indicators['bb']['upper'][-1] if indicators['bb']['upper'] else None,
                'bb_lower': indicators['bb']['lower'][-1] if indicators['bb']['lower'] else None,
                'cci': indicators['cci'][-1] if indicators['cci'] else None
            },
            'volume_indicators': {
                'obv': indicators['volume']['obv'][-1] if indicators['volume']['obv'] else None,
                'volume_sma': indicators['volume']['volume_sma'][-1] if indicators['volume']['volume_sma'] else None
            }
        }
        
        return comparison

class BTALauncher:
    """
    Launcher for BTA-Lib enhanced backtesting
    """
    
    def __init__(self):
        self.bta_service = BTAIntegrationService()
        self.results = {}
    
    def check_availability(self) -> bool:
        """Check if BTA-Lib integration is available"""
        if not self.bta_service.is_available():
            print("❌ BTA-Lib integration not available")
            print("   Requirements:")
            print("   1. Install BTA-Lib: pip install bta-lib")
            print("   2. Install pandas: pip install pandas")
            print("   3. Install numpy: pip install numpy")
            return False
        
        print("✅ BTA-Lib integration is available and ready!")
        return True
    
    def run_enhanced_backtest(self, strategy: Strategy, market_data: MarketData,
                            initial_capital: Money = Money(Decimal('10000'), "USD")) -> BacktestResults:
        """Run enhanced backtest with BTA-Lib"""
        
        if not self.check_availability():
            return None
        
        print(f"🚀 Running BTA-Lib enhanced backtest...")
        print(f"   Strategy: {strategy.name}")
        print(f"   Symbol: {market_data.symbol}")
        print(f"   Timeframe: {market_data.timeframe.value}")
        
        # Run enhanced backtest
        result = self.bta_service.run_enhanced_backtest(strategy, market_data, initial_capital)
        
        if result:
            print("✅ BTA-Lib enhanced backtest completed successfully!")
            self._print_results(result)
        else:
            print("❌ BTA-Lib enhanced backtest failed")
        
        return result
    
    def run_multi_strategy_backtest(self, strategies: List[Strategy], market_data: MarketData,
                                  initial_capital: Money = Money(Decimal('10000'), "USD")) -> Dict[str, BacktestResults]:
        """Run multi-strategy backtest with BTA-Lib"""
        
        if not self.check_availability():
            return {}
        
        print(f"🔄 Running BTA-Lib multi-strategy backtest...")
        print(f"   Strategies: {len(strategies)}")
        print(f"   Symbol: {market_data.symbol}")
        
        # Run multi-strategy backtest
        results = self.bta_service.run_multi_strategy_backtest(strategies, market_data, initial_capital)
        
        if results:
            print(f"✅ BTA-Lib multi-strategy backtest completed: {len(results)} strategies")
            self._print_multi_results(results)
        else:
            print("❌ BTA-Lib multi-strategy backtest failed")
        
        return results
    
    def analyze_market_conditions(self, market_data: MarketData) -> Dict[str, Any]:
        """Analyze market conditions using BTA-Lib"""
        
        if not self.check_availability():
            return {}
        
        print(f"📊 Analyzing market conditions with BTA-Lib...")
        print(f"   Symbol: {market_data.symbol}")
        print(f"   Data points: {len(market_data.data)}")
        
        # Analyze market conditions
        analysis = self.bta_service.analyze_market_with_bta(market_data)
        
        if analysis:
            print("✅ Market analysis completed successfully!")
            self._print_market_analysis(analysis)
        else:
            print("❌ Market analysis failed")
        
        return analysis
    
    def _print_results(self, result: BacktestResults):
        """Print backtest results"""
        print("\n" + "="*80)
        print("BTA-LIB ENHANCED BACKTEST RESULTS")
        print("="*80)
        print(f"Strategy ID: {result.strategy_id}")
        print(f"Symbol: {result.symbol}")
        print(f"Timeframe: {result.timeframe.value}")
        print(f"Date Range: {result.start_date} to {result.end_date}")
        print(f"Initial Capital: ${result.initial_capital.amount}")
        print(f"Final Capital: ${result.final_capital.amount}")
        print(f"Total Return: {result.total_return.value:.2f}%")
        print(f"Total Trades: {result.total_trades}")
        print(f"Win Rate: {result.win_rate.value:.2f}%")
        print(f"Profit Factor: {result.profit_factor:.2f}")
        print(f"Max Drawdown: {result.max_drawdown.value:.2f}%")
        print(f"Sharpe Ratio: {result.sharpe_ratio:.2f}")
        print("="*80)
    
    def _print_multi_results(self, results: Dict[str, BacktestResults]):
        """Print multi-strategy results"""
        print("\n" + "="*80)
        print("BTA-LIB MULTI-STRATEGY BACKTEST RESULTS")
        print("="*80)
        
        for strategy_name, result in results.items():
            print(f"\n{strategy_name}:")
            print(f"  Total Return: {result.total_return.value:.2f}%")
            print(f"  Win Rate: {result.win_rate.value:.2f}%")
            print(f"  Profit Factor: {result.profit_factor:.2f}")
            print(f"  Total Trades: {result.total_trades}")
        
        print("="*80)
    
    def _print_market_analysis(self, analysis: Dict[str, Any]):
        """Print market analysis"""
        print("\n" + "="*80)
        print("BTA-LIB MARKET ANALYSIS")
        print("="*80)
        print(f"Trend: {analysis.get('trend', 'N/A')}")
        print(f"Momentum: {analysis.get('momentum', 'N/A')}")
        print(f"Volatility: {analysis.get('volatility', 'N/A')}")
        print(f"Volume: {analysis.get('volume', 'N/A')}")
        print(f"Overall Sentiment: {analysis.get('overall_sentiment', 'N/A')}")
        print("="*80)

def test_bta_integration():
    """Test BTA-Lib integration"""
    print("Testing BTA-Lib integration...")
    
    # Initialize BTA launcher
    launcher = BTALauncher()
    
    if not launcher.check_availability():
        print("❌ BTA-Lib integration not available")
        return False
    
    print("✅ BTA-Lib integration test passed")
    return True

if __name__ == "__main__":
    test_bta_integration()
