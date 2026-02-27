/**
 * 论文详情页逻辑
 */

let currentPaper = null;
let currentAnalysis = null;
let currentRelations = [];
let allPapers = [];
let currentPaperId = null;

// 获取URL中的论文ID
function getPaperId() {
    const path = window.location.pathname;
    const match = path.match(/\/paper\/(\d+)/);
    return match ? parseInt(match[1]) : null;
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', async () => {
    const paperId = getPaperId();
    if (!paperId) {
        showToast('无效的论文ID', 'error');
        setTimeout(() => window.location.href = '/', 2000);
        return;
    }

    // 保存paper ID
    currentPaperId = paperId;

    // 加载论文详情和关系
    await loadPaperDetails(paperId);
    await loadAllPapers(); // 为关联关系下拉列表加载所有论文

    // 加载对话历史
    await loadConversations();
    // 检查AI配置状态
    checkAIStatus();
    // 检查论文内容状态
    checkContentStatus();
});

// 加载论文详情
async function loadPaperDetails(paperId) {
    try {
        const data = await PapersAPI.getFull(paperId);
        currentPaper = data.paper;
        currentAnalysis = data.analysis;
        currentRelations = data.relations;

        renderPaperInfo();
        renderAnalysis();
        renderRelations();
    } catch (error) {
        showToast('加载论文详情失败: ' + error.message, 'error');
    }
}

// 渲染论文基本信息
function renderPaperInfo() {
    document.getElementById('paperTitle').textContent = currentPaper.title;
    document.title = `${currentPaper.title} - 论文管理系统`;

    // 显示/隐藏查看PDF按钮
    const viewPdfBtn = document.getElementById('viewPdfBtn');
    if (currentPaper.pdf_path) {
        viewPdfBtn.style.display = 'inline-block';
    } else {
        viewPdfBtn.style.display = 'none';
    }

    const infoHtml = `
        <div class="row">
            <div class="col-md-6 mb-2">
                <strong>作者：</strong> ${currentPaper.authors || '未知'}
            </div>
            <div class="col-md-6 mb-2">
                <strong>年份：</strong> ${currentPaper.year || '未知'}
            </div>
            ${currentPaper.domain ? `
                <div class="col-md-6 mb-2">
                    <strong>研究领域：</strong> <span class="badge bg-primary">${escapeHtml(currentPaper.domain)}</span>
                </div>
            ` : ''}
            <div class="col-12 mb-2">
                <strong>PDF：</strong>
                ${currentPaper.pdf_path ? `<a href="${currentPaper.pdf_path}" target="_blank">${currentPaper.pdf_path}</a>` : '未设置'}
            </div>
            ${currentPaper.github_url ? `
                <div class="col-12 mb-2">
                    <strong>GitHub：</strong>
                    <a href="${currentPaper.github_url}" target="_blank">${currentPaper.github_url}</a>
                </div>
            ` : ''}
            ${currentPaper.tags ? `
                <div class="col-12 mb-2">
                    <strong>标签：</strong> ${renderTags(currentPaper.tags)}
                </div>
            ` : ''}
            ${currentPaper.abstract ? `
                <div class="col-12 mt-3">
                    <strong>摘要：</strong>
                    <p class="mt-2" style="line-height: 1.6;">${escapeHtml(currentPaper.abstract)}</p>
                </div>
            ` : ''}
        </div>
    `;

    document.getElementById('paperInfo').innerHTML = infoHtml;
}

// 渲染分析记录
function renderAnalysis() {
    if (currentAnalysis) {
        document.getElementById('innovationPoints').value = currentAnalysis.innovation_points || '';
        document.getElementById('personalNotes').value = currentAnalysis.personal_notes || '';

        if (currentAnalysis.framework_image) {
            document.getElementById('frameworkImageContainer').innerHTML = `
                <img src="${currentAnalysis.framework_image}" class="framework-image" alt="框架图">
            `;
        }
    }
}

