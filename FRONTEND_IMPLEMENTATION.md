# 前端实现指南

## 概述

由于前端修改较多（paper.html需增加约100行，paper.js需增加约300行），本文档提供详细的实现指南。

CSS样式已完成添加到 `frontend/assets/css/main.css`。

---

## 1. paper.html 修改

在 `paper.html` 中找到 `<div class="container mt-4">` 下的 `<div id="paperInfo" class="detail-section">` 之后，添加以下两个新区域：

### 1.1 论文内容输入区域（插入位置：在paperInfo区域之后）

```html
<!-- 论文内容输入区域 -->
<div class="detail-section" id="contentInputSection">
    <h4>📄 论文内容</h4>

    <!-- Tab切换 -->
    <ul class="nav nav-tabs" id="contentTabs" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="upload-tab" data-bs-toggle="tab" data-bs-target="#uploadTab" type="button">
                上传PDF
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="arxiv-tab" data-bs-toggle="tab" data-bs-target="#arxivTab" type="button">
                arXiv导入
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="text-tab" data-bs-toggle="tab" data-bs-target="#textTab" type="button">
                文本输入
            </button>
        </li>
    </ul>

    <div class="tab-content" id="contentTabsContent">
        <!-- PDF上传 -->
        <div class="tab-pane fade show active" id="uploadTab" role="tabpanel">
            <input type="file" id="pdfFile" accept=".pdf" class="form-control mb-2">
            <button class="btn btn-primary" onclick="uploadPDF()">上传并解析</button>
            <div id="uploadStatus" class="mt-2"></div>
        </div>

        <!-- arXiv导入 -->
        <div class="tab-pane fade" id="arxivTab" role="tabpanel">
            <input type="text" id="arxivInput" class="form-control mb-2" placeholder="输入arXiv ID或URL (如: 2301.12345)">
            <button class="btn btn-primary" onclick="importFromArxiv()">导入</button>
            <div id="arxivStatus" class="mt-2"></div>
        </div>

        <!-- 手动输入 -->
        <div class="tab-pane fade" id="textTab" role="tabpanel">
            <textarea id="textContent" class="form-control mb-2" rows="10" placeholder="粘贴论文全文或关键内容"></textarea>
            <button class="btn btn-primary" onclick="addTextContent()">保存</button>
            <div id="textStatus" class="mt-2"></div>
        </div>
    </div>

    <!-- 内容状态显示 -->
    <div id="contentStatus" class="mt-3">
        <small class="text-muted" id="contentStatusText">暂无论文内容</small>
    </div>
</div>
```

### 1.2 AI对话界面（插入位置：在contentInputSection之后，analysisSection之前）

```html
<!-- AI对话助手 -->
<div class="detail-section" id="chatSection">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h4>🤖 AI对话助手</h4>
        <div>
            <button class="btn btn-sm btn-info" onclick="autoAnalyzePaper()">
                一键分析
            </button>
            <button class="btn btn-sm btn-secondary" onclick="clearConversations()">
                清空对话
            </button>
        </div>
    </div>

    <!-- 快捷问题按钮 -->
    <div class="quick-questions">
        <button class="btn btn-sm btn-outline-primary" onclick="askQuickQuestion('这篇论文的主要创新点是什么？')">
            创新点
        </button>
        <button class="btn btn-sm btn-outline-primary" onclick="askQuickQuestion('这篇论文使用了哪些方法？')">
            使用方法
        </button>
        <button class="btn btn-sm btn-outline-primary" onclick="askQuickQuestion('论文的框架结构是怎样的？')">
            框架结构
        </button>
        <button class="btn btn-sm btn-outline-primary" onclick="askQuickQuestion('有没有源代码？')">
            源码
        </button>
        <button class="btn btn-sm btn-outline-primary" onclick="askQuickQuestion('帮我总结这篇论文')">
            论文总结
        </button>
    </div>

    <!-- 对话历史显示区 -->
    <div id="chatHistory" class="chat-history">
        <p class="text-muted text-center">暂无对话记录，开始提问吧！</p>
    </div>

    <!-- 输入区 -->
    <div class="chat-input-area">
        <textarea id="chatInput" rows="2" placeholder="输入你的问题..." onkeydown="handleChatKeydown(event)"></textarea>
        <button id="sendBtn" onclick="sendMessage()">
            发送
        </button>
    </div>
</div>
```

