# TradingView-Binance 自动量化交易系统

## ⚠️ 重要风险提醒

**量化交易存在风险，请务必注意以下几点：**

1. **不要投入超过自己承受能力的资金**
2. **首次使用务必在测试网验证，确认无误后再切换到主网**
3. **定期检查日志，监控系统运行状态**
4. **币安API Key只能开启"现货交易"权限，绝对不要开启"提现"权限**
5. **务必在币安后台设置API Key的IP白名单**

---

## 项目简介

这是一个将TradingView策略信号自动转化为币安现货交易的自动化系统。系统采用三层架构：

```
TradingView策略 → Webhook信号 → Python后端服务 → 币安API → 现货交易
```

### 核心功能

- ✅ 接收TradingView Webhook信号
- ✅ 自动解析信号并执行现货交易
- ✅ 支持币安测试网和主网切换
- ✅ 完整的风控机制（全局开关、重复信号过滤、余额检查、每日限额）
- ✅ 按日期分割的日志记录
- ✅ 可选的企业微信/邮件通知

---

## 项目结构

```
TV/
├── .env.example          # 配置文件模板
├── .env                  # 实际配置文件（需自行创建）
├── requirements.txt      # Python依赖
├── README.md            # 项目说明文档
├── main.py              # FastAPI应用入口
├── config.py            # 配置管理模块
├── binance_client.py    # 币安API客户端
├── webhook.py           # Webhook接口模块
├── risk_manager.py      # 风控管理模块
├── tradingview_signal.py # 信号数据模型
├── notifications.py     # 通知模块
├── logger_config.py     # 日志配置
├── logs/                # 日志目录（自动创建）
└── systemd/
    └── tv-trader.service # systemd服务配置
```

---

## 快速开始

### 1. 环境准备

确保已安装Python 3.8+：

```bash
python3 --version
```

### 2. 克隆项目

```bash
cd /opt
git clone <your-repo-url> tv-trader
cd tv-trader
```

### 3. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置环境变量

```bash
cp .env.example .env
nano .env  # 或使用其他编辑器
```

**必须配置的项：**
- `BINANCE_API_KEY` - 币安API Key
- `BINANCE_API_SECRET` - 币安API Secret
- `WEBHOOK_SECRET` - Webhook验证密钥（设置一个复杂的随机字符串）

**首次使用务必设置：**
- `USE_TESTNET=True` - 使用测试网

### 6. 启动服务

```bash
# 开发模式
python main.py

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8080
```

---

## 币安API配置指南

### 创建API Key