// 保存分析记录
async function saveAnalysis() {
    const saveBtnText = document.getElementById('saveBtnText');
    const saveSpinner = document.getElementById('saveSpinner');

    saveBtnText.classList.add('d-none');
    saveSpinner.classList.remove('d-none');

    try {
        const data = {
            innovation_points: document.getElementById('innovationPoints').value,
            personal_notes: document.getElementById('personalNotes').value,
        };

        // 如果有框架图URL，也保存
        if (currentAnalysis && currentAnalysis.framework_image) {
            data.framework_image = currentAnalysis.framework_image;
        }

        const result = await AnalysisAPI.upsert(currentPaper.id, data);
        currentAnalysis = result;

        showToast('分析记录已保存');
    } catch (error) {
        showToast('保存失败: ' + error.message, 'error');
    } finally {
        saveBtnText.classList.remove('d-none');
        saveSpinner.classList.add('d-none');
    }
}

// 上传框架图
async function uploadFrameworkImage() {
    const fileInput = document.getElementById('frameworkImageInput');
    const file = fileInput.files[0];

    if (!file) {
        showToast('请选择图片文件', 'error');
        return;
    }

    const uploadBtnText = document.getElementById('uploadBtnText');
    const uploadSpinner = document.getElementById('uploadSpinner');

    uploadBtnText.classList.add('d-none');
    uploadSpinner.classList.remove('d-none');

    try {
        const result = await AnalysisAPI.uploadImage(file);

        // 更新分析记录中的框架图URL
        if (!currentAnalysis) {
            currentAnalysis = { framework_image: result.url };
        } else {
            currentAnalysis.framework_image = result.url;
        }

        // 显示图片
        document.getElementById('frameworkImageContainer').innerHTML = `
            <img src="${result.url}" class="framework-image" alt="框架图">
        `;

        showToast('图片上传成功');
        fileInput.value = ''; // 清空文件选择
    } catch (error) {
        showToast('上传失败: ' + error.message, 'error');
    } finally {
        uploadBtnText.classList.remove('d-none');
        uploadSpinner.classList.add('d-none');
    }
}

// 加载所有论文（用于关联关系下拉列表）
async function loadAllPapers() {
    try {
        allPapers = await PapersAPI.list({ limit: 1000 });

        const select = document.getElementById('relatedPaperSelect');
        select.innerHTML = '<option value="">选择论文...</option>' +
            allPapers
                .filter(p => p.id !== currentPaper.id) // 排除当前论文
                .map(p => `<option value="${p.id}">${escapeHtml(p.title)} (${p.year || '未知年份'})</option>`)
                .join('');
    } catch (error) {
        console.error('加载论文列表失败:', error);
    }
}

// 渲染关联关系
function renderRelations() {
    const container = document.getElementById('relationsList');

    if (currentRelations.length === 0) {
        container.innerHTML = '<p class="text-muted">暂无关联论文</p>';
        return;
    }

    container.innerHTML = currentRelations.map(rel => {
        const relatedPaper = rel.related_paper;
        const relationType = rel.relation_type;
        const direction = rel.direction;

        return `
            <div class="paper-card">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <div class="mb-2">
                            <span class="relation-badge relation-${relationType}">
                                ${getRelationTypeLabel(relationType)}
                            </span>
                            ${direction === 'outgoing' ? '→' : '←'}
                        </div>
                        <h6>
                            <a href="/paper/${relatedPaper.id}" class="text-decoration-none">
                                ${escapeHtml(relatedPaper.title)}
                            </a>
                        </h6>
                        <div class="meta">
                            ${relatedPaper.authors || '未知作者'} • ${relatedPaper.year || '未知年份'}
                        </div>
                        ${rel.description ? `<p class="mt-2 text-muted small">${escapeHtml(rel.description)}</p>` : ''}
                    </div>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteRelation(${rel.id})">删除</button>
                </div>
            </div>
        `;
    }).join('');
}

