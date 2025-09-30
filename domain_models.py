"""
Domain Models for Pine Script to Python Backtesting Framework
Domain-Driven Design implementation with clear business logic separation
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Tuple
import uuid

# =============================================================================
# VALUE OBJECTS
# =============================================================================

@dataclass(frozen=True)
class Money:
    """Value object representing monetary amounts"""
    amount: Decimal
    currency: str = "USD"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        if not self.currency:
            raise ValueError("Currency must be specified")
    
    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __sub__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot subtract money with different currencies")
        return Money(self.amount - other.amount, self.currency)
    
    def __mul__(self, multiplier: Decimal) -> 'Money':
        return Money(self.amount * multiplier, self.currency)
    
    def __truediv__(self, divisor: Decimal) -> 'Money':
        return Money(self.amount / divisor, self.currency)

@dataclass(frozen=True)
class Price:
    """Value object representing price with currency"""
    value: Decimal
    currency: str = "USD"
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Price must be positive")
        if not self.currency:
            raise ValueError("Currency must be specified")

@dataclass(frozen=True)
class Quantity:
    """Value object representing quantity"""
    value: Decimal
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Quantity must be positive")

@dataclass(frozen=True)
class Percentage:
    """Value object representing percentage"""
    value: Decimal
    
    def __post_init__(self):
        if not (0 <= self.value <= 100):
            raise ValueError("Percentage must be between 0 and 100")
    
    def as_decimal(self) -> Decimal:
        return self.value / 100

@dataclass(frozen=True)
class Timeframe:
    """Value object representing timeframe"""
    value: str
    
    def __post_init__(self):
        valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
        if self.value not in valid_timeframes:
            raise ValueError(f"Invalid timeframe: {self.value}")

# =============================================================================
# ENUMS
# =============================================================================

class TradeSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

class StrategyType(Enum):
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    TREND_FOLLOWING = "trend_following"
    BREAKOUT = "breakout"
    SCALPING = "scalping"

class MarketType(Enum):
    CRYPTO = "crypto"
    STOCK = "stock"
    FOREX = "forex"
    COMMODITY = "commodity"

class SignalType(Enum):
    ENTRY_LONG = "entry_long"
    ENTRY_SHORT = "entry_short"
    EXIT_LONG = "exit_long"
    EXIT_SHORT = "exit_short"
    HOLD = "hold"

# =============================================================================
# DOMAIN ENTITIES
# =============================================================================

@dataclass
class TradingSignal:
    """Domain entity representing a trading signal"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str
    side: TradeSide
    signal_type: SignalType
    price: Price
    quantity: Quantity
    timestamp: datetime
    confidence: Percentage
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.symbol:
            raise ValueError("Symbol must be specified")
        if not self.reason:
            raise ValueError("Reason must be specified")

