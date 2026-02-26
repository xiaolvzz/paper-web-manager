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
