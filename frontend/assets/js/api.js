/**
 * API请求封装
 */

const API_BASE = '/api';

// 通用请求函数
async function request(url, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${url}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '请求失败');
        }

        // 处理204 No Content
        if (response.status === 204) {
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// 论文API
const PapersAPI = {
    // 获取论文列表
    async list(params = {}) {
        const query = new URLSearchParams();
        if (params.search) query.append('search', params.search);
        if (params.year) query.append('year', params.year);
        if (params.tags) query.append('tags', params.tags);
        if (params.limit) query.append('limit', params.limit);
        if (params.offset) query.append('offset', params.offset);

        return request(`/papers/?${query.toString()}`);
    },

    // 获取单篇论文
    async get(id) {
        return request(`/papers/${id}`);
    },

    // 获取论文完整信息（含分析和关系）
    async getFull(id) {
        return request(`/papers/${id}/full`);
    },

    // 创建论文
    async create(data) {
        return request('/papers/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    // 更新论文
    async update(id, data) {
        return request(`/papers/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    // 删除论文
    async delete(id) {
        return request(`/papers/${id}`, {
            method: 'DELETE',
        });
    },
};

// 分析API
const AnalysisAPI = {
    // 获取论文的分析记录
    async get(paperId) {
        return request(`/analysis/paper/${paperId}`);
    },

    // 创建分析记录
    async create(data) {
        return request('/analysis/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    // 更新分析记录
    async update(id, data) {
        return request(`/analysis/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    // 更新或创建分析记录
    async upsert(paperId, data) {
        return request(`/analysis/paper/${paperId}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    // 上传框架图
    async uploadImage(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE}/analysis/upload-image`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '上传失败');
        }

        return response.json();
    },
};

// arXiv API
const ArxivAPI = {
    // 搜索论文
    async search(query, maxResults = 10) {
        return request(`/arxiv/search?query=${encodeURIComponent(query)}&max_results=${maxResults}`);
    },

    // 通过ID获取论文
    async getById(arxivId) {
        return request(`/arxiv/paper/${arxivId}`);
    },

    // 从PDF URL添加论文
    async fromPdfUrl(pdfUrl) {
        return request(`/arxiv/from-pdf-url?pdf_url=${encodeURIComponent(pdfUrl)}`, {
            method: 'POST'
        });
    },
};

// 关联关系API
const RelationsAPI = {
    // 获取所有关联关系
    async list() {
        return request('/relations/');
    },

    // 获取论文的关联关系
    async getByPaper(paperId) {
        return request(`/relations/paper/${paperId}`);
    },

    // 创建关联关系
    async create(data) {
        return request('/relations/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    // 删除关联关系
    async delete(id) {
        return request(`/relations/${id}`, {
            method: 'DELETE',
        });
    },

    // 获取关系图数据
    async getGraph() {
        return request('/relations/graph');
    },
};

// Toast通知
function showToast(message, type = 'success') {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }

    const wrapper = document.createElement('div');
    wrapper.innerHTML = toastHtml;
    const toastElement = wrapper.firstElementChild;
    container.appendChild(toastElement);

    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}