// 获取关系类型标签
function getRelationTypeLabel(type) {
    const labels = {
        'method_similar': '方法相似',
        'problem_related': '问题相关',
        'custom': '自定义'
    };
    return labels[type] || type;
}

// 添加关联关系
async function addRelation() {
    const relatedPaperId = parseInt(document.getElementById('relatedPaperSelect').value);
    const relationType = document.getElementById('relationTypeSelect').value;
    const description = document.getElementById('relationDescription').value;

    if (!relatedPaperId) {
        showToast('请选择关联论文', 'error');
        return;
    }

    try {
        const data = {
            paper_from_id: currentPaper.id,
            paper_to_id: relatedPaperId,
            relation_type: relationType,
            description: description || null
        };

        await RelationsAPI.create(data);
        showToast('关联关系已添加');

        // 关闭modal并重新加载关系
        const modal = bootstrap.Modal.getInstance(document.getElementById('addRelationModal'));
        modal.hide();
        document.getElementById('addRelationForm').reset();

        await loadPaperDetails(currentPaper.id);
    } catch (error) {
        showToast('添加关联失败: ' + error.message, 'error');
    }
}

// 删除关联关系
async function deleteRelation(relationId) {
    if (!confirm('确定要删除这个关联关系吗？')) {
        return;
    }

    try {
        await RelationsAPI.delete(relationId);
        showToast('关联关系已删除');
        await loadPaperDetails(currentPaper.id);
    } catch (error) {
        showToast('删除失败: ' + error.message, 'error');
    }
}

// 编辑模式切换（简化版，未实现完整编辑功能）
function toggleEditMode() {
    showToast('编辑功能开发中，请在列表页删除后重新添加', 'error');
}

// 渲染标签
function renderTags(tagsStr) {
    if (!tagsStr) return '';
    const tags = tagsStr.split(',').map(t => t.trim()).filter(t => t);
    return tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('');
}

// HTML转义
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// ============ AI助手功能 ============

let lastAIOutput = '';
let lastAIType = '';

// 生成AI摘要
async function generateAISummary() {
    if (!currentPaper.abstract) {
        showToast('该论文没有摘要，无法生成', 'error');
        return;
    }

    const btnText = document.getElementById('aiSummaryBtnText');
    const spinner = document.getElementById('aiSummarySpinner');
    const output = document.getElementById('aiOutput');
    const outputContent = document.getElementById('aiOutputContent');

    btnText.classList.add('d-none');
    spinner.classList.remove('d-none');
    output.classList.add('d-none');

    try {
        const response = await fetch('/api/ai/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: currentPaper.abstract,
                max_length: 200
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '生成摘要失败');
        }

        const data = await response.json();
        lastAIOutput = data.content;
        lastAIType = 'summary';

        outputContent.innerHTML = `
            <h6 class="mb-2">📝 AI生成的中文摘要：</h6>
            <div style="white-space: pre-wrap;">${escapeHtml(data.content)}</div>
            <div class="mt-2 text-muted small">模型: ${data.model}</div>
        `;
        output.classList.remove('d-none');

        showToast('摘要生成成功');
    } catch (error) {
        showToast('生成摘要失败: ' + error.message, 'error');
    } finally {
        btnText.classList.remove('d-none');
        spinner.classList.add('d-none');
    }
}

// 提取创新点
async function extractInnovations() {
    if (!currentPaper.abstract) {
        showToast('该论文没有摘要，无法提取创新点', 'error');
        return;
    }

    const btnText = document.getElementById('aiInnovationBtnText');
    const spinner = document.getElementById('aiInnovationSpinner');
    const output = document.getElementById('aiOutput');
    const outputContent = document.getElementById('aiOutputContent');

    btnText.classList.add('d-none');
    spinner.classList.remove('d-none');
    output.classList.add('d-none');

    try {
        const response = await fetch('/api/ai/extract-innovations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                abstract: currentPaper.abstract,
                title: currentPaper.title
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '提取创新点失败');
        }

        const data = await response.json();
        lastAIOutput = data.content;
        lastAIType = 'innovations';

        outputContent.innerHTML = `
            <h6 class="mb-2">💡 AI提取的创新点：</h6>
            <div style="white-space: pre-wrap;">${escapeHtml(data.content)}</div>
            <div class="mt-2 text-muted small">模型: ${data.model}</div>
        `;
        output.classList.remove('d-none');

        showToast('创新点提取成功');
    } catch (error) {
        showToast('提取创新点失败: ' + error.message, 'error');
    } finally {
        btnText.classList.remove('d-none');
        spinner.classList.add('d-none');
    }
}

