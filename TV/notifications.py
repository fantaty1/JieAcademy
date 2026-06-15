"""
通知模块
提供交易结果的推送通知功能（企业微信、邮件）
"""
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import config
from logger_config import logger


def send_wecom_notification(title: str, content: str) -> bool:
    """
    发送企业微信Webhook通知

    Args:
        title: 通知标题
        content: 通知内容

    Returns:
        是否发送成功
    """
    if not config.ENABLE_NOTIFICATIONS or not config.WECOM_WEBHOOK_URL:
        return False

    try:
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"## {title}\n{content}"
            }
        }
        response = requests.post(
            config.WECOM_WEBHOOK_URL,
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            logger.info(f"企业微信通知发送成功: {title}")
            return True
        else:
            logger.warning(f"企业微信通知发送失败: {response.text}")
            return False
    except Exception as e:
        logger.error(f"企业微信通知发送异常: {e}")
        return False


def send_email_notification(subject: str, body: str) -> bool:
    """
    发送邮件通知

    Args:
        subject: 邮件主题
        body: 邮件正文

    Returns:
        是否发送成功
    """
    if not config.ENABLE_NOTIFICATIONS or not all([
        config.SMTP_SERVER,
        config.SMTP_USERNAME,
        config.SMTP_PASSWORD,
        config.NOTIFICATION_EMAIL
    ]):
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = config.SMTP_USERNAME
        msg["To"] = config.NOTIFICATION_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"邮件通知发送成功: {subject}")
        return True
    except Exception as e:
        logger.error(f"邮件通知发送异常: {e}")
        return False


def notify_trade_result(
    symbol: str,
    side: str,
    success: bool,
    quantity: float = 0,
    price: float = 0,
    message: str = ""
) -> None:
    """
    发送交易结果通知

    Args:
        symbol: 交易对
        side: 交易方向
        success: 是否成功
        quantity: 交易数量
        price: 交易价格
        message: 附加信息
    """
    if not config.ENABLE_NOTIFICATIONS:
        return

    status = "✅ 成功" if success else "❌ 失败"
    title = f"交易{status}: {symbol}"

    content = f"""
**交易对**: {symbol}
**方向**: {side}
**状态**: {status}
**数量**: {quantity}
**价格**: {price}
**信息**: {message}
"""

    # 尝试发送通知
    send_wecom_notification(title, content)
    send_email_notification(title, content)
