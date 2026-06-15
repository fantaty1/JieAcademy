"""
配置管理模块
从 .env 文件读取所有配置参数，提供类型安全的配置访问
"""
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


class Config:
    """应用配置类 - 所有配置项从环境变量读取"""

    # ============== 币安API配置 ==============
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
    BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET", "")
    USE_TESTNET: bool = os.getenv("USE_TESTNET", "True").lower() == "true"

    # ============== Webhook安全配置 ==============
    WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "")

    # ============== 风控参数配置 ==============
    TRADING_ENABLED: bool = os.getenv("TRADING_ENABLED", "True").lower() == "true"
    MAX_ORDER_RATIO: float = float(os.getenv("MAX_ORDER_RATIO", "0.1"))
    DUPLICATE_SIGNAL_WINDOW: int = int(os.getenv("DUPLICATE_SIGNAL_WINDOW", "60"))
    MAX_DAILY_TRADES: int = int(os.getenv("MAX_DAILY_TRADES", "50"))

    # ============== 通知配置 ==============
    ENABLE_NOTIFICATIONS: bool = os.getenv("ENABLE_NOTIFICATIONS", "False").lower() == "true"
    WECOM_WEBHOOK_URL: str = os.getenv("WECOM_WEBHOOK_URL", "")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.qq.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "465"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    NOTIFICATION_EMAIL: str = os.getenv("NOTIFICATION_EMAIL", "")

    # ============== 服务器配置 ==============
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8080"))

    @classmethod
    def validate(cls) -> list[str]:
        """验证必要配置项是否已设置，返回缺失配置项列表"""
        missing = []
        if not cls.BINANCE_API_KEY:
            missing.append("BINANCE_API_KEY")
        if not cls.BINANCE_API_SECRET:
            missing.append("BINANCE_API_SECRET")
        if not cls.WEBHOOK_SECRET:
            missing.append("WEBHOOK_SECRET")
        return missing


# 创建全局配置实例
config = Config()
