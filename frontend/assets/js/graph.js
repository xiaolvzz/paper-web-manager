/**
 * 关系图可视化逻辑
 */

let network = null;
let currentData = null;
let currentFilters = {
    domain: null,
    relationType: null,
    tag: null
};

// 全局数据
let allDomains = [];
let selectedNodeId = null;
let selectedNodeTitle = '';

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', async () => {
    await loadAllDomains();
    await loadGraph();
    initContextMenu();
});

// 加载关系图数据
async function loadGraph(domainFilter = null, relationTypeFilter = null) {
    const loading = document.getElementById('loading');
    const emptyState = document.getElementById('empty-state');
    const container = document.getElementById('graph-container');

    try {
        const data = await RelationsAPI.getGraph(domainFilter, relationTypeFilter);
        currentData = data;

        loading.classList.add('d-none');

        if (data.nodes.length === 0) {
            emptyState.classList.remove('d-none');
            container.style.display = 'none';
            return;
        }

        emptyState.classList.add('d-none');
        container.style.display = 'block';

        // 更新筛选器选项
        populateFilters(data);

        // 更新统计信息
        updateStats(data);

        renderGraph(data);
    } catch (error) {
        loading.classList.add('d-none');
        showToast('加载关系图失败: ' + error.message, 'error');
    }
}

// 填充筛选器选项
function populateFilters(data) {
    const domainFilter = document.getElementById('domainFilter');
    const modalDomainFilter = document.getElementById('modalDomainFilter');

    // 清空现有选项（保留"全部"）
    domainFilter.innerHTML = '<option value="">全部领域</option>';
    modalDomainFilter.innerHTML = '<option value="">全部领域</option>';

    // 添加领域选项
    if (data.available_domains) {
        data.available_domains.forEach(domain => {
            const option1 = document.createElement('option');
            option1.value = domain.name;
            option1.textContent = `${domain.icon || ''} ${domain.name}`;
            domainFilter.appendChild(option1);

            const option2 = document.createElement('option');
            option2.value = domain.name;
            option2.textContent = `${domain.icon || ''} ${domain.name}`;
            modalDomainFilter.appendChild(option2);
        });
    }

    // 设置当前筛选值
    if (currentFilters.domain) {
        domainFilter.value = currentFilters.domain;
        modalDomainFilter.value = currentFilters.domain;
    }
    if (currentFilters.relationType) {
        document.getElementById('modalRelationFilter').value = currentFilters.relationType;
    }

    // 更新关系类型图例
    updateRelationLegend(data.relation_types || {});
}

// 更新关系类型图例
function updateRelationLegend(relationTypes) {
    const legendDiv = document.getElementById('relationLegend');
    const typeLabels = {
        'derived_from': '衍生',
        'extends': '扩展',
        'method_similar': '方法相似',
        'problem_related': '问题相关',
        'compares_with': '对比',
        'same_domain': '同领域',
        'baseline': '基线',
        'custom': '自定义'
    };

    const html = Object.keys(relationTypes).map(type => {
        const color = getEdgeColor(type);
        const label = typeLabels[type] || type;
        const count = relationTypes[type];
        return `<span class="badge" style="background-color: ${color};">${label} (${count})</span>`;
    }).join('');

    legendDiv.innerHTML = html || '<span class="text-muted small">暂无关系</span>';
}

// 更新统计信息
function updateStats(data) {
    document.getElementById('statsNodes').textContent = `论文: ${data.nodes.length}`;
    document.getElementById('statsEdges').textContent = `关系: ${data.edges.length}`;

    const uniqueDomains = new Set();
    data.nodes.forEach(node => {
        if (node.domains) {
            node.domains.forEach(d => uniqueDomains.add(d.name));
        }
    });
    document.getElementById('statsDomains').textContent = `领域: ${uniqueDomains.size}`;
}

// 应用筛选
function applyFilters() {
    const domain = document.getElementById('domainFilter').value;
    currentFilters.domain = domain || null;
    loadGraph(currentFilters.domain, currentFilters.relationType);
}

// 应用模态框筛选
function applyModalFilters() {
    const domain = document.getElementById('modalDomainFilter').value;
    const relationType = document.getElementById('modalRelationFilter').value;
    currentFilters.domain = domain || null;
    currentFilters.relationType = relationType || null;
    loadGraph(currentFilters.domain, currentFilters.relationType);
}

