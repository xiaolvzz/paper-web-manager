# AI模型选择器使用指南

## 功能概述

现在你可以在论文详情页面的"AI代码架构分析"区域看到一个模型选择下拉框，可以：
- 查看所有已配置的AI模型
- 手动选择使用哪个模型进行代码分析
- 查看未配置的模型，并获取配置指南

## 使用方法

### 1. 查看可用模型

打开任意论文的详情页面，在"AI代码架构分析"区域会看到：

```
选择AI模型：
[Google Gemini (gemini-2.0-flash-exp) - 免费 [默认]]
```

下拉框会显示：
- ✅ **已配置的模型**：可以直接选择使用
  - 显示格式：`模型名称 (模型ID) - 成本`
  - 默认模型会标注 `[默认]`
- ❌ **未配置的模型**：灰色显示，不可选择
  - 显示格式：`模型名称 (模型ID) - 未配置`

### 2. 选择模型

1. 点击下拉框
2. 选择想要使用的AI模型
3. 系统会自动切换到该模型
4. 后续的代码分析将使用这个模型

### 3. 查看配置指南

在模型选择器下方，你会看到提示信息：
- 如果有已配置的模型：`已配置 3/7 个模型 | 配置更多`
- 如果没有配置：`⚠️ 点击查看配置指南`

点击"配置更多"或"点击查看配置指南"会弹出详细的配置说明。

## 支持的AI模型

| 模型 | Provider ID | 成本 | 特点 |
|------|------------|------|------|
| Google Gemini | `gemini` | 免费 | 性能强，完全免费 |
| 智谱AI (GLM-4) | `zhipu` | 免费 | 中文理解强，国内访问 |
| DeepSeek | `deepseek` | 极低 | 性价比极高 |
| 通义千问 | `qwen` | 廉价 | 阿里云，稳定快速 |
| Anthropic Claude | `claude` | 付费 | 推理能力最强 |
| OpenAI GPT | `openai` | 付费 | 业界标杆 |
| Groq | `groq` | 免费 | 速度极快 |

## 配置新模型

### 方法1：编辑 .env 文件

在项目根目录的 `.env` 文件中添加：

```bash
# 示例：配置Claude模型
CLAUDE_API_KEY=sk-ant-api03-xxx...
CLAUDE_MODEL=claude-3-5-haiku-20241022

# 示例：配置Gemini模型
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-2.0-flash-exp
```

然后重启应用：
```bash
# 本地开发
python -m uvicorn backend.main:app --reload
```

### 方法2：Vercel环境变量

1. 登录Vercel控制台
2. 进入项目设置
3. Settings → Environment Variables
4. 添加对应的环境变量（如 `CLAUDE_API_KEY`）
5. 重新部署

### 方法3：使用配置脚本（仅本地）

```bash
./configure_ai.sh
```

## API接口

### 获取模型列表

```http
GET /api/ai/models
```

**响应示例**：
```json
{
  "models": [
    {
      "id": "gemini",
      "name": "Google Gemini",
      "model": "gemini-2.0-flash-exp",
      "configured": true,
      "is_default": true,
      "cost": "免费",
      "description": "性能强，完全免费"
    },
    {
      "id": "claude",
      "name": "Anthropic Claude",
      "model": "claude-3-5-haiku-20241022",
      "configured": false,
      "is_default": false,
      "cost": "付费",
      "description": "推理能力最强"
    }
  ],
  "current_provider": "gemini",
  "any_configured": true
}
```

### 选择模型

```http
POST /api/ai/select-model
Content-Type: application/json

{
  "provider_id": "claude"
}
```

**响应示例**：
```json
{
  "success": true,
  "provider": "Anthropic Claude",
  "model": "claude-3-5-haiku-20241022",
  "provider_id": "claude"
}
```

### 代码分析（指定模型）

```http
POST /api/code-analysis/analyze
Content-Type: application/json

{
  "repo_url": "https://github.com/user/repo",
  "paper_id": 123,
  "force_refresh": false,
  "provider_id": "claude"  // 可选，不指定则使用当前选择的模型
}
```

## 技术实现

### 后端架构

1. **AIManager 增强**：
   - 新增 `all_providers` 字典，存储所有已配置的providers
   - 新增 `get_all_providers_status()` 方法，返回模型状态
   - 新增 `use_provider(provider_id)` 方法，临时切换模型
   - 新增 `get_provider_id()` 方法，获取当前provider ID

2. **新增API端点**：
   - `/api/ai/models` - 获取模型列表
   - `/api/ai/select-model` - 选择模型

3. **代码分析增强**：
   - 支持 `provider_id` 参数
   - 临时切换到指定模型进行分析
   - 分析完成后恢复原模型

### 前端实现

1. **页面加载时**：
   - 调用 `/api/ai/models` 获取模型列表
   - 渲染模型选择器
   - 显示配置状态

2. **用户选择模型时**：
   - 调用 `/api/ai/select-model` 切换模型
   - 更新全局变量 `selectedProviderId`
   - 显示切换成功提示

3. **代码分析时**：
   - 如果用户选择了特定模型，传递 `provider_id`
   - 分析结果头部显示使用的模型信息

## 优势

1. **灵活性**：根据任务复杂度选择合适的模型
2. **成本优化**：简单任务用免费模型，复杂任务用高级模型
3. **透明性**：清楚知道每次分析使用的是哪个模型
4. **易配置**：界面直接显示配置状态，一键查看配置指南

## 注意事项

1. **会话级别切换**：模型选择只在当前会话有效，刷新页面会恢复默认模型
2. **缓存机制**：分析结果会缓存，不同模型的分析结果会覆盖之前的缓存
3. **API限制**：注意各模型的API限流和配额限制
4. **网络要求**：部分模型（如Gemini）可能在某些地区无法访问

## 推荐配置

### 场景1：个人学习（零成本）
```bash
GEMINI_API_KEY=xxx        # 主力，完全免费
ZHIPU_API_KEY=xxx         # 备用，国内访问
```

### 场景2：公司项目（质量优先）
```bash
CLAUDE_API_KEY=xxx        # 主力，推理最强
DEEPSEEK_API_KEY=xxx      # 备用，性价比高
```

### 场景3：混合使用（平衡）
```bash
GEMINI_API_KEY=xxx        # 日常任务
CLAUDE_API_KEY=xxx        # 复杂任务
GROQ_API_KEY=xxx          # 快速响应
```

## 故障排查

### 问题1：下拉框显示"未配置任何AI模型"
**解决**：
- 检查 `.env` 文件是否正确配置API密钥
- 重启应用
- 查看后端日志确认模型是否加载

### 问题2：选择模型后提示"未配置"
**解决**：
- 该模型的API密钥未配置
- 在 `.env` 中添加对应的 `XXX_API_KEY`
- 重启应用

### 问题3：模型切换不生效
**解决**：
- 检查浏览器控制台是否有错误
- 确认 `/api/ai/select-model` 接口返回成功
- 尝试刷新页面

---

## 更多帮助

查看完整配置指南：
- `QUICK_START_AI.md` - 快速开始
- `AI_CONFIG_GUIDE.md` - 详细配置
