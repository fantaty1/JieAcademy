"""
TradingView-Binance 自动量化交易系统 - 主程序入口

系统架构：
  TradingView策略 → Webhook信号 → 本服务 → 币安API → 现货交易

使用方法：
  开发模式: python main.py
  生产模式: uvicorn main:app --host 0.0.0.0 --port 8080

安全提醒：
  1. 量化交易存在风险，请勿投入超过自己承受能力的资金
  2. 首次使用务必在测试网验证，确认无误后再切换到主网
  3. 定期检查日志，监控系统运行状态
  4. 币安API Key只能开启"现货交易"权限，绝对不要开启"提现"权限
"""
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import config
from logger_config import logger
from webhook import router as webhook_router
from binance_client import get_binance_trader


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    启动时初始化币安客户端并测试连接
    """
    # 启动时执行
    logger.info("=" * 60)
    logger.info("TradingView-Binance 自动量化交易系统启动中...")
    logger.info("=" * 60)

    # 检查必要配置
    missing_config = config.validate()
    if missing_config:
        logger.error(f"缺少必要配置项: {', '.join(missing_config)}")
        logger.error("请检查 .env 文件是否已正确配置")
    else:
        logger.info("配置项检查通过")

    # 显示当前配置
    mode = "测试网" if config.USE_TESTNET else "主网"
    logger.info(f"运行模式: {mode}")
    logger.info(f"交易开关: {'开启' if config.TRADING_ENABLED else '关闭'}")
    logger.info(f"单次下单最大比例: {config.MAX_ORDER_RATIO:.1%}")
    logger.info(f"重复信号窗口: {config.DUPLICATE_SIGNAL_WINDOW}秒")
    logger.info(f"每日最大交易次数: {config.MAX_DAILY_TRADES}")

    # 初始化币安客户端并测试连接
    if not missing_config:
        try:
            trader = get_binance_trader()
            if trader.test_connection():
                logger.info("币安API连接测试成功")
            else:
                logger.error("币安API连接测试失败，请检查API Key配置")
        except Exception as e:
            logger.error(f"初始化币安客户端失败: {e}")

    logger.info("=" * 60)
    logger.info("系统启动完成，等待TradingView信号...")
    logger.info("=" * 60)

    yield  # 应用运行中

    # 关闭时执行
    logger.info("系统正在关闭...")


# 创建FastAPI应用
app = FastAPI(
    title="TradingView-Binance 自动量化交易系统",
    description="接收TradingView策略信号，自动在币安执行现货交易",
    version="1.0.0",
    lifespan=lifespan
)

# 注册路由
app.include_router(webhook_router)


@app.get("/")
async def root():
    """根路径 - 系统状态信息"""
    return {
        "name": "TradingView-Binance 自动量化交易系统",
        "version": "1.0.0",
        "status": "running",
        "mode": "testnet" if config.USE_TESTNET else "mainnet",
        "endpoints": {
            "webhook": "POST /webhook - 接收TradingView信号",
            "health": "GET /health - 健康检查",
            "balance": "GET /balance - 查询账户余额"
        }
    }


if __name__ == "__main__":
    # 直接运行时的启动配置
    print("=" * 60)
    print("  TradingView-Binance 自动量化交易系统")
    print("=" * 60)
    print("  [!] 风险提醒: 量化交易存在风险，请勿投入超过承受能力的资金")
    print("-" * 60)
    print("  请确保已完成以下配置:")
    print("  1. 已创建 .env 文件并填写必要配置")
    print("  2. 币安API Key已设置IP白名单")
    print("  3. 币安API Key仅开启现货交易权限")
    print("=" * 60)

    uvicorn.run(
        "main:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=False,
        log_level="info"
    )
