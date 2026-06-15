"""
TradingView信号数据模型
定义Webhook接收的信号数据结构和验证规则
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class TradingViewSignal(BaseModel):
    """
    TradingView Webhook信号数据模型

    TradingView警报消息需要包含以下JSON格式数据:
    {
        "secret": "your_webhook_secret",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "quantity": 0.001,
        "order_type": "MARKET",
        "timestamp": "2024-01-01 12:00:00"
    }
    """
    secret: str = Field(..., description="Webhook验证密钥")
    symbol: str = Field(..., description="交易对，如BTCUSDT")
    side: str = Field(..., description="交易方向: BUY或SELL")
    quantity: Optional[float] = Field(None, description="交易数量")
    order_type: str = Field(default="MARKET", description="订单类型，默认MARKET")
    timestamp: Optional[str] = Field(None, description="信号触发时间")

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        """验证并标准化交易对格式"""
        v = v.upper().strip()
        # 移除可能的分隔符（如BTC/USDT -> BTCUSDT）
        v = v.replace("/", "").replace("-", "").replace(" ", "")
        if len(v) < 5:
            raise ValueError(f"无效的交易对格式: {v}")
        return v

    @field_validator("side")
    @classmethod
    def validate_side(cls, v: str) -> str:
        """验证交易方向"""
        v = v.upper().strip()
        if v not in ("BUY", "SELL"):
            raise ValueError(f"无效的交易方向: {v}，只支持BUY或SELL")
        return v

    @field_validator("order_type")
    @classmethod
    def validate_order_type(cls, v: str) -> str:
        """验证订单类型"""
        v = v.upper().strip()
        if v not in ("MARKET",):
            raise ValueError(f"当前版本只支持MARKET市价单，收到: {v}")
        return v


class SignalResult(BaseModel):
    """信号处理结果"""
    success: bool
    signal: TradingViewSignal
    order_id: Optional[str] = None
    message: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)
