"""代码架构分析API"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from supabase import Client
from backend.database import get_db
from backend.utils.ai_providers import ai_manager
from datetime import datetime
import httpx
import re

router = APIRouter(prefix="/code-analysis", tags=["code-analysis"])


class CodeAnalysisRequest(BaseModel):
    """代码分析请求模型"""
    repo_url: str
    paper_id: Optional[int] = None
    force_refresh: bool = False  # 是否强制重新分析


class CodeAnalysisResponse(BaseModel):
    """代码分析响应模型"""
    success: bool
    analysis: str
    repo_url: str
    ai_provider: str  # 使用的AI提供商
    ai_model: str     # 使用的AI模型
    cached: bool      # 是否来自缓存
    analysis_date: Optional[str] = None  # 分析时间


@router.post("/analyze")
async def analyze_code_architecture(request: CodeAnalysisRequest, db: Client = Depends(get_db)):
    """
    分析GitHub代码仓库的架构
    使用AI按照5级深度分析代码结构、算法逻辑和数据流向
    支持缓存，避免重复分析
    """
    try:
        repo_url = request.repo_url.strip()
        paper_id = request.paper_id
        force_refresh = request.force_refresh

        # 验证GitHub URL
        if not repo_url.startswith('http') or 'github.com' not in repo_url:
            raise HTTPException(status_code=400, detail="请提供有效的GitHub仓库链接")

        # 检查是否已有分析结果（如果提供了paper_id）
        if paper_id and not force_refresh:
            paper_response = db.table("papers").select(
                "code_analysis_result, code_analysis_date, code_analysis_model"
            ).eq("id", paper_id).execute()

            if paper_response.data:
                paper = paper_response.data[0]
                cached_analysis = paper.get("code_analysis_result")

                if cached_analysis:
                    # 返回缓存的分析结果
                    return CodeAnalysisResponse(
                        success=True,
                        analysis=cached_analysis,
                        repo_url=repo_url,
                        ai_provider="Cached",
                        ai_model=paper.get("code_analysis_model") or "Unknown",
                        cached=True,
                        analysis_date=paper.get("code_analysis_date")
                    )

        # 提取仓库信息 (owner/repo)
        match = re.search(r'github\.com/([^/]+)/([^/]+)', repo_url)
        if not match:
            raise HTTPException(status_code=400, detail="无法解析GitHub仓库信息")

        owner = match.group(1)
        repo = match.group(2).rstrip('.git')

        # 获取README内容（用于AI理解项目）
        readme_content = await fetch_github_readme(owner, repo)

        # 获取主要Python文件列表（用于AI理解代码结构）
        file_structure = await fetch_repo_structure(owner, repo)

        # 尝试获取主要模型文件的代码片段
        model_code = await fetch_model_code(owner, repo, file_structure)

        # 构建AI提示词（包含目录结构分析）
        prompt = build_analysis_prompt(repo_url, readme_content, file_structure, model_code)

        # 调用AI生成分析
        ai_response = await ai_manager.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=4096  # 增加token限制以支持更详细的分析
        )

        analysis_text = ai_response.strip()

        # 获取AI模型信息
        ai_provider_name = ai_manager.get_provider_name()
        ai_model_name = ai_manager.get_model_name()
        ai_display_name = f"{ai_provider_name} {ai_model_name}"

        # 如果提供了paper_id，保存分析结果到数据库
        if paper_id:
            db.table("papers").update({
                "code_analysis_result": analysis_text,
                "code_analysis_date": datetime.now().isoformat(),
                "code_analysis_model": ai_display_name
            }).eq("id", paper_id).execute()

        return CodeAnalysisResponse(
            success=True,
            analysis=analysis_text,
            repo_url=repo_url,
            ai_provider=ai_provider_name,
            ai_model=ai_model_name,
            cached=False,
            analysis_date=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


async def fetch_github_readme(owner: str, repo: str) -> str:
    """获取GitHub仓库的README内容"""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # 尝试获取README.md
            url = f"https://api.github.com/repos/{owner}/{repo}/readme"
            headers = {"Accept": "application/vnd.github.v3.raw"}

            response = await client.get(url, headers=headers)

            if response.status_code == 200:
                content = response.text
                # 限制长度，避免太长
                return content[:8000] if len(content) > 8000 else content
            else:
                return "README not found"

    except Exception as e:
        return f"Failed to fetch README: {str(e)}"


async def fetch_repo_structure(owner: str, repo: str) -> dict:
    """获取仓库的文件结构（主要关注Python文件）"""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # 获取仓库树结构
            url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
            response = await client.get(url)

            if response.status_code != 200:
                # 尝试master分支
                url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
                response = await client.get(url)

            if response.status_code != 200:
                return {"error": "Failed to fetch repo structure"}

            data = response.json()
            tree = data.get('tree', [])

            # 筛选Python文件和关键目录
            py_files = []
            for item in tree:
                path = item.get('path', '')
                if path.endswith('.py') and item.get('type') == 'blob':
                    # 重点关注模型相关文件
                    if any(keyword in path.lower() for keyword in ['model', 'network', 'arch', 'backbone', 'head']):
                        py_files.append(path)

            return {
                "python_files": py_files[:20],  # 限制数量
                "total_files": len(tree)
            }

    except Exception as e:
        return {"error": str(e)}


async def fetch_model_code(owner: str, repo: str, file_structure: dict) -> str:
    """获取主要模型文件的代码片段"""
    try:
        py_files = file_structure.get('python_files', [])
        if not py_files:
            return "No model files found"

        # 选择第一个看起来像模型的文件
        target_file = None
        for f in py_files:
            if 'model.py' in f.lower() or 'network.py' in f.lower():
                target_file = f
                break

        if not target_file:
            target_file = py_files[0]

        async with httpx.AsyncClient(timeout=15.0) as client:
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{target_file}"
            response = await client.get(url)

            if response.status_code != 200:
                url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{target_file}"
                response = await client.get(url)

            if response.status_code == 200:
                code = response.text
                # 限制长度
                return code[:10000] if len(code) > 10000 else code
            else:
                return "Failed to fetch model code"

    except Exception as e:
        return f"Error: {str(e)}"


def build_analysis_prompt(repo_url: str, readme: str, structure: dict, code: str) -> str:
    """构建AI分析提示词"""

    # 格式化文件结构为树形显示
    py_files = structure.get('python_files', [])
    file_tree = "\n".join([f"  - {f}" for f in py_files])

    prompt = f"""# Task (任务)