---

## 2. paper.js 修改

在 `paper.js` 文件末尾添加以下函数：

```javascript
// ========== 论文内容处理函数 ==========

/**
 * 上传PDF文件
 */
async function uploadPDF() {
    const fileInput = document.getElementById('pdfFile');
    const file = fileInput.files[0];
    if (!file) {
        alert('请选择PDF文件');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.innerHTML = '<span class="loading-spinner"></span> 正在上传并解析PDF...';

    try {
        const response = await fetch(`/api/papers/${currentPaperId}/upload-pdf`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            statusDiv.innerHTML = `<div class="status-indicator success">✓ PDF上传成功！提取了 ${data.text_length} 字符</div>`;
            updateContentStatus('PDF已上传');
            // 刷新对话（因为现在有PDF内容了）
            loadConversations();
        } else {
            const error = await response.json();
            statusDiv.innerHTML = `<div class="alert alert-danger">${error.detail}</div>`;
        }
    } catch (error) {
        statusDiv.innerHTML = `<div class="alert alert-danger">上传失败: ${error.message}</div>`;
    }
}

/**
 * 从arXiv导入论文
 */
async function importFromArxiv() {
    const arxivInput = document.getElementById('arxivInput').value.trim();
    if (!arxivInput) {
        alert('请输入arXiv ID或URL');
        return;
    }

    const statusDiv = document.getElementById('arxivStatus');
    statusDiv.innerHTML = '<span class="loading-spinner"></span> 正在从arXiv导入...';

    try {
        const response = await fetch(`/api/papers/${currentPaperId}/import-from-arxiv`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ arxiv_input: arxivInput })
        });

        if (response.ok) {
            const data = await response.json();
            statusDiv.innerHTML = `<div class="status-indicator success">✓ arXiv论文导入成功！</div>`;
            updateContentStatus('arXiv内容已导入');
            // 刷新页面数据
            loadPaperDetails(currentPaperId);
        } else {
            const error = await response.json();
            statusDiv.innerHTML = `<div class="alert alert-danger">${error.detail}</div>`;
        }
    } catch (error) {
        statusDiv.innerHTML = `<div class="alert alert-danger">导入失败: ${error.message}</div>`;
    }
}

/**
 * 添加文本内容
 */
async function addTextContent() {
    const textContent = document.getElementById('textContent').value.trim();
    if (!textContent) {
        alert('请输入论文内容');
        return;
    }

    const statusDiv = document.getElementById('textStatus');
    statusDiv.innerHTML = '<span class="loading-spinner"></span> 正在保存...';

    try {
        const response = await fetch(`/api/papers/${currentPaperId}/add-text-content`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text_content: textContent })
        });

        if (response.ok) {
            statusDiv.innerHTML = '<div class="status-indicator success">✓ 论文内容已保存</div>';
            updateContentStatus('文本内容已添加');
        } else {
            const error = await response.json();
            statusDiv.innerHTML = `<div class="alert alert-danger">${error.detail}</div>`;
        }
    } catch (error) {
        statusDiv.innerHTML = `<div class="alert alert-danger">保存失败: ${error.message}</div>`;
    }
}

/**
 * 更新内容状态显示
 */
function updateContentStatus(status) {
    const statusText = document.getElementById('contentStatusText');
    statusText.textContent = status;
    statusText.classList.add('text-success');
}

// ========== AI对话函数 ==========

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
        chatHistory.innerHTML = '<p class="text-muted text-center">暂无对话记录，开始提问吧！</p>';
        return;
    }

    chatHistory.innerHTML = conversations.map(conv => {
        if (conv.role === 'system') return ''; // 不显示system消息

        const time = new Date(conv.created_at).toLocaleString('zh-CN');
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
    const time = new Date().toLocaleString('zh-CN');

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
            throw new Error('AI回复失败');
        }

        const data = await response.json();
        appendMessage('assistant', data.content);

    } catch (error) {
        appendMessage('assistant', '抱歉，AI回复失败: ' + error.message);
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

    // 显示加载提示
    const originalText = document.querySelector('#chatSection h4').textContent;
    document.querySelector('#chatSection h4').textContent = '🤖 AI正在分析论文...';

    try {
        const response = await fetch('/api/ai/analyze-paper', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ paper_id: currentPaperId })
        });

        if (!response.ok) {
            throw new Error('分析失败');
        }

        const analysis = await response.json();

        // 自动填充分析区域
        const innovationField = document.getElementById('innovation_points');
        if (innovationField && analysis.innovations) {
            innovationField.value = analysis.innovations.map((item, i) => `${i + 1}. ${item}`).join('\n');
        }

        const notesField = document.getElementById('personal_notes');
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

        alert('自动分析完成！请查看分析区域并保存');

    } catch (error) {
        alert('自动分析失败: ' + error.message);
    } finally {
        document.querySelector('#chatSection h4').textContent = originalText;
    }
}

/**
 * 清空对话
 */
async function clearConversations() {
    if (!confirm('确定要清空当前论文的所有对话记录吗？')) {
        return;
    }

    try {
        const response = await fetch(`/api/conversations/paper/${currentPaperId}/all`, {
            method: 'DELETE'
        });

        if (response.ok) {
            document.getElementById('chatHistory').innerHTML = '<p class="text-muted text-center">对话已清空</p>';
            alert('对话已清空');
        } else {
            alert('清空失败');
        }
    } catch (error) {
        alert('清空失败: ' + error.message);
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

/**
 * HTML转义（防止XSS）
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ========== 页面加载时初始化 ==========

// 在现有的loadPaperDetails函数最后添加：
// loadConversations(); // 加载对话历史
```

