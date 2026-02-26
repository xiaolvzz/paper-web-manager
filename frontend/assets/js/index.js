/**
 * 首页逻辑
 */

let currentPapers = [];

// 页面加载时获取论文列表
document.addEventListener('DOMContentLoaded', () => {
    loadPapers();

    // 搜索框回车事件
    document.getElementById('searchInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchPapers();
        }
    });

    // arXiv搜索框回车事件（在modal打开后绑定）
    const addPaperModal = document.getElementById('addPaperModal');
    addPaperModal.addEventListener('shown.bs.modal', () => {
        const arxivInput = document.getElementById('arxivSearchInput');
        arxivInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchArxiv();
            }
        });
    });
});

// 加载论文列表
async function loadPapers(params = {}) {
    try {
        const papers = await PapersAPI.list(params);
        currentPapers = papers;
        renderPapers(papers);
    } catch (error) {
        showToast('加载论文列表失败: ' + error.message, 'error');
    }
}

// 搜索论文
async function searchPapers() {
    const searchInput = document.getElementById('searchInput').value.trim();
    const yearFilter = document.getElementById('yearFilter').value;

    const searchBtn = document.getElementById('searchBtnText');
    const searchSpinner = document.getElementById('searchSpinner');

    searchBtn.classList.add('d-none');
    searchSpinner.classList.remove('d-none');

    try {
        const params = {};
        if (searchInput) params.search = searchInput;
        if (yearFilter) params.year = parseInt(yearFilter);

        await loadPapers(params);
    } finally {
        searchBtn.classList.remove('d-none');
        searchSpinner.classList.add('d-none');
    }
}

// 渲染论文列表
function renderPapers(papers) {
    const papersList = document.getElementById('papersList');
    const emptyState = document.getElementById('emptyState');

    if (papers.length === 0) {
        papersList.innerHTML = '';
        emptyState.classList.remove('d-none');
        return;
    }

    emptyState.classList.add('d-none');

    papersList.innerHTML = papers.map(paper => `
        <div class="paper-card">
            <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                    <h5>
                        <a href="/paper/${paper.id}" class="text-decoration-none">
                            ${escapeHtml(paper.title)}
                        </a>
                    </h5>
                    <div class="meta">
                        ${paper.authors ? `<span>👤 ${escapeHtml(paper.authors)}</span>` : ''}
                        ${paper.year ? `<span class="ms-3">📅 ${paper.year}</span>` : ''}
                    </div>
                    ${paper.abstract ? `<p class="abstract mt-2">${escapeHtml(paper.abstract)}</p>` : ''}
                    ${paper.tags ? renderTags(paper.tags) : ''}
                </div>
                <div class="ms-3">
                    <button class="btn btn-sm btn-outline-primary" onclick="editPaper(${paper.id})">编辑</button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deletePaper(${paper.id})">删除</button>
                </div>
            </div>
        </div>
    `).join('');
}

// 渲染标签
function renderTags(tagsStr) {
    if (!tagsStr) return '';
    const tags = tagsStr.split(',').map(t => t.trim()).filter(t => t);
    return `
        <div class="mt-2">
            ${tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('')}
        </div>
    `;
}

