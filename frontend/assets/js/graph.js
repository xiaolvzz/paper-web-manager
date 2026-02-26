/**
 * 关系图可视化逻辑
 */

let network = null;

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', async () => {
    await loadGraph();
});

// 加载关系图数据
async function loadGraph() {
    const loading = document.getElementById('loading');
    const emptyState = document.getElementById('empty-state');
    const container = document.getElementById('graph-container');

    try {
        const data = await RelationsAPI.getGraph();

        loading.classList.add('d-none');

        if (data.nodes.length === 0) {
            emptyState.classList.remove('d-none');
            container.style.display = 'none';
            return;
        }

        emptyState.classList.add('d-none');
        container.style.display = 'block';

        renderGraph(data);
    } catch (error) {
        loading.classList.add('d-none');
        showToast('加载关系图失败: ' + error.message, 'error');
    }
}

// 渲染关系图
function renderGraph(data) {
    const container = document.getElementById('graph-container');

    // 准备节点数据
    const nodes = new vis.DataSet(
        data.nodes.map(node => ({
            id: node.id,
            label: node.label,
            title: `${node.title}\n${node.year || '未知年份'}${node.tags ? '\n标签: ' + node.tags : ''}`,
            shape: 'box',
            color: {
                background: '#ffffff',
                border: '#2563eb',
                highlight: {
                    background: '#dbeafe',
                    border: '#1d4ed8'
                },
                hover: {
                    background: '#eff6ff',
                    border: '#2563eb'
                }
            },
            font: {
                size: 14,
                face: 'Arial',
                color: '#1e293b'
            },
            margin: 10,
            borderWidth: 2,
            borderWidthSelected: 3
        }))
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

    // 节点点击事件
    network.on('click', (params) => {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            window.location.href = `/paper/${nodeId}`;
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
        'method_similar': '#2563eb',
        'problem_related': '#10b981',
        'custom': '#f59e0b'
    };
    return colors[relationType] || '#64748b';
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
