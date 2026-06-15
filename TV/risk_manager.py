"""
风控管理模块
实现所有交易前的风险控制检查，防止异常交易导致资金损失

风控机制清单：
1. 全局交易开关 - 紧急情况下一键停止所有交易
2. 重复信号过滤 - 防止TV重复触发警报导致多次下单
3. 账户余额校验 - 下单前检查资金是否充足
4. 单次下单比例限制 - 限制单次交易金额占总资金的比例
5. 每日最大交易次数限制 - 防止策略异常导致频繁交易
"""
import time
from datetime import datetime, date
from collections import defaultdict
from config import config
from logger_config import logger


class RiskManager:
    """风控管理器"""

    def __init__(self):
        # 信号去重缓存: key = "symbol_side", value = 最后执行时间戳
        self._signal_cache: dict[str, float] = {}
        # 每日交易计数: key = 日期, value = 交易次数
        self._daily_trade_count: dict[str, int] = defaultdict(int)
        self._current_date: str = date.today().isoformat()

    def check_trading_enabled(self) -> tuple[bool, str]:
        """
        检查全局交易开关

        Returns:
            (是否允许交易, 原因说明)
        """
        if not config.TRADING_ENABLED:
            logger.warning("交易已全局关闭，请检查.env中的TRADING_ENABLED配置")
            return False, "交易已全局关闭，请检查配置文件中的TRADING_ENABLED设置"
        return True, ""

    def check_duplicate_signal(self, symbol: str, side: str) -> tuple[bool, str]:
        """
        检查是否为重复信号

        Args:
            symbol: 交易对
            side: 交易方向

        Returns:
            (是否允许交易, 原因说明)
        """
        cache_key = f"{symbol}_{side}"
        current_time = time.time()

        if cache_key in self._signal_cache:
            last_time = self._signal_cache[cache_key]
            time_diff = current_time - last_time

            if time_diff < config.DUPLICATE_SIGNAL_WINDOW:
                logger.info(
                    f"重复信号过滤: {symbol} {side}，"
                    f"距上次信号仅{time_diff:.1f}秒，"
                    f"窗口期{config.DUPLICATE_SIGNAL_WINDOW}秒"
                )
                return False, f"重复信号，{config.DUPLICATE_SIGNAL_WINDOW}秒内已执行过相同交易"

        # 更新缓存
        self._signal_cache[cache_key] = current_time
        # 清理过期缓存
        self._cleanup_cache(current_time)
        return True, ""

    def check_daily_limit(self) -> tuple[bool, str]:
        """
        检查每日交易次数限制

        Returns:
            (是否允许交易, 原因说明)
        """
        # 检查是否跨天，重置计数
        today = date.today().isoformat()
        if today != self._current_date:
            logger.info(f"日期变更，重置每日交易计数: {self._current_date} -> {today}")
            self._current_date = today
            self._daily_trade_count[today] = 0

        current_count = self._daily_trade_count[today]
        if current_count >= config.MAX_DAILY_TRADES:
            logger.warning(
                f"达到每日最大交易次数限制: {current_count}/{config.MAX_DAILY_TRADES}"
            )
            return False, f"已达到每日最大交易次数限制({config.MAX_DAILY_TRADES}次)"

        return True, ""

    def check_balance(
        self,
        balance: dict,
        symbol: str,
        side: str,
        quantity: float,
        price: float
    ) -> tuple[bool, str]:
        """
        检查账户余额是否充足

        Args:
            balance: 账户余额信息 {asset: {free, locked, total}}
            symbol: 交易对
            side: 交易方向
            quantity: 交易数量
            price: 当前价格

        Returns:
            (是否允许交易, 原因说明)
        """
        # 解析交易对的基础资产和报价资产
        # 如BTCUSDT -> base=BTC, quote=USDT
        quote_assets = ["USDT", "BUSD", "USDC", "TUSD", "FDUSD"]
        base_asset = symbol
        quote_asset = None

        for qa in quote_assets:
            if symbol.endswith(qa):
                quote_asset = qa
                base_asset = symbol[:-len(qa)]
                break

        if not quote_asset:
            return False, f"无法识别交易对{symbol}的报价资产"

        if side == "BUY":
            # 买入时检查报价资产（如USDT）是否足够
            order_value = quantity * price
            available = balance.get(quote_asset, {}).get("free", 0)

            if available < order_value:
                logger.warning(
                    f"余额不足: 需要{order_value:.2f} {quote_asset}，"
                    f"可用{available:.2f} {quote_asset}"
                )
                return False, f"{quote_asset}余额不足，需要{order_value:.2f}，可用{available:.2f}"

            # 检查单次下单比例限制
            total_value = self._estimate_total_value(balance, quote_asset, price)
            if total_value > 0:
                ratio = order_value / total_value
                if ratio > config.MAX_ORDER_RATIO:
                    logger.warning(
                        f"单次下单比例超限: {ratio:.2%} > {config.MAX_ORDER_RATIO:.2%}"
                    )
                    return False, (
                        f"单次下单金额占总资产比例{ratio:.2%}超过限制"
                        f"{config.MAX_ORDER_RATIO:.2%}"
                    )

        elif side == "SELL":
            # 卖出时检查基础资产（如BTC）是否足够
            available = balance.get(base_asset, {}).get("free", 0)

            if available < quantity:
                logger.warning(
                    f"余额不足: 需要{quantity} {base_asset}，"
                    f"可用{available} {base_asset}"
                )
                return False, f"{base_asset}余额不足，需要{quantity}，可用{available}"

        return True, ""

    def record_trade(self) -> None:
        """记录一次交易（用于每日计数）"""
        today = date.today().isoformat()
        self._daily_trade_count[today] += 1
        logger.info(
            f"交易计数更新: 今日已执行{self._daily_trade_count[today]}次交易"
        )

    def get_trade_stats(self) -> dict:
        """
        获取交易统计信息

        Returns:
            包含今日交易次数等统计信息的字典
        """
        today = date.today().isoformat()
        return {
            "today_date": today,
            "today_trade_count": self._daily_trade_count.get(today, 0),
            "max_daily_trades": config.MAX_DAILY_TRADES,
            "trading_enabled": config.TRADING_ENABLED,
            "duplicate_window": config.DUPLICATE_SIGNAL_WINDOW
        }

    def _estimate_total_value(
        self,
        balance: dict,
        quote_asset: str,
        current_price: float
    ) -> float:
        """
        估算账户总资产价值（以报价资产计）

        Args:
            balance: 账户余额
            quote_asset: 报价资产（如USDT）
            current_price: 当前交易对价格

        Returns:
            估算的总资产价值
        """
        total = balance.get(quote_asset, {}).get("total", 0)

        # 简单估算：当前交易对的基础资产按当前价格折算
        # 注意：这是一个粗略估算，实际应查询所有资产的USDT价格
        for asset, info in balance.items():
            if asset != quote_asset and info["total"] > 0:
                # 对于正在交易的资产，使用当前价格
                total += info["total"] * current_price
                break

        return total

    def _cleanup_cache(self, current_time: float) -> None:
        """清理过期的信号缓存"""
        expired_keys = [
            key for key, timestamp in self._signal_cache.items()
            if current_time - timestamp > config.DUPLICATE_SIGNAL_WINDOW * 10
        ]
        for key in expired_keys:
            del self._signal_cache[key]


# 全局风控管理器实例
risk_manager = RiskManager()