1. 登录币安官网
2. 进入 [API管理](https://www.binance.com/zh-CN/my/settings/api-management)
3. 点击"创建API"
4. **重要：只勾选"现货交易"权限，绝对不要勾选"提现"权限**
5. 记录生成的API Key和Secret

### 设置IP白名单

1. 在API管理页面找到你创建的API Key
2. 点击"编辑"->"IP访问限制"
3. 添加你的服务器公网IP
4. 保存设置

### 获取测试网API Key

1. 访问 [币安测试网](https://testnet.binance.vision/)
2. 使用GitHub账号登录
3. 生成测试网API Key和Secret
4. 将测试网配置填入`.env`文件

---

## TradingView Webhook配置

### 创建警报

1. 在TradingView打开你的策略图表
2. 点击"警报"按钮创建新警报
3. 在"条件"中选择你的策略

### 配置Webhook

1. 在警报设置中，勾选"Webhook URL"
2. 填入你的服务器地址：`http://your-server-ip:8080/webhook`

### 配置消息格式

在"消息"字段中填入以下JSON格式（根据你的策略调整）：

```json
{
    "secret": "your_webhook_secret",
    "symbol": "{{ticker}}",
    "side": "BUY",
    "quantity": 0.001,
    "order_type": "MARKET",
    "timestamp": "{{timenow}}"
}
```

**字段说明：**
- `secret` - 必须与`.env`中的`WEBHOOK_SECRET`一致
- `symbol` - 交易对，`{{ticker}}`会自动替换为当前品种
- `side` - 交易方向：`BUY`(买入)或`SELL`(卖出)
- `quantity` - 交易数量
- `order_type` - 订单类型，当前只支持`MARKET`(市价单)
- `timestamp` - 信号时间，`{{timenow}}`会自动替换

### 为买卖信号分别创建警报

你需要为买入和卖出分别创建两个警报：

**买入警报消息示例：**
```json
{
    "secret": "your_webhook_secret",
    "symbol": "{{ticker}}",
    "side": "BUY",
    "quantity": 0.001,
    "order_type": "MARKET",
    "timestamp": "{{timenow}}"
}
```

**卖出警报消息示例：**
```json
{
    "secret": "your_webhook_secret",
    "symbol": "{{ticker}}",
    "side": "SELL",
    "quantity": 0.001,
    "order_type": "MARKET",
    "timestamp": "{{timenow}}"
}
```

---

## 风控机制说明

### 1. 全局交易开关

在`.env`中设置：
```bash
TRADING_ENABLED=True   # 开启交易
TRADING_ENABLED=False  # 关闭所有交易（紧急停止）
```

### 2. 重复信号过滤

同一交易对的同一方向信号，在配置的时间窗口内只执行一次：
```bash
DUPLICATE_SIGNAL_WINDOW=60  # 60秒内不重复执行
```

### 3. 单次下单比例限制

限制单次交易金额占账户总资金的最大比例：
```bash
MAX_ORDER_RATIO=0.1  # 不超过总资产的10%
```

### 4. 每日最大交易次数

防止策略异常导致频繁交易：
```bash
MAX_DAILY_TRADES=50  # 每天最多50次交易
```

### 5. 余额校验

下单前自动检查账户余额是否充足。

---

## API接口说明

### POST /webhook

接收TradingView信号并执行交易。

**请求示例：**
```bash
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "secret": "your_webhook_secret",
    "symbol": "BTCUSDT",
    "side": "BUY",
    "quantity": 0.001,
    "order_type": "MARKET"
  }'
```

**成功响应：**
```json
{
    "status": "success",
    "order_id": 123456789,
    "executed_qty": 0.001,
    "cumul_quote": 50.25
}
```

### GET /health

健康检查接口，返回系统状态和交易统计。

### GET /balance

查询当前账户余额。

---

## 生产环境部署

### 使用systemd部署

1. 复制服务文件：
```bash
sudo cp systemd/tv-trader.service /etc/systemd/system/
```

2. 修改服务文件中的路径和用户：
```bash
sudo nano /etc/systemd/system/tv-trader.service
```

3. 启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable tv-trader
sudo systemctl start tv-trader
```

4. 查看状态和日志：
```bash
sudo systemctl status tv-trader
sudo journalctl -u tv-trader -f
```

### 使用Docker部署（可选）

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

```bash
docker build -t tv-trader .
docker run -d --name tv-trader --env-file .env -p 8080:8080 tv-trader
```

---

## 日志说明

日志文件保存在`logs/`目录下：

- `tv_trader.log` - 系统运行日志（按日期分割，保留30天）
- `trades.log` - 交易专用日志（按日期分割，保留90天）

查看实时日志：
```bash
tail -f logs/tv_trader.log
```

---

## 测试流程

### 1. 测试网验证

确保`.env`中设置`USE_TESTNET=True`，然后：

```bash
# 启动服务
python main.py

# 测试健康检查
curl http://localhost:8080/health

# 测试Webhook
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "secret": "your_webhook_secret",
    "symbol": "BTCUSDT",
    "side": "BUY",
    "quantity": 0.001,
    "order_type": "MARKET"
  }'
```

### 2. 检查交易结果

```bash
# 查看账户余额
curl http://localhost:8080/balance

# 查看交易日志
cat logs/trades.log
```

### 3. 切换到主网

确认测试网一切正常后：
1. 在`.env`中将`USE_TESTNET`改为`False`
2. 填入主网的API Key和Secret
3. 重启服务

---

## 常见问题

### Q: 信号发送成功但没有执行交易？

检查以下几点：
1. Webhook密钥是否正确
2. 交易开关是否开启（`TRADING_ENABLED=True`）
3. 是否触发了重复信号过滤
4. 是否达到每日交易次数限制
5. 账户余额是否充足

### Q: 如何紧急停止交易？

将`.env`中的`TRADING_ENABLED`设置为`False`，然后重启服务。

### Q: 日志在哪里？

在项目目录的`logs/`文件夹下，按日期自动分割。

---

## 安全建议

1. **API权限**：只开启现货交易，不开提现
2. **IP白名单**：限制API Key只能从服务器IP访问
3. **密钥安全**：`.env`文件不要提交到代码仓库
4. **定期检查**：每天查看交易日志和账户状态
5. **资金控制**：不要在账户中放过多资金
6. **测试优先**：任何配置变更先在测试网验证

---

## 许可证

MIT License

---

**再次提醒：量化交易存在风险，请谨慎使用，不要投入超过自己承受能力的资金。**