// 复制AI输出到分析区
function copyAIOutput() {
    if (!lastAIOutput) {
        showToast('没有可复制的内容', 'error');
        return;
    }

    const targetField = document.getElementById('innovationPoints');
    const currentContent = targetField.value.trim();

    if (currentContent) {
        // 如果已有内容，追加到末尾
        targetField.value = currentContent + '\n\n' + lastAIOutput;
    } else {
        // 如果为空，直接填入
        targetField.value = lastAIOutput;
    }

    // 滚动到分析记录区域
    document.getElementById('innovationPoints').scrollIntoView({ behavior: 'smooth', block: 'center' });
    showToast('已复制到创新点分析区域');
}

// ========== 新增功能：论文内容处理 ==========

/**
 * 从arXiv导入论文
 */
async function importFromArxiv() {
    const arxivInput = document.getElementById('arxivInput').value.trim();
    if (!arxivInput) {
        showToast('请输入arXiv ID或URL', 'error');
        return;
    }

    const btnText = document.getElementById('arxivBtnText');
    const spinner = document.getElementById('arxivSpinner');
    const statusDiv = document.getElementById('arxivStatus');

    btnText.textContent = '导入中...';
    spinner.classList.remove('d-none');
    statusDiv.innerHTML = '';

    try {
        const response = await fetch(`/api/papers/${currentPaperId}/import-from-arxiv`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ arxiv_input: arxivInput })
        });

        if (response.ok) {
            const data = await response.json();
            statusDiv.innerHTML = '<div class="alert alert-success mt-2">✓ arXiv论文导入成功！页面将刷新...</div>';
            showToast('arXiv论文导入成功');
            
            // 刷新页面数据
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            const error = await response.json();
            statusDiv.innerHTML = `<div class="alert alert-danger mt-2">导入失败: ${error.detail}</div>`;
            showToast('导入失败', 'error');
        }
    } catch (error) {
        statusDiv.innerHTML = `<div class="alert alert-danger mt-2">导入失败: ${error.message}</div>`;
        showToast('导入失败: ' + error.message, 'error');
    } finally {
        btnText.textContent = '导入';
        spinner.classList.add('d-none');
    }
}

/**
 * 添加文本内容
 */
async function addTextContent() {
    const textContent = document.getElementById('textContent').value.trim();
    if (!textContent) {
        showToast('请输入论文内容', 'error');
        return;
    }

    const btnText = document.getElementById('textBtnText');
    const spinner = document.getElementById('textSpinner');
    const statusDiv = document.getElementById('textStatus');

    btnText.textContent = '保存中...';
    spinner.classList.remove('d-none');
    statusDiv.innerHTML = '';

    try {
        const response = await fetch(`/api/papers/${currentPaperId}/add-text-content`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text_content: textContent })
        });

        if (response.ok) {
            const data = await response.json();
            statusDiv.innerHTML = `<div class="alert alert-success mt-2">✓ 论文内容已保存 (${data.text_length} 字符)</div>`;
            updateContentStatus('文本内容已添加');
            showToast('论文内容已保存');
        } else {
            const error = await response.json();
            statusDiv.innerHTML = `<div class="alert alert-danger mt-2">保存失败: ${error.detail}</div>`;
            showToast('保存失败', 'error');
        }
    } catch (error) {
        statusDiv.innerHTML = `<div class="alert alert-danger mt-2">保存失败: ${error.message}</div>`;
        showToast('保存失败: ' + error.message, 'error');
    } finally {
        btnText.textContent = '保存';
        spinner.classList.add('d-none');
    }
}

