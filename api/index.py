"""Vercel serverless function entry point"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import sys
import os
import asyncio

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入FastAPI应用
from backend.main import app
from fastapi.testclient import TestClient

# 创建测试客户端用于转发请求
client = TestClient(app)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def do_PUT(self):
        self._handle_request()

    def do_DELETE(self):
        self._handle_request()

    def do_OPTIONS(self):
        # 处理CORS预检请求
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
        return

    def _handle_request(self):
        try:
            # 获取请求路径和查询参数
            parsed_path = urlparse(self.path)
            path = parsed_path.path

            # 移除/api前缀，因为FastAPI内部路由不包含/api
            # 例如：/api/health → /health, /api/papers → /papers
            if path.startswith('/api/'):
                path = path[4:]  # 去掉'/api'
            elif path.startswith('/api'):
                path = path[4:]  # 去掉'/api'

            # 保留查询参数
            if parsed_path.query:
                path = f"{path}?{parsed_path.query}"

            # 读取请求体（如果有）
            content_length = self.headers.get('Content-Length')
            body = None
            if content_length:
                body = self.rfile.read(int(content_length))

            # 使用TestClient转发到FastAPI
            method = self.command.lower()
            if method == 'get':
                response = client.get(path)
            elif method == 'post':
                response = client.post(path, content=body, headers=dict(self.headers))
            elif method == 'put':
                response = client.put(path, content=body, headers=dict(self.headers))
            elif method == 'delete':
                response = client.delete(path)
            else:
                self.send_response(405)
                self.end_headers()
                return

            # 返回响应
            self.send_response(response.status_code)
            self.send_header('Content-type', response.headers.get('content-type', 'application/json'))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            self.wfile.write(response.content)

        except Exception as e:
            # 错误处理
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            error_response = {
                "error": str(e),
                "type": type(e).__name__,
                "path": self.path
            }
            self.wfile.write(json.dumps(error_response).encode())
