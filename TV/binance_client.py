"""
币安API客户端模块
封装币安交易所API的所有操作，支持测试网和主网切换

【重要安全提醒】
1. 币安API Key只能开启"现货交易"权限，绝对不要开启"提现"权限
2. 务必在币安后台设置API Key的IP白名单，只允许服务器IP访问
3. 首次使用请务必在测试网验证无误后再切换到主网
"""
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from config import config
from logger_config import logger


class BinanceTrader:
    """币安交易客户端"""

    def __init__(self):
        """初始化币安客户端"""
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """初始化币安客户端，支持延迟重试"""
        try:
            self.client = Client(
                api_key=config.BINANCE_API_KEY,
                api_secret=config.BINANCE_API_SECRET,
                testnet=config.USE_TESTNET
            )
            mode = "测试网" if config.USE_TESTNET else "主网"
            logger.info(f"币安客户端初始化完成，当前模式: {mode}")
        except Exception as e:
            logger.error(f"币安客户端初始化失败: {e}")
            logger.warning("服务将继续运行，但交易功能不可用。请检查网络连接和API配置。")
            self.client = None

    def _check_client(self):
        """检查客户端是否可用，不可用时尝试重新初始化"""
        if self.client is None:
            logger.warning("币安客户端未初始化，尝试重新连接...")
            self._initialize_client()
        if self.client is None:
            raise ConnectionError("币安客户端不可用，请检查网络连接和API配置")

    def get_account_balance(self, asset: str = None) -> dict:
        """
        获取账户余额

        Args:
            asset: 指定资产（如BTC, USDT），为None时返回所有资产

        Returns:
            资产余额信息字典
        """
        self._check_client()
        try:
            account = self.client.get_account()
            balances = {}

            for balance in account["balances"]:
                free = float(balance["free"])
                locked = float(balance["locked"])
                total = free + locked

                if total > 0:  # 只返回有余额的资产
                    balances[balance["asset"]] = {
                        "free": free,
                        "locked": locked,
                        "total": total
                    }

            if asset:
                asset = asset.upper()
                return balances.get(asset, {"free": 0, "locked": 0, "total": 0})

            return balances

        except BinanceAPIException as e:
            logger.error(f"获取账户余额失败: {e}")
            raise

    def get_symbol_price(self, symbol: str) -> float:
        """
        获取交易对当前价格

        Args:
            symbol: 交易对（如BTCUSDT）

        Returns:
            当前价格
        """
        self._check_client()
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol.upper())
            price = float(ticker["price"])
            logger.debug(f"{symbol} 当前价格: {price}")
            return price
        except BinanceAPIException as e:
            logger.error(f"获取{symbol}价格失败: {e}")
            raise

    def get_symbol_info(self, symbol: str) -> dict:
        """
        获取交易对信息（精度、最小下单量等）

        Args:
            symbol: 交易对

        Returns:
            交易对信息字典
        """
        self._check_client()
        try:
            info = self.client.get_symbol_info(symbol.upper())
            return info
        except BinanceAPIException as e:
            logger.error(f"获取{symbol}交易对信息失败: {e}")
            raise

    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """
        下市价单

        Args:
            symbol: 交易对（如BTCUSDT）
            side: 交易方向（BUY或SELL）
            quantity: 交易数量

        Returns:
            订单信息字典

        Raises:
            BinanceOrderException: 下单失败
        """
        self._check_client()
        try:
            logger.info(f"准备下单: {side} {quantity} {symbol}")

            # 根据买卖方向执行下单
            if side == "BUY":
                order = self.client.order_market_buy(
                    symbol=symbol.upper(),
                    quantity=quantity
                )
            elif side == "SELL":
                order = self.client.order_market_sell(
                    symbol=symbol.upper(),
                    quantity=quantity
                )
            else:
                raise ValueError(f"无效的交易方向: {side}")

            # 解析订单结果
            order_id = order.get("orderId", "N/A")
            status = order.get("status", "N/A")
            executed_qty = order.get("executedQty", "0")
            cumul_quote = order.get("cummulativeQuoteQty", "0")

            logger.info(
                f"订单执行成功: ID={order_id}, 状态={status}, "
                f"成交数量={executed_qty}, 成交金额={cumul_quote}"
            )

            return {
                "success": True,
                "order_id": order_id,
                "status": status,
                "executed_qty": float(executed_qty),
                "cumul_quote": float(cumul_quote),
                "raw": order
            }

        except BinanceOrderException as e:
            logger.error(f"下单失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "order_id": None
            }
        except BinanceAPIException as e:
            logger.error(f"币安API错误: {e}")
            return {
                "success": False,
                "error": str(e),
                "order_id": None
            }

    def get_order_status(self, symbol: str, order_id: int) -> dict:
        """
        查询订单状态

        Args:
            symbol: 交易对
            order_id: 订单ID

        Returns:
            订单状态信息
        """
        self._check_client()
        try:
            order = self.client.get_order(
                symbol=symbol.upper(),
                orderId=order_id
            )
            return order
        except BinanceAPIException as e:
            logger.error(f"查询订单状态失败: {e}")
            raise

    def test_connection(self) -> bool:
        """
        测试与币安API的连接

        Returns:
            连接是否正常
        """
        self._check_client()
        try:
            # 尝试获取服务器时间来测试连接
            server_time = self.client.get_server_time()
            logger.info(f"币安API连接正常，服务器时间: {server_time}")

            # 尝试获取账户信息来验证API Key
            account = self.client.get_account()
            logger.info("API Key验证通过，账户信息获取成功")

            return True
        except BinanceAPIException as e:
            logger.error(f"币安API连接失败: {e}")
            return False
        except Exception as e:
            logger.error(f"连接测试异常: {e}")
            return False


# 全局币安客户端实例
binance_trader = None


def get_binance_trader() -> BinanceTrader:
    """获取币安交易客户端单例"""
    global binance_trader
    if binance_trader is None:
        binance_trader = BinanceTrader()
    return binance_trader