/**
 * 检查论文内容状态
 */
async function checkContentStatus() {
    if (!currentPaper) return;
    
    const statusText = document.getElementById('contentStatusText');
    if (currentPaper.pdf_text_content) {
        const length = currentPaper.pdf_text_content.length;
        statusText.textContent = `✓ 已有论文内容 (${length} 字符)`;
        statusText.className = 'text-success';
    } else {
        statusText.textContent = '暂无论文内容 - 请添加内容以使用AI对话功能';
        statusText.className = 'text-warning';
    }
}

/**
 * 更新内容状态显示
 */
function updateContentStatus(status) {
    const statusText = document.getElementById('contentStatusText');
    statusText.textContent = '✓ ' + status;
    statusText.className = 'text-success';
}

// ========== AI对话功能 ==========

/**
 * 检查AI配置状态
 */
async function checkAIStatus() {
    try {
        const response = await fetch('/api/ai/health');
        if (response.ok) {
            const data = await response.json();
            const statusEl = document.getElementById('aiConfigStatus');
            if (data.configured) {
                statusEl.innerHTML = '✓ AI服务已配置 (Groq)';
                statusEl.className = 'text-success';
            } else {
                statusEl.innerHTML = '⚠️ AI服务未配置 - 需要在Vercel中配置GROQ_API_KEY';
                statusEl.className = 'text-warning';
            }
        }
    } catch (error) {
        console.error('检查AI状态失败:', error);
    }
}

/**
 * 加载对话历史
 */
async function loadConversations() {
    try {
        const response = await fetch(`/api/conversations/paper/${currentPaperId}`);
        if (!response.ok) return;

        const conversations = await response.json();
        renderConversations(conversations);
    } catch (error) {
        console.error('加载对话失败:', error);
    }
}

/**
 * 渲染对话历史
 */
