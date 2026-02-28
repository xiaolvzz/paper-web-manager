/**
 * 全局AI模型设置管理
 * 此文件在所有页面共享，管理AI模型的选择和配置
 */

let availableModels = [];
let currentProviderData = null;

/**
 * 初始化AI模型（页面加载时调用）
 */
async function initializeAIModels() {
    try {
        const response = await fetch('/api/ai/models');
        if (!response.ok) {
            console.error('加载AI模型列表失败');
            return;
        }

        const data = await response.json();
        availableModels = data.models;

        // 检查localStorage中是否有用户选择的模型
        const savedProviderId = localStorage.getItem('selected_ai_provider');

        if (savedProviderId) {
            // 尝试使用保存的模型
            const switchSuccess = await switchAIProvider(savedProviderId, false);
            if (switchSuccess) {
                currentProviderData = data.models.find(m => m.id === savedProviderId);
            } else {
                // 如果保存的模型不可用，使用默认的
                currentProviderData = data.models.find(m => m.is_default);
            }
        } else {
            // 使用默认模型
            currentProviderData = data.models.find(m => m.is_default);
        }

        // 更新导航栏badge
        updateCurrentModelBadge();

    } catch (error) {
        console.error('初始化AI模型失败:', error);
    }
}

/**
 * 更新导航栏的当前模型badge
 */
function updateCurrentModelBadge() {
    const badge = document.getElementById('currentModelBadge');
    if (!badge) return;

    if (currentProviderData && currentProviderData.configured) {
        badge.textContent = currentProviderData.name.split(' ')[0];  // 只显示简称
        badge.className = 'badge bg-success';
        badge.style.fontSize = '0.7rem';
    } else {
        badge.textContent = '未配置';
        badge.className = 'badge bg-warning';
        badge.style.fontSize = '0.7rem';
    }
}

/**
 * 打开AI设置Modal
 */
async function openAISettings() {
    // 重新加载最新的模型列表
    try {
        const response = await fetch('/api/ai/models');
        if (!response.ok) {
            showToast('加载AI模型列表失败', 'error');
            return;
        }

        const data = await response.json();
        availableModels = data.models;

        // 渲染设置Modal
        renderAISettingsModal(data.models, data.current_provider);

        // 显示Modal
        const modal = new bootstrap.Modal(document.getElementById('aiSettingsModal'));
        modal.show();

    } catch (error) {
        showToast('加载AI设置失败: ' + error.message, 'error');
    }
}

/**
 * 渲染AI设置Modal内容
 */
