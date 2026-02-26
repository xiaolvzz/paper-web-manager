# 🐳 Docker快速启动指南

## 方法一：使用Docker Compose（推荐）

### 1. 安装Docker和Docker Compose

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo usermod -aG docker $USER
```

**Mac/Windows:**
下载Docker Desktop：https://www.docker.com/products/docker-desktop/

### 2. 配置环境变量

```bash
cd paper_web_manager
cp .env.example .env
# 编辑.env文件，填入Supabase配置
```

### 3. 启动服务

```bash
docker-compose up
```

第一次启动会自动构建镜像（约2-3分钟），之后启动只需几秒钟。

### 4. 访问

打开浏览器：http://localhost:8000

### 5. 停止服务

按 `Ctrl+C` 或运行：
```bash
docker-compose down
```

---

## 方法二：使用Docker命令

### 1. 构建镜像

```bash
docker build -t paper-manager .
```

### 2. 运行容器

```bash
docker run -d \
  -p 8000:8000 \
  -e SUPABASE_URL=your_url \
  -e SUPABASE_KEY=your_key \
  --name paper-manager \
  paper-manager
```

### 3. 查看日志

```bash
docker logs -f paper-manager
```

### 4. 停止容器

```bash
docker stop paper-manager
docker rm paper-manager
```

---

## 常见问题

**Q: Docker未安装怎么办？**
A: 参考上面的安装命令或访问 https://docs.docker.com/get-docker/

**Q: 端口8000被占用？**
A: 修改docker-compose.yml中的端口映射：`"8080:8000"`，然后访问8080端口

**Q: 修改代码后需要重启吗？**
A: 使用docker-compose会自动热重载，无需重启

---

## 🎉 优势

✅ 无需安装Python和依赖包
✅ 环境隔离，不污染系统
✅ 一条命令启动
✅ 跨平台兼容（Windows/Mac/Linux）