// 清除筛选
function clearFilters() {
    currentFilters = { domain: null, relationType: null };
    document.getElementById('domainFilter').value = '';
    document.getElementById('modalDomainFilter').value = '';
    document.getElementById('modalRelationFilter').value = '';
    loadGraph();
}

// 渲染关系图
function renderGraph(data) {
    const container = document.getElementById('graph-container');

    // 准备节点数据
    const nodes = new vis.DataSet(
        data.nodes.map(node => {
            // 使用领域颜色或默认颜色
            const borderColor = node.color || '#6366f1';
            const bgColor = '#ffffff';

            // 构建悬停提示
            const title = node.title;

            return {
                id: node.id,
                label: node.label,
                title: title,
                shape: 'box',
                color: {
                    background: bgColor,
                    border: borderColor,
                    highlight: {
                        background: lightenColor(borderColor, 0.9),
                        border: borderColor
                    },
                    hover: {
                        background: lightenColor(borderColor, 0.95),
                        border: borderColor
                    }
                },
                font: {
                    size: 13,
                    face: 'Arial',
                    color: '#1e293b'
                },
                margin: 10,
                borderWidth: 3,
                borderWidthSelected: 4
            };
        })
    );

    // 准备边数据
    const edges = new vis.DataSet(
        data.edges.map(edge => {
            const color = getEdgeColor(edge.label);
            return {
                from: edge.from,
                to: edge.to,
                label: getRelationTypeLabel(edge.label),
                title: edge.title,
                arrows: {
                    to: {
                        enabled: true,
                        scaleFactor: 0.8
                    }
                },
                color: {
                    color: color,
                    highlight: color,
                    hover: color
                },
                font: {
                    size: 11,
                    color: '#64748b',
                    strokeWidth: 3,
                    strokeColor: '#ffffff'
                },
                smooth: {
                    type: 'curvedCW',
                    roundness: 0.2
                },
                width: 2
            };
        })
    );

    // 配置选项
    const options = {
        layout: {
            improvedLayout: true,
            hierarchical: false
        },
        physics: {
            enabled: true,
            barnesHut: {
                gravitationalConstant: -15000,
                centralGravity: 0.3,
                springLength: 200,
                springConstant: 0.04,
                damping: 0.09,
                avoidOverlap: 0.5
            },
            stabilization: {
                enabled: true,
                iterations: 200
            }
        },
        interaction: {
            hover: true,
            tooltipDelay: 100,
            navigationButtons: true,
            keyboard: true,
            zoomView: true,
            dragView: true
        },
        nodes: {
            shadow: {
                enabled: true,
                color: 'rgba(0,0,0,0.1)',
                size: 5,
                x: 2,
                y: 2
            }
        },
        edges: {
            shadow: {
                enabled: true,
                color: 'rgba(0,0,0,0.1)',
                size: 3,
                x: 1,
                y: 1
            }
        }
    };

    // 创建网络图
    network = new vis.Network(container, { nodes, edges }, options);

    // 节点左键点击事件
    network.on('click', (params) => {
        if (params.nodes.length > 0 && params.event.srcEvent.button === 0) {
            const nodeId = params.nodes[0];
            window.location.href = `/paper/${nodeId}`;
        }
    });

    // 节点右键事件
    network.on('oncontext', (params) => {
        params.event.preventDefault();

        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = data.nodes.find(n => n.id === nodeId);

            if (node) {
                const domPosition = network.canvasToDOM({ x: params.pointer.canvas.x, y: params.pointer.canvas.y });
                showContextMenu(
                    params.event.clientX,
                    params.event.clientY,
                    nodeId,
                    node.label
                );
            }
        }
    });

    // 网络稳定后禁用物理引擎（提高性能）
    network.on('stabilizationIterationsDone', () => {
        network.setOptions({ physics: false });
    });
}

// 获取边的颜色
function getEdgeColor(relationType) {
    const colors = {
        'derived_from': '#8b5cf6',      // 紫色 - 衍生
        'extends': '#3b82f6',            // 蓝色 - 扩展
        'method_similar': '#2563eb',     // 深蓝 - 方法相似
        'problem_related': '#10b981',    // 绿色 - 问题相关
        'compares_with': '#f59e0b',      // 橙色 - 对比
        'same_domain': '#06b6d4',        // 青色 - 同领域
        'baseline': '#ef4444',           // 红色 - 基线
        'custom': '#64748b'              // 灰色 - 自定义
    };
    return colors[relationType] || '#64748b';
}