function renderConversations(conversations) {
    const chatHistory = document.getElementById('chatHistory');

    if (conversations.length === 0) {
        chatHistory.innerHTML = '<p class="text-muted text-center my-4">暂无对话记录，开始提问吧！</p>';
        return;
    }

    chatHistory.innerHTML = conversations.map(conv => {
        if (conv.role === 'system') return ''; // 不显示system消息

        const time = new Date(conv.created_at).toLocaleString('zh-CN', {
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        return `
            <div class="chat-message ${conv.role}">
                <div class="message-bubble">${escapeHtml(conv.content)}</div>
                <small class="message-time">${time}</small>
            </div>
        `;
    }).join('');

    // 滚动到底部
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

/**
 * 添加消息到界面（用于即时反馈）
 */
function appendMessage(role, content) {
    const chatHistory = document.getElementById('chatHistory');
    
    // 如果是第一条消息，清空提示文字
    if (chatHistory.querySelector('.text-muted.text-center')) {
        chatHistory.innerHTML = '';
    }
    
    const time = new Date().toLocaleString('zh-CN', {
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });

    const messageHTML = `
        <div class="chat-message ${role}">
            <div class="message-bubble">${escapeHtml(content)}</div>
            <small class="message-time">${time}</small>
        </div>
    `;

    chatHistory.insertAdjacentHTML('beforeend', messageHTML);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

/**
 * 发送消息
 */
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message) return;

    // 添加用户消息到界面
    appendMessage('user', message);
    input.value = '';

    // 禁用发送按钮
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;
    sendBtn.textContent = 'AI思考中...';

    try {
        const response = await fetch('/api/conversations/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                paper_id: currentPaperId,
                user_message: message
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'AI回复失败');
        }

        const data = await response.json();
        appendMessage('assistant', data.content);

    } catch (error) {
        if (error.message.includes('AI服务未配置')) {
            appendMessage('assistant', '⚠️ AI服务未配置。请在Vercel中配置GROQ_API_KEY环境变量。\n\n或者先使用arXiv导入和文本输入功能添加论文内容。');
        } else if (error.message.includes('暂无论文内容')) {
            appendMessage('assistant', '⚠️ 请先添加论文内容（通过arXiv导入或文本输入），然后再提问。');
        } else {
            appendMessage('assistant', '抱歉，AI回复失败: ' + error.message);
        }
    } finally {
        sendBtn.disabled = false;
        sendBtn.textContent = '发送';
    }
}

/**
 * 快捷提问
 */
function askQuickQuestion(question) {
    document.getElementById('chatInput').value = question;
    sendMessage();
}

/**
 * 一键分析论文
 */
async function autoAnalyzePaper() {
    if (!confirm('将使用AI自动分析论文并填充分析区域，是否继续？')) {
        return;
    }

    const originalText = '💬 AI对话助手';
    const headerEl = document.querySelector('#chatSection h4');
    headerEl.textContent = '🤖 AI正在分析论文...';

    try {
        const response = await fetch('/api/ai/analyze-paper', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ paper_id: currentPaperId })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '分析失败');
        }

        const analysis = await response.json();

        // 自动填充分析区域
        const innovationField = document.getElementById('innovationPoints');
        if (innovationField && analysis.innovations) {
            innovationField.value = analysis.innovations.map((item, i) => `${i + 1}. ${item}`).join('\n');
        }

        const notesField = document.getElementById('personalNotes');
        if (notesField) {
            let notes = notesField.value || '';

            // 添加框架信息
            if (analysis.framework) {
                notes += `\n\n【框架结构】\n${analysis.framework}`;
            }

            // 添加方法信息
            if (analysis.methods && analysis.methods.length > 0) {
                notes += `\n\n【使用方法】\n${analysis.methods.map((m, i) => `${i + 1}. ${m}`).join('\n')}`;
            }

            // 添加源码信息
            if (analysis.source_code) {
                notes += `\n\n【源码】\n${analysis.source_code}`;
            }

            notesField.value = notes.trim();
        }

        showToast('自动分析完成！请查看分析区域');
        
        // 滚动到分析区域
        document.getElementById('innovationPoints').scrollIntoView({ behavior: 'smooth', block: 'center' });

    } catch (error) {
        if (error.message.includes('AI服务未配置')) {
            showToast('AI服务未配置，请先配置GROQ_API_KEY', 'error');
        } else {
            showToast('自动分析失败: ' + error.message, 'error');
        }
    } finally {
        headerEl.textContent = originalText;
    }
}

/**
 * 清空对话
 */
async function clearConversations() {
    if (!confirm('确定要清空当前论文的所有对话记录吗？此操作不可恢复。')) {
        return;
    }

    try {
        const response = await fetch(`/api/conversations/paper/${currentPaperId}/all`, {
            method: 'DELETE'
        });

        if (response.ok) {
            document.getElementById('chatHistory').innerHTML = '<p class="text-muted text-center my-4">对话已清空</p>';
            showToast('对话已清空');
        } else {
            showToast('清空失败', 'error');
        }
    } catch (error) {
        showToast('清空失败: ' + error.message, 'error');
    }
}

/**
 * 处理Enter键发送
 */
function handleChatKeydown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// ========== PDF查看功能 ==========

/**
 * 打开PDF查看器
 */
function viewPDF() {
    if (!currentPaper || !currentPaper.pdf_path) {
        showToast('该论文没有PDF文件', 'error');
        return;
    }

    // 构建PDF查看器URL
    const pdfUrl = encodeURIComponent(currentPaper.pdf_path);
    const title = encodeURIComponent(currentPaper.title);
    const viewerUrl = `/pdf-viewer?url=${pdfUrl}&title=${title}&paper_id=${currentPaper.id}`;

    // 在新窗口打开
    window.open(viewerUrl, '_blank', 'width=1200,height=800');
}

// HTML转义函数已在文件开头定义，无需重复
