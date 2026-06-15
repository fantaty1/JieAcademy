"""
Webhook接口模块
接收TradingView发出的交易信号，验证后执行交易

TradingView Webhook配置说明：
在TradingView中创建警报时，需要在"警报动作"中选择"Webhook URL"，
并填入你的服务器地址，如：http://your-server:8080/webhook

在"消息"字段中填入JSON格式的信号数据，例如：
{
    "secret": "your_webhook_secret",
    "symbol": "{{ticker}}",
    "side": "BUY",
    "quantity": 0.001,
    "order_type": "MARKET",
    "timestamp": "{{timenow}}"
}
"""
from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from config import config
from logger_config import logger
from tradingview_signal import TradingViewSignal, SignalResult
from binance_client import get_binance_trader
from risk_manager import risk_manager
from notifications import notify_trade_result

router = APIRouter()


@router.post("/webhook")
async def handle_webhook(request: Request):
    """
    处理TradingView发来的Webhook信号

    完整处理流程：
    1. 解析并验证信号格式
    2. 验证Webhook密钥
    3. 执行风控检查
    4. 获取账户余额和市场价格
    5. 执行交易
    6. 记录日志并发送通知
    """
    # 1. 解析请求体
    try:
        raw_data = await request.json()
        logger.info(f"收到Webhook信号: {raw_data}")
    except Exception as e:
        logger.error(f"解析Webhook数据失败: {e}")
        raise HTTPException(status_code=400, detail="无效的JSON数据")

    # 2. 验证信号格式
    try:
        signal = TradingViewSignal(**raw_data)
    except Exception as e:
        logger.error(f"信号格式验证失败: {e}")
        raise HTTPException(status_code=400, detail=f"信号格式错误: {str(e)}")

    # 3. 验证Webhook密钥
    if signal.secret != config.WEBHOOK_SECRET:
        logger.warning(f"Webhook密钥验证失败，来源IP: {request.client.host}")
        raise HTTPException(status_code=401, detail="密钥验证失败")

    # 4. 执行风控检查
    # 4.1 全局开关检查
    allowed, reason = risk_manager.check_trading_enabled()
    if not allowed:
        logger.warning(f"风控拒绝交易: {reason}")
        return {"status": "rejected", "reason": reason}

    # 4.2 重复信号检查
    allowed, reason = risk_manager.check_duplicate_signal(signal.symbol, signal.side)
    if not allowed:
        logger.info(f"风控过滤重复信号: {reason}")
        return {"status": "filtered", "reason": reason}

    # 4.3 每日交易次数检查
    allowed, reason = risk_manager.check_daily_limit()
    if not allowed:
        logger.warning(f"风控拒绝交易: {reason}")
        return {"status": "rejected", "reason": reason}

    # 5. 执行交易
    try:
        trader = get_binance_trader()
    except Exception as e:
        error_msg = f"币安客户端初始化失败: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "reason": error_msg}

    try:
        # 5.1 获取当前价格
        price = trader.get_symbol_price(signal.symbol)
        logger.info(f"{signal.symbol}当前价格: {price}")

        # 5.2 获取账户余额
        balance = trader.get_account_balance()
        logger.debug(f"当前账户余额: {balance}")

        # 5.3 余额检查
        allowed, reason = risk_manager.check_balance(
            balance, signal.symbol, signal.side, signal.quantity, price
        )
        if not allowed:
            logger.warning(f"风控拒绝交易: {reason}")
            notify_trade_result(
                symbol=signal.symbol,
                side=signal.side,
                success=False,
                quantity=signal.quantity,
                price=price,
                message=reason
            )
            return {"status": "rejected", "reason": reason}

        # 5.4 执行下单
        result = trader.place_market_order(
            symbol=signal.symbol,
            side=signal.side,
            quantity=signal.quantity
        )

        # 6. 处理交易结果
        if result["success"]:
            # 记录交易
            risk_manager.record_trade()

            success_msg = (
                f"交易成功: {signal.side} {result['executed_qty']} {signal.symbol}，"
                f"成交金额: {result['cumul_quote']}"
            )
            logger.info(success_msg)

            # 发送成功通知
            notify_trade_result(
                symbol=signal.symbol,
                side=signal.side,
                success=True,
                quantity=result["executed_qty"],
                price=price,
                message=success_msg
            )

            return {
                "status": "success",
                "order_id": result["order_id"],
                "executed_qty": result["executed_qty"],
                "cumul_quote": result["cumul_quote"]
            }
        else:
            error_msg = f"交易失败: {result['error']}"
            logger.error(error_msg)

            # 发送失败通知
            notify_trade_result(
                symbol=signal.symbol,
                side=signal.side,
                success=False,
                quantity=signal.quantity,
                price=price,
                message=error_msg
            )

            return {
                "status": "failed",
                "error": result["error"]
            }

    except ConnectionError as e:
        error_msg = f"币安连接失败: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "reason": error_msg}

    except Exception as e:
        error_msg = f"交易执行异常: {str(e)}"
        logger.error(error_msg, exc_info=True)

        notify_trade_result(
            symbol=signal.symbol,
            side=signal.side,
            success=False,
            message=error_msg
        )

        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/health")
async def health_check():
    """健康检查接口"""
    stats = risk_manager.get_trade_stats()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "trading_stats": stats
    }


@router.get("/balance")
async def get_balance():
    """查询账户余额接口"""
    try:
        trader = get_binance_trader()
        balance = trader.get_account_balance()
        return {"status": "success", "balances": balance}
    except Exception as e:
        logger.error(f"查询余额失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