// 获取关系类型标签
function getRelationTypeLabel(type) {
    const labels = {
        'derived_from': '衍生',
        'extends': '扩展',
        'method_similar': '方法相似',
        'problem_related': '问题相关',
        'compares_with': '对比',
        'same_domain': '同领域',
        'baseline': '基线',
        'custom': '自定义'
    };
    return labels[type] || type;
}

// 颜色辅助函数：将hex颜色变亮
function lightenColor(hex, factor) {
    // 移除#号
    hex = hex.replace('#', '');

    // 转换为RGB
    let r = parseInt(hex.substring(0, 2), 16);
    let g = parseInt(hex.substring(2, 4), 16);
    let b = parseInt(hex.substring(4, 6), 16);

    // 向白色（255）靠拢
    r = Math.round(r + (255 - r) * factor);
    g = Math.round(g + (255 - g) * factor);
    b = Math.round(b + (255 - b) * factor);

    // 转回hex
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
}

// 适应屏幕
function fitGraph() {
    if (network) {
        network.fit({
            animation: {
                duration: 500,
                easingFunction: 'easeInOutQuad'
            }
        });
    }
}

// 重置缩放
function resetZoom() {
    if (network) {
        network.moveTo({
            scale: 1.0,
            animation: {
                duration: 500,
                easingFunction: 'easeInOutQuad'
            }
        });
    }
}

// ==================== 标签管理功能 ====================

/**
 * 加载所有领域标签
 */
async function loadAllDomains() {
    try {
        const response = await fetch('/api/tags/domains');
        if (!response.ok) throw new Error('加载标签失败');

        allDomains = await response.json();
        renderTagsQuickFilter();
    } catch (error) {
        console.error('加载标签失败:', error);
    }
}

/**
 * 渲染标签快速筛选面板
 */
function renderTagsQuickFilter() {
    const container = document.getElementById('tagsQuickFilter');
    if (!container) return;

    if (allDomains.length === 0) {
        container.innerHTML = '<span class="text-muted small">暂无标签</span>';
        return;
    }

    container.innerHTML = allDomains.map(domain => {
        const isActive = currentFilters.tag === domain.id;
        const activeClass = isActive ? 'active' : '';
        const bgColor = isActive ? domain.color : 'white';
        const textColor = isActive ? 'white' : domain.color;

        return `
            <button class="tag-button ${activeClass}"
                    style="border-color: ${domain.color}; color: ${textColor}; background: ${bgColor};"
                    onclick="filterByTag(${domain.id}, '${domain.name}')">
                ${domain.icon} ${domain.name}
            </button>
        `;
    }).join('');
}

/**
 * 按标签筛选
 */
function filterByTag(tagId, tagName) {
    if (currentFilters.tag === tagId) {
        // 取消筛选
        currentFilters.tag = null;
    } else {
        // 应用筛选
        currentFilters.tag = tagId;
    }

    renderTagsQuickFilter();
    applyTagFilter();
}

/**
 * 应用标签筛选（前端过滤）
 */
function applyTagFilter() {
    if (!network || !currentData) return;

    if (!currentFilters.tag) {
        // 显示所有节点
        currentData.nodes.forEach(node => {
            network.body.nodes[node.id].options.hidden = false;
        });
    } else {
        // 只显示包含该标签的节点
        currentData.nodes.forEach(node => {
            const hasDomain = node.domains && node.domains.some(d => d.id === currentFilters.tag);
            network.body.nodes[node.id].options.hidden = !hasDomain;
        });
    }

    network.redraw();
}

/**
 * 清除标签筛选
 */
function clearTagFilter() {
    currentFilters.tag = null;
    renderTagsQuickFilter();
    applyTagFilter();
}

/**
 * 初始化右键菜单
 */
function initContextMenu() {
    const contextMenu = document.getElementById('contextMenu');

    // 隐藏右键菜单当点击其他地方
    document.addEventListener('click', () => {
        contextMenu.style.display = 'none';
    });

    // 阻止默认右键菜单
    document.getElementById('graph-container').addEventListener('contextmenu', (e) => {
        e.preventDefault();
    });
}

/**
 * 显示右键菜单
 */
function showContextMenu(x, y, nodeId, nodeTitle) {
    const contextMenu = document.getElementById('contextMenu');
    selectedNodeId = nodeId;
    selectedNodeTitle = nodeTitle;

    contextMenu.style.display = 'block';
    contextMenu.style.left = x + 'px';
    contextMenu.style.top = y + 'px';
}

/**
 * 打开标签管理器
 */