---

## 3. 更新现有函数

在 `paper.js` 中找到 `loadPaperDetails` 函数，在其最后（return之前）添加：

```javascript
// 加载对话历史
loadConversations();
```

---

## 4. 测试清单

完成上述修改后，打开论文详情页测试：

1. ✅ 看到"论文内容"和"AI对话助手"两个新区域
2. ✅ 切换"上传PDF"、"arXiv导入"、"文本输入"三个标签
3. ✅ 上传PDF文件，查看是否显示成功提示
4. ✅ 输入arXiv ID测试导入
5. ✅ 在对话框输入问题，AI能够回复
6. ✅ 点击快捷问题按钮测试
7. ✅ 测试"一键分析"功能
8. ✅ 刷新页面，对话历史仍然显示

---

## 5. 注意事项

1. **paper.html修改**：新区域应插入在合适的位置，确保页面结构清晰
2. **paper.js修改**：所有新函数添加在文件末尾，确保不影响现有功能
3. **currentPaperId变量**：确保在paper.js中已定义（现有代码应该已有）
4. **Bootstrap依赖**：确认paper.html中已引入Bootstrap 5 CSS和JS

---

## 6. 简化实现（如果遇到问题）

如果完整实现有困难，可以先实现核心的对话功能：

**最小化版本**：
1. 只添加AI对话界面HTML（不添加论文内容输入区域）
2. 在paper.js中只实现 `sendMessage` 和 `loadConversations` 两个函数
3. 手动在Supabase中执行SQL为papers表添加pdf_text_content字段
4. 手动在数据库中填写论文内容进行测试

这样可以快速验证对话功能是否正常工作。

---

## 总结

前端修改主要包括：
- HTML: 约100行（两个新区域）
- JavaScript: 约300行（10个新函数）
- CSS: 已完成

按照本文档逐步实现即可完成前端功能。
