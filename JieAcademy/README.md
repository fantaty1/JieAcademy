# 劫招社 — 永劫无间教学资料库

## 快速开始

### 后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python manage.py makemigrations users weapons heroes tutorials
python manage.py migrate

# 初始化武器和英雄数据
python manage.py init_data

# 创建管理员账号
python manage.py createsuperuser

# 启动后端服务
python manage.py runserver
```

默认管理员账号：`admin` / `admin123`

### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:3000

### Django Admin 后台

访问 http://localhost:8000/admin/ 管理数据

## 技术栈

- **前端**: Vue 3 + Vite + Element Plus + Pinia + Vue Router
- **后端**: Django 4+ + Django REST Framework + JWT
- **数据库**: SQLite (开发) / MySQL (部署)

## 项目结构

```
JieAcademy/
├── backend/          # Django 后端
├── frontend/         # Vue 3 前端
├── docs/             # 开发文档
└── README.md
```

## API 接口

| 路径 | 说明 |
|------|------|
| GET /api/weapons/ | 武器列表 |
| GET /api/weapons/{id}/ | 武器详情 |
| GET /api/weapons/{id}/combos/ | 武器连招 |
| GET /api/heroes/ | 英雄列表 |
| GET /api/heroes/{id}/ | 英雄详情 |
| GET /api/heroes/{id}/matchups/ | 英雄应对 |
| GET /api/heroes/{id}/combos/ | 英雄连招 |
| GET /api/combos/ | 连招列表 |
| GET /api/matchups/ | 应对列表 |
| POST /api/auth/login/ | 登录 |
| POST /api/auth/register/ | 注册 |

## 部署

1. 修改 `backend/naraka/settings.py` 切换为 MySQL 数据库
2. 前端 `npm run build` 后用 Nginx 托管
3. 后端用 Gunicorn + Nginx 反向代理
