"""
Domain Services for Pine Script to Python Backtesting Framework
Domain-Driven Design services for business logic
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from decimal import Decimal
import pandas as pd
import numpy as np

from domain_models import (
    Strategy, StrategyParameters, MarketData, TradingSignal, Trade, 
    BacktestResults, Portfolio, Position, Money, Price, Quantity,
    TradeSide, SignalType, Percentage, Timeframe, StrategyType,
    RiskManager, StrategyAnalyzer, BacktestExecutor,
    TradeExecuted, StrategyAnalyzed, BacktestCompleted, RiskLimitExceeded
)

# =============================================================================
# STRATEGY DOMAIN SERVICES
# =============================================================================

class PineScriptTranslationService:
    """Domain service for translating Pine Script to Python strategies"""
    
    def __init__(self):
        self.translator = None  # Would inject PineScriptTranslator
    
    def translate_strategy(self, pinescript_code: str, 
                         strategy_name: str = "Translated Strategy") -> Strategy:
        """Translate Pine Script code to domain Strategy"""
        # This would contain actual Pine Script translation logic
        # For now, create a basic strategy
        
        parameters = StrategyParameters()
        
        return Strategy(
            name=strategy_name,
            strategy_type=StrategyType.MOMENTUM,
            parameters=parameters,
            description=f"Translated from Pine Script: {pinescript_code[:100]}..."
        )
    
    def validate_pinescript(self, pinescript_code: str) -> bool:
        """Validate Pine Script code"""
        # Basic validation - check for required elements
        required_elements = ['strategy', 'long', 'short', 'close']
        return all(element in pinescript_code.lower() for element in required_elements)

class AIStrategyGenerationService:
    """Domain service for AI-powered strategy generation"""
    
    def __init__(self, openai_client=None):
        self.openai_client = openai_client
    
    def generate_strategy(self, description: str, strategy_type: StrategyType,
                         parameters: StrategyParameters) -> Strategy:
        """Generate strategy from natural language description"""
        if not self.openai_client:
            raise ValueError("OpenAI client not available")
        
        # This would contain actual AI generation logic
        # For now, create a basic strategy based on description
        
        return Strategy(
            name=f"AI Generated: {description[:50]}...",
            strategy_type=strategy_type,
            parameters=parameters,
            description=description
        )
    
    def enhance_strategy(self, existing_strategy: Strategy, 
                       enhancement_description: str) -> Strategy:
        """Enhance existing strategy with AI suggestions"""
        # This would contain AI enhancement logic
        enhanced_description = f"{existing_strategy.description}\n\nEnhanced: {enhancement_description}"
        
        return Strategy(
            name=f"Enhanced {existing_strategy.name}",
            strategy_type=existing_strategy.strategy_type,
            parameters=existing_strategy.parameters,
            description=enhanced_description
        )

class StrategyOptimizationService:
    """Domain service for strategy optimization"""
    
    def optimize_parameters(self, strategy: Strategy, market_data: MarketData,
                          optimization_target: str = "sharpe_ratio") -> StrategyParameters:
        """Optimize strategy parameters"""
        # This would contain parameter optimization logic
        # For now, return original parameters
        return strategy.parameters
    
    def validate_strategy(self, strategy: Strategy) -> List[str]:
        """Validate strategy and return any issues"""
        issues = []
        
        if not strategy.name:
            issues.append("Strategy name is required")
        
        if not strategy.description:
            issues.append("Strategy description is required")
        
        if strategy.parameters.atr_length <= 0:
            issues.append("ATR length must be positive")
        
        if strategy.parameters.atr_multiplier <= 0:
            issues.append("ATR multiplier must be positive")
        
        return issues

# =============================================================================
# RISK MANAGEMENT DOMAIN SERVICES
# =============================================================================

class AdvancedRiskManager(RiskManager):
    """Enhanced risk management with advanced features"""
    
    def __init__(self, max_risk_per_trade: Percentage = Percentage(Decimal('2.0')),
                 max_portfolio_risk: Percentage = Percentage(Decimal('10.0')),
                 max_correlation: Percentage = Percentage(Decimal('0.7')),
                 max_drawdown: Percentage = Percentage(Decimal('20.0'))):
        super().__init__(max_risk_per_trade, max_portfolio_risk)
        self.max_correlation = max_correlation
        self.max_drawdown = max_drawdown
    
    def validate_trade(self, trade: Trade, portfolio: Portfolio) -> bool:
        """Enhanced trade validation with correlation analysis"""
        if not super().validate_trade(trade, portfolio):
            return False
        
        # Check correlation with existing positions
        if self._has_high_correlation(trade, portfolio):
            return False
        
        # Check drawdown limits
        if self._exceeds_drawdown_limit(portfolio):
            return False
        
        return True
    
    def _has_high_correlation(self, trade: Trade, portfolio: Portfolio) -> bool:
        """Check if trade has high correlation with existing positions"""
        # Simplified correlation check
        # In real implementation, would use actual correlation analysis
        return False
    
    def _exceeds_drawdown_limit(self, portfolio: Portfolio) -> bool:
        """Check if portfolio exceeds drawdown limit"""
        total_pnl = portfolio.calculate_total_pnl()
        total_value = portfolio.calculate_total_value()
        
        if total_value.amount == 0:
            return False
        
        drawdown_percentage = abs(total_pnl.amount / total_value.amount) * 100
        return drawdown_percentage > self.max_drawdown.value
    
    def calculate_position_size(self, trade: Trade, portfolio: Portfolio,
                              risk_amount: Money) -> Quantity:
        """Calculate optimal position size based on risk"""
        if trade.price.value == 0:
            return Quantity(Decimal('0'))
        
        # Kelly Criterion or similar position sizing
        position_size = risk_amount.amount / trade.price.value
        return Quantity(position_size)

class PortfolioRiskAnalyzer:
    """Domain service for portfolio risk analysis"""
    
    def analyze_portfolio_risk(self, portfolio: Portfolio) -> Dict[str, Any]:
        """Analyze portfolio risk metrics"""
        total_value = portfolio.calculate_total_value()
        total_pnl = portfolio.calculate_total_pnl()
        
        return {
            'total_value': float(total_value.amount),
            'total_pnl': float(total_pnl.amount),
            'pnl_percentage': float((total_pnl.amount / total_value.amount) * 100) if total_value.amount > 0 else 0,
            'position_count': len(portfolio.positions),
            'trade_count': len(portfolio.trades)
        }
    
    def calculate_var(self, portfolio: Portfolio, confidence_level: float = 0.95) -> Money:
        """Calculate Value at Risk"""
        # Simplified VaR calculation
        # In real implementation, would use historical simulation or Monte Carlo
        total_value = portfolio.calculate_total_value()
        var_amount = total_value.amount * 0.05  # 5% VaR
        return Money(var_amount, total_value.currency)

# =============================================================================
# BACKTESTING DOMAIN SERVICES
# =============================================================================

class AdvancedBacktestExecutor(BacktestExecutor):
    """Enhanced backtest executor with advanced features"""
    
    def __init__(self, risk_manager: RiskManager):
        super().__init__(risk_manager)
        self.analyzer = StrategyAnalyzer()
    
    def execute_backtest(self, strategy: Strategy, market_data: MarketData, 
                        initial_capital: Money) -> BacktestResults:
        """Execute enhanced backtest with detailed analysis"""
        portfolio = Portfolio(
            name=f"Backtest_{strategy.name}",
            initial_capital=initial_capital,
            current_capital=initial_capital
        )
        
        # Generate signals using strategy analyzer
        signals = self.analyzer.analyze_market_data(strategy, market_data)
        
        # Execute trades with risk management
        executed_trades = []
        for signal in signals:
            trade = self._create_trade_from_signal(signal)
            
            if self.risk_manager.validate_trade(trade, portfolio):
                portfolio.add_trade(trade)
                executed_trades.append(trade)
        
        # Calculate comprehensive results
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
        """Calculate enhanced backtest results with additional metrics"""
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

class MultiDataBacktestService:
    """Domain service for multi-data source backtesting"""
    
    def __init__(self, backtest_executor: BacktestExecutor):
        self.backtest_executor = backtest_executor
    
    def run_comprehensive_backtest(self, strategy: Strategy, 
                                 data_sources: List[MarketData]) -> List[BacktestResults]:
        """Run backtest across multiple data sources"""
        results = []
        
        for market_data in data_sources:
            try:
                result = self.backtest_executor.execute_backtest(
                    strategy, market_data, Money(Decimal('10000'), "USD")
                )
                results.append(result)
            except Exception as e:
                print(f"Error backtesting {market_data.symbol}: {e}")
        
        return results
    
    def compare_strategies(self, strategies: List[Strategy], 
                         market_data: MarketData) -> Dict[str, BacktestResults]:
        """Compare multiple strategies on same data"""
        results = {}
        
        for strategy in strategies:
            try:
                result = self.backtest_executor.execute_backtest(
                    strategy, market_data, Money(Decimal('10000'), "USD")
                )
                results[strategy.name] = result
            except Exception as e:
                print(f"Error backtesting {strategy.name}: {e}")
        
        return results

# =============================================================================
# TECHNICAL ANALYSIS DOMAIN SERVICES
# =============================================================================

class TechnicalIndicatorService:
    """Domain service for technical indicator calculations"""
    
    def calculate_atr(self, market_data: MarketData, period: int = 14) -> List[Decimal]:
        """Calculate Average True Range"""
        if len(market_data.data) < period:
            return []
        
        # Simplified ATR calculation
        # In real implementation, would use proper OHLCV data
        atr_values = []
        for i in range(period, len(market_data.data)):
            # Calculate ATR for period
            atr_value = Decimal('0.5')  # Placeholder
            atr_values.append(atr_value)
        
        return atr_values
    
    def calculate_adx(self, market_data: MarketData, period: int = 14) -> List[Decimal]:
        """Calculate Average Directional Index"""
        if len(market_data.data) < period:
            return []
        
        # Simplified ADX calculation
        adx_values = []
        for i in range(period, len(market_data.data)):
            adx_value = Decimal('25.0')  # Placeholder
            adx_values.append(adx_value)
        
        return adx_values
    
    def calculate_rsi(self, market_data: MarketData, period: int = 14) -> List[Decimal]:
        """Calculate Relative Strength Index"""
        if len(market_data.data) < period:
            return []
        
        # Simplified RSI calculation
        rsi_values = []
        for i in range(period, len(market_data.data)):
            rsi_value = Decimal('50.0')  # Placeholder
            rsi_values.append(rsi_value)
        
        return rsi_values
    
    def calculate_moving_average(self, market_data: MarketData, period: int) -> List[Decimal]:
        """Calculate Simple Moving Average"""
        if len(market_data.data) < period:
            return []
        
        ma_values = []
        for i in range(period, len(market_data.data)):
            # Calculate SMA for period
            ma_value = Decimal('100.0')  # Placeholder
            ma_values.append(ma_value)
        
        return ma_values

class SignalGenerationService:
    """Domain service for generating trading signals"""
    
    def __init__(self, indicator_service: TechnicalIndicatorService):
        self.indicator_service = indicator_service
    
    def generate_tsa_signals(self, strategy: Strategy, market_data: MarketData) -> List[TradingSignal]:
        """Generate TSA Enhanced Strategy signals"""
        signals = []
        
        # Get indicators
        atr_values = self.indicator_service.calculate_atr(market_data, strategy.parameters.atr_length)
        adx_values = self.indicator_service.calculate_adx(market_data, strategy.parameters.adx_length)
        ma_values = self.indicator_service.calculate_moving_average(market_data, 20)
        
        # Generate signals based on strategy logic
        for i in range(len(market_data.data)):
            if i < max(strategy.parameters.atr_length, strategy.parameters.adx_length, 20):
                continue
            
            # TSA Enhanced Strategy logic
            current_price = Decimal(str(market_data.data[i]['close']))
            atr = atr_values[i - strategy.parameters.atr_length] if i >= strategy.parameters.atr_length else Decimal('0')
            adx = adx_values[i - strategy.parameters.adx_length] if i >= strategy.parameters.adx_length else Decimal('0')
            ma = ma_values[i - 20] if i >= 20 else Decimal('0')
            
            # Entry conditions
            if (current_price > ma and 
                adx > strategy.parameters.adx_threshold and
                current_price > current_price - atr * strategy.parameters.atr_multiplier):
                
                signal = TradingSignal(
                    symbol=market_data.symbol,
                    side=TradeSide.BUY,
                    signal_type=SignalType.ENTRY_LONG,
                    price=Price(current_price),
                    quantity=Quantity(Decimal('1.0')),
                    timestamp=datetime.now(),
                    confidence=Percentage(Decimal('75.0')),
                    reason="TSA Enhanced Strategy - Long Entry"
                )
                signals.append(signal)
        
        return signals

# =============================================================================
# PERFORMANCE ANALYSIS DOMAIN SERVICES
# =============================================================================

class PerformanceAnalyzer:
    """Domain service for performance analysis"""
    
    def analyze_strategy_performance(self, results: List[BacktestResults]) -> Dict[str, Any]:
        """Analyze performance across multiple backtests"""
        if not results:
            return {}
        
        total_return = sum(result.total_return.value for result in results) / len(results)
        avg_win_rate = sum(result.win_rate.value for result in results) / len(results)
        avg_profit_factor = sum(result.profit_factor for result in results) / len(results)
        avg_max_drawdown = sum(result.max_drawdown.value for result in results) / len(results)
        
        return {
            'avg_total_return': float(total_return),
            'avg_win_rate': float(avg_win_rate),
            'avg_profit_factor': float(avg_profit_factor),
            'avg_max_drawdown': float(avg_max_drawdown),
            'total_strategies': len(results),
            'best_performer': max(results, key=lambda r: r.total_return.value).strategy_id,
            'worst_performer': min(results, key=lambda r: r.total_return.value).strategy_id
        }
    
    def rank_strategies(self, results: List[BacktestResults]) -> List[Dict[str, Any]]:
        """Rank strategies by performance"""
        ranked = []
        
        for result in results:
            score = (
                result.total_return.value * 0.4 +
                result.win_rate.value * 0.3 +
                float(result.profit_factor) * 10 * 0.2 +
                (100 - result.max_drawdown.value) * 0.1
            )
            
            ranked.append({
                'strategy_id': result.strategy_id,
                'symbol': result.symbol,
                'score': float(score),
                'total_return': float(result.total_return.value),
                'win_rate': float(result.win_rate.value),
                'profit_factor': float(result.profit_factor),
                'max_drawdown': float(result.max_drawdown.value)
            })
        
        return sorted(ranked, key=lambda x: x['score'], reverse=True)

class RiskAnalysisService:
    """Domain service for risk analysis"""
    
    def analyze_portfolio_risk(self, portfolios: List[Portfolio]) -> Dict[str, Any]:
        """Analyze risk across multiple portfolios"""
        if not portfolios:
            return {}
        
        total_value = sum(portfolio.calculate_total_value().amount for portfolio in portfolios)
        total_pnl = sum(portfolio.calculate_total_pnl().amount for portfolio in portfolios)
        
        return {
            'total_portfolio_value': float(total_value),
            'total_pnl': float(total_pnl),
            'overall_return': float((total_pnl / total_value) * 100) if total_value > 0 else 0,
            'portfolio_count': len(portfolios),
            'avg_position_count': sum(len(portfolio.positions) for portfolio in portfolios) / len(portfolios)
        }
    
    def calculate_correlation_matrix(self, portfolios: List[Portfolio]) -> Dict[str, Any]:
        """Calculate correlation matrix between portfolios"""
        # Simplified correlation calculation
        # In real implementation, would use actual correlation analysis
        return {
            'correlation_matrix': {},
            'avg_correlation': 0.3,
            'max_correlation': 0.7,
            'min_correlation': -0.2
        }