// 搜索arXiv论文
async function searchArxiv() {
    const input = document.getElementById('arxivSearchInput');
    const query = input.value.trim();

    if (!query) {
        showToast('请输入搜索关键词', 'error');
        return;
    }

    const searchBtn = document.getElementById('arxivSearchBtnText');
    const searchSpinner = document.getElementById('arxivSearchSpinner');
    const resultsDiv = document.getElementById('arxivResults');

    searchBtn.classList.add('d-none');
    searchSpinner.classList.remove('d-none');

    // 显示正在搜索的提示
    resultsDiv.innerHTML = '<div class="text-muted small">正在搜索 arXiv...</div>';

    try {
        console.log('搜索关键词:', query);
        const data = await ArxivAPI.search(query, 10);  // 增加到10个结果
        console.log('搜索结果:', data);

        if (data.count === 0) {
            resultsDiv.innerHTML = `
                <div class="alert alert-warning small mb-0">
                    <strong>未找到相关论文</strong><br>
                    尝试使用不同的关键词，或检查拼写是否正确。<br>
                    搜索词: "${escapeHtml(query)}"
                </div>
            `;
        } else {
            resultsDiv.innerHTML = `
                <div class="small text-success mb-2">
                    ✓ 找到 ${data.count} 篇论文，点击直接添加到系统
                </div>
                ${data.results.map((paper, index) => `
                    <div class="arxiv-result-item p-2 mb-2 border rounded d-flex justify-content-between align-items-center" style="cursor: pointer;" onclick='addPaperFromArxiv(${JSON.stringify(paper).replace(/'/g, "&#39;")})'>
                        <div class="flex-grow-1">
                            <div class="fw-bold small">${escapeHtml(paper.title)}</div>
                            <div class="text-muted" style="font-size: 0.85rem;">
                                ${escapeHtml(paper.authors)} · ${paper.year}
                            </div>
                        </div>
                        <div class="ms-2">
                            <button class="btn btn-sm btn-outline-primary" onclick='event.stopPropagation(); window.open("${paper.pdf_url}", "_blank")'>
                                查看PDF
                            </button>
                        </div>
                    </div>
                `).join('')}
                <style>
                    .arxiv-result-item {
                        transition: all 0.2s;
                    }
                    .arxiv-result-item:hover {
                        background-color: #f8f9fa;
                        border-color: #0d6efd !important;
                    }
                </style>
            `;
        }
    } catch (error) {
        console.error('arXiv搜索错误:', error);
        showToast('arXiv搜索失败: ' + error.message, 'error');
        resultsDiv.innerHTML = `
            <div class="alert alert-danger small mb-0">
                <strong>搜索失败</strong><br>
                ${escapeHtml(error.message)}<br>
                请稍后重试或联系管理员。
            </div>
        `;
    } finally {
        searchBtn.classList.remove('d-none');
        searchSpinner.classList.add('d-none');
    }
}

// 从arXiv直接添加论文
async function addPaperFromArxiv(paper) {
    // 确认是否添加
    if (!confirm(`确定要添加论文《${paper.title}》吗？`)) {
        return;
    }

    try {
        // 准备数据
        const data = {
            title: paper.title,
            authors: paper.authors,
            year: paper.year,
            pdf_path: paper.pdf_url,
            abstract: paper.abstract,
            tags: paper.categories
        };

        // 调用API添加论文
        await PapersAPI.create(data);
        showToast('论文添加成功！');

        // 关闭modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('addPaperModal'));
        modal.hide();

        // 清空搜索
        document.getElementById('arxivResults').innerHTML = '';
        document.getElementById('arxivSearchInput').value = '';

        // 清空表单
        document.getElementById('addPaperForm').reset();

        // 重新加载论文列表
        await loadPapers();
    } catch (error) {
        showToast('添加论文失败: ' + error.message, 'error');
    }
}

// 添加论文
async function addPaper() {
    const form = document.getElementById('addPaperForm');
    const formData = new FormData(form);

    const data = {};
    for (let [key, value] of formData.entries()) {
        if (value.trim()) {
            data[key] = key === 'year' ? parseInt(value) : value;
        }
    }

    const addBtn = document.getElementById('addBtnText');
    const addSpinner = document.getElementById('addSpinner');

    addBtn.classList.add('d-none');
    addSpinner.classList.remove('d-none');

    try {
        await PapersAPI.create(data);
        showToast('论文添加成功');

        // 关闭modal并重新加载列表
        const modal = bootstrap.Modal.getInstance(document.getElementById('addPaperModal'));
        modal.hide();
        form.reset();

        await loadPapers();
    } catch (error) {
        showToast('添加论文失败: ' + error.message, 'error');
    } finally {
        addBtn.classList.remove('d-none');
        addSpinner.classList.add('d-none');
    }
}

// 编辑论文（简化版，直接跳转到详情页）
function editPaper(id) {
    window.location.href = `/paper/${id}`;
}

// 删除论文
async function deletePaper(id) {
    if (!confirm('确定要删除这篇论文吗？相关的分析记录和关联关系也会被删除。')) {
        return;
    }

    try {
        await PapersAPI.delete(id);
        showToast('论文已删除');
        await loadPapers();
    } catch (error) {
        showToast('删除论文失败: ' + error.message, 'error');
    }
}

// HTML转义（防止XSS）
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