请忽略通用的软件架构分析，专注于**算法逻辑**和**数据流向**。请严格按照以下 **6个层级** 由浅入深地进行解析：

## Level 0: Directory Structure (目录结构分析) 🆕
*   **项目结构概览**：请分析代码仓库的目录组织，说明主要目录和文件的作用
*   **核心文件识别**：
    *   模型定义文件（model.py, network.py等）的路径和作用
    *   训练脚本（train.py, main.py等）的路径和作用
    *   配置文件（config.py, yaml等）的路径和作用
    *   工具函数（utils, helpers等）的路径和作用
*   **代码组织模式**：这个项目使用了什么样的代码组织模式？（如：按功能模块划分、按层次划分等）
*   **入口点**：如何运行这个项目？主入口文件是什么？

**请以树形结构展示关键文件和目录**，例如：
```
project/
├── models/
│   ├── backbone.py      # 特征提取骨干网络
│   ├── head.py          # 任务头
│   └── losses.py        # 损失函数
├── data/
│   ├── dataset.py       # 数据集加载
│   └── transforms.py    # 数据增强
├── configs/
│   └── default.yaml     # 默认配置
└── train.py             # 训练入口
```

## Level 1: Model Card & Scope (模型身份卡)
*   **算法归类**：这是什么类型的模型？（例如：One-stage Detector, Transformer-based Planner, VAE等）
*   **核心输入/输出**：
    *   Input: 数据模态是什么？（Camera, LiDAR, Radar?）维度大概是怎样的？
    *   Output: 输出是什么？（Bbox, Occupancy Grid, Trajectory points?）
*   **对应论文/SOTA**：这段代码看起来像是在复现哪篇论文？或者使用了哪种经典架构（ResNet, FPN, Transformer Decoder）？

## Level 2: Architecture & Components (骨架分析)
*   **模块拆解**：请指出模型的 Backbone（骨干）、Neck（颈部/特征融合）、Head（检测头/任务头）分别对应代码的哪些部分？
*   **特征流向图**：请简述特征提取的路径。例如：`Image -> ResNet -> FPN -> BEV Pool -> Head`。

## Level 3: Tensor Shape Tracking (张量维度追踪 —— **最重要**)
*   请以此格式分析核心函数 `forward()` 中的数据维度变化（假设 Batch_size=B）：
    *   输入: `x` -> `[B, 3, 256, 704]` (Image)
    *   经过 Backbone: `feat` -> `[B, 512, 32, 88]`
    *   经过 View/Reshape: `...` -> `[B, 512, 2816]`
    *   **重点标注**：哪里进行了 `permute`, `view`, `reshape` 或 `einsum`？这些操作的物理含义是什么？

## Level 4: Math to Code Mapping (数学原理映射)
*   **Loss Function**：代码中计算了哪些 Loss？（Focal Loss, L1 Loss, KL Divergence?）请解释每个 Loss 试图优化什么目标。
*   **核心算子**：如果有自定义的 CUDA 算子、复杂的 Attention 机制或坐标转换（World to Camera），请解释其数学原理。

## Level 5: Training Dynamics (训练工程细节)
*   **数据增强**：使用了哪些针对自动驾驶场景的增强？（Flip, Rotation, Photometric dist?）
*   **工程Trick**：有没有使用 Gradient Clipping, Mixed Precision (AMP), EMA (Exponential Moving Average) 或特殊的初始化策略？

---

**代码仓库**: {repo_url}

**README内容**:
```
{readme[:3000]}
```

**文件结构**:
Python文件: {len(structure.get('python_files', []))} 个
关键文件: {', '.join(structure.get('python_files', [])[:10])}

**代码片段**:
```python
{code[:5000]}
```

请开始分析。如果代码中包含复杂的张量变换，请务必详细解释维度的变化过程。如果信息不足，请基于README和代码结构进行合理推断。
"""
    return prompt
