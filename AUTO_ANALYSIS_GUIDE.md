# 📊 AI自动分析功能使用指南

## 🎉 新功能概览

### 1. **双Tab页面结构**
论文详情页现在分为两个Tab：
- **💬 论文讨论**：原有的AI对话、分析记录等功能
- **💻 源码信息**：展示开源代码相关信息

### 2. **AI自动分析**
添加论文后，AI会自动提取：
- 📝 **主要工作**：论文的核心贡献
- 💡 **创新点列表**：2-5个关键创新点
- 🏷️ **结构化标签**：技术关键词（如Transformer、NLP等）
- 💻 **源码链接**：自动识别GitHub等代码仓库链接

### 3. **可编辑字段**
AI生成的所有信息都可以手动编辑和完善。

---

## 🚀 快速开始

### 步骤1：执行数据库迁移

**重要**：首次使用前，需要在Supabase执行SQL迁移。

1. 登录 Supabase 控制台
2. 进入 **SQL Editor**
3. 打开 `migrations/003_add_auto_analysis_fields.sql`
4. 复制所有SQL代码
5. 在SQL Editor中执行

**迁移内容**：
```sql
-- 添加新字段：
ALTER TABLE papers ADD COLUMN IF NOT EXISTS source_code_url TEXT;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS main_work TEXT;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS innovations JSONB DEFAULT '[]'::jsonb;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS structured_tags JSONB DEFAULT '[]'::jsonb;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS auto_analyzed BOOLEAN DEFAULT FALSE;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS auto_analysis_date TIMESTAMPTZ;
```

### 步骤2：添加论文

有三种方式添加论文：

#### 方式1：手动创建
1. 在首页点击"添加论文"
2. 填写基本信息（标题、作者、摘要等）
3. 保存后进入论文详情页

#### 方式2：arXiv导入
1. 进入论文详情页
2. 在"论文内容"区域选择"arXiv导入"
3. 输入arXiv ID（如：2301.12345）
4. 自动获取标题、作者、摘要、PDF等

#### 方式3：PDF上传
1. 进入论文详情页
2. 在"论文内容"区域选择"上传PDF"
3. 选择PDF文件上传
4. 系统自动提取文本内容

### 步骤3：触发AI分析

**自动触发**（推荐）：
- 首次访问未分析的论文时，会提示"是否进行AI分析"
- 点击"确定"即可

**手动触发**：
1. 打开论文详情页
2. 点击"一键分析"按钮
3. 等待AI分析完成（约10-30秒）

### 步骤4：查看和编辑分析结果

#### 查看结果
AI分析完成后，会在页面顶部显示：
```
📊 AI自动分析
📝 主要工作：这篇论文提出了...
💡 创新点：
   1. 创新点1
   2. 创新点2
🏷️ 标签：Transformer NLP Attention
💻 源码：https://github.com/...
```

#### 编辑和保存
有两种方式保存：

**方式1：直接保存**
- 点击"保存到数据库"按钮
- 分析结果直接存入数据库

**方式2：编辑后保存**
- 点击"编辑"按钮
- 分析内容自动填充到表单
- 手动修改完善
- 点击"保存分析"

---

## 💻 源码信息功能

### 查看源码Tab

1. 切换到"💻 源码信息" Tab
2. 如果AI找到了源码链接，会自动显示

### 功能特性

#### 1. **源码链接管理**
- 手动输入或从AI分析自动填充
- 点击"🔗 打开链接"直接访问

#### 2. **GitHub仓库信息**（自动获取）
- 仓库名称和描述
- ⭐ Stars 和 🍴 Forks 数量
- 编程语言
- 最后更新时间

#### 3. **README预览**
- 自动获取GitHub README内容
- 支持基本Markdown渲染
- 方便快速了解项目

#### 4. **使用说明**
- 记录代码的安装步骤
- 运行方法
- 使用示例

#### 5. **代码特点**
- 记录代码的优势
- 注意事项
- 性能特点

---

## 🎯 使用场景

### 场景1：快速了解新论文

```
1. 添加论文（标题+摘要）
2. 点击"一键分析"
3. 10秒内获得：
   - 主要工作概述
   - 3-5个创新点
   - 技术标签
   - 源码链接（如有）
4. 决定是否深入阅读
```

### 场景2：整理论文笔记

```
1. AI分析生成初稿
2. 点击"编辑"
3. 补充个人理解
4. 添加更多创新点
5. 完善标签分类
6. 保存完整笔记
```

### 场景3：收集论文代码

```
1. 添加论文
2. AI自动识别源码链接
3. 切换到"源码信息"Tab
4. 查看GitHub仓库详情
5. 阅读README了解使用方法
6. 记录安装和运行笔记
7. 标注代码特点
```

### 场景4：批量管理论文

```
1. 批量添加多篇论文
2. 逐个运行AI分析
3. 快速生成标签
4. 统一分类管理
5. 按标签筛选论文
```

---

## 📝 字段说明