function renderAISettingsModal(models, currentProvider) {
    // 更新当前模型显示
    const currentModel = models.find(m => m.is_default) || models.find(m => m.configured);

    if (currentModel && currentModel.configured) {
        document.getElementById('currentProviderName').textContent = currentModel.name;
        document.getElementById('currentModelName').textContent = currentModel.model;
        document.getElementById('currentModelDesc').textContent =
            `${currentModel.description} | ${currentModel.cost}`;
    } else {
        document.getElementById('currentProviderName').textContent = '未配置';
        document.getElementById('currentModelName').textContent = '';
        document.getElementById('currentModelDesc').textContent = '请先配置至少一个AI模型';
    }

    // 渲染模型列表
    const modelsList = document.getElementById('modelsList');
    if (!modelsList) return;

    modelsList.innerHTML = '';

    models.forEach(model => {
        const card = document.createElement('div');
        card.className = `model-card ${model.configured ? '' : 'disabled'} ${model.is_default ? 'selected' : ''}`;

        card.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div class="flex-grow-1">
                    <div class="d-flex align-items-center mb-1">
                        <strong class="me-2">${model.name}</strong>
                        <span class="badge bg-secondary">${model.model}</span>
                        ${model.is_default ? '<span class="badge bg-success ms-2">✓ 当前使用</span>' : ''}
                        ${!model.configured ? '<span class="badge bg-warning ms-2">未配置</span>' : ''}
                    </div>
                    <div class="text-muted small">
                        ${model.description} | 成本: ${model.cost}
                    </div>
                </div>
                <div>
                    ${model.configured ?
                        `<button class="btn btn-sm btn-primary" onclick="selectModelGlobally('${model.id}')" ${model.is_default ? 'disabled' : ''}>
                            ${model.is_default ? '使用中' : '选择'}
                        </button>`
                        :
                        `<button class="btn btn-sm btn-outline-secondary" disabled>需要配置</button>`
                    }
                </div>
            </div>
        `;

        modelsList.appendChild(card);
    });
}

/**
 * 全局选择AI模型
 */
async function selectModelGlobally(providerId) {
    const success = await switchAIProvider(providerId, true);

    if (success) {
        // 保存到localStorage
        localStorage.setItem('selected_ai_provider', providerId);

        // 更新currentProviderData
        currentProviderData = availableModels.find(m => m.id === providerId);

        // 更新导航栏badge
        updateCurrentModelBadge();

        // 重新渲染Modal
        const response = await fetch('/api/ai/models');
        const data = await response.json();
        renderAISettingsModal(data.models, data.current_provider);

        showToast(`✓ 已切换到 ${currentProviderData.name}，全局生效`, 'success');
    }
}

/**
 * 切换AI Provider（后端）
 */
async function switchAIProvider(providerId, showError = true) {
    try {
        const response = await fetch('/api/ai/select-model', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ provider_id: providerId })
        });

        if (response.ok) {
            return true;
        } else {
            if (showError) {
                const error = await response.json();
                showToast(`切换失败: ${error.detail}`, 'error');
            }
            return false;
        }
    } catch (error) {
        if (showError) {
            showToast('切换模型失败: ' + error.message, 'error');
        }
        return false;
    }
}

/**
 * 获取当前选择的provider_id（供其他模块调用）
 */
function getSelectedProviderId() {
    return localStorage.getItem('selected_ai_provider') || null;
}

/**
 * 获取AI设置Modal HTML（供页面引入）
 */
function getAISettingsModalHTML() {
    return `
    <!-- AI设置Modal -->
    <div class="modal fade" id="aiSettingsModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title">⚙️ AI模型全局设置</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="alert alert-info">
                        <strong>💡 提示：</strong>此处配置将应用到所有AI功能（论文摘要、创新点提取、PDF翻译、代码分析等）
                    </div>

                    <!-- 当前使用的模型 -->
                    <div class="mb-4">
                        <h6 class="fw-bold">🎯 当前使用的模型</h6>
                        <div class="card bg-light">
                            <div class="card-body">
                                <div id="currentModelDisplay">
                                    <span class="badge bg-primary fs-6" id="currentProviderName">加载中...</span>
                                    <span class="badge bg-light text-dark fs-6" id="currentModelName"></span>
                                    <div class="mt-2">
                                        <small class="text-muted" id="currentModelDesc"></small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 模型选择列表 -->
                    <div class="mb-4">
                        <h6 class="fw-bold">📋 选择AI模型</h6>
                        <div id="modelsList">
                            <!-- 动态生成模型列表 -->
                        </div>
                    </div>

                    <!-- 配置指南 -->
                    <div>
                        <h6 class="fw-bold">📖 配置新模型</h6>
                        <div class="accordion" id="configAccordion">
                            <div class="accordion-item">
                                <h2 class="accordion-header">
                                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#configGuide">
                                        查看配置指南
                                    </button>
                                </h2>
                                <div id="configGuide" class="accordion-collapse collapse" data-bs-parent="#configAccordion">
                                    <div class="accordion-body">
                                        <h6>方法1：编辑 .env 文件（本地开发）</h6>
                                        <pre class="bg-dark text-light p-3 rounded"><code># Gemini (完全免费)
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.0-flash-exp

# Claude (推理能力强)
CLAUDE_API_KEY=sk-ant-api03-xxx
CLAUDE_MODEL=claude-3-5-haiku-20241022

# DeepSeek (极低成本)
DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_MODEL=deepseek-chat

# 智谱AI (免费，国内)
ZHIPU_API_KEY=your_key_here
ZHIPU_MODEL=glm-4-flash

# 通义千问
QWEN_API_KEY=your_key_here
QWEN_MODEL=qwen-turbo

# OpenAI
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4o-mini

# Groq (免费)
GROQ_API_KEY=gsk_xxx
GROQ_MODEL=llama-3.2-90b-text-preview</code></pre>

                                        <h6 class="mt-3">方法2：Vercel环境变量（线上部署）</h6>
                                        <ol>
                                            <li>打开 Vercel 项目设置</li>
                                            <li>Settings → Environment Variables</li>
                                            <li>添加对应的环境变量</li>
                                            <li>重新部署</li>
                                        </ol>

                                        <h6 class="mt-3">推荐组合</h6>
                                        <ul>
                                            <li>🎯 免费优先：Gemini + 智谱AI</li>
                                            <li>💰 公司使用：Claude + DeepSeek</li>
                                            <li>⚡ 速度优先：Groq + Gemini</li>
                                        </ul>

                                        <div class="alert alert-warning mt-3">
                                            <strong>注意：</strong>配置后需要重启应用（本地）或重新部署（Vercel）才能生效。
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                </div>
            </div>
        </div>
    </div>
    `;
}

// 页面加载时自动初始化
document.addEventListener('DOMContentLoaded', async () => {
    await initializeAIModels();
});
