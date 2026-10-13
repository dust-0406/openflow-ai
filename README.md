# OpenFlow AI

基于 FastAPI 的 AI 工作流自动化项目。

## 项目结构
```
openflow-ai/
├── app/
│   ├── api/          # API 路由
│   ├── services/     # 业务逻辑层
│   ├── templates/    # 前端模板
│   ├── main.py       # 应用入口
│   ├── models.py     # 数据模型
│   └── database.py   # 数据库连接
├── tests/            # 测试用例
├── requirements.txt  # 依赖清单
└── README.md
```

## 快速开始
1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 启动服务：
```bash
uvicorn app.main:app --reload
```

3. 访问 http://localhost:8000 查看效果。
