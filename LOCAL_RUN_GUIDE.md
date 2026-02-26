# 💻 本地运行完整指南

## 方法一：直接运行（推荐）

### 前置要求
- Python 3.8 或更高版本
- pip包管理器

### 快速启动（Windows/Mac/Linux）

#### 1. 下载代码

**方式A：使用Git**
```bash
git clone https://github.com/xiaolvzz/paper-web-manager.git
cd paper-web-manager
```

**方式B：直接下载**
- 访问：https://github.com/xiaolvzz/paper-web-manager
- 点击绿色的 "Code" 按钮
- 选择 "Download ZIP"
- 解压到任意文件夹

#### 2. 创建虚拟环境（可选但推荐）

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. 安装依赖

```bash
pip install fastapi uvicorn python-dotenv supabase pydantic python-multipart
```

或

```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量

编辑 `.env` 文件（已经配置好了）：

```
SUPABASE_URL=https://wlslekyepjebnzjmslld.supabase.co
SUPABASE_KEY=eyJhbGci...（已配置）
```

#### 5. 启动服务

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### 6. 访问

打开浏览器：**http://localhost:8000**

✅ 完成！开始使用！

---

## 方法二：使用Python自带的http.server（静态预览）

如果只想快速预览前端界面（无后端功能）：

```bash
cd frontend
python -m http.server 8080
```

访问：http://localhost:8080

⚠️ 注意：这种方式无法连接数据库，只能看界面

---

## 常见问题

### Q: 如何检查Python版本？

```bash
python --version
# 或
python3 --version
```

需要 Python 3.8 或更高版本

### Q: pip安装失败？

尝试：
```bash
pip3 install -r requirements.txt
# 或使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### Q: 端口8000被占用？

修改端口：
```bash
uvicorn backend.main:app --reload --port 8080
```

### Q: 找不到uvicorn命令？

确保已激活虚拟环境，或使用：
```bash
python -m uvicorn backend.main:app --reload
```

---

## 功能测试清单

启动成功后，测试以下功能：

- [ ] 访问首页，看到论文列表界面
- [ ] 点击"添加论文"，填写表单
- [ ] 成功添加一篇论文
- [ ] 查看论文详情
- [ ] 添加分析记录
- [ ] 上传框架图
- [ ] 建立论文关联
- [ ] 查看关系图

---

## 修改代码后

修改代码后，服务会自动重启（因为使用了 `--reload` 参数）

刷新浏览器即可看到修改效果！

---

## 停止服务

按 `Ctrl + C` 停止运行

---

## 提示

1. 虚拟环境可以避免依赖冲突
2. `--reload` 参数让修改代码后自动重启
3. 数据存储在Supabase云端，任何地方运行都能同步
4. 可以随时修改前端HTML/CSS/JS代码进行定制

---

祝您使用愉快！🚀
