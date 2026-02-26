# 🎨 功能定制指南

## 常见修改场景

### 1. 修改界面样式

**文件：** `frontend/assets/css/main.css`

**示例：修改主题色**
```css
:root {
    --primary-color: #2563eb;  /* 改成你喜欢的颜色 */
    --secondary-color: #64748b;
}
```

**示例：修改卡片样式**
```css
.paper-card {
    border-radius: 12px;  /* 修改圆角 */
    padding: 1.5rem;      /* 修改内边距 */
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);  /* 修改阴影 */
}
```

---

### 2. 添加新字段

**场景：** 想给论文添加"期刊名称"字段

**步骤1：修改数据库** (`database_schema.sql`)
```sql
ALTER TABLE papers ADD COLUMN journal TEXT;
```

**步骤2：修改数据模型** (`backend/models.py`)
```python
class PaperBase(BaseModel):
    title: str
    authors: Optional[str] = None
    journal: Optional[str] = None  # 新增字段
    year: Optional[int] = None
    # ...
```

**步骤3：修改前端表单** (`frontend/index.html`)
```html
<div class="mb-3">
    <label class="form-label">期刊名称</label>
    <input type="text" class="form-control" name="journal">
</div>
```

**步骤4：修改显示** (`frontend/assets/js/index.js`)
```javascript
${paper.journal ? `<span class="ms-3">📰 ${paper.journal}</span>` : ''}
```

---

### 3. 修改页面布局

**文件：** `frontend/index.html`, `frontend/paper.html`

**示例：改成两栏布局**
```html
<div class="row">
    <div class="col-md-8">
        <!-- 主要内容 -->
    </div>
    <div class="col-md-4">
        <!-- 侧边栏 -->
    </div>
</div>
```

---

### 4. 添加新功能：论文评分

**步骤1：数据库添加字段**
```sql
ALTER TABLE papers ADD COLUMN rating INTEGER CHECK (rating >= 1 AND rating <= 5);
```

**步骤2：后端添加字段**
```python
class PaperBase(BaseModel):
    # ... 其他字段
    rating: Optional[int] = Field(None, ge=1, le=5)
```

**步骤3：前端添加评分显示**
```javascript
function renderRating(rating) {
    if (!rating) return '';
    return '⭐'.repeat(rating);
}

// 在显示论文时调用
${renderRating(paper.rating)}
```

**步骤4：添加评分选择器**
```html
<div class="mb-3">
    <label class="form-label">评分</label>
    <select class="form-select" name="rating">
        <option value="">未评分</option>
        <option value="1">⭐</option>
        <option value="2">⭐⭐</option>
        <option value="3">⭐⭐⭐</option>
        <option value="4">⭐⭐⭐⭐</option>
        <option value="5">⭐⭐⭐⭐⭐</option>
    </select>
</div>
```

---

### 5. 修改搜索逻辑

**文件：** `backend/routers/papers.py`

**示例：添加摘要搜索**
```python
@router.get("/", response_model=List[Paper])
async def get_papers(
    search: Optional[str] = Query(None),
    # ...
):
    if search:
        # 修改这里，添加摘要搜索
        query = query.or_(
            f"title.ilike.%{search}%,authors.ilike.%{search}%,abstract.ilike.%{search}%"
        )
```

---

### 6. 自定义关系类型

**文件：** `frontend/paper.html`

**修改关系类型选项：**
```html
<select class="form-select" id="relationTypeSelect">
    <option value="method_similar">方法相似</option>
    <option value="problem_related">问题相关</option>
    <option value="extends">扩展关系</option>          <!-- 新增 -->
    <option value="compares_with">对比关系</option>     <!-- 新增 -->
    <option value="custom">自定义</option>
</select>
```

**同时修改颜色映射** (`frontend/assets/js/graph.js`)
```javascript
function getEdgeColor(relationType) {
    const colors = {
        'method_similar': '#2563eb',
        'problem_related': '#10b981',
        'extends': '#8b5cf6',        // 新增
        'compares_with': '#f59e0b',  // 新增
        'custom': '#64748b'
    };
    return colors[relationType] || '#64748b';
}
```

---

### 7. 添加导出功能

**新建文件：** `backend/routers/export.py`

```python
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import io

router = APIRouter(prefix="/api/export", tags=["export"])

@router.get("/papers/markdown")
async def export_papers_markdown(db: Client = Depends(get_db)):
    """导出所有论文为Markdown"""
    papers = db.table("papers").select("*").execute().data

    md_content = "# 我的论文库\n\n"
    for paper in papers:
        md_content += f"## {paper['title']}\n\n"
        md_content += f"**作者**: {paper['authors']}\n\n"
        md_content += f"**年份**: {paper['year']}\n\n"
        md_content += f"{paper['abstract']}\n\n"
        md_content += "---\n\n"

    return StreamingResponse(
        io.StringIO(md_content),
        media_type="text/markdown",
        headers={"Content-Disposition": "attachment; filename=papers.md"}
    )
```

**注册路由** (`backend/main.py`)
```python
from backend.routers import papers, analysis, relations, export

app.include_router(export.router)
```

**前端添加导出按钮**
```html
<a href="/api/export/papers/markdown" class="btn btn-outline-secondary" download>
    导出Markdown
</a>
```

---

### 8. 修改关系图样式

**文件：** `frontend/assets/js/graph.js`

**修改节点样式：**
```javascript
const nodes = new vis.DataSet(
    data.nodes.map(node => ({
        id: node.id,
        label: node.label,
        shape: 'circle',        // 改成圆形
        size: 30,              // 节点大小
        color: {
            background: '#ffffff',
            border: getNodeColor(node.year),  // 根据年份着色
        },
        font: { size: 14 }
    }))
);

function getNodeColor(year) {
    if (year >= 2020) return '#10b981';  // 绿色：新论文
    if (year >= 2015) return '#2563eb';  // 蓝色：中期
    return '#64748b';                     // 灰色：早期
}
```

---

## 🔧 调试技巧

### 1. 查看后端日志

运行时会显示所有API请求：
```
INFO:     127.0.0.1:50123 - "GET /api/papers/ HTTP/1.1" 200 OK
```

### 2. 使用浏览器开发者工具

- 按 F12 打开
- Console 标签：查看JavaScript错误
- Network 标签：查看API请求
- Elements 标签：实时修改HTML/CSS

### 3. 测试API

使用浏览器访问：
```
http://localhost:8000/docs
```

Swagger文档，可以直接测试所有API

---

## 💡 最佳实践

1. **修改前备份** - 复制文件再修改
2. **小步迭代** - 一次改一个功能
3. **测试验证** - 每次修改后测试
4. **查看日志** - 出错时看控制台输出
5. **使用Git** - 提交修改记录

---

## 📚 代码结构速查

```
backend/
├── models.py          # 数据模型定义
├── database.py        # 数据库连接
├── main.py           # 应用入口
└── routers/
    ├── papers.py     # 论文API（增删改查）
    ├── analysis.py   # 分析API
    └── relations.py  # 关系API

frontend/
├── index.html        # 论文列表页
├── paper.html        # 论文详情页
├── graph.html        # 关系图页
└── assets/
    ├── css/main.css  # 样式文件
    └── js/
        ├── api.js      # API封装
        ├── index.js    # 列表页逻辑
        ├── paper.js    # 详情页逻辑
        └── graph.js    # 图谱逻辑
```

---

需要添加特定功能？告诉我，我可以提供具体代码！🚀