@dataclass
class Trade:
    """Domain entity representing an executed trade"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str
    side: TradeSide
    quantity: Quantity
    price: Price
    timestamp: datetime
    fees: Money
    pnl: Optional[Money] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def calculate_value(self) -> Money:
        """Calculate total trade value"""
        return Money(self.quantity.value * self.price.value, self.price.currency)
    
    def calculate_pnl(self, current_price: Price) -> Money:
        """Calculate profit/loss for this trade"""
        if self.side == TradeSide.BUY:
            pnl_amount = (current_price.value - self.price.value) * self.quantity.value
        else:  # SELL
            pnl_amount = (self.price.value - current_price.value) * self.quantity.value
        
        return Money(pnl_amount, self.price.currency)

@dataclass
class Position:
    """Domain entity representing a position"""
    symbol: str
    quantity: Quantity
    average_price: Price
    current_price: Price
    unrealized_pnl: Money
    realized_pnl: Money = Money(Decimal('0'), "USD")
    
    def update_price(self, new_price: Price) -> 'Position':
        """Update position with new price"""
        if self.quantity.value > 0:  # Long position
            pnl_amount = (new_price.value - self.average_price.value) * self.quantity.value
        else:  # Short position
            pnl_amount = (self.average_price.value - new_price.value) * abs(self.quantity.value)
        
        return Position(
            symbol=self.symbol,
            quantity=self.quantity,
            average_price=self.average_price,
            current_price=new_price,
            unrealized_pnl=Money(pnl_amount, new_price.currency),
            realized_pnl=self.realized_pnl
        )

@dataclass
class StrategyParameters:
    """Value object for strategy parameters"""
    atr_length: int = 14
    atr_multiplier: Decimal = Decimal('3.0')
    risk_reward_ratio: Decimal = Decimal('1.5')
    adx_length: int = 14
    adx_threshold: Decimal = Decimal('25')
    stop_loss_percentage: Percentage = Percentage(Decimal('2.0'))
    take_profit_percentage: Percentage = Percentage(Decimal('3.0'))
    max_position_size: Percentage = Percentage(Decimal('10.0'))
    
    def __post_init__(self):
        if self.atr_length <= 0:
            raise ValueError("ATR length must be positive")
        if self.atr_multiplier <= 0:
            raise ValueError("ATR multiplier must be positive")
        if self.risk_reward_ratio <= 0:
            raise ValueError("Risk reward ratio must be positive")

@dataclass
class Strategy:
    """Domain entity representing a trading strategy"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    strategy_type: StrategyType
    parameters: StrategyParameters
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Strategy name must be specified")
        if not self.description:
            raise ValueError("Strategy description must be specified")

@dataclass
class MarketData:
    """Domain entity representing market data"""
    symbol: str
    timeframe: Timeframe
    data: List[Dict[str, Any]]  # OHLCV data
    start_date: datetime
    end_date: datetime
    last_updated: datetime = field(default_factory=datetime.now)
    
    def get_latest_price(self) -> Optional[Price]:
        """Get the latest price from market data"""
        if not self.data:
            return None
        
        latest = self.data[-1]
        return Price(Decimal(str(latest['close'])), "USD")
    
    def get_price_at_time(self, timestamp: datetime) -> Optional[Price]:
        """Get price at specific timestamp"""
        for candle in reversed(self.data):
            if datetime.fromisoformat(candle['timestamp']) <= timestamp:
                return Price(Decimal(str(candle['close'])), "USD")
        return None

@dataclass
class BacktestResults:
    """Domain entity representing backtest results"""
    strategy_id: str
    symbol: str
    timeframe: Timeframe
    start_date: datetime
    end_date: datetime
    initial_capital: Money
    final_capital: Money
    total_return: Percentage
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: Percentage
    profit_factor: Decimal
    max_drawdown: Percentage
    sharpe_ratio: Decimal
    trades: List[Trade] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate additional performance metrics"""
        return {
            'total_return': float(self.total_return.value),
            'win_rate': float(self.win_rate.value),
            'profit_factor': float(self.profit_factor),
            'max_drawdown': float(self.max_drawdown.value),
            'sharpe_ratio': float(self.sharpe_ratio),
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades
        }

@dataclass
class Portfolio:
    """Domain entity representing a portfolio"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    initial_capital: Money
    current_capital: Money
    positions: Dict[str, Position] = field(default_factory=dict)
    trades: List[Trade] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_trade(self, trade: Trade) -> None:
        """Add a trade to the portfolio"""
        self.trades.append(trade)
        
        # Update position
        if trade.symbol in self.positions:
            position = self.positions[trade.symbol]
            # Update position logic here
        else:
            # Create new position
            self.positions[trade.symbol] = Position(
                symbol=trade.symbol,
                quantity=trade.quantity,
                average_price=trade.price,
                current_price=trade.price,
                unrealized_pnl=Money(Decimal('0'), trade.price.currency)
            )
    
    def calculate_total_value(self) -> Money:
        """Calculate total portfolio value"""
        total = self.current_capital
        for position in self.positions.values():
            total = total + Money(
                position.quantity.value * position.current_price.value,
                position.current_price.currency
            )
        return total
    
    def calculate_total_pnl(self) -> Money:
        """Calculate total profit/loss"""
        total_pnl = Money(Decimal('0'), "USD")
        for position in self.positions.values():
            total_pnl = total_pnl + position.unrealized_pnl + position.realized_pnl
        return total_pnl