### 新增数据库字段

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `source_code_url` | TEXT | 源码链接 | `https://github.com/user/repo` |
| `main_work` | TEXT | 主要工作描述 | `提出了Transformer架构...` |
| `innovations` | JSONB | 创新点数组 | `["自注意力机制", "位置编码"]` |
| `structured_tags` | JSONB | 标签数组 | `["Transformer", "NLP"]` |
| `auto_analyzed` | BOOLEAN | 是否已分析 | `true` / `false` |
| `auto_analysis_date` | TIMESTAMPTZ | 分析时间 | `2024-01-01 12:00:00` |

### API端点

#### POST /api/papers/{paper_id}/auto-analyze

**参数**：
- `update_db` (query, boolean): 是否更新数据库，默认true

**返回**：
```json
{
  "success": true,
  "analysis": {
    "main_work": "这篇论文提出了...",
    "innovations": ["创新点1", "创新点2"],
    "structured_tags": ["标签1", "标签2"],
    "source_code_url": "https://github.com/...",
    "has_code": true
  },
  "message": "分析完成",
  "updated": true
}
```

---

## 💡 使用技巧

### 1. **提高分析质量**

✅ **推荐做法**：
- 确保论文有完整摘要
- 如果可能，上传PDF或添加全文内容
- 信息越完整，AI分析越准确

❌ **避免**：
- 只有标题，没有摘要
- 摘要过短（少于50字）
- 非英文论文可能识别不准

### 2. **标签管理**

AI生成的标签是**结构化**的（JSON数组），而老的`tags`字段是**逗号分隔字符串**。

**迁移建议**：
```javascript
// 旧字段：tags = "Transformer, NLP, Deep Learning"
// 新字段：structured_tags = ["Transformer", "NLP", "Deep Learning"]
```

系统已自动将旧标签转换为新格式。

### 3. **源码链接识别**

AI会在以下位置搜索源码链接：
- 论文摘要中的URL
- 全文中的GitHub、GitLab等关键词
- "Code available at" 等标记

**手动补充**：
如果AI没找到，可以：
1. 在PDF中搜索"github"
2. 访问论文官网
3. Google: "论文标题 github"
4. 手动添加到源码Tab

### 4. **批量分析**

目前不支持一键批量分析，但可以：
```
1. 打开论文列表
2. 依次打开每篇论文
3. 点击"一键分析"
4. 关闭，打开下一篇
```

**未来计划**：添加批量分析按钮

---

## ❓ 常见问题

### Q1: 分析时间太长怎么办？

**A:** 分析时间取决于：
- 论文长度（摘要 vs 全文）
- AI服务商速度
- 网络状况

**优化建议**：
- 使用Gemini或智谱AI（速度快）
- 只提供摘要即可（不必上传全文）
- 等待10-30秒即可完成

### Q2: AI分析结果不准确？

**A:** 可能原因：
- 论文内容不完整
- 摘要过于简短
- 专业术语AI不理解

**解决方法**：
- 点击"编辑"手动修改
- 补充更多论文内容后重新分析
- 使用不同的AI模型（在环境变量中配置）

### Q3: 源码链接没有识别出来？

**A:** AI可能无法100%识别所有链接。

**手动查找**：
1. 在PDF中搜索"github"、"code"
2. 访问作者主页
3. 在论文官网查找
4. Google搜索：`论文标题 code`

**手动添加**：
切换到"源码信息"Tab，手动输入链接并保存。

### Q4: 已有论文如何批量分析？

**A:** 目前需要手动逐个分析：
```
1. 访问论文详情页
2. 点击"一键分析"
3. 保存结果
4. 继续下一篇
```

**计划功能**：未来会添加批量分析功能。

### Q5: GitHub信息无法加载？

**A:** 可能原因：
- GitHub API限流（未认证每小时60次）
- 网络问题
- 仓库是私有的

**解决**：
- 等待一小时后重试
- 直接访问GitHub链接
- 手动记录仓库信息

### Q6: 分析结果可以导出吗？

**A:** 目前不支持直接导出。

**临时方案**：
- 复制分析内容粘贴到笔记
- 保存到"个人备注"字段
- 使用浏览器打印功能保存为PDF

---

## 🔧 配置说明

### AI服务配置

自动分析功能需要配置AI服务（已在之前配置完成）。

**支持的AI服务**：
- Gemini（推荐，免费）
- 智谱AI（推荐，glm-4-flash免费）
- DeepSeek（推荐，极低成本）
- 通义千问
- Claude
- OpenAI
- Groq

**环境变量**：
```env
# 至少配置一个
GEMINI_API_KEY=your-key
ZHIPU_API_KEY=your-key
DEEPSEEK_API_KEY=your-key
```

详见：`ENV_VARIABLES_GUIDE.md`

### 自定义AI提示词

如果想自定义分析的格式，可以修改：

文件：`backend/routers/papers.py`
函数：`auto_analyze_paper()`
变量：`system_prompt`

---

## 🚀 未来功能计划

- [ ] 批量自动分析（一键分析所有论文）
- [ ] 自定义提示词模板
- [ ] 分析历史记录
- [ ] 导出分析结果（Markdown、PDF）
- [ ] 代码片段收藏
- [ ] README自动翻译
- [ ] 源码下载和本地存储
- [ ] 多版本代码对比

---

## 💬 反馈与建议

如有问题或建议，欢迎反馈！

---

**更新日期**：2024-02-27
**版本**：v2.0