async function openTagManager() {
    if (!selectedNodeId) return;

    document.getElementById('tagManagerPaperId').value = selectedNodeId;
    document.getElementById('tagManagerPaperTitle').textContent = selectedNodeTitle;

    // 加载论文当前标签
    await loadPaperTags(selectedNodeId);

    // 渲染可用标签列表
    renderAvailableTags();

    const modal = new bootstrap.Modal(document.getElementById('tagManagerModal'));
    modal.show();
}

/**
 * 查看论文详情
 */
function viewPaperDetails() {
    if (selectedNodeId) {
        window.location.href = `/paper/${selectedNodeId}`;
    }
}

/**
 * 加载论文的标签
 */
async function loadPaperTags(paperId) {
    try {
        const response = await fetch(`/api/tags/paper/${paperId}/domains`);
        if (!response.ok) throw new Error('加载标签失败');

        const tags = await response.json();
        renderCurrentTags(tags);
    } catch (error) {
        console.error('加载论文标签失败:', error);
        showToast('加载标签失败', 'error');
    }
}

/**
 * 渲染当前标签
 */
function renderCurrentTags(tags) {
    const container = document.getElementById('currentTagsList');

    if (tags.length === 0) {
        container.innerHTML = '<span class="text-muted small">暂无标签</span>';
        return;
    }

    container.innerHTML = tags.map(tag => `
        <button class="tag-button removable"
                style="border-color: ${tag.color}; color: ${tag.color}; background: white;">
            ${tag.icon} ${tag.name}
            <span class="remove-tag" onclick="removeTag(${tag.id}, event)">×</span>
        </button>
    `).join('');
}

/**
 * 渲染可用标签列表
 */
function renderAvailableTags() {
    const container = document.getElementById('availableTagsList');
    const paperId = document.getElementById('tagManagerPaperId').value;

    if (allDomains.length === 0) {
        container.innerHTML = '<span class="text-muted small">暂无可用标签</span>';
        return;
    }

    container.innerHTML = allDomains.map(domain => `
        <button class="tag-button"
                style="border-color: ${domain.color}; color: white; background: ${domain.color};"
                onclick="addTag(${paperId}, ${domain.id})">
            ${domain.icon} ${domain.name}
        </button>
    `).join('');
}

/**
 * 添加标签
 */
async function addTag(paperId, domainId) {
    try {
        const response = await fetch('/api/tags/paper/add-domains', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                paper_id: parseInt(paperId),
                domain_ids: [domainId]
            })
        });

        if (!response.ok) throw new Error('添加标签失败');

        showToast('✓ 标签已添加', 'success');
        await loadPaperTags(paperId);
        await loadGraph(currentFilters.domain, currentFilters.relationType); // 重新加载图以更新节点颜色
    } catch (error) {
        console.error('添加标签失败:', error);
        showToast('添加标签失败', 'error');
    }
}

/**
 * 移除标签
 */
async function removeTag(domainId, event) {
    event.stopPropagation();

    const paperId = document.getElementById('tagManagerPaperId').value;

    if (!confirm('确定要移除这个标签吗？')) return;

    try {
        const response = await fetch(`/api/tags/paper/remove-domain?paper_id=${paperId}&domain_id=${domainId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('移除标签失败');

        showToast('✓ 标签已移除', 'success');
        await loadPaperTags(paperId);
        await loadGraph(currentFilters.domain, currentFilters.relationType); // 重新加载图
    } catch (error) {
        console.error('移除标签失败:', error);
        showToast('移除标签失败', 'error');
    }
}

/**
 * 创建自定义标签
 */
async function createCustomTag() {
    const name = document.getElementById('newTagName').value.trim();
    const color = document.getElementById('newTagColor').value;
    const icon = document.getElementById('newTagIcon').value.trim() || '🏷️';

    if (!name) {
        showToast('请输入标签名称', 'error');
        return;
    }

    try {
        const response = await fetch('/api/tags/domains/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name,
                color,
                icon
            })
        });

        if (!response.ok) throw new Error('创建标签失败');

        showToast('✓ 自定义标签创建成功', 'success');

        // 清空输入
        document.getElementById('newTagName').value = '';
        document.getElementById('newTagColor').value = '#6366f1';
        document.getElementById('newTagIcon').value = '';

        // 重新加载标签列表
        await loadAllDomains();
        renderAvailableTags();
    } catch (error) {
        console.error('创建标签失败:', error);
        showToast('创建标签失败: ' + error.message, 'error');
    }
}