# =============================================================================
# DOMAIN SERVICES
# =============================================================================

class RiskManager:
    """Domain service for risk management"""
    
    def __init__(self, max_risk_per_trade: Percentage = Percentage(Decimal('2.0')),
                 max_portfolio_risk: Percentage = Percentage(Decimal('10.0'))):
        self.max_risk_per_trade = max_risk_per_trade
        self.max_portfolio_risk = max_portfolio_risk
    
    def validate_trade(self, trade: Trade, portfolio: Portfolio) -> bool:
        """Validate if a trade meets risk criteria"""
        # Check position size
        trade_value = trade.calculate_value()
        portfolio_value = portfolio.calculate_total_value()
        
        position_risk = (trade_value.amount / portfolio_value.amount) * 100
        
        if position_risk > self.max_risk_per_trade.value:
            return False
        
        # Check portfolio risk
        total_risk = self._calculate_portfolio_risk(portfolio)
        if total_risk > self.max_portfolio_risk.value:
            return False
        
        return True
    
    def _calculate_portfolio_risk(self, portfolio: Portfolio) -> Decimal:
        """Calculate total portfolio risk"""
        # Simplified risk calculation
        total_value = portfolio.calculate_total_value()
        total_pnl = portfolio.calculate_total_pnl()
        
        if total_value.amount == 0:
            return Decimal('0')
        
        return abs(total_pnl.amount / total_value.amount) * 100

class StrategyAnalyzer:
    """Domain service for strategy analysis"""
    
    def analyze_market_data(self, strategy: Strategy, market_data: MarketData) -> List[TradingSignal]:
        """Analyze market data and generate trading signals"""
        signals = []
        
        # This would contain the actual strategy logic
        # For now, return empty list
        return signals
    
    def calculate_indicators(self, market_data: MarketData, parameters: StrategyParameters) -> Dict[str, Any]:
        """Calculate technical indicators"""
        # This would contain indicator calculation logic
        return {}

class BacktestExecutor:
    """Domain service for executing backtests"""
    
    def __init__(self, risk_manager: RiskManager):
        self.risk_manager = risk_manager
    
    def execute_backtest(self, strategy: Strategy, market_data: MarketData, 
                        initial_capital: Money) -> BacktestResults:
        """Execute a backtest for a strategy"""
        portfolio = Portfolio(
            name=f"Backtest_{strategy.name}",
            initial_capital=initial_capital,
            current_capital=initial_capital
        )
        
        # Generate signals
        analyzer = StrategyAnalyzer()
        signals = analyzer.analyze_market_data(strategy, market_data)
        
        # Execute trades
        for signal in signals:
            if self.risk_manager.validate_trade(
                Trade(
                    symbol=signal.symbol,
                    side=signal.side,
                    quantity=signal.quantity,
                    price=signal.price,
                    timestamp=signal.timestamp,
                    fees=Money(Decimal('0'), signal.price.currency)
                ),
                portfolio
            ):
                # Execute trade logic here
                pass
        
        # Calculate results
        return self._calculate_results(strategy, portfolio, market_data)
    
    def _calculate_results(self, strategy: Strategy, portfolio: Portfolio, 
                         market_data: MarketData) -> BacktestResults:
        """Calculate backtest results"""
        total_trades = len(portfolio.trades)
        winning_trades = sum(1 for trade in portfolio.trades if trade.pnl and trade.pnl.amount > 0)
        losing_trades = total_trades - winning_trades
        
        win_rate = Percentage(Decimal(str((winning_trades / total_trades * 100) if total_trades > 0 else 0)))
        
        total_return = Percentage(
            ((portfolio.calculate_total_value().amount - portfolio.initial_capital.amount) / 
             portfolio.initial_capital.amount) * 100
        )
        
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
            profit_factor=Decimal('1.0'),  # Calculate actual profit factor
            max_drawdown=Percentage(Decimal('0.0')),  # Calculate actual max drawdown
            sharpe_ratio=Decimal('0.0'),  # Calculate actual Sharpe ratio
            trades=portfolio.trades
        )

