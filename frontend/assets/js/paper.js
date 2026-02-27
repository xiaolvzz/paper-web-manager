/**
 * 论文详情页逻辑
 */

let currentPaper = null;
let currentAnalysis = null;
let currentRelations = [];
let allPapers = [];

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

    await loadPaperDetails(paperId);
    await loadAllPapers(); // 为关联关系下拉列表加载所有论文
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