# =============================================================================
# DOMAIN EVENTS
# =============================================================================

@dataclass
class DomainEvent:
    """Base class for domain events"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    event_type: str = ""

@dataclass
class TradeExecuted(DomainEvent):
    """Domain event when a trade is executed"""
    trade: Trade
    event_type: str = "trade_executed"

@dataclass
class StrategyAnalyzed(DomainEvent):
    """Domain event when a strategy is analyzed"""
    strategy: Strategy
    market_data: MarketData
    signals: List[TradingSignal]
    event_type: str = "strategy_analyzed"

@dataclass
class BacktestCompleted(DomainEvent):
    """Domain event when a backtest is completed"""
    strategy: Strategy
    results: BacktestResults
    event_type: str = "backtest_completed"

@dataclass
class RiskLimitExceeded(DomainEvent):
    """Domain event when risk limits are exceeded"""
    trade: Trade
    risk_type: str
    current_risk: Percentage
    max_risk: Percentage
    event_type: str = "risk_limit_exceeded"

# =============================================================================
# FACTORIES
# =============================================================================

class StrategyFactory:
    """Factory for creating strategies"""
    
    @staticmethod
    def create_tsa_enhanced_strategy(parameters: StrategyParameters) -> Strategy:
        """Create TSA Enhanced Strategy"""
        return Strategy(
            name="TSA Enhanced Strategy",
            strategy_type=StrategyType.MOMENTUM,
            parameters=parameters,
            description="TSA Enhanced Strategy with ATR and ADX filters"
        )
    
    @staticmethod
    def create_ai_generated_strategy(name: str, description: str, 
                                  parameters: StrategyParameters) -> Strategy:
        """Create AI-generated strategy"""
        return Strategy(
            name=name,
            strategy_type=StrategyType.MOMENTUM,  # Default type
            parameters=parameters,
            description=description
        )

class MarketDataFactory:
    """Factory for creating market data"""
    
    @staticmethod
    def create_from_yfinance(symbol: str, timeframe: Timeframe, 
                           start_date: datetime, end_date: datetime) -> MarketData:
        """Create market data from yfinance"""
        # This would contain actual yfinance integration
        return MarketData(
            symbol=symbol,
            timeframe=timeframe,
            data=[],  # Would contain actual OHLCV data
            start_date=start_date,
            end_date=end_date
        )

# =============================================================================
# SPECIFICATIONS
# =============================================================================

class StrategySpecification:
    """Specification for strategy validation"""
    
    @staticmethod
    def is_profitable(results: BacktestResults) -> bool:
        """Check if strategy is profitable"""
        return results.total_return.value > 0
    
    @staticmethod
    def has_acceptable_drawdown(results: BacktestResults, max_drawdown: Percentage) -> bool:
        """Check if strategy has acceptable drawdown"""
        return results.max_drawdown.value <= max_drawdown.value
    
    @staticmethod
    def has_minimum_trades(results: BacktestResults, min_trades: int) -> bool:
        """Check if strategy has minimum number of trades"""
        return results.total_trades >= min_trades

class RiskSpecification:
    """Specification for risk validation"""
    
    @staticmethod
    def is_within_risk_limits(trade: Trade, portfolio: Portfolio, 
                            max_risk: Percentage) -> bool:
        """Check if trade is within risk limits"""
        trade_value = trade.calculate_value()
        portfolio_value = portfolio.calculate_total_value()
        
        if portfolio_value.amount == 0:
            return False
        
        risk_percentage = (trade_value.amount / portfolio_value.amount) * 100
        return risk_percentage <= max_risk.value
